#!/usr/bin/env python3
"""Normalize full-width parentheses around technical/Latin text in a DOCX.

Only the two parenthesis characters are changed. Text runs, Word fields,
equations, drawings, tables, styles, and section structure are preserved.
"""

from __future__ import annotations

import argparse
import re
import tempfile
import zipfile
from pathlib import Path

from lxml import etree


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
NS = {"w": W_NS, "m": M_NS}
TEXT_TAGS = {f"{{{W_NS}}}t", f"{{{M_NS}}}t"}
FULLWIDTH_PAREN_RE = re.compile(r"（([^（）]{1,200})）")
LATIN_OR_GREEK_RE = re.compile(r"[A-Za-z_]|[\u0370-\u03ff]|[µΩ℃]")
CJK_RE = re.compile(r"[\u3400-\u9fff]")
FORMULA_RE = re.compile(r"[0-9]\s*[+\-−×÷/*=<>≤≥^~～√]|[+\-−×÷/*=<>≤≥^~～√]\s*[0-9]")
CONTENT_PART_RE = re.compile(
    r"^word/(?:document|header\d+|footer\d+|footnotes|endnotes|comments)\.xml$"
)


def is_technical_parenthetical(inner: str) -> bool:
    if LATIN_OR_GREEK_RE.search(inner):
        return True
    return not CJK_RE.search(inner) and bool(FORMULA_RE.search(inner))


def text_nodes(paragraph: etree._Element) -> list[etree._Element]:
    return [node for node in paragraph.iter() if node.tag in TEXT_TAGS and node.text]


def locate(nodes: list[etree._Element], absolute_offset: int) -> tuple[etree._Element, int]:
    cursor = 0
    for node in nodes:
        length = len(node.text or "")
        if cursor <= absolute_offset < cursor + length:
            return node, absolute_offset - cursor
        cursor += length
    raise IndexError(f"Text offset {absolute_offset} is outside the paragraph")


def normalize_xml(data: bytes) -> tuple[bytes, list[str]]:
    parser = etree.XMLParser(resolve_entities=False, remove_blank_text=False)
    root = etree.fromstring(data, parser)
    changes: list[str] = []

    for paragraph in root.xpath(".//w:p", namespaces=NS):
        nodes = text_nodes(paragraph)
        if not nodes:
            continue
        combined = "".join(node.text or "" for node in nodes)
        matches = [m for m in FULLWIDTH_PAREN_RE.finditer(combined) if is_technical_parenthetical(m.group(1))]
        if not matches:
            continue

        replacements: dict[etree._Element, dict[int, str]] = {}
        for match in matches:
            open_node, open_offset = locate(nodes, match.start())
            close_node, close_offset = locate(nodes, match.end() - 1)
            replacements.setdefault(open_node, {})[open_offset] = "("
            replacements.setdefault(close_node, {})[close_offset] = ")"
            changes.append(match.group(0))

        for node, node_replacements in replacements.items():
            chars = list(node.text or "")
            for offset, value in node_replacements.items():
                chars[offset] = value
            node.text = "".join(chars)

    if not changes:
        return data, changes
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True), changes


def normalize_docx(source: Path, output: Path) -> list[tuple[str, str]]:
    if source.resolve() == output.resolve():
        raise ValueError("Source and output must differ; create a backup before replacing a report")
    output.parent.mkdir(parents=True, exist_ok=True)

    all_changes: list[tuple[str, str]] = []
    with tempfile.NamedTemporaryFile(prefix="paren_", suffix=".docx", delete=False, dir=output.parent) as handle:
        temp_path = Path(handle.name)
    try:
        with zipfile.ZipFile(source, "r") as src, zipfile.ZipFile(temp_path, "w") as dst:
            for item in src.infolist():
                data = src.read(item.filename)
                if CONTENT_PART_RE.match(item.filename):
                    data, changes = normalize_xml(data)
                    all_changes.extend((item.filename, change) for change in changes)
                dst.writestr(item, data)
        temp_path.replace(output)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise
    return all_changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Source DOCX")
    parser.add_argument("output", type=Path, help="Output DOCX; must differ from source")
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"DOCX not found: {source}")

    changes = normalize_docx(source, output)
    print(f"source: {source}")
    print(f"output: {output}")
    print(f"parentheses_normalized: {len(changes)}")
    for part, text in changes[:50]:
        print(f"  - {part}: {text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
