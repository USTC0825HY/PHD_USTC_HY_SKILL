# Report Standard

Formal DOCX and Markdown reports belong under `C:\01_obsidian\ustc_hy\01_科研主系统\04_实验测试与证据\03_超稳激光电控箱指标测试\LASER 测试报告\202607\01_正式报告`. The template asset remains inside the skill.

## 1. Document Logic

Use `laser-test-report-writing` as the source of truth for report content order, engineering narrative, result-item method placement, evidence logic, figures, captions, tables, formulas, status terms, and safe DOCX editing. A formal engineering report normally starts with purpose and conclusion summary, then explains the test object, connection, and shared conditions before presenting device-oriented results. This standard only adds the project template contract below.

## 2. Information And Heading Rules

The title is not a heading. Use `报告题名`.

Use a structured two-column information table immediately after `报告题名` and `报告短题名`. Record version, test time, report date, location, personnel, author/reviewer/approver, and a compact revision history. The legacy `报告信息` style remains available for converted reports.

Use three new-page sections: an unnumbered cover, a directory section with lower-Roman page numbers, and a body section that restarts decimal page numbering at 1. The body header uses a `STYLEREF` field bound to `报告短题名`; the cover has no header or footer.

Use the original report's custom quick styles. Do not use the built-in Heading 1/2/3 styles:

| Level | Display | Example |
|---|---|---|
| `一级标题` | `%1.` | `1.指标需求与判定依据` |
| `二级标题` | `%1.%2` | `3.1测试项信息` |
| `三级标题` | `%1.%2.%3` | `4.1.1测试指标与条件` |

Do not type the number in the heading text. Do not use normal text or list paragraphs as a substitute for headings. Do not skip a level. All three levels share one automatic list and remain in the `\u` TOC.

Keep ordinary numbered lists on an independent list definition. A legacy list must never share the heading list instance or an abstract numbering definition linked to `一级标题/二级标题`; otherwise its items silently advance later section numbers.

The active values are defined in `scripts/style_contract.py`. All three levels use list left/hanging indents of 510/226 twips. Level 1 uses restrained dark-blue Microsoft YaHei; levels 2 and 3 use black Microsoft YaHei. Heading styles provide deliberate before/after spacing and pagination protection. Clear direct numbering, point indents, character-unit indents, tabs, fonts, and sizes from heading paragraphs.

## 3. Engineering Writing

Apply the engineering language, evidence classification, section naming, and status vocabulary from `laser-test-report-writing`. Do not maintain a second project-specific wording system.

## 4. Figures, Tables, Formulas, And Paths

Apply the global figure, caption, table, formula, and source-path rules from `laser-test-report-writing`. In this project template:

- Map captions to `图表题注`.
- Map image anchors to `图片`.
- Map header/body cell text to `表格表头` and `表格文字`.
- Convert LaTeX through the project Pandoc/OMML helper when professional equations are required.

Directory entries use explicit `TOC 1/2/3` styles: Songti/Times New Roman 12 pt, left aligned, zero first-line indent, level left indents of 0/21/42 pt, and one right-aligned dotted page-number tab at 15.5 cm. Do not allow TOC styles to inherit body justification or the body first-line indent.

## 5. DOCX Layout Contract

| Object | Required style or behavior |
|---|---|
| Page | A4, left 3.0 cm, right 2.5 cm, top/bottom 2.5 cm; header/footer distance 1.25 cm |
| Body | Songti Chinese, Times New Roman Latin, 12 pt, exact 20 pt line spacing, first-line indent 24 pt |
| Report title | Microsoft YaHei 22 pt, bold, centered, `1F4E79` |
| Report short title | Microsoft YaHei 14 pt, bold, centered; used by the body running header |
| Directory title | Microsoft YaHei 16 pt, bold, centered |
| `一级标题` | Microsoft YaHei 15 pt, bold, `1F4E79`, automatic `1.`, 12/6 pt before/after |
| `二级标题` | Microsoft YaHei 12 pt, bold, black, automatic `1.1`, 9/3 pt before/after |
| `三级标题` | Microsoft YaHei 12 pt, bold, black, automatic `1.1.1`, 6/3 pt before/after |
| Report information | Songti/Times New Roman 12 pt, no indent, not numbered |
| Caption | Songti/Times New Roman 10.5 pt, centered, no indent |
| Table header | `表格表头`, Songti/Times New Roman 9.5 pt, bold, centered, zero first/left/right indent |
| Table body | `表格文字`, Songti/Times New Roman 9.5 pt, centered, zero first/left/right indent |
| Image anchor | `图片`, centered, zero first/left/right indent, kept with its following figure caption |

Repeat table header rows. Vertically and horizontally center every table cell, including long technical notes and path text.
Set the table object itself to centered, keep `tblInd` absent or explicitly zero, and proportionally shrink only tables whose grid exceeds the containing section's body width.

### Project Table Visual Contract

Apply this contract to newly created tables and to existing tables only when the user explicitly requests restyling:

- Use `报告表格样式`; place a centered `图表题注` caption above the table.
- Fill the header row with `DDEBF7`; use a white `FFFFFF` body without banded rows.
- Use `808080` 0.5 pt single borders for all outside and inside edges.
- Use `表格表头` for bold 9.5 pt header text and `表格文字` for 9.5 pt body text; center horizontally and vertically. Use 85 twip top/bottom and 102 twip left/right cell margins.
- Use status fills only in a column explicitly named `结论`: `满足`=`E2F0D9`, `不满足`=`F4CCCC`, `暂不能判定`=`FFF2CC`, `未测试`=`E7E6E6`.
- Insert line breaks at semantic or unit boundaries in long headers; do not end headers or captions with punctuation.
- Use fixed columns within the body width, zero table/paragraph indents, a repeated header row, and non-splitting data rows.
- Run `audit_standard_test_report_docx.py <docx> --strict-table-style` for newly generated documents whose complete table set is expected to follow this visual contract.
- Before final delivery, also use `--final-content` to reject residual `待填写`, figure placeholders, short-title placeholders, and technical full-width parentheses.

The delivery audit scans high-confidence template wording that weakens engineering prose and, when an equivalent-input noise result appears, checks that calibration and FPGA gain or transfer terms are recorded. Use `--profile engineering` for the engineering-narrative contract and `--profile ad2208-da9726` for the digital-lock-board ADC/DAC review. A warning identifies a possible problem; it is not a substitute for source-data review.

## 6. Known Project-Specific Legacy Defects To Correct

The 20260703-20260708 report is a content and layout reference, not a style implementation to copy verbatim. Correct these defects in all new reports:

- Numbers in section text are manual rather than automatic Word numbering.
- `测试时间` and related information paragraphs use the legacy `一级标题` style.
- Some reports use built-in Heading styles or inconsistent custom styles instead of `一级标题/二级标题/三级标题`.
Generic caption, table, equation, evidence, and result-structure defects are governed by `laser-test-report-writing` and its audit rather than duplicated here.
