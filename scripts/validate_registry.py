#!/usr/bin/env python3
"""Validate the canonical Skill registry without modifying repository files."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import Any


FORBIDDEN_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    "dist",
    "build",
}

SECRET_PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "openai_key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "generic_secret_assignment": re.compile(
        r"""(?imx)
        \b(?:api[_-]?key|access[_-]?token|auth[_-]?token|password|secret)
        \s*=\s*
        ["']([A-Za-z0-9_./+=-]{16,})["']
        """
    ),
}

LOCAL_PATH_PATTERN = re.compile(
    r"(?i)(?:[A-Z]:[\\/]Users[\\/][^\\/]+[\\/]|"
    r"[A-Z]:[\\/](?:01_|02_|03_|04_|05_|06_|07_|08_|09_)|"
    r"/(?:Users|home)/[^/]+/)"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    match = re.match(r"^---\s*\r?\n(.*?)\r?\n---(?:\s*\r?\n|$)", text, re.S)
    if not match:
        return {}
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(match.group(1))
        return loaded if isinstance(loaded, dict) else {}
    except Exception:
        data: dict[str, Any] = {}
        for key in ("name", "description"):
            item = re.search(rf"(?m)^{key}:\s*(.+?)\s*$", match.group(1))
            if item:
                data[key] = item.group(1).strip().strip("'\"")
        return data


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
        relative = item.relative_to(path).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hash_file(item).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def is_placeholder(value: str) -> bool:
    lowered = value.lower()
    return any(
        marker in lowered
        for marker in (
            "your_",
            "example",
            "placeholder",
            "changeme",
            "dummy",
            "xxxx",
            "token_here",
        )
    )


def inspect_text_file(path: Path) -> tuple[list[str], bool]:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return [], False
    findings: list[str] = []
    for label, pattern in SECRET_PATTERNS.items():
        for match in pattern.finditer(text):
            value = match.group(1) if match.groups() else match.group(0)
            if not is_placeholder(value):
                findings.append(label)
                break
    return findings, bool(LOCAL_PATH_PATTERN.search(text))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--write-report")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    registry = load_json(repo / "registry" / "skills.json")
    entries = registry.get("skills", [])
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    secret_findings: list[dict[str, str]] = []
    local_path_files: list[str] = []
    canonical_paths: list[str] = []

    for entry in entries:
        name = str(entry["name"])
        canonical = repo / str(entry["canonical_path"])
        canonical_paths.append(str(canonical.resolve()).lower())
        skill_file = canonical / "SKILL.md"
        if not skill_file.is_file():
            errors.append({"skill": name, "issue": "missing_SKILL.md"})
            continue
        if skill_file.read_bytes().startswith(b"\xef\xbb\xbf"):
            errors.append({"skill": name, "issue": "utf8_bom_present"})
        frontmatter = parse_frontmatter(skill_file)
        if frontmatter.get("name") != name:
            errors.append(
                {
                    "skill": name,
                    "issue": f"frontmatter_name_mismatch:{frontmatter.get('name')}",
                }
            )
        description = frontmatter.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append({"skill": name, "issue": "missing_description"})
        if not re.fullmatch(r"[a-z0-9-]{1,63}", name):
            errors.append({"skill": name, "issue": "nonstandard_name"})
        openai_yaml = canonical / "agents" / "openai.yaml"
        if not openai_yaml.is_file():
            warnings.append({"skill": name, "issue": "missing_agents_openai_yaml"})
        else:
            try:
                ui_text = openai_yaml.read_text(encoding="utf-8")
                if f"${name}" not in ui_text:
                    warnings.append(
                        {"skill": name, "issue": "default_prompt_missing_skill_name"}
                    )
            except UnicodeDecodeError:
                errors.append({"skill": name, "issue": "openai_yaml_not_utf8"})
        if hash_file(skill_file) != entry.get("staged_skill_sha256"):
            errors.append({"skill": name, "issue": "SKILL_hash_drift"})
        if hash_tree(canonical) != entry.get("staged_tree_sha256"):
            errors.append({"skill": name, "issue": "tree_hash_drift"})

    duplicate_paths = [
        path for path, count in Counter(canonical_paths).items() if count > 1
    ]
    for path in duplicate_paths:
        errors.append({"skill": "*", "issue": f"duplicate_canonical_path:{path}"})

    registry_names = {str(entry["name"]) for entry in entries}
    top_level_names = {
        str(entry["name"]) for entry in entries if not entry.get("nested_under")
    }
    for profile_name in ("codex", "cc_switch", "all"):
        profile_path = repo / "profiles" / f"{profile_name}.json"
        if not profile_path.is_file():
            errors.append({"skill": "*", "issue": f"missing_profile:{profile_name}"})
            continue
        profile_skills = [str(item) for item in load_json(profile_path).get("skills", [])]
        if len(profile_skills) != len(set(profile_skills)):
            errors.append(
                {"skill": "*", "issue": f"duplicate_profile_entry:{profile_name}"}
            )
        unknown = sorted(set(profile_skills) - registry_names)
        for name in unknown:
            errors.append(
                {"skill": name, "issue": f"unknown_profile_entry:{profile_name}"}
            )
        nested = sorted(set(profile_skills) - top_level_names)
        for name in nested:
            if name in registry_names:
                errors.append(
                    {"skill": name, "issue": f"nested_profile_entry:{profile_name}"}
                )
        if profile_name == "all" and set(profile_skills) != top_level_names:
            errors.append({"skill": "*", "issue": "all_profile_top_level_mismatch"})

    csv_path = repo / "registry" / "skills.csv"
    if not csv_path.is_file():
        errors.append({"skill": "*", "issue": "missing_registry_csv"})
    else:
        with csv_path.open(encoding="utf-8-sig", newline="") as handle:
            csv_rows = {row["name"]: row for row in csv.DictReader(handle)}
        if set(csv_rows) != registry_names:
            errors.append({"skill": "*", "issue": "registry_csv_name_mismatch"})
        for entry in entries:
            row = csv_rows.get(str(entry["name"]))
            if not row:
                continue
            for field in ("staged_skill_sha256", "staged_tree_sha256"):
                if row.get(field) != entry.get(field):
                    errors.append(
                        {
                            "skill": str(entry["name"]),
                            "issue": f"registry_csv_{field}_mismatch",
                        }
                    )

    for root, dirs, files in os.walk(repo):
        root_path = Path(root)
        if ".git" in dirs:
            dirs.remove(".git")
        for name in dirs:
            relative_dir = (root_path / name).relative_to(repo)
            if (
                relative_dir.parts
                and relative_dir.parts[0] == "skills"
                and name in FORBIDDEN_DIRS
            ):
                errors.append(
                    {
                        "skill": "*",
                        "issue": f"forbidden_directory:{relative_dir}",
                    }
                )
        for name in files:
            path = root_path / name
            try:
                if path.stat().st_size >= 100 * 1024 * 1024:
                    errors.append(
                        {
                            "skill": "*",
                            "issue": f"github_100mb_limit:{path.relative_to(repo)}",
                        }
                    )
            except OSError:
                continue
            findings, has_local_path = inspect_text_file(path)
            for finding in findings:
                secret_findings.append(
                    {"file": path.relative_to(repo).as_posix(), "type": finding}
                )
            if has_local_path:
                local_path_files.append(path.relative_to(repo).as_posix())

    report = {
        "schema_version": 1,
        "logical_skills": len(entries),
        "errors": errors,
        "warnings": warnings,
        "secret_findings": secret_findings,
        "local_path_files": sorted(set(local_path_files)),
        "license_unverified": sorted(
            entry["name"]
            for entry in entries
            if entry.get("license_evidence") == "unverified"
        ),
        "status": "fail" if errors or secret_findings else "pass_with_warnings"
        if warnings
        else "pass",
    }
    if args.write_report:
        target = repo / args.write_report
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors or secret_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
