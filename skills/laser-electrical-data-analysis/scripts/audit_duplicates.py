"""Read-only duplicate audit. No deletion/keeper selection; outputs outside source root."""
from __future__ import annotations
import argparse
import collections
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "hardware-evidence-report-sync" / "scripts"))
from evidence_paths import inside, long_path, probe, sha256, walk, write_csv

def scan(root):
    errors, files = [], []
    state = probe(root)
    if state["status"] != "exists" or not state.get("is_dir"):
        return [], [{"path": str(root), "error": state["status"] + ": " + state["reason"]}]
    for _, _, paths in walk(root, errors):
        for path in paths:
            try:
                size = os.stat(long_path(path)).st_size
                files.append({"path": str(path), "relative_path": str(path.relative_to(root)), "bytes": size})
            except OSError as exc:
                errors.append({"path": str(path), "error": str(exc)})
    return files, errors

def duplicate_groups(files, errors):
    by_size = collections.defaultdict(list)
    for row in files:
        by_size[row["bytes"]].append(row)
    groups = []
    for rows in by_size.values():
        if len(rows) < 2:
            continue
        by_hash = collections.defaultdict(list)
        for row in rows:
            try:
                digest = sha256(row["path"])
                by_hash[digest].append({**row, "sha256": digest})
            except OSError as exc:
                errors.append({"path": row["path"], "error": str(exc)})
        for digest, equal in by_hash.items():
            if len(equal) < 2:
                continue
            parents = collections.Counter(str(Path(r["path"]).parent).casefold() for r in equal)
            for row in equal:
                row["classification"] = "B_同目录双名_只标注" if parents[str(Path(row["path"]).parent).casefold()] > 1 else "跨目录重复候选_待确认"
            groups.append({"sha256": digest, "copies": len(equal), "bytes_each": equal[0]["bytes"], "redundant_bytes": (len(equal)-1)*equal[0]["bytes"], "files": equal})
    return sorted(groups, key=lambda g: (-g["redundant_bytes"], g["sha256"]))

def run(root, out):
    root, out = root.resolve(), out.resolve()
    if inside(out, root):
        raise ValueError("output must be outside source root")
    out.mkdir(parents=True, exist_ok=True)
    files, errors = scan(root)
    groups = duplicate_groups(files, errors)
    rows = [{**r, "group": i} for i, group in enumerate(groups, 1) for r in group["files"]]
    fields = ["group", "relative_path", "path", "bytes", "sha256", "classification"]
    write_csv(out/"重复文件清单.csv", rows, fields)
    write_csv(out/"B类标注清单.csv", [r for r in rows if r["classification"].startswith("B_")], fields)
    partitions = {}
    for row in rows:
        key = Path(row["relative_path"]).parts[0]
        part = partitions.setdefault(key, {"partition": key, "duplicate_copies": 0, "duplicate_copy_bytes": 0})
        part["duplicate_copies"] += 1
        part["duplicate_copy_bytes"] += row["bytes"]
    write_csv(out/"重复数据分区汇总.csv", list(partitions.values()), ["partition","duplicate_copies","duplicate_copy_bytes"])
    summary = {"complete": not errors, "files": len(files), "bytes": sum(r["bytes"] for r in files), "groups": len(groups), "duplicate_copies": len(rows), "redundant_bytes": sum(g["redundant_bytes"] for g in groups), "errors": errors, "note": "冗余字节是内容重复理论值，不是允许删除量；分区字节含全部重复份，不跨分区指定保留件。"}
    (out/"baseline_snapshot.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    result = run(args.root, args.out)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["complete"] else 2

if __name__ == "__main__":
    raise SystemExit(main())

