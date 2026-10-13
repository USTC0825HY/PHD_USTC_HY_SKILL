#!/usr/bin/env python3
"""Read-only coverage and link check for the root and category READMEs."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT_ROW = re.compile(r"^\| \[([^]]+)\]\(docs/categories/([a-z0-9-]+)/README\.md\) \| (\d+) \|", re.M)
CLASS_ROW = re.compile(r"^\| \[([^]]+)\]\(categories/([a-z0-9-]+)/README\.md\) \| (\d+) \|", re.M)
SKILL_ROW = re.compile(r"^\| \[([a-z0-9-]+)\]\(([^)]+/SKILL\.md)\) \| ([^|]+) \|$", re.M)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    registry = json.loads((repo / "registry" / "skills.json").read_text(encoding="utf-8"))
    entries = {item["name"]: item for item in registry["skills"]}
    errors: list[str] = []
    root = (repo / "README.md").read_text(encoding="utf-8")
    rows = ROOT_ROW.findall(root)
    classification = (repo / "docs" / "CLASSIFICATION.md").read_text(encoding="utf-8")
    if CLASS_ROW.findall(classification) != rows:
        errors.append("classification_index_mismatch")
    if not rows or len({label for label, _, _ in rows}) != len(rows):
        errors.append(f"root_category_rows:{len(rows)}")
    category_counts = Counter(item["category"] for item in entries.values())
    if set(category_counts) != {label for label, _, _ in rows}:
        errors.append("root_category_labels_mismatch")
    if f"{len(entries)} 个逻辑 Skill" not in root:
        errors.append("root_logical_count_mismatch")
    physical = len([item for item in (repo / "skills").iterdir() if item.is_dir()])
    if f"{physical} 个顶层目录" not in root:
        errors.append("root_physical_count_mismatch")
    nested = sum(bool(item.get("nested_under")) for item in entries.values())
    if f"{nested} 个" not in root:
        errors.append("root_nested_count_mismatch")

    observed: Counter[str] = Counter()
    for label, slug, count_text in rows:
        path = repo / "docs" / "categories" / slug / "README.md"
        if not path.is_file():
            errors.append(f"missing_category_page:{slug}")
            continue
        text = path.read_text(encoding="utf-8")
        found = SKILL_ROW.findall(text)
        if len(found) != int(count_text) or len(found) != category_counts[label]:
            errors.append(f"category_count_mismatch:{slug}")
        for name, link, summary in found:
            observed[name] += 1
            entry = entries.get(name)
            if entry is None:
                errors.append(f"unregistered_skill:{name}")
                continue
            if entry["category"] != label:
                errors.append(f"wrong_category:{name}")
            expected = f"../../../{entry['canonical_path']}/SKILL.md"
            if link != expected or not (path.parent / link).is_file():
                errors.append(f"invalid_skill_link:{name}")
            if not re.search(r"[\u4e00-\u9fff]", summary):
                errors.append(f"missing_chinese_summary:{name}")
    if set(observed) != set(entries):
        errors.append(f"skill_coverage_mismatch:missing={sorted(set(entries) - set(observed))}")
    errors.extend(f"duplicate_skill:{name}" for name, count in observed.items() if count != 1)

    actual_pages = {path.parent.name for path in (repo / "docs" / "categories").glob("*/README.md")}
    if actual_pages != {slug for _, slug, _ in rows}:
        errors.append("category_page_set_mismatch")
    result = {"status": "fail" if errors else "pass", "logical_skills": len(entries), "top_level_directories": physical, "categories": len(rows), "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
