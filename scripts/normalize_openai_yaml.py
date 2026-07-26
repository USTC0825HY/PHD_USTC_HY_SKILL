#!/usr/bin/env python3
"""Ensure every Skill default prompt explicitly references its Skill name."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def load_registry(repo: Path) -> list[dict[str, object]]:
    payload = json.loads((repo / "registry" / "skills.json").read_text(encoding="utf-8"))
    return payload["skills"]


def normalized_prompt(name: str, current: str) -> str:
    marker = f"${name}"
    if marker in current:
        return current
    if current:
        return f"Use {marker} to {current[0].lower()}{current[1:]}"
    readable = name.replace("-", " ")
    return f"Use {marker} to handle this {readable} task."


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()
    changed = 0

    for entry in load_registry(repo):
        name = str(entry["name"])
        skill_dir = repo / str(entry["canonical_path"])
        yaml_path = skill_dir / "agents" / "openai.yaml"
        text = yaml_path.read_text(encoding="utf-8")
        match = re.search(r'(?m)^  default_prompt:\s*(["\'])(.*?)\1\s*$', text)
        current = match.group(2) if match else ""
        prompt = normalized_prompt(name, current)

        if match:
            replacement = f"  default_prompt: {json.dumps(prompt, ensure_ascii=False)}"
            updated = text[: match.start()] + replacement + text[match.end() :]
        else:
            if not text.endswith("\n"):
                text += "\n"
            updated = text + f"  default_prompt: {json.dumps(prompt, ensure_ascii=False)}\n"

        if updated != text:
            yaml_path.write_text(updated, encoding="utf-8", newline="\n")
            changed += 1

    print(json.dumps({"normalized_openai_yaml": changed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
