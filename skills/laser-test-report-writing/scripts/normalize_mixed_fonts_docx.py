#!/usr/bin/env python3
"""Apply Chinese/Latin run fonts without changing DOCX text, fields, or math."""

from __future__ import annotations

import argparse
import os
import re
import tempfile
import zipfile
from pathlib import Path

from lxml import etree


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
NS = {"w": W, "m": M}
REPORT_HEADING_NAMES = {"报告题名", "报告短题名", "目录标题", "一级标题", "二级标题", "三级标题", "标题 1", "标题 2", "标题 3", "Heading 1", "Heading 2", "Heading 3"}
MANUAL_HEADING_NAMES = {"标题 1", "标题 2", "标题 3", "Heading 1", "Heading 2", "Heading 3"}


def qn(namespace: str, local: str) -> str:
    return f"{{{namespace}}}{local}"


def parse_selection(value: str | None) -> set[int]:
    selected: set[int] = set()
    if not value:
        return selected
    for token in value.split(","):
        token = token.strip()
        if not token:
            continue
        if "-" in token:
            start, end = (int(part) for part in token.split("-", 1))
            selected.update(range(start, end + 1))
        else:
            selected.add(int(token))
    return selected


def style_names(styles_xml: bytes) -> dict[str, str]:
    root = etree.fromstring(styles_xml)
    result: dict[str, str] = {}
    for style in root.xpath(".//w:style", namespaces=NS):
        style_id = style.get(qn(W, "styleId"), "")
        name = style.find(qn(W, "name"))
        result[style_id] = name.get(qn(W, "val"), "") if name is not None else ""
    return result


def paragraph_style_name(paragraph: etree._Element, names: dict[str, str]) -> str:
    style = paragraph.find("./w:pPr/w:pStyle", namespaces=NS)
    return names.get(style.get(qn(W, "val"), ""), "") if style is not None else ""


def set_run_fonts(run: etree._Element, east_asia: str) -> None:
    if run.xpath("ancestor::m:oMath | ancestor::m:oMathPara", namespaces=NS):
        return
    rpr = run.find(qn(W, "rPr"))
    if rpr is None:
        rpr = etree.Element(qn(W, "rPr"))
        run.insert(0, rpr)
    fonts = rpr.find(qn(W, "rFonts"))
    if fonts is None:
        fonts = etree.Element(qn(W, "rFonts"))
        rpr.insert(0, fonts)
    fonts.set(qn(W, "ascii"), "Times New Roman")
    fonts.set(qn(W, "hAnsi"), "Times New Roman")
    fonts.set(qn(W, "cs"), "Times New Roman")
    fonts.set(qn(W, "eastAsia"), east_asia)


def normalize_xml(xml: bytes, names: dict[str, str], profile: str, mode: str, paragraph_ids: set[int], table_ids: set[int]) -> tuple[bytes, int]:
    root = etree.fromstring(xml)
    all_paragraphs = root.xpath(".//w:p", namespaces=NS)
    selected_paragraphs: set[int] = set(paragraph_ids)
    for table_index, table in enumerate(root.xpath(".//w:tbl", namespaces=NS), 1):
        if table_index in table_ids:
            for paragraph in table.xpath(".//w:p", namespaces=NS):
                try:
                    selected_paragraphs.add(all_paragraphs.index(paragraph) + 1)
                except ValueError:
                    pass

    changed = 0
    for index, paragraph in enumerate(all_paragraphs, 1):
        if mode == "surgical" and index not in selected_paragraphs:
            continue
        style_name = paragraph_style_name(paragraph, names)
        if profile == "manual":
            east_asia = "微软雅黑"
        else:
            east_asia = "微软雅黑" if style_name in REPORT_HEADING_NAMES else "宋体"
        for run in paragraph.xpath(".//w:r", namespaces=NS):
            if not run.xpath(".//w:t | .//w:instrText", namespaces=NS):
                continue
            set_run_fonts(run, east_asia)
            changed += 1
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes"), changed


def normalize(source: Path, output: Path, profile: str, mode: str, paragraphs: set[int], tables: set[int]) -> int:
    if source.resolve() == output.resolve():
        raise ValueError("output must differ from source")
    if mode == "surgical" and not paragraphs and not tables:
        raise ValueError("surgical mode requires --paragraphs and/or --tables")
    with zipfile.ZipFile(source, "r") as archive:
        entries = [(item, archive.read(item.filename)) for item in archive.infolist()]
    entry_map = {item.filename: data for item, data in entries}
    names = style_names(entry_map["word/styles.xml"])
    changed = 0
    updated: dict[str, bytes] = {}
    for item, data in entries:
        if not item.filename.startswith("word/") or not item.filename.endswith(".xml"):
            continue
        if item.filename == "word/styles.xml":
            continue
        try:
            new_data, count = normalize_xml(data, names, profile, mode, paragraphs, tables)
        except etree.XMLSyntaxError:
            continue
        if count:
            updated[item.filename] = new_data
            changed += count
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(suffix=".docx", dir=str(output.parent))
    os.close(fd)
    try:
        with zipfile.ZipFile(temporary, "w") as destination:
            for item, data in entries:
                destination.writestr(item, updated.get(item.filename, data))
        os.replace(temporary, output)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--profile", choices=["report", "manual"], required=True)
    parser.add_argument("--mode", choices=["surgical", "full"], default="surgical")
    parser.add_argument("--paragraphs", help="1-based paragraph indexes/ranges, e.g. 3,7-10")
    parser.add_argument("--tables", help="1-based table indexes/ranges, e.g. 1,4-6")
    args = parser.parse_args()
    changed = normalize(
        args.source.resolve(),
        args.output.resolve(),
        args.profile,
        args.mode,
        parse_selection(args.paragraphs),
        parse_selection(args.tables),
    )
    print(f"updated_runs={changed}")
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
