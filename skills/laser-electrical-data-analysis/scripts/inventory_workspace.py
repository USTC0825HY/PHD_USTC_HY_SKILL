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

from _portable_profile import profile_path


DEFAULT_LASER_ROOT = profile_path("laser_source_root", Path.home() / "Laser")
DEFAULT_VAULT_ROOT = profile_path("obsidian_vault_root", Path.home() / "Obsidian")
DEFAULT_CODE = profile_path(
    "matlab_code_root",
    DEFAULT_LASER_ROOT / "03_Code_代码工程" / "02_MATLAB分析" / "MATLAB",
)
DEFAULT_DATA = profile_path("test_data_root", Path.home() / "Laser-Test-Data")
DEFAULT_513_CODE = profile_path(
    "cw513_analysis_root",
    DEFAULT_LASER_ROOT
    / "code"
    / "matlab"
    / "513DIANXING_analysis"
    / "CW_analysis"
    / "CW_513_ANALYSIS",
)
DEFAULT_513_DATA = profile_path(
    "cw513_test_data_root",
    DEFAULT_LASER_ROOT / "0_20260727_513test" / "CW_Data" / "513_CW_DATA",
)
DEFAULT_REPORT = (
    DEFAULT_VAULT_ROOT
    / "01_科研主系统"
    / "04_实验测试与证据"
    / "03_超稳激光电控箱指标测试"
    / "LASER 测试报告"
    / "202607"
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
            [
                "git",
                "-c",
                f"safe.directory={root}",
                "-C",
                str(root),
                "status",
                "--short",
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return [line for line in result.stdout.splitlines() if line]
    except OSError:
        return ["git unavailable"]


ROOT_CONFIG = {
    "code": ("matlab_code_root", "LASER_TEST_CODE_ROOT", DEFAULT_CODE),
    "data": ("test_data_root", "LASER_TEST_DATA_ROOT", DEFAULT_DATA),
    "report": ("formal_report_corpus", "LASER_TEST_REPORT_ROOT", DEFAULT_REPORT),
    "cw513_code": ("cw513_analysis_root", "LASER_TEST_513_CODE_ROOT", DEFAULT_513_CODE),
    "cw513_data": ("cw513_test_data_root", "LASER_TEST_513_DATA_ROOT", DEFAULT_513_DATA),
    "requirement": ("requirement_root", "LASER_TEST_REQUIREMENT_ROOT", profile_path("requirement_root", DEFAULT_DATA / "测试参考文件_20260630")),
}


def resolve_roots(overrides=None, required_roots=None):
    overrides = overrides or {}
    required = set(ROOT_CONFIG if required_roots is None else required_roots)
    unknown = (set(overrides) | required) - set(ROOT_CONFIG)
    if unknown:
        raise ValueError("unknown roots: " + ", ".join(sorted(unknown)))
    roots = {name: Path(overrides[name]) if overrides.get(name) is not None else env_path(env, default)
             for name, (_, env, default) in ROOT_CONFIG.items()}
    unavailable = [{"root": name, "key": ROOT_CONFIG[name][0], "path": str(path),
                    "required": name in required, "error": "directory missing or wrong type"}
                   for name, path in roots.items() if not path.is_dir()]
    return roots, unavailable


def build_inventory(include_hash: bool, overrides=None, required_roots=None) -> dict:
    roots, unavailable = resolve_roots(overrides, required_roots)
    if any(row["required"] for row in unavailable):
        raise ValueError(json.dumps({"status": "missing_required_roots", "unavailable_roots": unavailable}, ensure_ascii=False))
    code, data, report = (roots[k] for k in ("code", "data", "report"))
    cw513_code, cw513_data, requirement_root = (roots[k] for k in ("cw513_code", "cw513_data", "requirement"))
    formal_root = report / "01_正式报告"
    digital_report = formal_root / "02_SZSD_数字锁定板" / "数字锁定板测试报告.docx"

    scripts = []
    if code.is_dir():
        for path in sorted(code.glob("s[0-9][0-9]_*.m")):
            text = path.read_text(encoding="utf-8", errors="replace")
            row = info(path, include_hash)
            row["has_conflict_markers"] = bool(
                re.search(r"(?m)^(?:<<<<<<< .+|=======\s*|>>>>>>> .+)$", text)
            )
            scripts.append(row)

    cw513_scripts = []
    if cw513_code.is_dir():
        for path in sorted(cw513_code.rglob("*.m")):
            if any(part in {"legacy", "_release"} for part in path.parts):
                continue
            row = info(path, include_hash)
            row["device"] = next(
                (part for part in ("9245_hy", "2208_hy", "9726_hy", "766_hy") if part in path.parts),
                "_shared/tools/tests",
            )
            row["has_conflict_markers"] = bool(
                re.search(r"(?m)^(?:<<<<<<< .+|=======\s*|>>>>>>> .+)$", path.read_text(encoding="utf-8", errors="replace"))
            )
            cw513_scripts.append(row)

    top_data = []
    if data.is_dir():
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
        "status": "partial_inventory" if unavailable else "available",
        "unavailable_roots": unavailable,
        "verified_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "roots": {name: str(path) for name, path in roots.items()},
        "git_status": git_status(code),
        "matlab_scripts": scripts,
        "cw513_matlab_scripts": cw513_scripts,
        "cw513_data_directories": [
            info(path) for path in sorted(cw513_data.iterdir())
        ] if cw513_data.is_dir() else [],
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
    rows = [{"category": "unavailable_root", **item} for item in inventory.get("unavailable_roots", [])]
    for key in ("matlab_scripts", "cw513_matlab_scripts", "data_directories", "cw513_data_directories", "report_locks",
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
    for name in ROOT_CONFIG:
        parser.add_argument("--" + name.replace("_", "-") + "-root", type=Path)
    parser.add_argument("--require-root", action="append", choices=sorted(ROOT_CONFIG),
                        help="Require only these task roots; default requires all roots")
    args = parser.parse_args()
    overrides = {name: getattr(args, name + "_root") for name in ROOT_CONFIG
                 if getattr(args, name + "_root") is not None}
    try:
        inventory = build_inventory(args.hash, overrides, args.require_root)
    except ValueError as exc:
        print(str(exc))
        return 2
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
