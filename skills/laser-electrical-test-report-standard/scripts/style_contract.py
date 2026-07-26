#!/usr/bin/env python3
"""Active style contract for ultra-stable-laser electrical-test reports."""

from __future__ import annotations


REFERENCE_DOCX = (
    r"C:\01_obsidian\ustc_hy\01_科研主系统\04_实验测试与证据"
    r"\03_超稳激光电控箱指标测试"
    r"\LASER 测试报告\202607\01_正式报告\00_参考"
    r"\电信件1 1397nm超稳激光PDH数字锁定环路分析20260710.docx"
)

BODY_STYLE = {
    "east_asia": "宋体",
    "latin": "Times New Roman",
    "size_pt": 12.0,
    "first_line_pt": 24.0,
    "line_spacing_pt": 20.0,
    "space_before_pt": 0.0,
    "space_after_pt": 0.0,
}

REPORT_TITLE_STYLE = {
    "east_asia": "微软雅黑",
    "latin": "Microsoft YaHei",
    "size_pt": 22.0,
    "bold": True,
    "color": "1F4E79",
}

REPORT_SUBTITLE_STYLE = {
    "east_asia": "微软雅黑",
    "latin": "Microsoft YaHei",
    "size_pt": 14.0,
    "bold": True,
    "color": "000000",
}

PAGE_STYLE = {
    "page_width_cm": 21.0,
    "page_height_cm": 29.7,
    "top_margin_cm": 2.5,
    "bottom_margin_cm": 2.5,
    "left_margin_cm": 3.0,
    "right_margin_cm": 2.5,
    "header_distance_cm": 1.25,
    "footer_distance_cm": 1.25,
}

TABLE_STYLE = {
    "name": "报告表格样式",
    "header_fill": "DDEBF7",
    "body_fill": "FFFFFF",
    "border_color": "808080",
    "border_size_eighth_pt": "4",
    "east_asia": "宋体",
    "latin": "Times New Roman",
    "font_size_pt": 9.5,
    "cell_margin_top_twips": "85",
    "cell_margin_bottom_twips": "85",
    "cell_margin_left_twips": "102",
    "cell_margin_right_twips": "102",
    "status_fills": {
        "满足": "E2F0D9",
        "不满足": "F4CCCC",
        "暂不能判定": "FFF2CC",
        "未测试": "E7E6E6",
    },
}

# All three project quick styles participate in one automatic multilevel list.
HEADING_STYLES = {
    1: {
        "name": "一级标题",
        "east_asia": "微软雅黑",
        "latin": "Microsoft YaHei",
        "size_pt": 15.0,
        "bold": True,
        "outline_level": 0,
        "first_line_pt": 0.0,
        "space_before_pt": 12.0,
        "space_after_pt": 6.0,
        "line_spacing": 1.15,
        "keep_with_next": True,
        "keep_together": True,
        "color": "1F4E79",
        "numbered": True,
    },
    2: {
        "name": "二级标题",
        "east_asia": "微软雅黑",
        "latin": "Microsoft YaHei",
        "size_pt": 12.0,
        "bold": True,
        "outline_level": 1,
        "first_line_pt": 0.0,
        "space_before_pt": 9.0,
        "space_after_pt": 3.0,
        "line_spacing": 1.15,
        "keep_with_next": True,
        "keep_together": True,
        "color": "000000",
        "numbered": True,
    },
    3: {
        "name": "三级标题",
        "east_asia": "微软雅黑",
        "latin": "Microsoft YaHei",
        "size_pt": 12.0,
        "bold": True,
        "outline_level": 2,
        "first_line_pt": 0.0,
        "space_before_pt": 6.0,
        "space_after_pt": 3.0,
        "line_spacing": 1.15,
        "keep_with_next": True,
        "keep_together": True,
        "color": "000000",
        "numbered": True,
    },
}

# level, display text, left indent, hanging indent, suffix
NUMBERING_LEVELS = (
    (0, "%1.", 510, 226, "nothing"),
    (1, "%1.%2", 510, 226, "nothing"),
    (2, "%1.%2.%3", 510, 226, "nothing"),
)
