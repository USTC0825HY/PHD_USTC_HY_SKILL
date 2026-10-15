#!/usr/bin/env python3
"""Preflight a typed multi-board PST/XPR/XDC graph without joining board edges."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


PST_FILES = ("pstxnet.dat", "pstxprt.dat", "pstchip.dat")
SOURCE_FIELDS = ("dsn", "pdf", "schdoc", "pcbdoc")
EDGE_TYPES = {"fpga_control", "status_return", "board_signal", "clock_reference", "power_rail", "ground_return"}
FPGA_CHAIN_TYPES = {"fpga_control", "status_return"}
KNOWN_ROLES = {
    "SZSD": "controller",
    "BASE": "interconnect",
    "POWER": "power_source",
    "YCQD": "function",
    "PZ": "frequency_synthesis",
    "LASER_DRIVE": "laser_drive",
    "TEMP_CONTROL": "temperature_control",
    "LOCK_DRIVE": "lock_drive",
    "ERROR_DETECT": "error_detection",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def text_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def file_record(path: Path) -> dict[str, Any]:
    record: dict[str, Any] = {"path": str(path), "exists": path.is_file()}
    if path.is_file():
        stat = path.stat()
        record.update({
            "size": stat.st_size,
            "mtime_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
            "sha256": sha256(path),
        })
    return record


def find_file(directory: Path, name: str) -> Path | None:
    if not directory.is_dir():
        return None
    matches = [item for item in directory.iterdir() if item.is_file() and item.name.lower() == name]
    return matches[0] if len(matches) == 1 else None


def pst_header(path: Path) -> str | None:
    for line in text_lines(path)[:12]:
        if "PSTWRITER" in line.upper():
            return line.strip(" {}")
    return None


def quoted(line: str) -> str | None:
    match = re.match(r"^\s*'([^']*)'", line)
    return match.group(1) if match else None


def parse_pstxnet(path: Path) -> list[dict[str, Any]]:
    lines = text_lines(path)
    nets: list[dict[str, Any]] = []
    index = 0
    while index < len(lines):
        if lines[index].strip().upper() != "NET_NAME":
            index += 1
            continue
        marker_line = index + 1
        index += 1
        while index < len(lines) and quoted(lines[index]) is None:
            index += 1
        if index >= len(lines):
            break
        name = quoted(lines[index]) or ""
        nodes: list[dict[str, Any]] = []
        index += 1
        while index < len(lines) and lines[index].strip().upper() != "NET_NAME":
            match = re.match(r"^NODE_NAME\s+(\S+)\s+(\S+)", lines[index], re.I)
            if match:
                pin_name = None
                for lookahead in range(index + 1, min(index + 4, len(lines))):
                    candidate = re.match(r"^\s*'([^']*)':;", lines[lookahead])
                    if candidate:
                        pin_name = candidate.group(1)
                        break
                nodes.append({
                    "refdes": match.group(1),
                    "pin": match.group(2),
                    "pin_name": pin_name,
                    "source_line": index + 1,
                })
            index += 1
        nets.append({"name": name, "source_line": marker_line, "nodes": nodes})
    if not nets:
        raise ValueError(f"未解析到NET_NAME记录：{path}")
    return nets


def query_nets(nets: list[dict[str, Any]], queries: list[tuple[str, str]]) -> list[dict[str, Any]]:
    results = []
    for kind, selector in queries:
        hits = []
        for net in nets:
            if kind == "net" and net["name"].casefold() == selector.casefold():
                hits.append(net)
            elif kind == "node" and any(
                f"{node['refdes']}.{node['pin']}".casefold() == selector.casefold() for node in net["nodes"]
            ):
                hits.append(net)
        results.append({"kind": kind, "selector": selector, "matches": hits, "status": "found" if hits else "not_found"})
    return results


def summarize_pst(label: str, directory: Path, queries: list[tuple[str, str]]) -> dict[str, Any]:
    directory = directory.resolve()
    files = {name: find_file(directory, name) for name in PST_FILES}
    errors = []
    if not directory.is_dir():
        errors.append(f"{label}: PST目录不存在：{directory}")
    if files["pstxnet.dat"] is None:
        errors.append(f"{label}: 缺少pstxnet.dat：{directory}")
        return {
            "pst_dir": str(directory),
            "status": "E0 输入不完整",
            "files": {name: None for name in PST_FILES},
            "errors": errors,
            "queries": [{"kind": kind, "selector": selector, "matches": [], "status": "not_applicable_no_pst"} for kind, selector in queries],
        }
    nets = parse_pstxnet(files["pstxnet.dat"])
    result: dict[str, Any] = {
        "pst_dir": str(directory),
        "status": "E1 原理图/PST 已确认",
        "files": {},
        "pstwriter": pst_header(files["pstxnet.dat"]),
        "net_count": len(nets),
        "node_count": sum(len(net["nodes"]) for net in nets),
        "candidate_connector_nodes": sorted({
            node["refdes"] for net in nets for node in net["nodes"] if node["refdes"].upper().startswith("X")
        }),
        "errors": errors,
        "queries": query_nets(nets, queries),
    }
    for name, path in files.items():
        result["files"][name] = None if path is None else file_record(path)
    if any(path is None for path in files.values()):
        result["status"] = "E1 原理图/PST 已确认（缺少可选PST辅助文件）"
    return result


def resolve_path(value: str | None, base_dir: Path) -> str | None:
    if not value:
        return None
    path = Path(value)
    if not path.is_absolute():
        path = base_dir / path
    return str(path.resolve())


def normalize_source_value(value: Any, base_dir: Path) -> Any:
    if isinstance(value, list):
        return [resolve_path(str(item), base_dir) for item in value]
    if isinstance(value, str):
        return resolve_path(value, base_dir)
    return value


def load_registry(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("boards-file顶层必须是JSON对象")
    if data.get("schema") != "fpga-board-signal-chain-closure/board-registry-v2":
        raise ValueError("boards-file schema必须为fpga-board-signal-chain-closure/board-registry-v2")
    data.setdefault("boards", [])
    data.setdefault("evidence_sets", [])
    data.setdefault("edges", [])
    data.setdefault("chains", [])
    data.setdefault("conflicts", [])
    data.setdefault("unclosed_points", [])
    data.setdefault("physical_checks", [])
    base_dir = path.resolve().parent
    for evidence in data["evidence_sets"]:
        if evidence.get("pst_dir"):
            evidence["pst_dir"] = resolve_path(str(evidence["pst_dir"]), base_dir)
        if evidence.get("root"):
            evidence["root"] = resolve_path(str(evidence["root"]), base_dir)
        for field in SOURCE_FIELDS:
            if field in evidence:
                evidence[field] = normalize_source_value(evidence[field], base_dir)
    data["registry_path"] = str(path.resolve())
    return data


def parse_board_arg(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("--board格式必须为ID=PATH")
    board_id, raw_path = value.split("=", 1)
    board_id = board_id.strip().upper()
    if not re.fullmatch(r"[A-Z][A-Z0-9_-]*", board_id) or not raw_path.strip():
        raise argparse.ArgumentTypeError("--board格式必须为ID=PATH，ID仅含字母、数字、下划线或连字符")
    return board_id, Path(raw_path.strip())


def empty_registry() -> dict[str, Any]:
    return {
        "schema": "fpga-board-signal-chain-closure/board-registry-v2",
        "boards": [],
        "evidence_sets": [],
        "edges": [],
        "chains": [],
        "conflicts": [],
        "unclosed_points": [],
        "physical_checks": [],
    }


def upsert_pst_board(registry: dict[str, Any], board_id: str, pst_dir: Path, label: str | None = None) -> None:
    evidence_id = f"cli-{board_id.lower()}"
    board = next((item for item in registry["boards"] if str(item.get("id", "")).upper() == board_id), None)
    if board is None:
        board = {"id": board_id, "name": label or board_id, "role": KNOWN_ROLES.get(board_id, "other")}
        registry["boards"].append(board)
    board["selected_evidence_set"] = evidence_id
    if label:
        board["legacy_label"] = label
    registry["evidence_sets"] = [item for item in registry["evidence_sets"] if item.get("id") != evidence_id]
    for item in registry["evidence_sets"]:
        if str(item.get("board_id", "")).upper() == board_id:
            item["selected"] = False
    registry["evidence_sets"].append({
        "id": evidence_id,
        "board_id": board_id,
        "pst_dir": str(pst_dir.resolve()),
        "selected": True,
        "source_class": "cli",
    })


def validate_registry(registry: dict[str, Any]) -> dict[str, str | None]:
    boards = registry.get("boards", [])
    evidence_sets = registry.get("evidence_sets", [])
    if not isinstance(boards, list) or not isinstance(evidence_sets, list):
        raise ValueError("boards和evidence_sets必须是数组")
    board_ids = [str(board.get("id", "")).upper() for board in boards]
    if any(not re.fullmatch(r"[A-Z][A-Z0-9_-]*", board_id) for board_id in board_ids):
        raise ValueError("每块板必须有合法且稳定的id")
    if len(board_ids) != len(set(board_ids)):
        raise ValueError("物理板卡id重复")
    for board, board_id in zip(boards, board_ids):
        board["id"] = board_id
    evidence_ids = [str(item.get("id", "")) for item in evidence_sets]
    if any(not item for item in evidence_ids) or len(evidence_ids) != len(set(evidence_ids)):
        raise ValueError("evidence_sets中的id缺失或重复")
    by_board: dict[str, list[dict[str, Any]]] = {board_id: [] for board_id in board_ids}
    for evidence in evidence_sets:
        board_id = str(evidence.get("board_id", "")).upper()
        if board_id not in by_board:
            raise ValueError(f"证据集{evidence.get('id')}引用未知板卡{board_id}")
        evidence["board_id"] = board_id
        by_board[board_id].append(evidence)
    selected: dict[str, str | None] = {}
    for board in boards:
        board_id = board["id"]
        explicit = board.get("selected_evidence_set")
        flagged = [item["id"] for item in by_board[board_id] if item.get("selected") is True]
        if len(flagged) > 1:
            raise ValueError(f"板卡{board_id}存在多个selected证据集")
        if explicit is not None and explicit not in {item["id"] for item in by_board[board_id]}:
            raise ValueError(f"板卡{board_id}选择了不属于它的证据集{explicit}")
        if explicit is not None and flagged and explicit != flagged[0]:
            raise ValueError(f"板卡{board_id}的selected_evidence_set与selected标记冲突")
        selected[board_id] = explicit if explicit is not None else (flagged[0] if flagged else None)
        board["selected_evidence_set"] = selected[board_id]
    edges = registry.get("edges", [])
    chains = registry.get("chains", [])
    report_lists = ("conflicts", "unclosed_points", "physical_checks")
    if not isinstance(edges, list) or not isinstance(chains, list) or any(
        not isinstance(registry.get(name, []), list) for name in report_lists
    ):
        raise ValueError("edges、chains及报告列表必须是数组")
    edge_ids = [str(edge.get("id", "")) for edge in edges]
    chain_ids = [str(chain.get("id", "")) for chain in chains]
    if any(not item for item in edge_ids) or len(edge_ids) != len(set(edge_ids)):
        raise ValueError("edges中的id缺失或重复")
    if any(not item for item in chain_ids) or len(chain_ids) != len(set(chain_ids)):
        raise ValueError("chains中的id缺失或重复")
    for edge in edges:
        edge_type = edge.get("type")
        if edge_type not in EDGE_TYPES:
            raise ValueError(f"边{edge.get('id')}使用未知类型{edge_type}")
        if edge.get("from") not in board_ids or edge.get("to") not in board_ids:
            raise ValueError(f"边{edge.get('id')}引用未知板卡")
        evidence = edge.get("connector_mapping_evidence") or []
        if edge.get("status") in {"已闭环", "E2 跨板映射已定义", "E3 实物/线缆已确认"} and not evidence:
            raise ValueError(f"边{edge.get('id')}声明闭合但没有connector_mapping_evidence")
    for chain in chains:
        kind = chain.get("kind")
        if kind not in EDGE_TYPES:
            raise ValueError(f"链{chain.get('id')}使用未知类型{kind}")
        path = chain.get("path") or []
        if len(path) < 2 or any(board_id not in board_ids for board_id in path):
            raise ValueError(f"链{chain.get('id')}的path无效")
        if kind in {"power_rail", "ground_return"} and chain.get("evidence_level") == "E4 FPGA实现已复核":
            raise ValueError(f"供电/回流链{chain.get('id')}不能标记为E4")
    return selected


def evidence_source_records(evidence: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for field in SOURCE_FIELDS:
        value = evidence.get(field)
        if isinstance(value, list):
            result[field] = [file_record(Path(item)) for item in value]
        elif isinstance(value, str):
            result[field] = file_record(Path(value))
        elif value is not None:
            result[field] = value
    return result


def summarize_board(
    board: dict[str, Any],
    evidence_sets: list[dict[str, Any]],
    selected_id: str | None,
    queries: list[tuple[str, str]],
) -> dict[str, Any]:
    board_id = board["id"]
    candidates = [item for item in evidence_sets if item["board_id"] == board_id]
    candidate_rows = []
    for evidence in candidates:
        candidate_rows.append({
            "id": evidence["id"],
            "selected": evidence["id"] == selected_id,
            "source_class": evidence.get("source_class"),
            "root": evidence.get("root"),
            "pst_dir": evidence.get("pst_dir"),
            "sources": evidence_source_records(evidence),
        })
    result: dict[str, Any] = {
        "id": board_id,
        "label": board.get("legacy_label") or board_id,
        "name": board.get("name") or board_id,
        "role": board.get("role") or "other",
        "selected_evidence_set": selected_id,
        "evidence_sets": candidate_rows,
    }
    if selected_id is None:
        result.update({
            "source_availability": "unselected",
            "status": "E0 输入不完整",
            "errors": [f"{board_id}: 未选择证据集"],
            "queries": [{"kind": kind, "selector": selector, "matches": [], "status": "not_applicable_no_pst"} for kind, selector in queries],
        })
        return result
    selected = next(item for item in candidates if item["id"] == selected_id)
    pst_dir = selected.get("pst_dir")
    if not pst_dir:
        source_records = evidence_source_records(selected)
        available = []
        for field, records in source_records.items():
            for record in records if isinstance(records, list) else [records]:
                if isinstance(record, dict) and record.get("exists"):
                    available.append(field)
        availability = "schematic_available_unreviewed" if "pdf" in available else "native_source_available_unreviewed" if available else "missing_sources"
        result.update({
            "source_availability": availability,
            "status": "E0 无PST（原理图文件可用，内容待核对）" if "pdf" in available else "E0 无PST（原生源待查看或导出）" if available else "E0 输入不完整（资料缺失）",
            "errors": [f"{board_id}: 选定证据集{selected_id}没有pst_dir"],
            "queries": [{"kind": kind, "selector": selector, "matches": [], "status": "not_applicable_no_pst"} for kind, selector in queries],
        })
        return result
    result.update(summarize_pst(board_id, Path(pst_dir), queries))
    result["source_availability"] = "pst_available" if result.get("net_count") else "missing_pst"
    return result


def attr_map(element: ET.Element) -> dict[str, str]:
    return {
        item.attrib.get("Name", ""): item.attrib.get("Val", "")
        for item in element.iter() if item.tag.rsplit("}", 1)[-1] == "Option"
    }


def parse_xpr(path: Path, requested_xdc: Path) -> dict[str, Any]:
    root = ET.parse(path).getroot()
    project_dir = path.resolve().parent
    source_dir = project_dir / f"{path.stem}.srcs"

    def resolve_xpr_path(raw_path: str | None) -> str | None:
        if not raw_path:
            return None
        value = raw_path.replace("$PPRDIR", str(project_dir)).replace("$PSRCDIR", str(source_dir))
        return str(Path(value).resolve())

    config = next((item for item in root.iter() if item.tag.rsplit("}", 1)[-1] == "Configuration"), None)
    config_options = attr_map(config) if config is not None else {}
    filesets = []
    active_constraints = []
    top_candidates = []
    design_top_candidates = []
    for fileset in (item for item in root.iter() if item.tag.rsplit("}", 1)[-1] == "FileSet"):
        record = {"name": fileset.attrib.get("Name"), "type": fileset.attrib.get("Type"), "files": []}
        for option in fileset.iter():
            if option.tag.rsplit("}", 1)[-1] == "Option" and option.attrib.get("Name") == "TopModule":
                top_candidates.append(option.attrib.get("Val"))
                if fileset.attrib.get("Type") == "DesignSrcs":
                    design_top_candidates.append(option.attrib.get("Val"))
        for file_item in (item for item in fileset if item.tag.rsplit("}", 1)[-1] == "File"):
            attrs = [child for child in file_item.iter() if child.tag.rsplit("}", 1)[-1] == "Attr"]
            used_in = [item.attrib.get("Val") for item in attrs if item.attrib.get("Name") == "UsedIn"]
            disabled = [item.attrib.get("Val") for item in attrs if item.attrib.get("Name") in {"AutoDisabled", "UserDisabled"}]
            import_path = next((item.attrib.get("Val") for item in attrs if item.attrib.get("Name") == "ImportPath"), None)
            file_record_row = {
                "path": file_item.attrib.get("Path"),
                "resolved_path": resolve_xpr_path(file_item.attrib.get("Path")),
                "import_path": import_path,
                "resolved_import_path": resolve_xpr_path(import_path),
                "used_in": used_in,
                "disabled_attrs": disabled,
            }
            record["files"].append(file_record_row)
            if record["type"] == "Constrs" and any(value in {"synthesis", "implementation"} for value in used_in) and not any(str(value).lower() in {"1", "true"} for value in disabled):
                active_constraints.append(file_record_row)
        filesets.append(record)
    requested_xdc = requested_xdc.resolve()
    matches = [
        item for item in active_constraints
        if requested_xdc in {
            Path(item["resolved_path"]) if item["resolved_path"] else None,
            Path(item["resolved_import_path"]) if item["resolved_import_path"] else None,
        }
    ]
    return {
        "path": str(path.resolve()),
        "part": config_options.get("Part"),
        "top": next((candidate for candidate in design_top_candidates if candidate), None),
        "design_top_candidates": design_top_candidates,
        "top_candidates": top_candidates,
        "filesets": filesets,
        "active_constraint_candidates": active_constraints,
        "requested_xdc": str(requested_xdc),
        "requested_xdc_active_membership": "matched" if len(matches) == 1 else ("ambiguous" if len(matches) > 1 else "not_matched"),
        "requested_xdc_active_paths": [item["resolved_path"] or item["resolved_import_path"] for item in matches],
        "runs": [
            {"id": run.attrib.get("Id"), "state": run.attrib.get("State"), "part": run.attrib.get("Part"), "constrs_set": run.attrib.get("ConstrsSet")}
            for run in root.iter() if run.tag.rsplit("}", 1)[-1] == "Run"
        ],
    }


def parse_xdc(path: Path) -> dict[str, Any]:
    records = []
    for number, raw in enumerate(text_lines(path), start=1):
        line = raw.split("#", 1)[0].strip()
        match = re.match(r"set_property\s+(PACKAGE_PIN|IOSTANDARD)\s+(\S+)\s+\[get_ports\s+(?:\{([^}]*)\}|([^\]]+))\]", line, re.I)
        if match:
            expression = (match.group(3) or match.group(4) or "").strip()
            records.append({"line": number, "property": match.group(1).upper(), "value": match.group(2), "ports": expression.split()})
    by_property: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_property.setdefault(record["property"], []).append(record)
    pins = [record["value"].casefold() for record in by_property.get("PACKAGE_PIN", [])]
    return {
        "path": str(path.resolve()),
        "records": records,
        "package_pin_count": len(by_property.get("PACKAGE_PIN", [])),
        "iostandard_count": len(by_property.get("IOSTANDARD", [])),
        "duplicate_package_pins": sorted({pin for pin in pins if pins.count(pin) > 1}),
        "unique_ports": sorted({port for record in records for port in record["ports"]}),
    }


def annotate_topology(registry: dict[str, Any], board_results: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    status_by_board = {item["id"]: item["status"] for item in board_results}
    edges = []
    for declared in registry.get("edges", []):
        edge = dict(declared)
        mapping_evidence = edge.get("connector_mapping_evidence") or []
        edge["closure_evidence_present"] = bool(mapping_evidence)
        edge["preflight_status"] = "映射证据待复核" if mapping_evidence else "跨板待确认"
        edge["automatic_join"] = False
        edges.append(edge)
    chains = []
    for declared in registry.get("chains", []):
        chain = dict(declared)
        kind = chain["kind"]
        if not chain.get("segments"):
            chain["segments"] = [
                {
                    "order": index,
                    "board_id": board_id,
                    "from": "未确认",
                    "to": "未确认",
                    "net": "未确认",
                    "connector_pin": "未确认",
                    "components": [],
                    "assembly": "待确认",
                    "evidence_level": "E0 输入不完整",
                    "status": "资料不完整，无法继续",
                    "generated_placeholder": True,
                }
                for index, board_id in enumerate(chain["path"], start=1)
            ]
        missing = [board_id for board_id in chain["path"] if status_by_board.get(board_id, "E0").startswith("E0")]
        chain["requires_fpga_alignment"] = kind in FPGA_CHAIN_TYPES
        chain["rtl_xdc_requirement"] = "required" if kind in FPGA_CHAIN_TYPES else "not_applicable"
        chain["boards_with_incomplete_evidence"] = missing
        reviewable = {item["id"] for item in board_results if item.get("source_availability") in {"schematic_available_unreviewed", "native_source_available_unreviewed"}}
        blocking = [board_id for board_id in missing if board_id not in reviewable]
        chain["preflight_status"] = "资料不完整，无法继续" if blocking else "无PST区段需人工核图；跨板待确认" if missing else "跨板待确认"
        chains.append(chain)
    return edges, chains


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--boards-file", type=Path, help="schema v2 JSON board/evidence/edge/chain registry")
    parser.add_argument("--board", action="append", default=[], type=parse_board_arg, metavar="ID=PATH")
    parser.add_argument("--szsd-pst-dir", type=Path)
    parser.add_argument("--backplane-pst-dir", type=Path)
    parser.add_argument("--child-pst-dir", type=Path)
    parser.add_argument("--xpr", type=Path)
    parser.add_argument("--xdc", type=Path)
    parser.add_argument("--fpga-refdes", default="D1")
    parser.add_argument("--query-net", action="append", default=[])
    parser.add_argument("--query-node", action="append", default=[])
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        registry = load_registry(args.boards_file) if args.boards_file else empty_registry()
        modes = ["registry"] if args.boards_file else []
        legacy = [args.szsd_pst_dir, args.backplane_pst_dir, args.child_pst_dir]
        if any(legacy):
            if not all(legacy):
                raise ValueError("旧接口必须同时提供--szsd-pst-dir、--backplane-pst-dir和--child-pst-dir")
            upsert_pst_board(registry, "SZSD", args.szsd_pst_dir, "SZSD")
            upsert_pst_board(registry, "BASE", args.backplane_pst_dir, "backplane")
            upsert_pst_board(registry, "CHILD_LEGACY", args.child_pst_dir, "child")
            if not registry["chains"]:
                registry["chains"].append({"id": "LEGACY_CHAIN", "kind": "fpga_control", "path": ["SZSD", "BASE", "CHILD_LEGACY"]})
            modes.append("legacy_three_board")
        for board_id, path in args.board:
            upsert_pst_board(registry, board_id, path)
            modes.append("board_override")
        if not registry["boards"]:
            raise ValueError("必须提供--boards-file、至少一个--board，或完整旧三板参数")
        if bool(args.xpr) != bool(args.xdc):
            raise ValueError("--xpr和--xdc必须同时提供或同时省略")
        if args.xpr and (not args.xpr.is_file() or not args.xdc.is_file()):
            raise ValueError("XPR或XDC不存在")
        selected = validate_registry(registry)
        queries = [("net", value) for value in args.query_net] + [("node", value) for value in args.query_node]
        board_results = [summarize_board(board, registry["evidence_sets"], selected[board["id"]], queries) for board in registry["boards"]]
        edges, chains = annotate_topology(registry, board_results)
        generated_unclosed = [
            {
                "id": f"EDGE_{edge['id']}_CONNECTOR_MAPPING",
                "type": "cross_board_boundary",
                "edge_id": edge["id"],
                "reason": "缺少连接器针脚/底板PST/接口表/实测导通闭合证据",
                "status": "跨板待确认",
            }
            for edge in edges if not edge["closure_evidence_present"]
        ]
        generated_unclosed.extend(
            {
                "id": f"BOARD_{board['id']}_PST",
                "type": "board_evidence",
                "board_id": board["id"],
                "reason": "无可用PST；已有原理图需逐节点人工核对" if board.get("source_availability") == "schematic_available_unreviewed" else "缺少可用连接证据；原生源需查看或导出后核对",
                "status": board["status"],
            }
            for board in board_results if board["status"].startswith("E0")
        )
        implementation = {
            "status": "not_supplied",
            "vivado_status": "未提供RTL/XDC输入；未核查FPGA实现",
        }
        if args.xpr and args.xdc:
            implementation = {
                "status": "static_inputs_parsed",
                "xpr": parse_xpr(args.xpr, args.xdc),
                "xdc": parse_xdc(args.xdc),
                "vivado_status": "已解析XPR/XDC输入；RTL/PST对齐和Vivado应用状态未复核",
            }
        data = {
            "schema": "fpga-board-signal-chain-closure/preflight-v2",
            "input_modes": sorted(set(modes)),
            "registry_path": registry.get("registry_path"),
            "fpga_refdes": args.fpga_refdes,
            "boards": board_results,
            "edges": edges,
            "chains": chains,
            "conflicts": registry.get("conflicts", []),
            "unclosed_points": registry.get("unclosed_points", []) + generated_unclosed,
            "physical_checks": registry.get("physical_checks", []),
            "fpga_implementation": implementation,
            "boundary": "Board summaries and declared graph edges are independent; no cross-board continuity is asserted automatically.",
            "next_checks": [
                "通过连接器配对、底板PST、受控接口表或导通记录逐边闭合",
                "逐通道记录translator DIR/OE/pull/assembly并标记禁用支路",
                "供电链逐负载记录rail、保护、开关、滤波、连接器和回流地",
                "仅对FPGA控制/返回链运行RTL/XDC静态审计；已有synth_1时再复核report_io",
            ],
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as report:
            report.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"output": str(args.output.resolve()), "status": "ok", "board_count": len(board_results), "chain_count": len(chains)}, ensure_ascii=False))
        return 0
    except (ET.ParseError, json.JSONDecodeError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
