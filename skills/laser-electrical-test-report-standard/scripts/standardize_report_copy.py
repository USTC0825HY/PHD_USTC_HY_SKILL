#!/usr/bin/env python3
"""Create a standardized copy of a legacy laser electrical-test DOCX report."""

from __future__ import annotations

import argparse
import re
import shutil
import stat
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph

from create_standard_template import (
    BODY_FONT_EAST_ASIA,
    TOC_TITLE_FONT_EAST_ASIA,
    TOC_TITLE_FONT_LATIN,
    add_field,
    add_math,
    add_table,
    apply_reference_heading_style,
    clear_direct_run_font,
    configure_document,
    document_body_width_twips,
    ensure_front_matter_page_break,
    ensure_page_break_before,
    format_table,
    set_run_font,
    set_zero_indent,
)
from style_contract import HEADING_STYLES


METADATA_PATTERN = re.compile(r"^测试(时间|人员|地点|目的|内容)\s*[：:]")
MANUAL_HEADING_PATTERN = re.compile(r"^(\d+(?:\.\d+){0,2})[.、]?\s*|^([一二三四五六七八九十]+、)\s*")
CAPTION_PATTERN = re.compile(r"^(图|表)\s*\d+(?:[-.]\d+)?\s*(.*)$")
FORMULA_PATTERN = re.compile(r"(A_v\(f\)\s*=\s*sqrt\(S_v\(f\)\)|V_rms\s*=\s*sqrt\(.+\))")
FORMULA_LATEX = {
    "A_v(f)=sqrt(S_v(f))": r"A_v(f)=\sqrt{S_v(f)}",
    "V_rms=sqrt(integralS_v(f)df)": r"V_{\mathrm{rms}}=\sqrt{\int S_v(f)\,\mathrm{d}f}",
}
MEASUREMENT_PREFIX_PATTERN = re.compile(r"^(?:s|ms|us|ns|Hz|kHz|MHz|GHz|V|mV|uV|dB|dBm|dBc)\b", re.IGNORECASE)


def clean(text: str) -> str:
    return " ".join(text.split())


def manual_heading_match(text: str):
    match = MANUAL_HEADING_PATTERN.match(text)
    if match and MEASUREMENT_PREFIX_PATTERN.match(text[match.end() :].lstrip()):
        return None
    return match


def legacy_heading_level(paragraph, promote_numbered_normal: bool) -> int | None:
    style_id = (paragraph.style.style_id or "").lower().replace(" ", "")
    name = paragraph.style.name
    normalized_name = name.lower().replace(" ", "")
    if style_id in {"heading1", "1"} or normalized_name in {"heading1", "标题1"} or "一级标题" in name:
        return 1
    if style_id in {"heading2", "2"} or normalized_name in {"heading2", "标题2"} or "二级标题" in name:
        return 2
    if style_id in {"heading3", "3"} or normalized_name in {"heading3", "标题3"} or "三级标题" in name:
        return 3
    if not promote_numbered_normal:
        return None
    match = manual_heading_match(clean(paragraph.text))
    if match:
        token = match.group(1) or match.group(2)
        if token[0].isdigit():
            return min(token.count(".") + 1, 3)
        return 1
    return None


def clear_content(paragraph) -> None:
    paragraph._p.clear_content()


def insert_paragraph_after(paragraph, text: str = "", style: str | None = None) -> Paragraph:
    element = OxmlElement("w:p")
    paragraph._p.addnext(element)
    inserted = Paragraph(element, paragraph._parent)
    if style:
        inserted.style = style
    if text:
        inserted.add_run(text)
    return inserted


def contains_image(paragraph) -> bool:
    return "<w:drawing" in paragraph._p.xml or "<w:pict" in paragraph._p.xml


def normalize_runs(paragraph, east_asia: str, size_pt: float, bold: bool | None = None, latin: str = "Times New Roman") -> None:
    for run in paragraph.runs:
        set_run_font(run, east_asia, size_pt, bold=bold, latin=latin)


def apply_image_style(paragraph) -> None:
    paragraph.style = "图片"
    set_zero_indent(paragraph)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = 0
    paragraph.paragraph_format.space_after = 0
    paragraph.paragraph_format.keep_with_next = True


def convert_caption(paragraph, label: str, description: str) -> None:
    paragraph.style = "图表题注"
    clear_content(paragraph)
    paragraph.add_run(f"{label} ")
    add_field(paragraph, f" SEQ {label} \\* ARABIC ", "1")
    clean_description = (description or "待填写").rstrip().rstrip("。.")
    paragraph.add_run(f" {clean_description}")
    set_zero_indent(paragraph)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.keep_with_next = label == "表"
    normalize_runs(paragraph, BODY_FONT_EAST_ASIA, 10.5)


def convert_formula(paragraph) -> None:
    text = clean(paragraph.text)
    match = FORMULA_PATTERN.search(text)
    if not match:
        return
    prefix = text[: match.start()].rstrip("：: ")
    formula = re.sub(r"\s+", "", match.group(1))
    if prefix:
        paragraph.insert_paragraph_before(f"{prefix}：", style="Normal")
    paragraph.style = "公式"
    clear_content(paragraph)
    latex = FORMULA_LATEX.get(formula)
    if latex is None:
        raise ValueError(f"No reviewed LaTeX mapping for legacy formula: {formula}")
    add_math(paragraph, latex)


def standardize(
    source: Path,
    output: Path,
    convert_captions: bool,
    promote_numbered_normal: bool,
    repair_level_jumps: bool,
    append_required_sections: bool,
    convert_formulas: bool,
    insert_toc: bool,
) -> None:
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite existing output: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, output)
    output.chmod(output.stat().st_mode | stat.S_IWRITE)
    doc = Document(output)
    configure_document(doc)

    nonempty = [paragraph for paragraph in doc.paragraphs if clean(paragraph.text)]
    title_paragraph = nonempty[0] if nonempty else None
    if title_paragraph is not None:
        title_paragraph.style = "报告题名"
        clear_direct_run_font(title_paragraph, remove_bold=True)

    previous_heading_level = 0
    for paragraph in doc.paragraphs:
        text = clean(paragraph.text)
        if contains_image(paragraph):
            apply_image_style(paragraph)
            if not text:
                continue
        if not text:
            continue
        if paragraph is title_paragraph:
            continue
        if text == "目录":
            paragraph.style = "目录标题"
            set_zero_indent(paragraph)
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            normalize_runs(paragraph, TOC_TITLE_FONT_EAST_ASIA, 16, True, TOC_TITLE_FONT_LATIN)
            continue
        if METADATA_PATTERN.match(text):
            paragraph.style = "报告信息"
            set_zero_indent(paragraph)
            normalize_runs(paragraph, BODY_FONT_EAST_ASIA, 12, False)
            continue
        level = legacy_heading_level(paragraph, promote_numbered_normal)
        if level is not None:
            if repair_level_jumps and previous_heading_level and level > previous_heading_level + 1:
                level = previous_heading_level + 1
            match = manual_heading_match(text)
            normalized = text[match.end() :] if match else text
            paragraph.text = normalized
            apply_reference_heading_style(paragraph, level)
            previous_heading_level = level
            continue
        if convert_captions:
            match = CAPTION_PATTERN.match(text)
            if match:
                convert_caption(paragraph, match.group(1), match.group(2))
                continue
        if convert_formulas:
            convert_formula(paragraph)

    max_table_width = document_body_width_twips(doc)
    for table in doc.tables:
        format_table(table, {len(table.columns) - 1}, max_table_width)
    if insert_toc and not any(" TOC " in paragraph._p.xml for paragraph in doc.paragraphs):
        anchor = title_paragraph
        for paragraph in doc.paragraphs[1:]:
            if paragraph.style.name == "报告信息":
                anchor = paragraph
            elif clean(paragraph.text):
                break
        toc_title = insert_paragraph_after(anchor, "目录", "目录标题")
        ensure_page_break_before(toc_title)
        set_zero_indent(toc_title)
        toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        normalize_runs(toc_title, TOC_TITLE_FONT_EAST_ASIA, 16, True, TOC_TITLE_FONT_LATIN)
        toc = insert_paragraph_after(toc_title)
        add_field(toc, ' TOC \\o "1-3" \\h \\z \\u ', "右键更新域或按 F9 更新目录。")
        page_break = insert_paragraph_after(toc)
        page_break.add_run().add_break(WD_BREAK.PAGE)
    if append_required_sections:
        full_text = "\n".join(clean(paragraph.text) for paragraph in doc.paragraphs)
        if not any(token in full_text for token in ("总结与后续测试", "后续测试", "下一步计划")):
            paragraph = doc.add_paragraph("总结与后续测试", style=HEADING_STYLES[1]["name"])
            apply_reference_heading_style(paragraph, 1)
            paragraph = doc.add_paragraph("后续测试", style=HEADING_STYLES[2]["name"])
            apply_reference_heading_style(paragraph, 2)
            add_table(
                doc,
                ["项目", "当前缺口", "后续测试", "必须保存的数据", "优先级"],
                [["待填写", "待填写", "待填写", "待填写", "待填写"]],
                {0, 1, 2, 3},
            )
        if not any(token in full_text for token in ("数据来源", "数据与脚本索引", "原始记录与数据索引")):
            if "附录" not in full_text:
                paragraph = doc.add_paragraph("附录", style=HEADING_STYLES[1]["name"])
                apply_reference_heading_style(paragraph, 1)
            paragraph = doc.add_paragraph("仪器设置、原始记录与数据索引", style=HEADING_STYLES[2]["name"])
            apply_reference_heading_style(paragraph, 2)
            add_table(
                doc,
                ["数据编号", "内容", "测试日期", "原始文件", "处理脚本", "版本"],
                [["待填写", "待填写", "待填写", "待填写", "待填写", "待填写"]],
                {1, 3, 4, 5},
            )
    ensure_front_matter_page_break(doc)
    doc.save(output)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--convert-captions", action="store_true")
    parser.add_argument("--insert-toc", action="store_true", help="Insert an automatic outline-level 1-3 directory after the report-information block.")
    parser.add_argument(
        "--promote-numbered-normal",
        action="store_true",
        help="Treat short manually numbered Normal paragraphs as headings after manual review.",
    )
    parser.add_argument(
        "--convert-formulas",
        action="store_true",
        help="Move recognized plain-text noise formulas into Office Math paragraphs.",
    )
    parser.add_argument(
        "--append-required-sections",
        action="store_true",
        help="Append missing follow-up-test or data-index sections with 待填写 rows.",
    )
    parser.add_argument(
        "--repair-level-jumps",
        action="store_true",
        help="Downgrade a legacy heading that skips more than one outline level.",
    )
    args = parser.parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    if not source.is_file():
        parser.error(f"Source DOCX not found: {source}")
    standardize(
        source,
        output,
        args.convert_captions,
        args.promote_numbered_normal,
        args.repair_level_jumps,
        args.append_required_sections,
        args.convert_formulas,
        args.insert_toc,
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
