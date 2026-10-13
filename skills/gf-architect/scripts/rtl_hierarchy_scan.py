#!/usr/bin/env python3
"""Deterministic first-pass Verilog/SystemVerilog hierarchy mapper."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'fpga-vivado-tcl-automation' / 'scripts'))
from project_inputs import inspect_project, sha256
from rtl_ports import module_ports, port_bits


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
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def source_files(root: Path, extensions: set[str]) -> list[Path]:
    result: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        rel_parts = path.relative_to(root).parts
        if any(part.lower() in EXCLUDED_DIRS or part.lower().endswith(('.runs', '.cache', '.sim', '.gen')) for part in rel_parts[:-1]):
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
    ports, _ = module_ports(block)
    return [dict(name=name, direction=item['direction'], width=item['width_expr'] or '1',
                 resolved_width=item['width'], indices=item['indices'], line=base_line)
            for name, item in sorted(ports.items())]


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
        r"(?m)^\s*([A-Za-z_]\w*)\b\s*"
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
        try:
            ports = parse_ports(block, start_line)
            _, issues = module_ports(block)
        except ValueError as exc:
            ports, issues = [], [str(exc)]
        if re.search(r'`|\bgenerate\b', text):
            issues.append('Macros/generate are not elaborated; instances are candidates')
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
            "needs_review": issues,
            "instance_semantics": "text-level candidates, not elaborated hierarchy",
        })
    return modules


def parse_xdc_ports(root: Path, paths=None, ports=None) -> dict[str, list[str]]:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'rtl-schematic-xdc-alignment' / 'scripts'))
    from rtl_xdc_pst_audit import parse_xdc_full
    evidence: dict[str, list[str]] = defaultdict(list)
    records, _, _, _ = parse_xdc_full(paths if paths is not None else source_files(root, XDC_EXTENSIONS), ports or {})
    for record in records:
        evidence[record['port']] += record['xdc_sources']
    return {name: sorted(locations) for name, locations in sorted(evidence.items())}


def hierarchy_edges(modules: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    counts = defaultdict(int)
    for module in modules: counts[str(module['name'])] += 1
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
            if counts[str(inst['module'])] == 1 and counts[str(parent['name'])] == 1:
                edges.append(record)
            else:
                record['reason'] = 'duplicate_definition' if counts[str(inst['module'])] > 1 or counts[str(parent['name'])] > 1 else 'vendor_ip_or_missing_source_or_parser_limit'
                unresolved.append(record)
    key = lambda item: (str(item["parent"]), str(item["instance"]), str(item["module"]))
    return sorted(edges, key=key), sorted(unresolved, key=key)


def build_map(root, modules, paths, xdc_paths, top=None, manifest=None, mode='inventory'):
    modules = sorted(modules, key=lambda item: (str(item["name"]), str(item["file"])))
    edges, unresolved = hierarchy_edges(modules)
    instantiated = {str(edge["module"]) for edge in edges}
    tops = [top] if top else sorted(str(module["name"]) for module in modules if str(module["name"]) not in instantiated)
    counts = defaultdict(list)
    for module in modules: counts[str(module['name'])].append(module['file'])
    duplicate = {n: files for n, files in counts.items() if len(files) > 1}
    ports = {}
    for module in modules:
        if module['name'] in tops and module['name'] not in duplicate:
            for p in module['ports']:
                ports[p['name']] = dict(direction=p['direction'], width=p['resolved_width'], indices=p['indices'], width_expr=p['width'])
    review = [str(issue) for m in modules for issue in m['needs_review']]
    mapped_files = {m['file'] for m in modules}
    for path in paths:
        if path.suffix.lower() in RTL_EXTENSIONS and relpath(path, root) not in mapped_files:
            review.append('No supported module definition parsed: ' + str(path))
    if duplicate: review.append('Duplicate module definitions: ' + ', '.join(duplicate))
    if top and top not in counts: review.append('Configured top not found: ' + top)
    if manifest: review.extend(str(i) for i in manifest['issues'])
    if unresolved: review.append('Unresolved instances remain')
    if not top: review.append('No authoritative top; inventory roots are candidates')
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'rtl-schematic-xdc-alignment' / 'scripts'))
    from rtl_xdc_pst_audit import parse_xdc_full
    _, xerrors, xunknown, _ = parse_xdc_full(xdc_paths, ports)
    review += xerrors + [str(i) for i in xunknown]
    reachable = set(tops)
    while True:
        children = {e['module'] for e in edges if e['parent'] in reachable}
        if children <= reachable: break
        reachable |= children
    for module in modules:
        module['reachable_candidate'] = module['name'] in reachable
    return {
        "schema_version": 2,
        "project": root.name,
        "mode": mode,
        "configured_top": top,
        "top_modules": tops,
        "modules": modules,
        "edges": edges,
        "unresolved": unresolved,
        "xdc_ports": parse_xdc_ports(root, xdc_paths, ports),
        "duplicates": duplicate,
        "needs_review": sorted(set(review)),
        "status": "needs_review" if review else "static_map_complete",
        "project_manifest": manifest,
        "input_sha256": {str(p.resolve()): sha256(p) for p in paths + xdc_paths},
        "boundary": "No elaboration, effective-XDC, unused-code, CDC safety or board acceptance claim",
    }


def write_outputs(root: Path, out: Path, data) -> None:
    out.mkdir(parents=True, exist_ok=True)
    modules, edges, unresolved = data['modules'], data['edges'], data['unresolved']
    tops, xdc_ports = data['top_modules'], data['xdc_ports']
    (out / "rtl_hierarchy.json").write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    module_by_name = {str(module["name"]): module for module in modules if module['name'] not in data['duplicates']}
    lines = [f"# RTL hierarchy: {root.name}", "", f"Top candidates: {', '.join(tops) or 'none'}", ""]
    lines += [data['boundary'], '', *['- ' + i for i in data['needs_review']], '']
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
            if top in module_by_name:
                for port in module_by_name[top]['ports']:
                    top_ports.update(port['name'] if i is None else f"{port['name']}[{i}]" for i in port['indices'] or [])
        align += ["| Port | RTL top | XDC | Evidence/status |", "|---|---|---|---|"]
        for name in sorted(top_ports | set(xdc_ports)):
            in_rtl = name in top_ports
            in_xdc = name in xdc_ports
            status = "static_name_candidate" if in_rtl and in_xdc else "not_detected_xdc" if in_rtl else "not_detected_rtl"
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
    parser.add_argument("--output", type=Path, help="Explicit full artifact directory; default JSON to stdout, no writes")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--project', type=Path)
    group.add_argument('--filelist', type=Path, help='Literal one-path-per-line list; paths relative to filelist')
    parser.add_argument('--top')
    args = parser.parse_args()
    root = args.repo.resolve()
    if not root.is_dir():
        parser.error(f"repository does not exist: {root}")
    manifest = None
    top = args.top
    mode = 'inventory'
    extras = []
    if args.project:
        manifest = inspect_project(args.project, top=args.top)
        top = manifest['top']; mode = 'xpr_membership'
        paths = [Path(i['path']) for i in manifest['inputs'] if i['active'] and i['exists'] and Path(i['path']).suffix.lower() in RTL_EXTENSIONS]
        xdcs = [Path(i['path']) for i in manifest['inputs'] if i['active'] and i['exists'] and i['role'] == 'constraint']
        extras = [args.project.resolve()]
    elif args.filelist:
        mode = 'explicit_filelist'; paths = []; xdcs = []
        for line in args.filelist.read_text(encoding='utf-8-sig').splitlines():
            line = line.strip()
            if not line or line.startswith('#'): continue
            if line.startswith(('-', '+')) or '$' in line: parser.error('Filelist supports literal paths only; options must be resolved externally')
            path = (args.filelist.resolve().parent / line).resolve(strict=True)
            (xdcs if path.suffix.lower() == '.xdc' else paths).append(path)
        extras = [args.filelist.resolve()]
    else:
        paths = source_files(root, RTL_EXTENSIONS); xdcs = source_files(root, XDC_EXTENSIONS)
    modules: list[dict[str, object]] = []
    for path in paths:
        modules.extend(parse_modules(path, root))
    if not modules:
        parser.error("no Verilog/SystemVerilog modules found")
    data = build_map(root, modules, paths + extras, xdcs, top, manifest, mode)
    if args.output:
        write_outputs(root, args.output.resolve(), data)
        print(f"Mapped {len(modules)} modules to {args.output}; status={data['status']}")
    else: print(json.dumps(data, ensure_ascii=False, indent=2))
    return 2 if data['needs_review'] else 0


if __name__ == "__main__":
    raise SystemExit(main())
