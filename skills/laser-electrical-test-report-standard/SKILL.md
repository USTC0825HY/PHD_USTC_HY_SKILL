---
name: laser-electrical-test-report-standard
description: Apply the formal Laser DOCX template only when a cover, contents, running header or formal pagination is explicitly requested. Compact device/indicator test results use laser-test-report-writing instead.
---

运行脚本前按 [运行时验证](../hardware-dev-router/references/runtime-validation.md) 探测实际 Python 版本和所需导入；优先复用可执行专用环境。

## Explicit formal-report boundary

Default Laser test-result writing uses `laser-test-report-writing` and its 加强件 compact profile. Apply this skill only when the user explicitly requests a formal cover, contents, running header or formal pagination. The generic words 报告 or 正式交付 alone do not trigger the formal template. Do not impose this skill on result summaries or local revisions.


# Laser Electrical Test Report Standard

Before consuming profile-derived inputs, read [path validation](../hardware-dev-router/references/profile-path-resolution.md) and run its read-only validator for the required keys only (or validate an explicit task path). Missing inputs stop dependent work; do not create obsolete directories or guess replacement campaigns. Keep existing CLI/environment overrides ahead of profile defaults.

Use this skill for the formal DOCX report standard of the ultra-stable laser electronic-control project. Treat the standard template as the Word-format source and the measured artifacts as the only source of technical facts.

Read `<CODEX_HOME>/laser-fpga-profile.json` before resolving the Obsidian or test-data roots. Use `<CODEX_HOME>/tools/laser-fpga-runtime/.venv/Scripts/python.exe` for bundled DOCX dependencies.

## Workflow

1. Apply the active `laser-test-report-writing` skill for report content, evidence logic, figures, tables, captions, equations, and safe DOCX editing.
2. Consume existing processed measurements after checking source, conditions and completeness. Apply `laser-electrical-data-analysis` for missing results, contradictions, recalculation or explicit analysis requests, then audit its generated bundle. Never recalculate formal results during DOCX generation.
3. Read [report-standard.md](references/report-standard.md) and [template-contract.md](references/template-contract.md) for the project-specific template contract.
4. For a new formal report, copy `assets/超稳激光电控箱测试报告标准模板.docx`. Replace the cover title, short title, information table, and revision record; retain the cover/directory/body section boundaries.
5. Apply the custom quick styles `一级标题`, `二级标题`, and `三级标题`. Link all three levels to the shared automatic `1.`/`1.1`/`1.1.1` list. Never use built-in Heading 1/2/3 in formal output.
6. For a newly created formal report, run both the global report audit and `scripts/audit_standard_test_report_docx.py <report.docx> --strict-table-style --final-content`. When figures exist, also run the figure-manifest audit with --strict. Local revisions use the baseline/scope workflow in laser-test-report-writing; untouched historical formal-style differences are advisory. Resolve all errors and review every warning. Export using the refreshed private copy; -SaveUpdated -UpdatedDocx <new-copy.docx> also saves that copy. No source overwrite or default whole-document sanitation.

## Template And Scripts

- Regenerate the standard asset with `python scripts/create_standard_template.py` only when the template design changes, then run `scripts/refresh_and_export_docx.ps1` with `-SaveUpdated` so the stored TOC is current.
- Use `scripts/standardize_report_copy.py <source.docx> <output.docx> --convert-captions --convert-formulas --repair-level-jumps --append-required-sections --insert-toc` to make a review copy of a legacy report. Never standardize a source report in place.
- Use `scripts/repair_report_corpus.py --root <formal-report-root>` only for an approved standardized corpus. It preserves unsuffixed originals, converts reviewed legacy math, reapplies the reference heading contract, and centers/fits every table.
- For a Markdown method note containing Mermaid and LaTeX, use Pandoc with `scripts/markdown_report_filter.lua`, the standard DOCX reference asset, and the rendered Mermaid PNG; audit the result with `--method-note`.
- Use `scripts/refresh_and_export_docx.ps1 -InputDocx <report.docx> -PdfPath <preview.pdf> -SaveUpdated -PythonExe <bundled-python>` only on an output copy or template asset. Without explicit restyle/normalize flags, no sanitizer runs; preview and saved output both use actually refreshed fields. UpdatedDocx defaults to a new _refreshed.docx, and existing outputs are never overwritten. Add `-RestyleTables -NormalizeFonts` only for a new report or an explicitly authorized full restyle.
- `-SkipSanitize` remains a compatible explicit no-sanitizer flag; sanitation is already off by default. Saving occurs only with -SaveUpdated, to a new UpdatedDocx output copy.

## Project-Specific Formatting Rules

- Use A4 pages with the active template margins: left 3.0 cm, right 2.5 cm, top/bottom 2.5 cm.
- Keep three front-matter sections. The cover is unnumbered; the directory uses lower-Roman page numbers; the body restarts at Arabic page 1 and uses the `报告短题名` running header.
- Use the structured cover table for version, test/report dates, location, personnel, author/reviewer/approver, and revision history. Keep `报告信息` only for legacy conversions.
- Use Microsoft YaHei 22 pt bold `1F4E79` for `报告题名` and Microsoft YaHei 16 pt bold for `目录标题`. Use Microsoft YaHei 15/12/12 pt for `一级标题/二级标题/三级标题`, with automatic three-level numbering and the spacing/pagination controls in `scripts/style_contract.py`.
- Treat `00_参考/电信件1 1397nm超稳激光PDH数字锁定环路分析20260710.docx` as the only heading-style reference. Apply the canonical values in `scripts/style_contract.py`; do not copy formatting from a `_规范修订版.docx`.
- Use `TOC 1/2/3` only for generated directory entries. Keep them left-aligned, unindented on the first line, and connected to a right-aligned dotted page-number tab.
- Apply the global caption/table/image rules from `laser-test-report-writing`; in this template use `图表题注`, `表格表头`, `表格文字`, and `图片` as the corresponding project quick styles.
- Use natural visible captions `图{SEQ 图} 对象/接口：图像内容`. Keep evidence IDs and source filenames in the figure manifest and appendix traceability table, not in visible captions.
- Apply the project table palette to every newly created table: `1F4E79` dark-blue header fill, bold `FFFFFF` white header text, white body, `808080` 0.5 pt single borders, centered 9.5 pt text, 85/102 twip vertical/horizontal cell margins, repeated header, and non-splitting data rows. Use restrained status fills only in a `结论` column. Rework before/after comparison tables (改焊前/改焊后 dual rows with a `状态`/`焊接情况` column) follow `laser-test-report-writing/references/rework-comparison-style.md`; this formal template does not pre-place them. Preserve existing hand-edited tables unless the user requests restyling.
- Keep hardware identifiers such as `DAC_OUT`, `REF_100M_OUT`, and `IO_UPDATE` as text. Convert confirmed mathematical quantities such as `f_s`, `T_{\mathrm{alias}}`, `K_{\mathrm{out}}`, and `L_{\mathrm{ADC}}` to inline OMML, except inside headings and TOC entries where text must remain stable.

## Output Discipline

- Preserve source facts and original files. Choose the user-specified file/current authoritative report directory first, then verified workspace rules. Historical Obsidian report directories are discovery hints only; never migrate reports automatically. Laser scratch copies use .codex_work/<task>.
- Store historical versions, local supplements, review copies, and review materials under the matching `02_过程报告` branch. Store raw data, complete CSV/PNG/MAT analysis bundles, hashes, and calculation manifests below the configured test-data root.
- Keep temporary previews and audit JSON in a temporary directory. Do not use the formal-report directory as a MATLAB output directory.
- Before changing a formal report, check for its Word `~$` lock file, record the closed source file's SHA-256, and use a separate revision unless in-place replacement is explicitly authorized. Never refresh, export, overwrite, or hash a report that Word currently holds open.
- Apply local edits to hand-formatted reports. Preserve untouched text, tables, figures, and styles; allow only requested nodes plus required field-number/TOC refresh changes.
- Always start from the newest user-edited report. Do not rebuild it from an earlier generated version, even when the earlier file is easier to automate.
- Post-refresh sanitation is preservation-only by default. It may repair zero indents, image/caption anchors, mixed fonts, and white text on a standard dark-blue header, but it must not reset table fills, widths, borders, row heights, styles, or user wording. Use explicit table-restyling mode only for a new report or when the user requests full restyling.
- Use Markdown only when requested. Its headings, status terms, formulas, figure captions, and evidence index must match the formal DOCX.
