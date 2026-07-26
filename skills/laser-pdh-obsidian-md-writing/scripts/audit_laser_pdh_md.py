#!/usr/bin/env python3
"""Audit Laser_PDH_Study Markdown for Obsidian rendering and governance issues."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

DEFAULT_ROOT = Path("C:/01_obsidian/ustc_hy/01_科研主系统")
DEFAULT_PROJECT = "Laser_PDH_Study"
MAX_MERMAID_LABEL_LEN = 12

LATEX_COMMAND_RE = re.compile(
    r"\\(frac|mathrm|operatorname|approx|gg|ll|delta|nu|lvert|rvert|Theta|Phi|omega|sqrt|angle|pm)"
)
WIKILINK_RE = re.compile(r"\[\[([^\]#|]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
FENCE_RE = re.compile(r"^\s*```(\S*)\s*$")
MERMAID_LINE_ESCAPE_RE = re.compile(r"/n|\\n|<br\s*/?>", re.IGNORECASE)
MERMAID_NODE_LABEL_RE = re.compile(
    r"""(?x)
    (?P<node>[A-Za-z_][\w]*)\s*
    (?:
      (?:\[\[|\[|\(\(|\(|\{\{|\{)\s*
      (?:
        (?P<quote>["\'])
        (?P<label_q>[^"'\n]+)
        (?P=quote)
      |
        (?P<label_u>[^]\}\)\n]+?)
      )
      \s*(?:\]\]|\]|\)\)|\)|\}\}|\})
    )
    """
)
MERMAID_LINK_RE = re.compile(r"<a[^>]*href=[\"']([^\"']+)[\"'][^>]*>", re.IGNORECASE)
MERMAID_SOURCE_BLOCK_RE = re.compile(r"<pre\b[^>]*id=[\"']diagram-source[\"'][^>]*>(.*?)</pre>", re.IGNORECASE | re.DOTALL)
MD_IMAGE_RE = re.compile(r"!\[[^\]\n]*\]\(([^)\n]+)\)")
OBSIDIAN_IMAGE_RE = re.compile(r"!\[\[([^\]\n]+)\]\]")
REMOTE_RESOURCE_RE = re.compile(r"^(?:https?://|data:|mailto:)", re.IGNORECASE)
SCHEMATIC_DIR_RE = re.compile(r"(?:^|[\\/])assets[\\/]原理图截图(?:[\\/]|$)")
SCHEMATIC_FULLPAGE_RE = re.compile(r"(整页|全页|fullpage|wholepage)", re.IGNORECASE)
SCHEMATIC_CONTEXT_RE = re.compile(
    r"(来源|来自|PDF|pdf|页|P\d+|功能|模块|测试|看什么|易错|needs_check|局部|对应)"
)
TABLE_SCREENSHOT_HEADER = ("截图", "来源", "页码/位置", "功能块", "测试关注点", "易错点")
TABLE_WIDE_COLS = 6
TABLE_WIDE_CELL_LEN = 60
TABLE_SEVERE_COLS = 9
TABLE_SEVERE_CELL_LEN = 75


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def iter_md_files(root: Path, project: str | None = None) -> list[Path]:
    files = sorted(p for p in root.rglob("*.md") if p.is_file())
    if not project:
        return files
    project_re = re.compile(rf"(?m)^project\s*:\s*[\"']?{re.escape(project)}[\"']?\s*$")
    return [p for p in files if project_re.search(read_text(p))]


def iter_mmd_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.mmd") if p.is_file())


def iter_html_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.html") if p.is_file())


def strip_inline_code(text: str) -> str:
    return re.sub(r"`[^`]*`", "", text)


def strip_inline_math(text: str) -> str:
    return re.sub(r"\$[^$\n]*\$", "", text)


def add_issue(issues: dict[str, list[str]], key: str, path: Path, line_no: int | None, line: str | None) -> None:
    if line_no is None:
        issues.setdefault(key, []).append(str(path))
    else:
        issues.setdefault(key, []).append(f"{path}:{line_no}: {line.strip() if line else ''}")


def is_mermaid_asset(path: Path) -> bool:
    return "_mermaid" in path.parts


def is_raw_source(path: Path) -> bool:
    return "03_原始摘录" in path.parts or "01_Raw" in path.parts


def is_backup_note(path: Path) -> bool:
    return path.name.endswith("_旧版.md")


def normalize_image_target(target: str) -> str:
    target = target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    if "|" in target and not target.startswith(("C:/", "C:\\")):
        target = target.split("|", 1)[0]
    return unquote(target.strip())


def is_local_image_target(target: str) -> bool:
    return bool(target) and not REMOTE_RESOURCE_RE.match(target)


def resolve_image_target(path: Path, target: str) -> Path:
    target_path = Path(target)
    if target_path.is_absolute():
        return target_path
    return (path.parent / target_path).resolve()


def is_schematic_image_target(target: str, resolved: Path) -> bool:
    target_norm = target.replace("\\", "/")
    resolved_norm = str(resolved).replace("\\", "/")
    return bool(SCHEMATIC_DIR_RE.search(target_norm) or SCHEMATIC_DIR_RE.search(resolved_norm))


def iter_image_targets(line: str) -> list[str]:
    targets = [normalize_image_target(match.group(1)) for match in MD_IMAGE_RE.finditer(line)]
    targets.extend(normalize_image_target(match.group(1)) for match in OBSIDIAN_IMAGE_RE.finditer(line))
    return targets


def nearby_context(lines: list[str], line_index: int, radius: int = 3) -> str:
    snippets: list[str] = []

    before = line_index - 1
    while before >= 0 and len(snippets) < radius:
        line = lines[before].strip()
        if line and not iter_image_targets(line):
            snippets.append(line)
        before -= 1

    after: list[str] = []
    cursor = line_index + 1
    while cursor < len(lines) and len(after) < radius:
        line = lines[cursor].strip()
        if line and not iter_image_targets(line):
            after.append(line)
        cursor += 1

    return "\n".join(list(reversed(snippets)) + after)


def split_table_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None

    if stripped.endswith("|"):
        stripped = stripped[1:-1]
    else:
        stripped = stripped[1:]

    cells: list[str] = []
    buffer: list[str] = []
    escaped = False
    for char in stripped:
        if char == "\\" and not escaped:
            escaped = True
            buffer.append(char)
            continue
        if char == "|" and not escaped:
            cells.append("".join(buffer).strip())
            buffer = []
        else:
            buffer.append(char)
        escaped = False
    cells.append("".join(buffer).strip())
    return cells


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def table_cell_text_len(cell: str) -> int:
    cell = re.sub(r"`([^`]*)`", r"\1", cell)
    return len(cell.strip())


def iter_markdown_tables(lines: list[str]) -> list[tuple[int, list[str], list[list[str]], int]]:
    tables: list[tuple[int, list[str], list[list[str]], int]] = []
    idx = 0
    while idx < len(lines) - 1:
        header = split_table_row(lines[idx])
        if header and is_table_separator(lines[idx + 1]):
            cursor = idx + 2
            rows: list[list[str]] = []
            while cursor < len(lines):
                row = split_table_row(lines[cursor])
                if not row or len(row) != len(header):
                    break
                rows.append(row)
                cursor += 1

            max_cell_len = 0
            for row in [header, *rows]:
                for cell in row:
                    max_cell_len = max(max_cell_len, table_cell_text_len(cell))
            tables.append((idx + 1, header, rows, max_cell_len))
            idx = cursor
            continue
        idx += 1
    return tables


def audit_tables(path: Path, issues: dict[str, list[str]]) -> None:
    if is_raw_source(path) or is_backup_note(path):
        return

    lines = read_text(path).splitlines()
    for line_no, header, rows, max_cell_len in iter_markdown_tables(lines):
        col_count = len(header)
        row_count = len(rows)
        header_text = "| " + " | ".join(header) + " |"
        summary = f"cols={col_count} rows={row_count} maxcell={max_cell_len}: {header_text}"

        if tuple(header) == TABLE_SCREENSHOT_HEADER:
            add_issue(issues, "TABLE_SCREENSHOT_METADATA", path, line_no, summary)

        if col_count >= TABLE_WIDE_COLS or max_cell_len >= TABLE_WIDE_CELL_LEN:
            add_issue(issues, "TABLE_WIDE", path, line_no, summary)

        if col_count >= TABLE_SEVERE_COLS or max_cell_len >= TABLE_SEVERE_CELL_LEN:
            add_issue(issues, "TABLE_SEVERE", path, line_no, summary)


def iter_mermaid_blocks(text: str) -> list[tuple[int, str]]:
    blocks: list[tuple[int, str]] = []
    in_fence = False
    start_line = 0
    buffer: list[str] = []

    for idx, line in enumerate(text.splitlines(), start=1):
        fence_match = FENCE_RE.match(line)
        if fence_match:
            lang = (fence_match.group(1) or "").lower()
            if not in_fence and lang == "mermaid":
                in_fence = True
                start_line = idx
                buffer = []
                continue
            if in_fence:
                blocks.append((start_line, "\n".join(buffer)))
                in_fence = False
                buffer = []
                continue
        if in_fence:
            buffer.append(line)
    return blocks


def check_mermaid_escape_and_labels(
    path: Path,
    block_text: str,
    start_line: int,
    issues: dict[str, list[str]],
) -> None:
    check_label_length = not is_raw_source(path)
    for i, line in enumerate(block_text.splitlines(), start=start_line + 1):
        if MERMAID_LINE_ESCAPE_RE.search(line):
            add_issue(issues, "MERMAID_LABEL_ESCAPES", path, i, line)

        for match in MERMAID_NODE_LABEL_RE.finditer(line):
            label = (match.group("label_q") or match.group("label_u") or "").strip()
            if check_label_length and label and len(label) > MAX_MERMAID_LABEL_LEN:
                add_issue(
                    issues,
                    "MERMAID_LABEL_LEN",
                    path,
                    i,
                    f"{match.group('node')} label_len={len(label)}: {label}",
                )


def audit_markdown_mermaid(path: Path, issues: dict[str, list[str]]) -> None:
    text = read_text(path)
    for start_line, block in iter_mermaid_blocks(text):
        check_mermaid_escape_and_labels(path, block, start_line, issues)


def audit_schematic_images(path: Path, issues: dict[str, list[str]]) -> None:
    if is_raw_source(path):
        return

    lines = read_text(path).splitlines()
    for idx, line in enumerate(lines):
        for target in iter_image_targets(line):
            if not is_local_image_target(target):
                continue

            resolved = resolve_image_target(path, target)
            if not is_schematic_image_target(target, resolved):
                continue

            line_no = idx + 1
            if not resolved.exists():
                add_issue(issues, "SCHEMATIC_IMAGE_EXISTS", path, line_no, f"missing image: {target}")

            path_text = str(resolved).replace("\\", "/")
            if "局部" not in path_text or SCHEMATIC_FULLPAGE_RE.search(path_text):
                add_issue(issues, "SCHEMATIC_IMAGE_SCOPE", path, line_no, f"image should be local crop: {target}")

            context = nearby_context(lines, idx)
            if not SCHEMATIC_CONTEXT_RE.search(context):
                add_issue(
                    issues,
                    "SCHEMATIC_IMAGE_CONTEXT",
                    path,
                    line_no,
                    f"missing nearby schematic context: {target}",
                )


def audit_file(path: Path, all_note_targets: set[str], issues: dict[str, list[str]]) -> None:
    text = read_text(path)
    lines = text.splitlines()

    if not re.search(r"(?m)^cssclasses:\s*\[laser-pdh-note\]", text):
        add_issue(issues, "CSS_MISSING", path, None, None)

    in_fence = False
    in_math = False
    for idx, line in enumerate(lines, start=1):
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if re.search(r"\\\(|\\\)|\\\[|\\\]", line):
            add_issue(issues, "RESIDUAL_DELIMS", path, idx, line)

        if re.search(r"\$\||\|\$|\$\\left\|", line):
            add_issue(issues, "PIPE_MATH_HITS", path, idx, line)

        if re.match(r"^\s+\$\$\s*$", line):
            add_issue(issues, "INDENTED_DOLLAR_BLOCK_DELIMS", path, idx, line)

        if re.match(r"^\s*\$\$\s*$", line):
            in_math = not in_math
            continue

        if not in_math:
            stripped = strip_inline_math(strip_inline_code(line))
            if LATEX_COMMAND_RE.search(stripped):
                add_issue(issues, "BARE_LATEX_OUTSIDE_MATH", path, idx, line)

    for match in WIKILINK_RE.finditer(text):
        target = match.group(1).strip().replace("\\", "/")
        if target.lower().endswith(".md"):
            target = target[:-3]
        if target and target not in all_note_targets:
            issues.setdefault("BROKEN_WIKILINKS", []).append(f"{path}: [[{target}]]")


def audit_mmd_file(path: Path, issues: dict[str, list[str]]) -> None:
    text = read_text(path)
    for i, line in enumerate(text.splitlines(), start=1):
        if MERMAID_LINE_ESCAPE_RE.search(line):
            add_issue(issues, "MERMAID_LABEL_ESCAPES", path, i, line)
        for match in MERMAID_NODE_LABEL_RE.finditer(line):
            label = (match.group("label_q") or match.group("label_u") or "").strip()
            if label and len(label) > MAX_MERMAID_LABEL_LEN:
                add_issue(
                    issues,
                    "MERMAID_LABEL_LEN",
                    path,
                    i,
                    f"{match.group('node')} label_len={len(label)}: {label}",
                )


def audit_mermaid_pairing(html_files: list[Path], mmd_files: list[Path], issues: dict[str, list[str]]) -> None:
    mmd_stems = {str(p.with_suffix("").relative_to(p.parents[0])): p for p in mmd_files}
    html_stems = {str(p.with_suffix("").relative_to(p.parents[0])): p for p in html_files}

    for stem, path in mmd_stems.items():
        expected_html = path.with_suffix(".html")
        if stem not in html_stems:
            add_issue(issues, "MERMAID_PAIR_CHECK", expected_html, None, None)

    for stem, path in html_stems.items():
        expected_mmd = path.with_suffix(".mmd")
        if stem not in mmd_stems:
            add_issue(issues, "MERMAID_PAIR_CHECK", path, None, None)


def audit_mermaid_html_viewer(path: Path, issues: dict[str, list[str]]) -> None:
    text = read_text(path)
    source_blocks = MERMAID_SOURCE_BLOCK_RE.findall(text)
    if len(source_blocks) != 1:
        add_issue(
            issues,
            "MERMAID_SINGLE_VIEWER",
            path,
            None,
            f"diagram-source blocks = {len(source_blocks)}",
        )

    href_matches = MERMAID_LINK_RE.findall(text)
    if not href_matches:
        add_issue(issues, "MERMAID_SINGLE_VIEWER", path, None, "missing .mmd href link")
    else:
        matched = False
        target_name = f"{path.stem}.mmd"
        for href in href_matches:
            if href.endswith(target_name) or Path(href).name == target_name:
                matched = True
                break
        if not matched:
            add_issue(
                issues,
                "MERMAID_SINGLE_VIEWER",
                path,
                None,
                f"href links do not point to {target_name}: {href_matches[0]}",
            )

    if "mermaid_viewer.js" not in text or "mermaid_viewer.css" not in text:
        add_issue(
            issues,
            "MERMAID_SINGLE_VIEWER",
            path,
            None,
            "viewer assets mermaid_viewer.js/css not both referenced",
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--max-lines", type=int, default=80)
    args = parser.parse_args()

    root = args.root
    if not root.exists():
        print(f"ERROR: root does not exist: {root}", file=sys.stderr)
        return 2

    md_files = iter_md_files(root, args.project or None)
    all_md_files = iter_md_files(root)
    all_note_targets = {p.stem for p in all_md_files}
    for path in all_md_files:
        all_note_targets.add(path.with_suffix("").relative_to(root).as_posix())
        if root.name == "01_科研主系统":
            all_note_targets.add(f"01_科研主系统/{path.with_suffix('').relative_to(root).as_posix()}")
    mmd_files = [
        p for p in iter_mmd_files(root)
        if is_mermaid_asset(p) and "90_历史项目" not in p.parts and "_archive" not in p.parts
    ]
    html_files = [
        p for p in iter_html_files(root)
        if is_mermaid_asset(p) and "90_历史项目" not in p.parts and "_archive" not in p.parts
    ]

    issues: dict[str, list[str]] = {
        "CSS_MISSING": [],
        "RESIDUAL_DELIMS": [],
        "PIPE_MATH_HITS": [],
        "INDENTED_DOLLAR_BLOCK_DELIMS": [],
        "BARE_LATEX_OUTSIDE_MATH": [],
        "BROKEN_WIKILINKS": [],
        "MERMAID_LABEL_ESCAPES": [],
        "MERMAID_LABEL_LEN": [],
        "MERMAID_PAIR_CHECK": [],
        "MERMAID_SINGLE_VIEWER": [],
        "SCHEMATIC_IMAGE_EXISTS": [],
        "SCHEMATIC_IMAGE_SCOPE": [],
        "SCHEMATIC_IMAGE_CONTEXT": [],
        "TABLE_WIDE": [],
        "TABLE_SEVERE": [],
        "TABLE_SCREENSHOT_METADATA": [],
    }
    report_only_keys = {"TABLE_WIDE", "TABLE_SEVERE", "TABLE_SCREENSHOT_METADATA"}

    for path in md_files:
        audit_file(path, all_note_targets, issues)
        audit_markdown_mermaid(path, issues)
        audit_schematic_images(path, issues)
        audit_tables(path, issues)

    for path in mmd_files:
        audit_mmd_file(path, issues)

    audit_mermaid_pairing(html_files, mmd_files, issues)

    for path in html_files:
        # 仅审计 mermaid viewer 的 html，避免把大量普通页面误报
        if "_mermaid" in str(path):
            audit_mermaid_html_viewer(path, issues)

    failed = False
    for key, values in issues.items():
        print(f"{key} = {len(values)}")
        if values and key not in report_only_keys:
            failed = True
        if values:
            for item in values[: args.max_lines]:
                print(f"  {item}")
            if len(values) > args.max_lines:
                print(f"  ... {len(values) - args.max_lines} more")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
