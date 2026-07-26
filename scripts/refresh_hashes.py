#!/usr/bin/env python3
"""Refresh staged content hashes after an intentional repository edit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


def hash_file(path: Path) -> str:
    payload = path.read_bytes()
    if b"\0" not in payload:
        try:
            text = payload.decode("utf-8-sig")
            payload = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
        except UnicodeDecodeError:
            pass
    return hashlib.sha256(payload).hexdigest()


def hash_tree(path: Path) -> str:
    digest = hashlib.sha256()
    files = sorted(
        (item for item in path.rglob("*") if item.is_file()),
        key=lambda item: item.as_posix().lower(),
    )
    for item in files:
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(hash_file(item).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    registry_path = repo / "registry" / "skills.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    for entry in registry["skills"]:
        skill_dir = repo / entry["canonical_path"]
        entry["staged_skill_sha256"] = hash_file(skill_dir / "SKILL.md")
        entry["staged_tree_sha256"] = hash_tree(skill_dir)
    registry_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    csv_path = repo / "registry" / "skills.csv"
    fieldnames = [
        "name",
        "category",
        "canonical_path",
        "nested_under",
        "source_kind",
        "source_relative_path",
        "declared_license",
        "license_evidence",
        "source_remote",
        "ownership_status",
        "publish_policy",
        "source_skill_sha256",
        "staged_skill_sha256",
        "staged_tree_sha256",
        "generated_openai_yaml",
        "issues_from_audit",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for entry in registry["skills"]:
            row = dict(entry)
            row["issues_from_audit"] = " | ".join(entry.get("issues_from_audit", []))
            writer.writerow(row)
    print(f"Refreshed {len(registry['skills'])} registry entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
