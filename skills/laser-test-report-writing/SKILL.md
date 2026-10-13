---
name: laser-test-report-writing
description: Write or revise concise Chinese Laser electrical test-result Word documents, organized by device and indicator, using the 加强件 result-summary template. Use for measured-result tables, selected result figures, conclusions, and local report updates. Formal cover-and-contents reports are an explicit alternative; operation manuals use their own skill.
---

# Laser Test Report Writing

运行脚本前按 [运行时验证](../hardware-dev-router/references/runtime-validation.md) 探测实际 Python 版本和所需导入；优先复用可执行专用环境。

任务模式优先于后文通用格式要求：①新建紧凑报告加载完整版式与溯源附录；②局部修订保留既有版式，只修改授权节点/单元格，旧附录缺项列为历史问题，不借此整篇重建；③用户明确要求封面、目录、页眉或正式分页时才使用 laser-electrical-test-report-standard。仅审查默认输出发现，不修改文档。

## Default and reference priority

Default to the compact 加强件 test-result profile. The approved reference is `02_Test_Reports_测试报告/02_jiaqiang/电性加强件 SZSD_YCQD_20260927.docx` (rework before/after comparison style included); `电性加强件 SZSD_YCQD_20260920.docx` remains the pre-rework baseline reference. The extracted format is in [the format contract](references/result-summary-format-contract.md).

Use the user's current reference or newest edited target ahead of the bundled template. Never reconstruct a user-edited report from an older generated version. Use `assets/超稳激光电控箱测试结果说明标准模板.docx` for a new report with no task-specific template. Do not copy the reference's measured values, figures, interface assignments, or conclusions into another campaign.

Use `laser-electrical-test-report-standard` only for an explicitly requested formal cover, contents, running header, or formal pagination. Operation manuals remain under `laser-cw-operation-manual-writing`.

## Complete format authority

For any 513/CW result report, follow [the complete format spec](references/report-format-spec.md): fixed opening block, board-grouped chapter order (SZSD: AD2208, DA9726, GTH&RF, yaoce(TLV2548), FREQ_COUNTER; YCQD: AD9245, DA766, AD677, ADC128, yaoce(ADG526+AD677)), section order `method -> requirement -> table -> result explanation -> figures (last)`, table/figure conventions, remark sentence patterns, and evidence-based pre/post-rework comparison with a dated example list. Indicator method texts in [method-templates.md](references/method-templates.md) are dated historical examples. Reuse their structure only after checking every acquisition parameter, threshold, unit and conclusion against the current evidence; unmarked historical constants are not defaults. Every newly created report carries a trailing `附录：数据溯源表` per [data-traceability.md](references/data-traceability.md); `scripts/make_traceability_rows.py` drafts its rows from run/session paths.

## Rework comparison tables

When the selected board/indicator has both pre- and post-rework evidence, show the comparison side by side. The 20260919/0927 interface list is a historical campaign example; current board records and the latest edited report determine the actual rows. Follow [the rework comparison style](references/rework-comparison-style.md): a `状态`/`焊接情况` column right after the interface column, post-rework row first with light-blue `B8CCE4` status+data cells, pre-rework row after with light-red `E5B8B7` and gray `595959` text, the interface column vertically merged per interface (one `vMerge restart` cell showing the name on the post row, empty continuation on the pre row - never repeat the name or write a hatched suffix), comparisons on the same reference basis. The same rule applies to future 鉴定件 report updates. Whether non-reworked interfaces are listed follows each table's settled convention (for example the AD2208 ILA noise table lists reworked interfaces only); never re-insert deleted rows. Never fill a pre-rework cell with a post-rework basis value or vice versa.

## Workflow

1. Confirm the board/campaign, devices, interfaces, measurement dates, source results, and requested output location. Use explicit paths first; validate profile-derived paths with `../hardware-dev-router/references/profile-path-resolution.md` only when profile defaults are needed.
2. Check existing processed results against their source, acquisition conditions, units, calibration, completeness, and figure identity. Consume valid existing outputs directly. Invoke `laser-electrical-data-analysis` when results are missing, contradictory, need recalculation, or the user requests analysis; do not recalculate inside a DOCX editing script. Audit newly generated analysis bundles before use.
3. Choose new-document or local-revision mode. Read [structure](references/report_structure.md), [format](references/result-summary-format-contract.md), and [language](references/language_rules.md). For local edits preserve every unrelated paragraph, table, figure, field, and formatting property.
4. Fill each device/indicator block: short test/analysis method → requirement → result table → result explanation → selected result figures and captions. Write missing requirements as `未提供`. Explain only key values, anomalies, judgment, and limitations; do not repeat every table row.
5. Check numbers, conditions, formal states, fonts, table alignment, captions, image mapping, and rework comparison tables against [the rework style](references/rework-comparison-style.md). Render the output copy with LibreOffice (or available Word export) and inspect changed pages plus adjacent pagination; inspect all pages for a new document. Deliver the requested DOCX; PDF/page images are internal unless requested.
6. Before overwriting an authoritative report, re-check its mtime and hash against the session snapshot and probe the Word owner lock (`~$` file). If the user saved a newer version meanwhile, rebase the scripted edits onto that version instead of overwriting. Prefer LibreOffice rendering plus a page-by-page visual inspection as the delivery gate when Word is unavailable.

The opening contains only title, test object, update date, and board state that affects interpretation. Do not automatically add a cover, contents, opening summary matrix, extra traceability chapter beyond the required appendix, pending-test summary, or process narrative. A pending-test summary is optional and contains only genuinely unfinished measurements.

## Evidence and language

Use only `满足`, `不满足`, `暂不能判定`, and `未测试` as formal states. Existing measurements with missing judgment conditions are `暂不能判定`, not `未测试`. Unknown requirements are not inferred from old boards. Preserve configured/direct/calculated values as distinct quantities. Never invent settings, connections, test coverage, causes, or conclusions.

Keep SHA, audit workflow, and internal IDs out of the reader-facing report. Paths use the verified relative/absolute convention in `附录：数据溯源表` (see data-traceability.md); do not put disk paths in body text, captions, or result tables. New reports require a visible traceability appendix; surgical work only adds authorized traceability and reports untouched legacy omissions.

Read [data and formula rules](references/data_formula_rules.md) for noise/calibration and [AD2208/DA9726 rules](references/ad2208_da9726_report_rules.md) or [DDS rules](references/dds_report_rules.md) only when relevant. These are technical checks, not fixed board maps or reusable measured conclusions. Read [final review](references/final_review_rules.md) for editorial-only work.

## Safe editing and validation

- Use a task-local copy. Preserve the original unless in-place replacement is authorized. Check the target owner lock, target access and source changes; an unrelated WINWORD process alone is not a lock. Never overwrite or automate export of a report held open in Word.
- For plain text cells use scripts/docx_safe_edit.py set_cell_text; cells containing formulas, drawings, fields, hyperlinks or tracked content require dedicated edits. Build new tables with the required grid, not cloned populated rows. Do not inherit stale merges, extra cell paragraphs, status fills, or image relationships.
- Read [DOCX mechanics](references/docx_format_rules.md) and [figure mapping](references/figure-identity-typography.md) for relevant edits. Internal `figure_manifest.csv` maps each image to its interface and adjacent caption.
- Run `scripts/audit_result_summary_docx.py <docx> --mode new --final-content` for a new compact report. In `--mode surgical`, global differences are advisory; acceptance requires --strict --before <source> --scope-json <scope> to compare untouched content and package parts, not globally restyling the target. Optional --table-profiles <json> declares table-specific required columns. Read [editing and acceptance](references/editing-and-acceptance.md) for these interfaces.
- Run `scripts/audit_test_report_docx.py <docx> --mode new|surgical --strict` for technical and object checks; surgical mode also requires `--before <source> --scope-json <scope>`. Use `scripts/audit_figure_mapping.py <docx> --manifest <csv> --mode new|surgical` --strict (and --before for surgical mode) for new/changed figure identity. The `engineering` profile is for explicitly requested long reports only.
- Refresh fields on an output copy, then inspect the final saved DOCX and render it read-only. Check readable pictures, adjacent captions, table breaks, and blank pages. Use two visual passes: inspect all changed/adjacent pages, repair scoped defects, then reinspect the affected/related pages. Report rendering limitations honestly. Record MD5/SHA-256 only after the final delivered file is saved, closed and read back; never prewrite delivery hashes.
- `scripts/standardize_result_summary_copy.py` is for explicitly authorized whole-document formatting only. Ordinary updates must not call it.

## Maintained assets

`scripts/result_summary_style_contract.py` is the shared format definition used by the template generator and new-document checker. Regenerate the clean template with `scripts/create_result_summary_template.py --output <docx>`. Keep that definition, the written contract, and the template consistent. Never bake current measurement values into the template.
