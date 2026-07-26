---
name: laser-electrical-test-report-standard
description: Apply the ultra-stable-laser project-specific formal DOCX template contract, including the minimalist engineering cover, three-section page-number system, automatic 1./1.1/1.1.1 headings, TOC layout, blue-header tables, status fills, project quick styles, and compliance auditing. Use together with laser-test-report-writing for content, evidence, captions, tables, equations, and safe Word editing.
---

# Laser Electrical Test Report Standard

Use this skill for the formal DOCX report standard of the ultra-stable laser electronic-control project. Treat the standard template as the Word-format source and the measured artifacts as the only source of technical facts.

## Workflow

1. Apply the active `laser-test-report-writing` skill for report content, evidence logic, figures, tables, captions, equations, and safe DOCX editing.
2. When numerical results originate from raw ILA/Pico/counter/calibration data, apply `laser-electrical-data-analysis` first and accept only its audited evidence bundle. Never recalculate formal results during DOCX generation.
3. Read [report-standard.md](references/report-standard.md) and [template-contract.md](references/template-contract.md) for the project-specific template contract.
4. For a new formal report, copy `assets/超稳激光电控箱测试报告标准模板.docx`. Replace the cover title, short title, information table, and revision record; retain the cover/directory/body section boundaries.
5. Apply the custom quick styles `一级标题`, `二级标题`, and `三级标题`. Link all three levels to the shared automatic `1.`/`1.1`/`1.1.1` list. Never use built-in Heading 1/2/3 in formal output.
6. Before delivery, run both the global report audit and `scripts/audit_standard_test_report_docx.py <report.docx> --strict-table-style --final-content`. Resolve all errors and review every warning. Use `scripts/refresh_and_export_docx.ps1` to update fields and inspect a temporary PDF when layout matters.

## Template And Scripts

- Regenerate the standard asset with `python scripts/create_standard_template.py` only when the template design changes, then run `scripts/refresh_and_export_docx.ps1` with `-SaveUpdated` so the stored TOC is current.
- Use `scripts/standardize_report_copy.py <source.docx> <output.docx> --convert-captions --convert-formulas --repair-level-jumps --append-required-sections --insert-toc` to make a review copy of a legacy report. Never standardize a source report in place.
- Use `scripts/repair_report_corpus.py --root <formal-report-root>` only for an approved standardized corpus. It preserves unsuffixed originals, converts reviewed legacy math, reapplies the reference heading contract, and centers/fits every table.
- For a Markdown method note containing Mermaid and LaTeX, use Pandoc with `scripts/markdown_report_filter.lua`, the standard DOCX reference asset, and the rendered Mermaid PNG; audit the result with `--method-note`.
- Use `scripts/refresh_and_export_docx.ps1 -InputDocx <report.docx> -PdfPath <preview.pdf>` only on an output copy or template asset; with `-SaveUpdated` it refreshes Word fields and then reapplies table/image/caption layout through `sanitize_docx_layout.py`.
- Add `-SkipSanitize` when refreshing a hand-edited report whose existing table formatting must remain untouched; this saves updated fields and exports the PDF without restyling the table corpus.

## Project-Specific Formatting Rules

- Use A4 pages with the active template margins: left 3.0 cm, right 2.5 cm, top/bottom 2.5 cm.
- Keep three front-matter sections. The cover is unnumbered; the directory uses lower-Roman page numbers; the body restarts at Arabic page 1 and uses the `报告短题名` running header.
- Use the structured cover table for version, test/report dates, location, personnel, author/reviewer/approver, and revision history. Keep `报告信息` only for legacy conversions.
- Use Microsoft YaHei 22 pt bold `1F4E79` for `报告题名` and Microsoft YaHei 16 pt bold for `目录标题`. Use Microsoft YaHei 15/12/12 pt for `一级标题/二级标题/三级标题`, with automatic three-level numbering and the spacing/pagination controls in `scripts/style_contract.py`.
- Treat `00_参考/电信件1 1397nm超稳激光PDH数字锁定环路分析20260710.docx` as the only heading-style reference. Apply the canonical values in `scripts/style_contract.py`; do not copy formatting from a `_规范修订版.docx`.
- Use `TOC 1/2/3` only for generated directory entries. Keep them left-aligned, unindented on the first line, and connected to a right-aligned dotted page-number tab.
- Apply the global caption/table/image rules from `laser-test-report-writing`; in this template use `图表题注`, `表格表头`, `表格文字`, and `图片` as the corresponding project quick styles.
- Apply the project table palette to every newly created table: `DDEBF7` header fill, white body, `808080` 0.5 pt single borders, centered 9.5 pt text, 85/102 twip vertical/horizontal cell margins, repeated header, and non-splitting data rows. Use restrained status fills only in a `结论` column. Preserve existing hand-edited tables unless the user requests restyling.
- Keep hardware identifiers such as `DAC_OUT`, `REF_100M_OUT`, and `IO_UPDATE` as text. Convert confirmed mathematical quantities such as `f_s`, `T_{\mathrm{alias}}`, `K_{\mathrm{out}}`, and `L_{\mathrm{ADC}}` to inline OMML, except inside headings and TOC entries where text must remain stable.

## Output Discipline

- Preserve source facts and original files. Store only final DOCX/PDF and necessary TODO workbooks under `C:\01_obsidian\ustc_hy\01_科研主系统\04_实验测试与证据\03_超稳激光电控箱指标测试\LASER 测试报告\202607\01_正式报告`.
- Store historical versions, local supplements, review copies, and review materials under the matching `02_过程报告` branch. Store raw data, complete CSV/PNG/MAT analysis bundles, hashes, and calculation manifests below `G:\01_laser\202607_电2test`.
- Keep temporary previews and audit JSON in a temporary directory. Do not use the formal-report directory as a MATLAB output directory.
- Before changing a formal report, check for its Word `~$` lock file, record the closed source file's SHA-256, and use a separate revision unless in-place replacement is explicitly authorized. Never refresh, export, overwrite, or hash a report that Word currently holds open.
- Apply local edits to hand-formatted reports. Preserve untouched text, tables, figures, and styles; allow only requested nodes plus required field-number/TOC refresh changes.
- Use Markdown only when requested. Its headings, status terms, formulas, figure captions, and evidence index must match the formal DOCX.
