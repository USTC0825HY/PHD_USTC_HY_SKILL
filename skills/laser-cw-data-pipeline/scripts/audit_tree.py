"""Read-only 513 layout audit. Exit 2: unavailable/unknown; 1: errors; 0: complete scan."""
import argparse
import json
import os
import re
from pathlib import Path
from taxonomy import BLACKLIST, CAMPAIGNS, DEVICES, GROUPS, INDICATORS, INTERFACES
from layouts import LAYOUTS, SNAPSHOT_INDICATORS, campaign_roots, detect_layout, probe, walk
from evidence_paths import long_path

SESSION_RE = re.compile(r"^20\d{6}_\d{4}$")
RUN_RE = re.compile(r"^run_20\d{6}_\d{6}_.+$")
META_FILES = {"INDEX.md", "_session.md", "README.md", "README_先看.md"}

def audit(root, layout="auto", campaign=None):
    findings, errors, coverage, empty, stray, large, failed = [], [], [], [], [], [], []
    def add(severity, code, path, message):
        findings.append(dict(severity=severity, code=code, path=str(path), message=message))
    try:
        layout = detect_layout(root, layout)
        targets = campaign_roots(root, layout, campaign)
    except ValueError as exc:
        return dict(layout="unknown", errors=1, warnings=0, complete=False, findings=[dict(severity="error", code="TREE.UNRESOLVED", path=str(root), message=str(exc))])
    file_count = byte_count = 0
    for target in targets:
        state = probe(target)
        if state["status"] != "exists":
            add("error", "TREE.ROOT_" + state["status"].upper(), target, state["reason"])
            continue
        inventory = list(walk(target, errors))
        counts = {}
        for folder, _, files in inventory:
            data_files = [p for p in files if p.name not in META_FILES]
            for ancestor in (folder, *folder.parents):
                if ancestor == target.parent:
                    break
                counts[ancestor] = counts.get(ancestor, 0) + len(data_files)
        for folder, dirs, files in inventory:
            parts = folder.relative_to(target).parts
            if not dirs and not files:
                empty.append(str(folder))
            if any(f.name.startswith("STATUS_FAIL") for f in files):
                failed.append(str(folder))
            for path in files:
                try:
                    size = os.stat(long_path(path)).st_size
                    file_count += 1
                    byte_count += size
                    if size >= 500 * 1024 * 1024:
                        large.append({"path": str(path), "bytes": size, "disposition": "低频归档候选；原地保留"})
                except OSError as exc:
                    errors.append({"path": str(path), "error": str(exc)})
            if not parts:
                stray.extend(str(p) for p in files if p.name not in META_FILES)
                continue
            if folder.name.startswith("run_") and not RUN_RE.fullmatch(folder.name):
                add("warning", "RUN.NAME", folder, "run 日期应为 YYYYMMDD_HHMMSS")
            if layout == "snapshot-v2":
                if folder.name == "result":
                    add("info", "LEGACY.RESULT", folder, "历史单数结果目录；原位保留")
                if folder.name == "results" and "raw" in parts:
                    add("info", "COMPAT.RESULTS_IN_RAW", folder, "现行 MATLAB 输出位置；不上提、不改名")
                if any(p.startswith(("_legacy", "_from_")) for p in parts):
                    if len(parts) == 2:
                        add("info", "LEGACY.PRESERVE", folder, "隔离树保留；不从名称推断可删除")
                    continue
                if any(token in folder.name.lower() for token in BLACKLIST):
                    add("warning", "LEGACY.SPELLING", folder, "目录笔误候选；需明确逐目录映射")
                if len(parts) == 1 and parts[0] in ("ADC128", "ad677"):
                    add("warning", "NAME.DEVICE_ALIAS", folder, "v2 标准名 AD128/AD677；不自动改名")
                device = parts[0]
                if device in SNAPSHOT_INDICATORS and folder.name in SNAPSHOT_INDICATORS[device]:
                    covered = counts.get(folder, 0)
                    coverage.append({"campaign": target.name, "device": device, "indicator": folder.name, "path": str(folder), "files": covered, "state": "有文件，测量覆盖另核" if covered else "空脚手架"})
                # Batch/theme/readme directories are legitimate in this snapshot.
                continue
            if parts[0].startswith("_"):
                continue
            if parts[0] not in GROUPS:
                if len(parts) == 1:
                    add("error", "TREE.GROUP", folder, "板组应为 SZSD/YCQD")
                continue
            if len(parts) < 2:
                continue
            dev = parts[1]
            if dev not in DEVICES[parts[0]]:
                if len(parts) == 2:
                    add("error", "TREE.DEVICE", folder, "器件不在本板组枚举")
                continue
            if len(parts) >= 3 and parts[2] not in INDICATORS[dev]:
                if len(parts) == 3:
                    add("error", "TREE.INDICATOR", folder, "指标不在 session-v1 枚举")
                continue
            if len(parts) == 3:
                covered = counts.get(folder, 0)
                coverage.append({"campaign": target.name, "device": dev, "indicator": parts[2], "path": str(folder), "files": covered, "state": "有文件，测量覆盖另核" if covered else "空脚手架"})
                stray.extend(str(p) for p in files if p.name not in META_FILES)
            if len(parts) == 4 and parts[3] not in INTERFACES[dev]:
                add("error", "TREE.INTERFACE", folder, "接口不在枚举")
            if len(parts) == 5:
                if not SESSION_RE.fullmatch(parts[4]):
                    add("error", "SESSION.FORMAT", folder, "会话日期应为 YYYYMMDD_HHMM")
                else:
                    if "_session.md" not in {p.name for p in files}:
                        add("warning", "SESSION.NO_META", folder, "采集条件与改焊状态待填写")
                    if "raw" not in {p.name for p in dirs} and (files or dirs):
                        add("warning", "SESSION.NO_RAW", folder, "缺 raw；核查是否为纯分析会话")
            if len(parts) == 6 and parts[5] not in ("raw", "results"):
                add("warning", "SESSION.STRAY_DIR", folder, "会话层非 raw/results 目录")
    for issue in errors:
        add("error", "SCAN.INACCESSIBLE", issue["path"], issue["error"])
    return dict(layout=layout, errors=sum(f["severity"] == "error" for f in findings), warnings=sum(f["severity"] == "warning" for f in findings), complete=not errors and not any(f["code"].startswith("TREE.ROOT_") for f in findings), files=file_count, bytes=byte_count, findings=findings, coverage=coverage, empty_directories=empty, stray_files=stray, large_files=large, failed_runs=failed)

def audit_campaign(croot):
    return audit(croot, "session-v1")["findings"]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--campaign", choices=CAMPAIGNS)
    parser.add_argument("--layout", choices=LAYOUTS, default="auto")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = audit(args.root.absolute(), args.layout, args.campaign)
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else "\n".join(f"{r['severity']} {r['code']}: {r['path']} {r['message']}" for r in report["findings"]) + f"\nerrors={report['errors']} warnings={report['warnings']} complete={report['complete']}")
    return 2 if not report["complete"] else (1 if report["errors"] else 0)

if __name__ == "__main__":
    raise SystemExit(main())

