#!/usr/bin/env python3
"""Mechanically fix common Laser_PDH_Study Obsidian LaTeX rendering issues."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

DEFAULT_ROOT = Path("C:/01_obsidian/ustc_hy/01_科研主系统")
DEFAULT_PROJECT = "Laser_PDH_Study"

COMMON_ABS_REPLACEMENTS = {
    "|l_g(f)|": r"\lvert l_g(f)\rvert",
    "|l_g|": r"\lvert l_g\rvert",
    "|D(f)|": r"\lvert D(f)\rvert",
    "|H(f)|": r"\lvert H(f)\rvert",
    "|c_{gD}(f_m)|": r"\lvert c_{gD}(f_m)\rvert",
    r"|\nu_\mathrm{cl}(f)|": r"\lvert \nu_\mathrm{cl}(f)\rvert",
    r"|\nu_\mathrm{free}(f)|": r"\lvert \nu_\mathrm{free}(f)\rvert",
    r"|\nu_1-\nu_2|": r"\lvert \nu_1-\nu_2\rvert",
    r"|\Delta\nu(t)|": r"\lvert \Delta\nu(t)\rvert",
    r"|\Delta\nu|": r"\lvert \Delta\nu\rvert",
}


def iter_md_files(root: Path, project: str | None = None) -> list[Path]:
    files = sorted(p for p in root.rglob("*.md") if p.is_file())
    if not project:
        return files
    project_re = re.compile(rf"(?m)^project\s*:\s*[\"']?{re.escape(project)}[\"']?\s*$")
    return [p for p in files if project_re.search(p.read_text(encoding="utf-8-sig"))]


def fix_text(text: str) -> str:
    out_lines: list[str] = []
    in_fence = False

    for line in text.splitlines():
        new = line
        if re.match(r"^\s*```", new):
            out_lines.append(new)
            in_fence = not in_fence
            continue

        if not in_fence:
            new = re.sub(r"^\s*\\\[\s*$", "$$", new)
            new = re.sub(r"^\s*\\\]\s*$", "$$", new)
            new = re.sub(r"^\s+\$\$\s*$", "$$", new)
            new = re.sub(r"\\\[(.+?)\\\]", lambda m: "$$" + m.group(1) + "$$", new)
            new = re.sub(r"\\\((.+?)\\\)", lambda m: "$" + m.group(1) + "$", new)

            for old, replacement in COMMON_ABS_REPLACEMENTS.items():
                new = new.replace(old, replacement)
            new = new.replace(r"\left|", r"\left\lvert")
            new = new.replace(r"\right|", r"\right\rvert")

        out_lines.append(new)

    return "\n".join(out_lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--write", action="store_true", help="write changes; default is dry-run")
    args = parser.parse_args()

    changed: list[Path] = []
    for path in iter_md_files(args.root, args.project or None):
        old = path.read_text(encoding="utf-8-sig")
        new = fix_text(old)
        if new != old:
            changed.append(path)
            if args.write:
                path.write_text(new, encoding="utf-8")

    mode = "WRITE" if args.write else "DRY_RUN"
    print(f"{mode}_CHANGED = {len(changed)}")
    for path in changed:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
