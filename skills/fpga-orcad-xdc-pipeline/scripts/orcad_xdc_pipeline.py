#!/usr/bin/env python3
"""Extract, validate, and generate audited physical XDC from OrCAD PST netlists."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # JSON is valid YAML and remains the dependency-free fallback.
    yaml = None


SCHEMA_VERSION = 1
DIRECTIONS = {"input", "output", "inout"}
STATUSES = {"verified", "needs_review", "waived"}
PROPERTY_ENUMS = {
    "slew": {"SLOW", "FAST"},
    "pulltype": {"PULLUP", "PULLDOWN", "NONE"},
}
VOLTAGE_BY_STANDARD = {
    "LVCMOS33": 3.3,
    "LVTTL": 3.3,
    "LVCMOS25": 2.5,
    "LVDS_25": 2.5,
    "TMDS_33": 3.3,
    "LVCMOS18": 1.8,
    "SSTL18_I": 1.8,
    "SSTL18_II": 1.8,
    "LVCMOS15": 1.5,
    "SSTL15": 1.5,
    "LVCMOS12": 1.2,
}
FORBIDDEN_TIMING_KEYS = {
    "create_clock", "set_input_delay", "set_output_delay", "set_false_path",
    "set_multicycle_path", "set_clock_groups", "set_max_delay", "set_min_delay",
    "set_bus_skew",
}


def load_map(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("map root must be an object")
    return data


def dump_map(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_pstxnet(path: Path, refdes: str) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    current_net: str | None = None
    expect_net_name = False
    entries: list[dict[str, Any]] = []
    node_pattern = re.compile(r"^NODE_NAME\s+([^\s]+)\s+([^\s]+)", re.I)
    quoted_pattern = re.compile(r"^\s*'([^']*)'")
    for number, line in enumerate(lines, start=1):
        if line.strip().upper() == "NET_NAME":
            expect_net_name = True
            continue
        if expect_net_name:
            match = quoted_pattern.match(line)
            if match:
                current_net = match.group(1)
                expect_net_name = False
            continue
        node = node_pattern.match(line)
        if node and node.group(1).upper() == refdes.upper():
            entries.append({
                "net_name": current_net or "",
                "fpga_pin": node.group(2),
                "source_line": number,
            })
    if not entries:
        raise ValueError(f"no NODE_NAME entries found for FPGA refdes {refdes}")
    return sorted(entries, key=lambda item: (natural_key(str(item["fpga_pin"])), str(item["net_name"])))


def natural_key(value: str) -> list[Any]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", value)]


def draft_map(args: argparse.Namespace) -> dict[str, Any]:
    pstxnet = args.pstxnet.resolve()
    entries = parse_pstxnet(pstxnet, args.fpga_refdes)
    ports = []
    for entry in entries:
        ports.append({
            "bank": None,
            "bank_vcco": None,
            "direction": None,
            "drive": None,
            "evidence": {
                "component": args.fpga_refdes,
                "datasheet": None,
                "schematic_page": None,
                "source_ref": f"{pstxnet}:{entry['source_line']}",
            },
            "fpga_pin": entry["fpga_pin"],
            "iostandard": None,
            "net_name": entry["net_name"],
            "pulltype": None,
            "role": "data",
            "rtl_port": None,
            "slew": None,
            "status": "needs_review",
            "waiver_reason": None,
        })
    return {
        "schema_version": SCHEMA_VERSION,
        "source": {
            "format": "orcad-pstxnet",
            "netlist_file": str(pstxnet),
            "schematic_file": str(args.schematic.resolve()) if args.schematic else None,
        },
        "fpga": {
            "cfgbvs": None,
            "config_voltage": None,
            "part": args.part,
            "refdes": args.fpga_refdes,
        },
        "ports": ports,
        "timing": [],
    }


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", lambda m: "".join("\n" if c == "\n" else " " for c in m.group(0)), text, flags=re.S)
    return re.sub(r"//[^\n]*", "", text)


def rtl_port_names(paths: list[Path]) -> set[str]:
    names: set[str] = set()
    declaration = re.compile(
        r"\b(?:input|output|inout)\b\s*(?:(?:wire|reg|logic|bit|signed|unsigned)\s+)*"
        r"(?:\[[^\]]+\]\s*)?([^;\)]+)[;\)]",
        re.I | re.S,
    )
    for path in paths:
        text = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        for match in declaration.finditer(text):
            for fragment in match.group(1).split(","):
                name_match = re.search(r"([A-Za-z_]\w*)\s*(?:=.*)?$", fragment.strip())
                if name_match:
                    names.add(name_match.group(1))
    return names


def base_port_name(name: str) -> str:
    return name.split("[", 1)[0]


def validate(data: dict[str, Any], rtl_paths: list[Path]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    fpga = data.get("fpga")
    ports = data.get("ports")
    if not isinstance(fpga, dict):
        errors.append("fpga must be an object")
        fpga = {}
    if not isinstance(ports, list) or not ports:
        errors.append("ports must be a non-empty array")
        ports = []

    seen_pins: dict[str, int] = {}
    seen_ports: dict[str, int] = {}
    rtl_names = rtl_port_names(rtl_paths) if rtl_paths else set()
    for index, port in enumerate(ports):
        label = f"ports[{index}]"
        if not isinstance(port, dict):
            errors.append(f"{label} must be an object")
            continue
        status = port.get("status")
        if status not in STATUSES:
            errors.append(f"{label}.status must be one of {sorted(STATUSES)}")
        pin = str(port.get("fpga_pin") or "").strip()
        if not pin:
            errors.append(f"{label}.fpga_pin is required")
        elif pin in seen_pins:
            errors.append(f"duplicate FPGA pin {pin} at ports[{seen_pins[pin]}] and {label}")
        else:
            seen_pins[pin] = index

        rtl_port = str(port.get("rtl_port") or "").strip()
        if rtl_port:
            if rtl_port in seen_ports:
                errors.append(f"duplicate RTL port {rtl_port} at ports[{seen_ports[rtl_port]}] and {label}")
            else:
                seen_ports[rtl_port] = index
            if rtl_names and base_port_name(rtl_port) not in rtl_names:
                errors.append(f"{label}.rtl_port {rtl_port} not found in supplied RTL")

        if status == "waived":
            if not str(port.get("waiver_reason") or "").strip():
                errors.append(f"{label}.waiver_reason is required for waived rows")
            continue
        if status != "verified":
            errors.append(f"{label} remains needs_review; physical XDC generation is blocked")
            continue

        for field in ("rtl_port", "direction", "iostandard", "bank", "bank_vcco", "role"):
            if port.get(field) in (None, ""):
                errors.append(f"{label}.{field} is required for verified rows")
        if port.get("direction") not in DIRECTIONS:
            errors.append(f"{label}.direction must be one of {sorted(DIRECTIONS)}")
        evidence = port.get("evidence")
        if not isinstance(evidence, dict) or not any(evidence.get(key) for key in ("schematic_page", "source_ref")):
            errors.append(f"{label}.evidence requires schematic_page or source_ref")

        standard = str(port.get("iostandard") or "").upper()
        expected_voltage = VOLTAGE_BY_STANDARD.get(standard)
        if expected_voltage is None:
            errors.append(f"{label}.iostandard {standard or '<empty>'} has no audited VCCO rule")
        else:
            try:
                actual_voltage = float(port.get("bank_vcco"))
                if abs(actual_voltage - expected_voltage) > 0.05:
                    errors.append(
                        f"{label} bank VCCO {actual_voltage:g} V is incompatible with {standard} ({expected_voltage:g} V)"
                    )
            except (TypeError, ValueError):
                errors.append(f"{label}.bank_vcco must be numeric")

        if port.get("slew") and str(port["slew"]).upper() not in PROPERTY_ENUMS["slew"]:
            errors.append(f"{label}.slew must be SLOW or FAST")
        if port.get("pulltype") and str(port["pulltype"]).upper() not in PROPERTY_ENUMS["pulltype"]:
            errors.append(f"{label}.pulltype must be PULLUP, PULLDOWN, or NONE")
        if port.get("drive") not in (None, ""):
            try:
                if int(port["drive"]) <= 0:
                    raise ValueError
            except (TypeError, ValueError):
                errors.append(f"{label}.drive must be a positive integer")

    timing = data.get("timing", [])
    if not isinstance(timing, list):
        errors.append("timing must be an array")
    else:
        for index, item in enumerate(timing):
            if not isinstance(item, dict):
                errors.append(f"timing[{index}] must be an object")
                continue
            forbidden = FORBIDDEN_TIMING_KEYS.intersection(item)
            if forbidden:
                errors.append(f"timing[{index}] contains forbidden automatic constraints: {sorted(forbidden)}")
            warnings.append(f"timing[{index}] is documentation-only and will not be emitted")

    if not fpga.get("part"):
        errors.append("fpga.part is required")
    if fpga.get("cfgbvs") not in {"VCCO", "GND"}:
        errors.append("fpga.cfgbvs must be VCCO or GND")
    if fpga.get("config_voltage") not in {1.5, 1.8, 2.5, 3.3}:
        errors.append("fpga.config_voltage must be 1.5, 1.8, 2.5, or 3.3")

    return {
        "valid": not errors,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "verified_ports": sum(1 for p in ports if isinstance(p, dict) and p.get("status") == "verified"),
        "waived_ports": sum(1 for p in ports if isinstance(p, dict) and p.get("status") == "waived"),
        "rtl_ports_detected": sorted(rtl_names),
    }


def xdc_port_ref(name: str) -> str:
    return "{" + name + "}" if any(char in name for char in "[] ") else name


def generate(data: dict[str, Any], report: dict[str, Any], output_dir: Path, rtl_paths: list[Path]) -> None:
    if not report["valid"]:
        raise ValueError("validation failed; XDC generation is blocked")
    output_dir.mkdir(parents=True, exist_ok=True)
    fpga = data["fpga"]
    verified = sorted(
        (port for port in data["ports"] if port["status"] == "verified"),
        key=lambda port: (str(port["rtl_port"]), natural_key(str(port["fpga_pin"]))),
    )

    xdc = [
        "# Generated by fpga-orcad-xdc-pipeline. Physical constraints only.",
        f"# FPGA part: {fpga['part']}",
        f"set_property CONFIG_VOLTAGE {fpga['config_voltage']} [current_design]",
        f"set_property CFGBVS {fpga['cfgbvs']} [current_design]",
        "",
    ]
    for port in verified:
        ref = xdc_port_ref(str(port["rtl_port"]))
        evidence = port.get("evidence", {})
        xdc.append(
            f"# net={port['net_name']} bank={port['bank']} vcco={port['bank_vcco']}V "
            f"evidence={evidence.get('schematic_page') or evidence.get('source_ref')}"
        )
        xdc.append(f"set_property PACKAGE_PIN {port['fpga_pin']} [get_ports {ref}]")
        xdc.append(f"set_property IOSTANDARD {str(port['iostandard']).upper()} [get_ports {ref}]")
        for field, prop in (("drive", "DRIVE"), ("slew", "SLEW"), ("pulltype", "PULLTYPE")):
            if port.get(field) not in (None, ""):
                xdc.append(f"set_property {prop} {str(port[field]).upper()} [get_ports {ref}]")
        xdc.append("")
    (output_dir / "pins.xdc").write_text("\n".join(xdc), encoding="utf-8")

    timing = [
        "# Timing constraints are intentionally not generated from OrCAD net names.",
        "# Add create_clock, I/O delays, clock groups, and exceptions only after datasheet/RTL review.",
        "# Keep every active timing constraint tied to an evidence reference and reviewer.",
    ]
    (output_dir / "timing.xdc").write_text("\n".join(timing) + "\n", encoding="utf-8")

    rtl_names = rtl_port_names(rtl_paths) if rtl_paths else set()
    md = [
        "# OrCAD / RTL / XDC alignment report", "",
        f"- FPGA: `{fpga['refdes']}` / `{fpga['part']}`",
        f"- Verified physical ports: {len(verified)}",
        f"- RTL supplied: {'yes' if rtl_paths else 'no'}", "",
        "| RTL port | Direction | Package pin | IOSTANDARD | Bank/VCCO | Schematic net | Evidence | Status |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for port in verified:
        exists = not rtl_names or base_port_name(str(port["rtl_port"])) in rtl_names
        evidence = port.get("evidence", {})
        md.append(
            f"| `{port['rtl_port']}` | {port['direction']} | `{port['fpga_pin']}` | {port['iostandard']} | "
            f"{port['bank']} / {port['bank_vcco']} V | `{port['net_name']}` | "
            f"{evidence.get('schematic_page') or evidence.get('source_ref')} | {'matched' if exists else 'missing_rtl'} |"
        )
    md += ["", "## Evidence boundary", "", "This report proves intended source alignment only; it does not prove board activity or timing closure."]
    (output_dir / "io_alignment_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    io_gen = {
        "title": f"Audited FPGA I/O for {fpga['refdes']}",
        "part": fpga["part"],
        "constraints": {"cfgbvs": fpga["cfgbvs"], "config_voltage": fpga["config_voltage"]},
        "signals": [],
    }
    for port in verified:
        io_gen["signals"].append({
            "name": re.sub(r"[^A-Za-z0-9_]", "_", str(port["rtl_port"])),
            "direction": {"input": "in", "output": "out", "inout": "inout"}[port["direction"]],
            "bypass": True,
            "iostandard": str(port["iostandard"]).upper(),
            "pins": str(port["fpga_pin"]),
            "comment": {"xdc": f"Original RTL port: {port['rtl_port']}; net: {port['net_name']}"},
        })
    dump_map(output_dir / "io_gen_input.yaml", io_gen)
    dump_map(output_dir / "validation.json", report)


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--map", required=True, type=Path)
    parser.add_argument("--rtl", action="append", default=[], type=Path, help="Top-level RTL; repeat as needed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    extract = sub.add_parser("extract-netlist", help="Create a needs-review map from pstxnet.dat")
    extract.add_argument("--pstxnet", required=True, type=Path)
    extract.add_argument("--fpga-refdes", required=True)
    extract.add_argument("--schematic", type=Path)
    extract.add_argument("--part", required=True)
    extract.add_argument("--output", required=True, type=Path)

    validate_parser = sub.add_parser("validate", help="Validate the audited map")
    add_common(validate_parser)
    validate_parser.add_argument("--report", type=Path)

    generate_parser = sub.add_parser("generate", help="Generate physical XDC after strict validation")
    add_common(generate_parser)
    generate_parser.add_argument("--output-dir", required=True, type=Path)

    args = parser.parse_args()
    try:
        if args.command == "extract-netlist":
            dump_map(args.output.resolve(), draft_map(args))
            print(f"Wrote needs-review map: {args.output.resolve()}")
            return 0

        data = load_map(args.map.resolve())
        rtl_paths = [path.resolve() for path in args.rtl]
        report = validate(data, rtl_paths)
        if args.command == "validate":
            if args.report:
                dump_map(args.report.resolve(), report)
            print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
            return 0 if report["valid"] else 2
        generate(data, report, args.output_dir.resolve(), rtl_paths)
        print(f"Generated audited outputs in {args.output_dir.resolve()}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
