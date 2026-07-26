#!/usr/bin/env python3
"""Collect likely report assets from a measurement-result directory."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}
DATA_EXTS = {".csv", ".mat", ".xls", ".xlsx", ".xlsm", ".txt", ".md"}


@dataclass
class Asset:
    category: str
    role: str
    name: str
    rel_path: str
    abs_path: str
    size_bytes: int
    modified_time: str


def classify(path: Path) -> tuple[str, str]:
    suffix = path.suffix.lower()
    name = path.name.lower()
    if suffix in IMAGE_EXTS:
        category = "image"
    elif suffix in DATA_EXTS:
        category = "data"
    else:
        category = "other"

    role_parts: list[str] = []
    if "asd" in name:
        role_parts.append("ASD")
    if "psd" in name:
        role_parts.append("PSD")
    if "compare" in name or "对比" in name:
        role_parts.append("compare")
    if "summary" in name or "汇总" in name:
        role_parts.append("summary")
    if "manifest" in name:
        role_parts.append("manifest")
    if "report" in name or "报告" in name:
        role_parts.append("report")
    if not role_parts:
        role_parts.append("raw")
    return category, "+".join(role_parts)


def collect(root: Path) -> list[Asset]:
    assets: list[Asset] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in IMAGE_EXTS | DATA_EXTS:
            continue
        category, role = classify(path)
        stat = path.stat()
        assets.append(
            Asset(
                category=category,
                role=role,
                name=path.name,
                rel_path=str(path.relative_to(root)),
                abs_path=str(path.resolve()),
                size_bytes=stat.st_size,
                modified_time=str(stat.st_mtime),
            )
        )
    return assets


def write_csv(path: Path, assets: list[Asset]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "category",
                "role",
                "name",
                "rel_path",
                "abs_path",
                "size_bytes",
                "modified_time",
            ],
        )
        writer.writeheader()
        for asset in assets:
            writer.writerow(asdict(asset))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result_dir", help="Directory containing result figures/data")
    parser.add_argument("--output", help="Optional CSV manifest path")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text summary")
    args = parser.parse_args()

    root = Path(args.result_dir).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Result directory not found: {root}")

    assets = collect(root)
    if args.output:
        write_csv(Path(args.output).expanduser().resolve(), assets)

    if args.json:
        print(json.dumps([asdict(asset) for asset in assets], ensure_ascii=False, indent=2))
    else:
        print(f"root: {root}")
        print(f"assets: {len(assets)}")
        for category in ["image", "data", "other"]:
            count = sum(1 for item in assets if item.category == category)
            print(f"{category}: {count}")
        for asset in assets[:50]:
            print(f"{asset.category:5s} {asset.role:18s} {asset.rel_path}")
        if len(assets) > 50:
            print(f"... {len(assets) - 50} more")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
