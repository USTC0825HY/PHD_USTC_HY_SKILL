---
name: laser-test-report-writing
description: Create, deeply reconstruct, surgically revise, final-edit, de-AI, and audit Chinese engineering test reports for Laser/PDH electrical tests from measurement data, figures, CSV/Excel/Markdown summaries, reference reports, and hand-edited DOCX files. Use for AD/DAC/DDS/noise/bandwidth/range/power reports, final editorial review, conclusion-consistency checks, evidence-preserving language cleanup, format-preserving Word edits, global figure/table/caption rules, or formal DOCX/PDF delivery.
---

# Laser Test Report Writing

## Operating Modes

Choose one mode before acting:

1. **New report**: build a report from raw measurements and requirement files.
2. **Deep reconstruction**: compare a reference report with a target DOCX, audit all content and layout objects, then rebuild the target as an engineering test report. Read `references/engineering_report_reconstruction.md`.
3. **Surgical revision**: preserve the user's completed content and formatting; change only the requested nodes and produce a separate revision unless replacement is explicitly authorized.

Treat measured artifacts as the only source of technical facts. Never invent instruments, settings, connections, parameters, values, causes, or conclusions. Write `未记录`, `未测试`, or `暂不能判定` when the evidence requires it.

### Final Editorial Review

Treat final review, de-AI cleanup, conclusion synchronization, and format correction as a surgical revision unless the user explicitly authorizes reconstruction. Read `references/final_review_rules.md` before editing. Preserve the existing level-1 chapter structure, measured values, tables, formulas, images, and valid limitations. Do not let a profile's preferred architecture trigger a large restructure during final review.

## Analysis Gate

When the task includes raw code streams, waveform MAT files, PSD/ASD, integrated noise, Vpp-Codepp calibration, input-equivalent conversion, 1 Hz noise, or Allan stability, apply `laser-electrical-data-analysis` before editing Word. The report may consume only an evidence bundle that has passed `audit_analysis_bundle.py` without structural errors. Do not recalculate a spectrum, fit, gain conversion, or formal judgment inside a DOCX-editing script.

## Core Workflow

1. Gather source truth:
   - Read requirement files, raw data, calculation outputs, result figures, software or instrument screenshots, and relevant reference reports.
   - If raw data must be recalculated, hand it to `laser-electrical-data-analysis`, then use the audited `analysis_parameters.csv`, summary CSV, full-spectrum CSV, figures, MAT result, hashes, and calibration provenance as the report source.
   - Run `scripts/collect_report_assets.py <dir>` when a result directory is supplied.
   - Separate configured values, direct measurements, calculated values, and indicator determinations.
   - Record device, channel, date, connection, operating condition, frequency band, duration, processing parameters, units, and missing information.
2. Audit before rewriting:
   - For deep reconstruction, inspect body text, headings, TOC, tables, formulas, images, captions, headers/footers, fields, cross-references, tracked changes, and local paths.
   - Build an issue register before changing prose. Record conflicts, missing conditions, damaged formulas, duplicate results, unsupported conclusions, terminology problems, visual defects, and traceability gaps.
3. Write an engineering narrative:
   - Lead with purpose and conclusion summary, then describe the test object, connection, shared conditions, actual procedures, results, anomalies, limitations, and follow-up tests.
   - Keep shared system conditions centralized. Put item-specific methods and processing next to the result they produce.
   - In each result item, follow `purpose -> conditions -> method -> processing -> result -> analysis -> conclusion`.
   - Read `references/report_structure.md` before drafting or restructuring.
4. Apply technical rules:
   - Read `references/data_formula_rules.md` for PSD/ASD, integrated noise, calibration, equivalent-input conversion, or noise separation.
   - Read `references/dds_report_rules.md` for DDS reports.
   - Read `references/ad2208_da9726_report_rules.md` when AD2208, DA9726, JG12/JG15/JG18, JG2/JG3/JG32/JG11, or the digital-lock-board ADC/DAC chain is in scope.
5. Apply language and layout rules:
   - Read `references/language_rules.md` before revising prose.
   - Read `references/docx_format_rules.md` before creating or editing Word.
   - Read `references/final_review_rules.md` for final editorial review, de-AI cleanup, conclusion consistency, repeated channel text, and delivery statistics.
   - Use `laser-electrical-test-report-standard` for the ultra-stable-laser project's exact page, style, table-palette, heading, TOC, and template contract.
6. Validate delivery:
   - Preserve original files and record source hash, size, and modification time.
   - Keep raw data and complete analysis bundles in the `G:\01_laser\202607_电2test` data tree. Keep historical/review DOCX files in `02_过程报告`; place only final DOCX/PDF and necessary TODO workbooks in `01_正式报告`.
   - If the target report has a Word `~$` lock file, do not overwrite, refresh, export, or hash that open report.
   - Refresh Word fields on an output copy. Run `scripts/audit_test_report_docx.py <report.docx> --mode surgical` for final/local revisions, or use `--mode new|reconstruction` for their matching modes.
   - Render to PDF and visually inspect every page. Verify the TOC, captions, formulas, subscripts/superscripts, tables, images, page breaks, abnormal blank space, comments, highlights, and tracked changes.
   - State generated files, major structural changes, downgraded conclusions, unresolved conflicts, and rendering limitations in the handoff.

## Report Behavior

- Keep the main report focused on information needed to understand and judge the test. Move long parameter listings, raw screenshots, full paths, formulas, and data indexes to appendices.
- Use only `满足`, `不满足`, `暂不能判定`, and `未测试` as formal conclusion states. Use descriptive prose for intermediate evidence status.
- For new reports and deep reconstruction, use one core result-summary table near the front and do not repeat it later under a different schema. During surgical revision, preserve the approved structure and repair only duplicated or conflicting summaries in scope.
- Keep each result figure beside its quantitative interpretation. Do not create a standalone image-inspection chapter or duplicate figures in the main body.
- Use tables for compact comparison, not for paragraph-length narrative. Put units in headers and use consistent precision.
- State exact acquisition limits. Never judge an indicator from data that does not cover its required band, duration, load, range, resolution, or operating condition.
- Treat possible causes as hypotheses. Pair each hypothesis with a distinguishing follow-up test.
- Make every follow-up action correspond to an unresolved indicator, anomaly, conflict, or missing condition.

## References

- `laser-electrical-data-analysis`: reproducible calculation, calibration, indicator coverage, and evidence-bundle audit before report editing.
- `references/report_structure.md`: engineering narrative, section architecture, result-item pattern, states, appendices.
- `references/engineering_report_reconstruction.md`: reference/target comparison, issue register, companion review files, preservation rules.
- `references/data_formula_rules.md`: PSD/ASD formulas, units, integration, calibration, and noise separation.
- `references/language_rules.md`: concise engineering prose, terminology, anomaly writing, mixed-language typography.
- `references/docx_format_rules.md`: Word tables, figures, formulas, captions, layout, safe editing, and rendering checks.
- `references/final_review_rules.md`: report-specific de-AI cleanup, conclusion matrix, repeated-result compression, format normalization, and final QA.
- `references/dds_report_rules.md`: DDS-specific content order and result rules.
- `references/ad2208_da9726_report_rules.md`: digital-lock-board AD2208/DA9726 technical review profile.

## Scripts

- `scripts/collect_report_assets.py <result_dir> [--output manifest.csv]`: inventory report evidence.
- `scripts/normalize_mixed_parentheses_docx.py <source.docx> <output.docx>`: normalize technical parentheses without flattening DOCX structure.
- `scripts/audit_test_report_docx.py <report.docx> [--mode new|reconstruction|surgical] [--profile engineering|ad2208-da9726|dds]`: audit global rules with mode-aware severity and optional technical profiles.
