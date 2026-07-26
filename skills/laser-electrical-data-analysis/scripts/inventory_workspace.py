#!/usr/bin/env python3
"""Read-only inventory for the Laser electrical-test workspace."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_CODE = Path(r"F:\01_Laser\03_Code_代码工程\02_MATLAB分析\MATLAB")
DEFAULT_DATA = Path(r"G:\01_laser\202607_电2test")
DEFAULT_REPORT = Path(
    r"C:\01_obsidian\ustc_hy\01_科研主系统\04_实验测试与证据"
    r"\03_超稳激光电控箱指标测试\LASER 测试报告\202607"
)


def env_path(name: str, default: Path) -> Path:
    value = os.environ.get(name, "").strip()
    return Path(value) if value else default


def info(path: Path, with_hash: bool = False) -> dict:
    row = {"path": str(path), "exists": path.exists()}
    if not path.exists():
        return row
    stat = path.stat()
    row.update(size=stat.st_size, modified=datetime.fromtimestamp(stat.st_mtime).isoformat())
    if with_hash and path.is_file():
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        row["sha256"] = digest.hexdigest()
    return row


def newest(
    root: Path, pattern: str, limit: int = 20, include_lock_files: bool = False
) -> list[dict]:
    if not root.exists():
        return []
    candidates = root.rglob(pattern)
    if not include_lock_files:
        candidates = (path for path in candidates if not path.name.startswith("~$"))
    files = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)
    return [info(path) for path in files[:limit]]


def git_status(root: Path) -> list[str]:
    if not root.exists():
        return []
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "status", "--short"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return [line for line in result.stdout.splitlines() if line]
    except OSError:
        return ["git unavailable"]


def build_inventory(include_hash: bool) -> dict:
    code = env_path("LASER_TEST_CODE_ROOT", DEFAULT_CODE)
    data = env_path("LASER_TEST_DATA_ROOT", DEFAULT_DATA)
    report = env_path("LASER_TEST_REPORT_ROOT", DEFAULT_REPORT)
    requirement_root = data / "测试参考文件_20260630"
    formal_root = report / "01_正式报告"
    digital_report = formal_root / "02_SZSD_数字锁定板" / "数字锁定板测试报告.docx"

    scripts = []
    if code.exists():
        for path in sorted(code.glob("s[0-9][0-9]_*.m")):
            text = path.read_text(encoding="utf-8", errors="replace")
            row = info(path, include_hash)
            row["has_conflict_markers"] = bool(
                re.search(r"(?m)^(?:<<<<<<< .+|=======\s*|>>>>>>> .+)$", text)
            )
            scripts.append(row)

    top_data = []
    if data.exists():
        top_data = [info(path) for path in sorted(data.iterdir()) if path.is_dir()]

    locks = newest(report, "~$*", include_lock_files=True) if report.exists() else []
    sibling_locks = []
    if digital_report.parent.exists():
        sibling_locks = [
            item for item in newest(
                digital_report.parent, "~$*", 50, include_lock_files=True
            )
            if Path(item["path"]).parent == digital_report.parent
            and Path(item["path"]).suffix.lower() == digital_report.suffix.lower()
        ]
    expected_lock_names = {
        "~$" + digital_report.name,
        "~$" + digital_report.name[2:],
    }
    digital_report_locks = [
        item for item in sibling_locks
        if Path(item["path"]).name in expected_lock_names
    ]
    return {
        "verified_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "roots": {"code": str(code), "data": str(data), "report": str(report)},
        "git_status": git_status(code),
        "matlab_scripts": scripts,
        "data_directories": top_data,
        "digital_lock_report": info(
            digital_report, include_hash and not digital_report_locks
        ),
        "digital_lock_report_locked": bool(digital_report_locks),
        "digital_lock_report_locks": digital_report_locks,
        "report_locks": locks,
        "latest_requirements": newest(requirement_root, "*性能测试项*.docx", 10),
        "latest_ad_fit_summaries": newest(
            data / "SZSD_AD2208", "*vpp_fit_summary*.csv", 20
        ),
        "latest_da_fit_summaries": newest(
            data / "SZSD_DAC9726", "*vpp_fit_summary*.csv", 20
        ),
    }


def flatten(inventory: dict) -> list[dict]:
    rows = []
    for key in ("matlab_scripts", "data_directories", "report_locks",
                "digital_lock_report_locks", "latest_requirements",
                "latest_ad_fit_summaries", "latest_da_fit_summaries"):
        for item in inventory.get(key, []):
            rows.append({"category": key, **item})
    rows.append({"category": "digital_lock_report", **inventory["digital_lock_report"]})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="Optional .json or .csv output; stdout is default")
    parser.add_argument("--hash", action="store_true", help="Hash files; skipped for a locked report")
    args = parser.parse_args()
    inventory = build_inventory(args.hash)
    if not args.output:
        print(json.dumps(inventory, ensure_ascii=False, indent=2))
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.suffix.lower() == ".csv":
        rows = flatten(inventory)
        fields = sorted({key for row in rows for key in row})
        with args.output.open("w", newline="", encoding="utf-8-sig") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    else:
        args.output.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
