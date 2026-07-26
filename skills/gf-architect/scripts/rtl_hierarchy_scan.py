#!/usr/bin/env python3
"""Deterministic first-pass Verilog/SystemVerilog hierarchy mapper."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


RTL_EXTENSIONS = {".v", ".sv"}
XDC_EXTENSIONS = {".xdc"}
EXCLUDED_DIRS = {
    ".git", ".fpga-map", ".gateflow", ".xil", "xsim.dir", "ip_user_files",
    "runs", "sim", "synth", "impl", "node_modules", "__pycache__",
}
NON_MODULE_WORDS = {
    "always", "always_comb", "always_ff", "always_latch", "assign", "begin",
    "case", "casex", "casez", "else", "end", "endcase", "for", "foreach",
    "function", "generate", "if", "initial", "module", "package", "repeat",
    "task", "while", "assert", "assume", "cover", "property", "sequence",
    "and", "buf", "bufif0", "bufif1", "cmos", "nand", "nmos", "nor", "not",
    "or", "pmos", "pulldown", "pullup", "rcmos", "rnmos", "rpmos", "rtran",
    "rtranif0", "rtranif1", "tran", "tranif0", "tranif1", "xnor", "xor",
}


def strip_comments(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        return "".join("\n" if ch == "\n" else " " for ch in match.group(0))

    text = re.sub(r"/\*.*?\*/", repl, text, flags=re.S)
    return re.sub(r"//[^\n]*", repl, text)


def relpath(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def source_files(root: Path, extensions: set[str]) -> list[Path]:
    result: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        rel_parts = path.relative_to(root).parts
        if any(part.lower() in EXCLUDED_DIRS for part in rel_parts[:-1]):
            continue
        result.append(path)
    return sorted(result, key=lambda p: relpath(p, root).lower())


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def split_names(fragment: str) -> list[str]:
    fragment = re.sub(r"\[[^\]]+\]", " ", fragment)
    fragment = re.sub(r"\b(?:wire|reg|logic|bit|signed|unsigned|var)\b", " ", fragment)
    names: list[str] = []
    for item in fragment.split(","):
        name_match = re.search(r"([A-Za-z_]\w*)\s*(?:=.*)?$", item.strip())
        if name_match:
            names.append(name_match.group(1))
    return names


def parse_ports(block: str, base_line: int) -> list[dict[str, object]]:
    ports: dict[str, dict[str, object]] = {}
    pattern = re.compile(
        r"\b(input|output|inout)\b\s*"
        r"((?:(?:wire|reg|logic|bit|signed|unsigned|var)\s+)*)"
        r"(\[[^\]]+\])?\s*"
        r"([^;\)]+)[;\)]",
        re.I | re.S,
    )
    for match in pattern.finditer(block):
        direction = match.group(1).lower()
        width = (match.group(3) or "1").strip()
        for name in split_names(match.group(4)):
            if name not in ports:
                ports[name] = {
                    "name": name,
                    "direction": direction,
                    "width": width,
                    "line": base_line + block.count("\n", 0, match.start()),
                }
    return [ports[name] for name in sorted(ports)]


def parse_parameters(block: str, base_line: int) -> list[dict[str, object]]:
    params: list[dict[str, object]] = []
    for match in re.finditer(
        r"\b(?:parameter|localparam)\b\s+(?:(?:integer|int|logic|bit|signed|unsigned)\s+)?"
        r"([A-Za-z_]\w*)\s*=\s*([^,;\)]+)",
        block,
    ):
        params.append({
            "name": match.group(1),
            "default": " ".join(match.group(2).split()),
            "line": base_line + block.count("\n", 0, match.start()),
        })
    return sorted(params, key=lambda item: str(item["name"]))


def parse_instances(block: str, base_line: int) -> list[dict[str, object]]:
    instances: list[dict[str, object]] = []
    pattern = re.compile(
        r"(?m)^\s*([A-Za-z_]\w*)\s*"
        r"(?:#\s*\((?:[^()]|\([^()]*\))*\)\s*)?"
        r"([A-Za-z_]\w*)\s*\(",
    )
    for match in pattern.finditer(block):
        module_type, instance_name = match.group(1), match.group(2)
        if module_type.lower() in NON_MODULE_WORDS:
            continue
        instances.append({
            "module": module_type,
            "instance": instance_name,
            "line": base_line + block.count("\n", 0, match.start()),
        })
    unique = {(str(i["module"]), str(i["instance"]), int(i["line"])): i for i in instances}
    return [unique[key] for key in sorted(unique)]


def parse_clock_reset(block: str, ports: list[dict[str, object]]) -> tuple[list[str], list[str]]:
    port_names = [str(port["name"]) for port in ports]
    sensitivity = re.findall(r"(?:posedge|negedge)\s+([A-Za-z_]\w*)", block)
    clocks = {name for name in sensitivity if re.search(r"clk|clock", name, re.I)}
    resets = {name for name in sensitivity if re.search(r"rst|reset", name, re.I)}
    clocks.update(name for name in port_names if re.search(r"(^|_)clk($|_)|clock", name, re.I))
    resets.update(name for name in port_names if re.search(r"rst|reset", name, re.I))
    return sorted(clocks), sorted(resets)


def parse_fsms(block: str, base_line: int) -> list[dict[str, object]]:
    fsms: list[dict[str, object]] = []
    for match in re.finditer(
        r"typedef\s+enum(?:\s+logic\s*(\[[^\]]+\]))?\s*\{([^}]+)\}\s*([A-Za-z_]\w*)",
        block,
        flags=re.S,
    ):
        states = []
        for item in match.group(2).split(","):
            state_match = re.match(r"\s*([A-Za-z_]\w*)", item)
            if state_match:
                states.append(state_match.group(1))
        fsms.append({
            "type": match.group(3),
            "width": (match.group(1) or "auto").strip(),
            "states": states,
            "line": base_line + block.count("\n", 0, match.start()),
        })
    return sorted(fsms, key=lambda item: str(item["type"]))


def parse_modules(path: Path, root: Path) -> list[dict[str, object]]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    text = strip_comments(raw)
    declarations = list(re.finditer(r"(?m)^\s*module\s+([A-Za-z_]\w*)\b", text))
    modules: list[dict[str, object]] = []
    for index, match in enumerate(declarations):
        end_match = re.search(r"(?m)^\s*endmodule\b", text[match.end():])
        limit = match.end() + end_match.end() if end_match else (
            declarations[index + 1].start() if index + 1 < len(declarations) else len(text)
        )
        block = text[match.start():limit]
        start_line = line_number(text, match.start())
        ports = parse_ports(block, start_line)
        clocks, resets = parse_clock_reset(block, ports)
        modules.append({
            "name": match.group(1),
            "file": relpath(path, root),
            "line": start_line,
            "parameters": parse_parameters(block, start_line),
            "ports": ports,
            "instances": parse_instances(block, start_line),
            "clocks": clocks,
            "resets": resets,
            "fsms": parse_fsms(block, start_line),
        })
    return modules


def parse_xdc_ports(root: Path) -> dict[str, list[str]]:
    evidence: dict[str, list[str]] = defaultdict(list)
    pattern = re.compile(r"get_ports\s+(?:-\S+\s+)*\{?([^\}\]\s]+)")
    for path in source_files(root, XDC_EXTENSIONS):
        text = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        for match in pattern.finditer(text):
            name = match.group(1).strip("{}")
            evidence[name].append(f"{relpath(path, root)}:{line_number(text, match.start())}")
    return {name: sorted(locations) for name, locations in sorted(evidence.items())}


def hierarchy_edges(modules: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    names = {str(module["name"]) for module in modules}
    edges: list[dict[str, object]] = []
    unresolved: list[dict[str, object]] = []
    for parent in modules:
        for inst in parent["instances"]:  # type: ignore[index]
            record = {
                "parent": parent["name"],
                "module": inst["module"],
                "instance": inst["instance"],
                "file": parent["file"],
                "line": inst["line"],
            }
            if str(inst["module"]) in names:
                edges.append(record)
            else:
                unresolved.append(record)
    key = lambda item: (str(item["parent"]), str(item["instance"]), str(item["module"]))
    return sorted(edges, key=key), sorted(unresolved, key=key)


def write_outputs(root: Path, out: Path, modules: list[dict[str, object]]) -> None:
    out.mkdir(parents=True, exist_ok=True)
    modules = sorted(modules, key=lambda item: (str(item["name"]), str(item["file"])))
    edges, unresolved = hierarchy_edges(modules)
    instantiated = {str(edge["module"]) for edge in edges}
    tops = sorted(str(module["name"]) for module in modules if str(module["name"]) not in instantiated)
    xdc_ports = parse_xdc_ports(root)
    data = {
        "schema_version": 1,
        "project": root.name,
        "top_modules": tops,
        "modules": modules,
        "edges": edges,
        "unresolved": unresolved,
        "xdc_ports": xdc_ports,
    }
    (out / "rtl_hierarchy.json").write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    module_by_name = {str(module["name"]): module for module in modules}
    lines = [f"# RTL hierarchy: {root.name}", "", f"Top candidates: {', '.join(tops) or 'none'}", ""]
    lines += ["## Modules", "", "| Module | File | Ports | Instances | Clocks | Resets |", "|---|---|---:|---:|---|---|"]
    for module in modules:
        lines.append(
            f"| `{module['name']}` | `{module['file']}:{module['line']}` | {len(module['ports'])} | "
            f"{len(module['instances'])} | {', '.join(module['clocks']) or '-'} | {', '.join(module['resets']) or '-'} |"
        )
    lines += ["", "## Instances", "", "| Parent | Instance | Module | Evidence |", "|---|---|---|---|"]
    for edge in edges:
        lines.append(f"| `{edge['parent']}` | `{edge['instance']}` | `{edge['module']}` | `{edge['file']}:{edge['line']}` |")
    if not edges:
        lines.append("| - | - | - | No resolved instances detected |")
    (out / "rtl_hierarchy.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    mmd = ["flowchart TD"]
    for module in modules:
        safe = re.sub(r"\W", "_", str(module["name"]))
        mmd.append(f'    {safe}["{module["name"]}"]')
    for edge in edges:
        parent = re.sub(r"\W", "_", str(edge["parent"]))
        child = re.sub(r"\W", "_", str(edge["module"]))
        mmd.append(f'    {parent} -->|"{edge["instance"]}"| {child}')
    (out / "rtl_hierarchy.mmd").write_text("\n".join(mmd) + "\n", encoding="utf-8")

    cr = ["# Clock and reset map", "", "Static candidates; confirm with Vivado elaboration and XDC.", ""]
    cr += ["| Module | Clocks | Resets | Evidence |", "|---|---|---|---|"]
    for module in modules:
        cr.append(
            f"| `{module['name']}` | {', '.join(module['clocks']) or '-'} | "
            f"{', '.join(module['resets']) or '-'} | `{module['file']}:{module['line']}` |"
        )
    (out / "clock_reset_map.md").write_text("\n".join(cr) + "\n", encoding="utf-8")

    cdc = ["# CDC inventory", "", "| Module | Candidate domains | Status | Follow-up |", "|---|---|---|---|"]
    for module in modules:
        if len(module["clocks"]) > 1:
            cdc.append(
                f"| `{module['name']}` | {', '.join(module['clocks'])} | needs_review | "
                f"Inspect crossings and synchronizers at `{module['file']}:{module['line']}` |"
            )
    if len(cdc) == 4:
        cdc.append("| - | - | not_detected | Static scan found no multi-clock module; this does not prove CDC safety |")
    (out / "cdc_inventory.md").write_text("\n".join(cdc) + "\n", encoding="utf-8")

    align = ["# Top RTL to XDC alignment", ""]
    if not xdc_ports:
        align.append("No XDC `get_ports` objects were detected. Alignment is not proven.")
    else:
        top_ports = set()
        for top in tops:
            top_ports.update(str(port["name"]) for port in module_by_name[top]["ports"])
        align += ["| Port | RTL top | XDC | Evidence/status |", "|---|---|---|---|"]
        for name in sorted(top_ports | set(xdc_ports)):
            in_rtl = name in top_ports
            in_xdc = name in xdc_ports
            status = "matched" if in_rtl and in_xdc else "missing_xdc" if in_rtl else "missing_rtl"
            align.append(f"| `{name}` | {in_rtl} | {in_xdc} | {status}; {', '.join(xdc_ports.get(name, []))} |")
    (out / "top_xdc_alignment.md").write_text("\n".join(align) + "\n", encoding="utf-8")

    missing = ["# Unresolved modules", "", "| Parent | Instance | Referenced module | Evidence | Classification |", "|---|---|---|---|---|"]
    for item in unresolved:
        missing.append(
            f"| `{item['parent']}` | `{item['instance']}` | `{item['module']}` | "
            f"`{item['file']}:{item['line']}` | vendor IP / missing source / parser review |"
        )
    if not unresolved:
        missing.append("| - | - | - | - | none detected |")
    (out / "unresolved_modules.md").write_text("\n".join(missing) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path, help="RTL repository root")
    parser.add_argument("--output", type=Path, help="Output directory; default <repo>/.fpga-map")
    args = parser.parse_args()
    root = args.repo.resolve()
    if not root.is_dir():
        parser.error(f"repository does not exist: {root}")
    output = (args.output.resolve() if args.output else root / ".fpga-map")
    modules: list[dict[str, object]] = []
    for path in source_files(root, RTL_EXTENSIONS):
        modules.extend(parse_modules(path, root))
    if not modules:
        parser.error("no Verilog/SystemVerilog modules found")
    write_outputs(root, output, modules)
    print(f"Mapped {len(modules)} modules to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
