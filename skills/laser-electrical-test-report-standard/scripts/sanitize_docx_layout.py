#!/usr/bin/env python3
"""Reapply table, image, and caption layout after Microsoft Word field updates."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

from create_standard_template import document_body_width_twips, format_table, set_zero_indent


def contains_image(paragraph) -> bool:
    return "<w:drawing" in paragraph._p.xml or "<w:pict" in paragraph._p.xml


def sanitize(path: Path) -> None:
    doc = Document(path)
    max_table_width = document_body_width_twips(doc)
    for table in doc.tables:
        format_table(table, max_width_twips=max_table_width)
    for paragraph in doc.paragraphs:
        if contains_image(paragraph):
            paragraph.style = "图片"
            set_zero_indent(paragraph)
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.keep_with_next = True
        elif paragraph.style.name == "图表题注":
            set_zero_indent(paragraph)
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.save(path)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path)
    args = parser.parse_args()
    path = args.docx.resolve()
    if not path.is_file():
        parser.error(f"DOCX not found: {path}")
    sanitize(path)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
