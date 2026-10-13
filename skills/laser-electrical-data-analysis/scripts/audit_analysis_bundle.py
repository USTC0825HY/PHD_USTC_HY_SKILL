#!/usr/bin/env python3
"""Audit the minimum evidence contract of a Laser analysis result directory."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ALLOWED_STATES = {"满足", "不满足", "暂不能判定", "未测试"}


def matching(files: list[Path], *tokens: str) -> list[Path]:
    return [p for p in files if all(token.lower() in p.name.lower() for token in tokens)]


def read_headers(path: Path) -> list[str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            return next(csv.reader(stream))
    except (OSError, StopIteration, UnicodeError):
        return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result_dir", type=Path)
    parser.add_argument(
        "--kind", choices=("auto", "spectral", "calibration", "allan", "generic"),
        default="auto",
    )
    parser.add_argument("--json", dest="json_path", type=Path)
    parser.add_argument("--strict", action="store_true", help="Validate declared evidence layers; unverified is nonzero")
    args = parser.parse_args()
    root = args.result_dir
    errors: list[str] = []
    warnings: list[str] = []
    if not root.is_dir():
        print(f"ERROR: result directory not found: {root}")
        return 2
    if args.strict:
        from bundle_validation import strict_audit
        result = strict_audit(root, args.kind)
        payload = json.dumps(result, ensure_ascii=False, indent=2)
        print(payload)
        if args.json_path: args.json_path.write_text(payload, encoding="utf-8")
        return 0 if result["status"] == "PASS" else 1
    files = [p for p in root.rglob("*") if p.is_file()]
    csv_files = [p for p in files if p.suffix.lower() == ".csv"]
    png_files = [p for p in files if p.suffix.lower() == ".png"]
    mat_files = [p for p in files if p.suffix.lower() == ".mat"]

    parameter_files = matching(csv_files, "parameter")
    summary_files = matching(csv_files, "summary")
    spectrum_files = [p for p in csv_files if "psd" in p.name.lower() and "asd" in p.name.lower()]
    asd_figures = matching(png_files, "asd")
    psd_figures = matching(png_files, "psd")
    measurement_files = matching(csv_files, "measurement")
    fit_figures = matching(png_files, "fit")
    allan_figures = [p for p in png_files if any(t in p.name.lower() for t in ("allan", "adev", "mdev"))]
    kind = args.kind
    if kind == "auto":
        names = "\n".join(p.name.lower() for p in files)
        if "fit_summary" in names or "vpp_measurement" in names:
            kind = "calibration"
        elif any(token in names for token in ("allan", "adev", "mdev")):
            kind = "allan"
        elif spectrum_files or asd_figures or psd_figures:
            kind = "spectral"
        else:
            kind = "generic"
    if not parameter_files:
        errors.append("missing analysis-parameters CSV")
    if not summary_files:
        errors.append("missing summary CSV")
    if kind == "spectral":
        if not spectrum_files:
            errors.append("missing full PSD/ASD spectrum CSV")
        if not asd_figures:
            errors.append("missing ASD figure")
        if not psd_figures:
            errors.append("missing PSD figure")
    elif kind == "calibration":
        if not measurement_files:
            errors.append("missing calibration measurements CSV")
        if not fit_figures:
            errors.append("missing calibration fit/residual figure")
    elif kind == "allan" and not allan_figures:
        errors.append("missing Allan/ADEV/MDEV figure")
    if not mat_files:
        warnings.append("missing reproducible MAT result")

    metadata_text = "\n".join(
        p.read_text(encoding="utf-8", errors="replace").lower()
        for p in parameter_files + summary_files + measurement_files
    )
    required_groups = {
        "sample rate": ("sample_rate", "fshz", "fs_hz", "total_fs", "sampling_rate"),
        "calibration/reference": ("calibration", "reference_plane", "l_adc", "k_adc"),
    }
    if kind == "spectral":
        required_groups["band"] = ("band_start", "starthz", "band_start_hz", "analysis_band", "target_band")
    for label, tokens in required_groups.items():
        if not any(token in metadata_text for token in tokens):
            warnings.append(f"metadata not discoverable in CSV headers: {label}")

    text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in summary_files)
    seen_states = {state for state in ALLOWED_STATES if state in text}
    invalid = set(re.findall(r"\b(?:PASS|FAIL|MEETS|DOES_NOT_MEET|通过|未通过)\b", text, re.I))
    if invalid:
        warnings.append("noncanonical formal states found: " + ", ".join(sorted(invalid)))
    if kind in {"spectral", "allan", "generic"} and not seen_states:
        warnings.append("no canonical formal conclusion state found")
    if not re.search(r"sha[-_ ]?256", text, re.I):
        warnings.append("input SHA-256 is not recorded in summary CSV")

    result = {
        "result_dir": str(root),
        "kind": kind,
        "file_count": len(files),
        "mode": "legacy_structure_only",
        "acceptance": "not_strictly_verified",
        "errors": errors,
        "warnings": warnings,
        "status": "ERROR" if errors else ("WARN" if warnings else "PASS"),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.json_path:
        args.json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
