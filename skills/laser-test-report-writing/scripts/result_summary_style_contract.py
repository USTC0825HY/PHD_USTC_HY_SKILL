#!/usr/bin/env python3
"""Single source of truth for the Laser test-result summary DOCX format."""

from __future__ import annotations


PAGE_STYLE = {
    "page_width_cm": 21.59,
    "page_height_cm": 27.94,
    "top_margin_cm": 1.4,
    "bottom_margin_cm": 1.4,
    "left_margin_cm": 1.4,
    "right_margin_cm": 1.4,
    "header_distance_cm": 0.76,
    "footer_distance_cm": 0.76,
}

BODY_STYLE = {
    "name": "Normal",
    "east_asia": "宋体",
    "latin": "Times New Roman",
    "size_pt": 12.0,
    "color": "000000",
    "first_line_chars": 200,
}

TITLE_STYLE = {
    "name": "报告题名",
    "east_asia": "宋体",
    "latin": "Times New Roman",
    "size_pt": 16.0,
    "bold": True,
    "color": "000000",
    "alignment": "center",
}

HEADING_STYLES = {
    1: {
        "name": "一级标题",
        "east_asia": "微软雅黑",
        "latin": "Times New Roman",
        "size_pt": 15.0,
        "bold": True,
        "color": "000000",
        "outline_level": 0,
        "space_before_pt": 12.0,
        "space_after_pt": 6.0,
    },
    2: {
        "name": "二级标题",
        "east_asia": "微软雅黑",
        "latin": "Times New Roman",
        "size_pt": 12.0,
        "bold": True,
        "color": "000000",
        "outline_level": 1,
        "space_before_pt": 9.0,
        "space_after_pt": 3.0,
    },
    3: {
        "name": "三级标题",
        "east_asia": "微软雅黑",
        "latin": "Times New Roman",
        "size_pt": 12.0,
        "bold": True,
        "color": "000000",
        "outline_level": 2,
        "space_before_pt": 6.0,
        "space_after_pt": 3.0,
    },
}

NUMBERING_LEVELS = (
    (0, "%1.", 510, 226),
    (1, "%1.%2", 510, 226),
    (2, "%1.%2.%3", 510, 226),
)

SPECIAL_STYLES = {
    "图片": {
        "east_asia": "宋体",
        "latin": "Times New Roman",
        "size_pt": 12.0,
        "bold": False,
        "color": "000000",
        "alignment": "center",
        "keep_with_next": True,
    },
    "图表题注": {
        "east_asia": "宋体",
        "latin": "Times New Roman",
        "size_pt": 10.5,
        "bold": False,
        "color": "000000",
        "alignment": "center",
    },
    "表格表头": {
        "east_asia": "宋体",
        "latin": "Times New Roman",
        "size_pt": 10.5,
        "bold": True,
        "color": "FFFFFF",
        "alignment": "center",
    },
    "表格文字": {
        "east_asia": "宋体",
        "latin": "Times New Roman",
        "size_pt": 10.5,
        "bold": False,
        "color": "000000",
        "alignment": "center",
    },
}

TABLE_STYLE = {
    "name": "测试结果说明表格",
    "default_width_twips": 9360,
    "header_fill": "1F4E79",
    "header_font_color": "FFFFFF",
    "body_fill": "FFFFFF",
    "border_color": "B7C9D6",
    "border_size_eighth_pt": "4",
    "cell_margin_top_twips": "70",
    "cell_margin_bottom_twips": "70",
    "cell_margin_left_twips": "90",
    "cell_margin_right_twips": "90",
    "status_fills": {
        "满足": "E2F0D9",
        "不满足": "F4CCCC",
        "暂不能判定": "FFF2CC",
        "未测试": "FCE4D6",
    },
    "status_font_colors": {
        "满足": "000000",
        "不满足": "C00000",
        "暂不能判定": "000000",
        "未测试": "C00000",
    },
    "exception_fill": "C0504D",
    "exception_font_color": "FFFFFF",
    "rework_post_fill": "B8CCE4",
    "rework_pre_fill": "E5B8B7",
    "rework_pre_font_color": "595959",
    "rework_status_keywords": ("改焊后", "改焊前"),
}

PLACEHOLDERS = (
    "测试结果说明",
    "器件名称",
    "测试项目名称",
    "填写指标要求",
    "填写测试结果",
    "填写结论",
    "插入结果图片",
    "测试结果图",
    "填写实测值、判定及未覆盖内容",
    "填写未完成测试项目",
)

FORMAL_STATES = ("满足", "不满足", "暂不能判定", "未测试")

# 改焊前后对比表规范（权威范本：电性加强件 SZSD_YCQD_20260927.docx，JG15 标准行）。
REWORK_COMPARISON = {
    "status_column_names": ("状态", "焊接情况"),
    "post_first": True,
    "interface_column_white": True,
    "post_fill": "B8CCE4",
    "post_theme_fill": ("accent1", "66"),
    "pre_fill": "E5B8B7",
    "pre_theme_fill": ("accent2", "66"),
    "pre_font_color": "595959",
    "pre_interface_cell_empty": True,
    "not_reworked_status": ("改焊前", "—"),
    "over_limit_style": "bold",
    "legacy_over_limit_fill": "D99594",
}

