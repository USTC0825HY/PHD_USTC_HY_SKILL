#!/usr/bin/env python3
"""Query OrCAD/Allegro PST evidence without inferring cross-board continuity."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


EVIDENCE_CONFIRMED = "原理图/PST 已确认"
EVIDENCE_INCOMPLETE = "资料不完整，无法继续"
PENDING_CONTINUITY = "待实物/线缆导通确认"
EVIDENCE_NAMES = {"pstxnet.dat", "pstxprt.dat", "pstchip.dat"}


@dataclass
class Node:
    refdes: str
    pin: str
    pin_name: str | None
    hierarchy: str | None
    source_line: int


@dataclass
class Net:
    name: str
    hierarchy: str | None
    source_line: int
    nodes: list[Node]


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def first_quoted(line: str) -> str | None:
    match = re.match(r"^\s*'([^']*)'", line)
    return match.group(1) if match else None


def parse_pstxnet(path: Path) -> list[Net]:
    lines = read_lines(path)
    nets: list[Net] = []
    index = 0
    while index < len(lines):
        if lines[index].strip().upper() != "NET_NAME":
            index += 1
            continue
        net_line = index + 2
        index += 1
        while index < len(lines) and first_quoted(lines[index]) is None:
            index += 1
        if index >= len(lines):
            break
        name = first_quoted(lines[index]) or ""
        hierarchy = first_quoted(lines[index + 1]) if index + 1 < len(lines) else None
        nodes: list[Node] = []
        index += 1
        while index < len(lines) and lines[index].strip().upper() != "NET_NAME":
            match = re.match(r"^NODE_NAME\s+([^\s]+)\s+([^\s]+)", lines[index], re.I)
            if match:
                node_line = index + 1
                node_hierarchy = first_quoted(lines[index + 1]) if index + 1 < len(lines) else None
                pin_name = None
                for lookahead in range(index + 1, min(index + 4, len(lines))):
                    pin_match = re.match(r"^\s*'([^']*)':;", lines[lookahead])
                    if pin_match:
                        pin_name = pin_match.group(1)
                        break
                nodes.append(Node(match.group(1), match.group(2), pin_name, node_hierarchy, node_line))
            index += 1
        nets.append(Net(name, hierarchy, net_line, nodes))
    if not nets:
        raise ValueError(f"未在{path}中解析到NET_NAME记录")
    return nets


def parse_pstxprt(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None or not path.exists():
        return {}
    lines = read_lines(path)
    parts: dict[str, dict[str, Any]] = {}
    current: dict[str, Any] | None = None
    for number, line in enumerate(lines, start=1):
        match = re.match(r"^\s*([^\s]+)\s+'([^']*)':;", line)
        if match and not line.lstrip().startswith(("C_PATH", "P_PATH")):
            current = {"refdes": match.group(1), "part_name": match.group(2), "source_line": number}
            parts[match.group(1).upper()] = current
            continue
        if current:
            path_match = re.match(r"^\s*(C_PATH|P_PATH)='([^']*)'", line)
            if path_match:
                current[path_match.group(1).lower()] = path_match.group(2)
    return parts


def parse_pstchip(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None or not path.exists():
        return {}
    lines = read_lines(path)
    primitives: dict[str, dict[str, Any]] = {}
    current: dict[str, Any] | None = None
    for number, line in enumerate(lines, start=1):
        match = re.match(r"^\s*primitive\s+'([^']*)'", line, re.I)
        if match:
            current = {"primitive": match.group(1), "source_line": number, "value": None}
            primitives[match.group(1).upper()] = current
            continue
        if current:
            value_match = re.match(r"^\s*VALUE='([^']*)'", line, re.I)
            if value_match:
                current["value"] = value_match.group(1)
    return primitives


def resolve_pst_files(pst_dir: Path) -> dict[str, Path | None]:
    pst_dir = pst_dir.resolve()
    if not pst_dir.is_dir():
        raise ValueError(f"PST目录不存在：{pst_dir}")
    found: dict[str, Path | None] = {}
    for name in EVIDENCE_NAMES:
        matches = [p for p in pst_dir.iterdir() if p.is_file() and p.name.lower() == name]
        if len(matches) > 1:
            raise ValueError(f"PST目录内存在多个{name}：{pst_dir}")
        found[name] = matches[0] if matches else None
    if found["pstxnet.dat"] is None:
        raise ValueError(f"缺少pstxnet.dat：{pst_dir}")
    return found


def load_evidence(pst_dir: Path) -> tuple[list[Net], dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, Path | None]]:
    files = resolve_pst_files(pst_dir)
    return (
        parse_pstxnet(files["pstxnet.dat"]),
        parse_pstxprt(files["pstxprt.dat"]),
        parse_pstchip(files["pstchip.dat"]),
        files,
    )


def assembly_markers(part: dict[str, Any] | None, chip: dict[str, Any] | None) -> list[str]:
    fields = [
        (part or {}).get("part_name", ""),
        (chip or {}).get("primitive", ""),
        (chip or {}).get("value", ""),
    ]
    return [marker for marker in ("TSD", "DNP") if any(marker in str(field).upper() for field in fields)]


def assembly_status(part: dict[str, Any] | None, chip: dict[str, Any] | None) -> str:
    markers = assembly_markers(part, chip)
    return ("原图标记：" + "/".join(markers) if markers else "未发现TSD/DNP标记") + "；当前装配未核实"


def enrich_net(net: Net, parts: dict[str, dict[str, Any]], chips: dict[str, dict[str, Any]], files: dict[str, Path | None], board: str) -> dict[str, Any]:
    rows = []
    for node in net.nodes:
        part = parts.get(node.refdes.upper())
        chip = chips.get(str((part or {}).get("part_name", "")).upper())
        rows.append({
            **asdict(node),
            "part_name": (part or {}).get("part_name"),
            "value": (chip or {}).get("value"),
            "assembly_status": assembly_status(part, chip),
            "assembly_markers": assembly_markers(part, chip),
            "fitted_state": "unknown",
            "assembly_basis": "source_marker_only",
            "part_source": f"{files['pstxprt.dat']}:{part['source_line']}" if part and files["pstxprt.dat"] else None,
            "value_source": f"{files['pstchip.dat']}:{chip['source_line']}" if chip and files["pstchip.dat"] else None,
        })
    complete = all(files[name] is not None for name in EVIDENCE_NAMES)
    return {
        "board": board,
        "pst_dir": str(Path(files["pstxnet.dat"]).parent),
        "network": net.name,
        "network_hierarchy": net.hierarchy,
        "network_source": f"{files['pstxnet.dat']}:{net.source_line}",
        "nodes": rows,
        "evidence_level": EVIDENCE_CONFIRMED,
        "evidence_set_complete": complete,
        "pending": PENDING_CONTINUITY,
    }


def parse_node_selector(selector: str) -> tuple[str, str | None]:
    selector = selector.strip()
    if not selector:
        raise ValueError("节点选择器不能为空")
    if "." in selector:
        refdes, pin = selector.split(".", 1)
        return refdes.upper(), pin.upper()
    return selector.upper(), None


def query_evidence(pst_dir: Path, board: str, net_name: str | None, node_selector: str | None, regex: bool) -> list[dict[str, Any]]:
    if bool(net_name) == bool(node_selector):
        raise ValueError("必须且只能指定--net或--node之一")
    nets, parts, chips, files = load_evidence(pst_dir)
    matched: list[Net] = []
    if net_name:
        if regex:
            pattern = re.compile(net_name, re.I)
            matched = [net for net in nets if pattern.search(net.name)]
        else:
            matched = [net for net in nets if net.name.casefold() == net_name.casefold()]
    else:
        refdes, pin = parse_node_selector(node_selector or "")
        matched = [
            net for net in nets
            if any(node.refdes.upper() == refdes and (pin is None or node.pin.upper() == pin) for node in net.nodes)
        ]
    if not matched:
        key = f"网络{net_name}" if net_name else f"节点{node_selector}"
        raise LookupError(f"未找到{key}：{pst_dir}")
    return [enrich_net(net, parts, chips, files, board) for net in matched]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def pst_header(path: Path) -> str | None:
    for line in read_lines(path)[:10]:
        if "PSTWRITER" in line.upper():
            return line.strip(" {}")
    return None


def file_record(path: Path, root: Path) -> dict[str, Any]:
    stat = path.stat()
    result = {
        "path": str(path),
        "relative_path": str(path.relative_to(root)),
        "size": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
        "sha256": sha256(path),
    }
    if path.name.lower() == "pstxnet.dat":
        result["pstwriter"] = pst_header(path)
    return result


def inventory(root: Path) -> list[dict[str, Any]]:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"资料根目录不存在：{root}")
    boards = []
    for board_dir in sorted((p for p in root.iterdir() if p.is_dir()), key=lambda p: p.name.casefold()):
        relevant = [
            p for p in board_dir.rglob("*") if p.is_file()
            and (p.suffix.lower() in {".dsn", ".pdf"} or p.name.lower() in EVIDENCE_NAMES)
        ]
        if not relevant:
            continue
        by_kind = {
            "dsn": [p for p in relevant if p.suffix.lower() == ".dsn"],
            "pdf": [p for p in relevant if p.suffix.lower() == ".pdf"],
            "pstxnet": [p for p in relevant if p.name.lower() == "pstxnet.dat"],
            "pstxprt": [p for p in relevant if p.name.lower() == "pstxprt.dat"],
            "pstchip": [p for p in relevant if p.name.lower() == "pstchip.dat"],
        }
        counts = {key: len(value) for key, value in by_kind.items()}
        pst_sets = []
        for pst_dir in sorted({p.parent for p in by_kind["pstxnet"]}, key=lambda p: str(p).casefold()):
            local = {name: next((p for p in relevant if p.parent == pst_dir and p.name.lower() == f"{name}.dat"), None) for name in ("pstxnet", "pstxprt", "pstchip")}
            pst_sets.append({
                "directory": str(pst_dir),
                "complete": all(local.values()),
                "files": {name: str(value) if value else None for name, value in local.items()},
                "pstwriter": pst_header(local["pstxnet"]) if local["pstxnet"] else None,
            })
        exact_one = counts["dsn"] == 1 and counts["pdf"] == 1 and len(pst_sets) == 1 and pst_sets[0]["complete"]
        ambiguous = counts["dsn"] > 1 or counts["pdf"] > 1 or len(pst_sets) > 1
        if exact_one:
            status = "完整证据集"
        elif ambiguous:
            status = "多版本候选—禁止自动混用"
        else:
            status = EVIDENCE_INCOMPLETE
        boards.append({
            "board": board_dir.name,
            "board_dir": str(board_dir),
            "status": status,
            "counts": counts,
            "pst_sets": pst_sets,
            "files": [file_record(p, root) for p in sorted(relevant, key=lambda p: str(p).casefold())],
            "pending": None if exact_one else "补齐或人工选择同一版本的DSN、PDF及三类PST文件",
        })
    return boards


def flatten_results(results: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for result in results:
        for node in result["nodes"]:
            rows.append({
                "board": result["board"], "network": result["network"], "refdes": node["refdes"],
                "pin": node["pin"], "pin_name": node["pin_name"], "part_name": node["part_name"],
                "value": node["value"], "assembly_status": node["assembly_status"],
                "assembly_markers": node["assembly_markers"], "fitted_state": node["fitted_state"],
                "assembly_basis": node["assembly_basis"],
                "network_source": result["network_source"], "node_source_line": node["source_line"],
                "evidence_level": result["evidence_level"], "pending": result["pending"],
            })
    return rows


def emit(data: Any, fmt: str) -> None:
    if fmt == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    if isinstance(data, list) and data and "nodes" in data[0]:
        rows = flatten_results(data)
    else:
        rows = data if isinstance(data, list) else [data]
    if fmt == "csv":
        if not rows:
            return
        writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys()), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        return
    if not rows:
        print("无结果")
        return
    if rows and "nodes" not in rows[0] and "network" in rows[0]:
        columns = ["board", "network", "refdes", "pin", "pin_name", "value", "assembly_status", "network_source"]
    else:
        columns = ["board", "status", "counts", "pst_sets", "pending"]
    print("\t".join(columns))
    for row in rows:
        print("\t".join(json.dumps(row.get(column), ensure_ascii=False) if isinstance(row.get(column), (dict, list)) else str(row.get(column) or "") for column in columns))


def parse_board(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("--board格式必须为标签=目录")
    label, directory = value.split("=", 1)
    if not label.strip() or not directory.strip():
        raise argparse.ArgumentTypeError("--board格式必须为标签=目录")
    return label.strip(), Path(directory.strip())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    inventory_parser = sub.add_parser("inventory", help="递归清点板卡DSN/PDF/PST证据")
    inventory_parser.add_argument("--root", required=True, type=Path)
    inventory_parser.add_argument("--format", choices=("table", "json", "csv"), default="table")
    for name in ("query", "multi-query"):
        query = sub.add_parser(name, help="查询PST网络或器件引脚")
        if name == "query":
            query.add_argument("--pst-dir", required=True, type=Path)
            query.add_argument("--board-label")
        else:
            query.add_argument("--board", required=True, action="append", type=parse_board)
        query.add_argument("--net")
        query.add_argument("--node")
        query.add_argument("--regex", action="store_true", help="将--net解释为正则；默认完整网络名匹配")
        query.add_argument("--format", choices=("table", "json", "csv"), default="table")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "inventory":
            emit(inventory(args.root), args.format)
            return 0
        if args.command == "query":
            label = args.board_label or args.pst_dir.resolve().parent.name
            results = query_evidence(args.pst_dir, label, args.net, args.node, args.regex)
        else:
            labels = [label.casefold() for label, _ in args.board]
            if len(labels) != len(set(labels)):
                raise ValueError("--board标签重复")
            results = []
            failures = []
            for label, directory in args.board:
                try:
                    results.extend(query_evidence(directory, label, args.net, args.node, args.regex))
                except LookupError as exc:
                    failures.append(str(exc))
            if not results:
                raise LookupError("；".join(failures))
        emit(results, args.format)
        return 0
    except (ValueError, LookupError, OSError, re.error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
