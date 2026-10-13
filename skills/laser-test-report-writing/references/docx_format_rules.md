# DOCX Format Rules

Use this reference when generating or revising a Word test report. For a final editorial pass or de-AI cleanup, also read `final_review_rules.md` and preserve the approved level-1 structure.

## Contents

- Template and page-density guidance
- Tables
- Formulas
- Figures and captions
- Preserving hand-edited DOCX files
- Software screenshots
- Audit before delivery

## Template

When the user provides a reference DOCX, use it as the style source. Preserve page size, margins, major heading styles, captions, and table look as much as practical.

For laser test-result reports, titles and all multilevel headings must be black. Use Microsoft YaHei for Chinese/CJK characters and Times New Roman for English, Latin letters, numbers, and symbols. Apply this mapping both to the paragraph style and to direct run formatting so theme colors or copied-run overrides cannot restore blue text or Arial. Preserve the existing automatic multilevel-numbering link; font normalization must never replace numbering with typed labels.

For the scoped test-result summary profile, keep the title and all heading levels black and apply the same mixed-script font mapping to title/heading styles. Apply automatic multilevel numbering through the paragraph style or numbering definition; do not type chapter numbers into heading text. Every table cell is explicitly horizontal- and vertical-centered, and each indicator follows brief method → requirement → table → result explanation → figures/captions. Do not force an empty coverage note.

If no template is provided, use these defaults:

- Body Chinese font: 宋体
- Body Latin font: Times New Roman
- Heading Chinese font: 微软雅黑
- Heading Latin font: Times New Roman
- Heading color: black (`000000`) at every level
- Body size: 12 pt
- Table text size: 10.5 pt

For a formal engineering report, keep the main body readable rather than maximizing content density. A 12–15 page main report is a useful target when evidence permits, but never shrink figures, tables, or equations below readable size to reach it. Move raw screenshots, long processing settings, complete paths, and data inventories to appendices.

## Tables

Place each table caption immediately above its table. For explicitly formal engineering reports use an automatic Word `SEQ 表` field; preserve the selected compact report convention and do not end the caption with `。` or `.`.

Center the table object and keep its object indent at zero. All table text must have no first-line indent. Explicitly set:

- `firstLine = 0`
- `left = 0`
- `right = 0`

Center all table-cell text horizontally and vertically by default. Use left alignment only when the user explicitly requests it for a specific long-text table. Apply centering to header and body rows, then verify it after Word updates fields or the table of contents.

For a report whose table-alignment requirement is global, write horizontal centering on every paragraph in every cell and vertical centering on every cell explicitly; do not rely on style inheritance or the current Word display. Set first-line, left, and right paragraph indents to zero without changing table widths, merges, borders, fills, row heights, images, or cell content. Re-audit all cells after refresh/export.

Repeat the header row across pages and set data rows not to split across pages. Preserve user-adjusted column widths and header wording unless the requested change explicitly targets them.

For newly created project tables, use a dark-blue `1F4E79` header with bold white `FFFFFF` text. Apply white explicitly to every nonempty run in the first row; do not rely only on style inheritance because Word field refresh or copied cells can restore black direct formatting. Body text remains black.

Use tables only when row-to-row or channel-to-channel comparison is useful. Do not place paragraph-length explanations in cells. Put units in headers rather than repeating them in every data cell. Use consistent decimal places based on the source resolution. Do not end a header cell with `。`, `.`, `；`, `;`, `：`, or `:`.

Only for an explicitly requested formal engineering profile, keep one core result-summary table near the front of the report. Do not repeat the same summary later with renamed columns. Put detailed conflict registers, long missing-information lists, and full data indexes in appendices or companion review files.

## Formulas

Markdown source should use LaTeX display math. In DOCX, convert important formulas to Word Office Math when possible.

An `m:oMath` wrapper around plain linear text is insufficient. Generate professional Word equations by either:

- converting the LaTeX source through Pandoc and inserting the generated native OMML `m:oMath` element; or
- using Word `OMaths.Add(...).BuildUp()` only after the exact UnicodeMath syntax has passed a rendered test; or
- writing structured OMML elements such as `m:sSub`, `m:sSup`, `m:f`, `m:rad`, and `m:nary`.

Prefer the Pandoc LaTeX-to-OMML route for equations containing several equality signs, fractions, radicals, or integrals. Do not use escaped `\/` as a generic fraction shortcut: Word can absorb the equality expression into the numerator or denominator and produce a visually plausible but mathematically incorrect equation. Render the DOCX to PDF and visually confirm subscripts, superscripts, fraction boundaries, radicals, integral limits, and relation-sign placement. Counting `m:oMath` objects alone does not prove that a formula is correctly built.

Required formulas for noise reports usually include:

$$
A_v(f)=\sqrt{S_v(f)}
$$

$$
S_{\mathrm{AD,est}}(f)=S_{\mathrm{total}}(f)-S_{\mathrm{DA}}(f)
$$

$$
V_{\mathrm{rms}}=\sqrt{\int_{f_1}^{f_2}S_v(f)\,\mathrm{d}f}
$$

For ADC input-equivalent noise through DAC output, include the calibration chain formulas with `K_out`, `L_ADC`, and `G/H_FPGA(f)`.

## Figures And Captions

For a single result, place figure and caption together inside the result subsection that interprets it. Do not collect quantitative figures in a later standalone image-inspection chapter.

Place each figure caption immediately below its figure. Compact 513 reports use plain-text 图N captions; preserve untouched legacy fields during surgical edits. Formal engineering profiles may use SEQ fields. Do not end either figure or table captions with a Chinese or ASCII period (`。` or `.`).

Use the figure identity, visible-caption, manifest, traceability-table, and mixed-font contract in `figure-identity-typography.md`. Visible compact captions use `图N` without a space and do not show the report-internal evidence ID. Evidence IDs and source filenames belong only in the task-local manifest and appendix traceability table.

Each figure must:

- appear exactly once;
- remain adjacent to its caption and nearby result text;
- have a preceding sentence that states the question or comparison;
- have preceding result explanation that extracts numerical observations and states the supported conclusion;
- use the same units and status wording as the corresponding result table.

Each figure should communicate one main result. Prefer a redrawn response curve, comparison curve, clear PSD/ASD plot, phase-noise plot, fit plot, or residual plot over a low-resolution handwritten collage. Preserve the collage as a raw record in an appendix when it remains relevant. If the source data do not support redrawing, crop and enlarge the original rather than inventing points.

For paired ASD/PSD figures of the same device/channel:

- one device/channel per row
- ASD figure in one cell
- PSD figure in the adjacent cell
- channel label in the first cell if using a table

This layout is preferred for 4-channel DAC comparisons.

## Preserving Hand-Edited DOCX Files

Treat an existing user-edited DOCX as the source of truth for both content and layout.

1. Record the source path, modification time, file size, and SHA-256 hash; check whether Word holds an exclusive lock.
2. Create a dated or task-specific backup before any mutation.
3. For caption fixes, section moves, or isolated text changes, edit only the required OOXML nodes. Do not rerun a full report generator.
4. If the source is open or its hash changes, write a separate revision and do not close Word or overwrite the source.
5. Replace the formal file only after confirming the original hash is unchanged and the file is unlocked.
6. Verify that paragraphs, tables, images, equations, fields, and unrelated text remain unchanged except for the requested edits.
7. Refresh fields and captions, run the audit, render a PDF, and visually inspect formulas, captions, tables, images, and page breaks.
8. Use the newest user-edited file as the edit base. Do not regenerate it from an older snapshot or reapply a template to untouched content.
9. Default post-refresh cleanup must preserve table fills, borders, widths, row heights, fonts, font colors, alignment exceptions, merged cells, pagination, and user wording. Full table restyling requires explicit user authorization.
10. Build a before/after fingerprint for every untouched table and section. At minimum compare paragraph text, table dimensions, grid widths, cell fills, header font colors, image count, section geometry, and field count. Treat any difference outside the authorized nodes as a failed revision.

For a deep reconstruction, also inspect headers/footers, section geometry, TOC entries, cross-references, tracked changes, comments, external links, and local paths. Generate a separate revision plus modification notes, conflict/open-item records, and a technical review record when requested; never replace the original with the reconstructed file.

## Software Screenshots

When the user references instrument or software screenshots:

- insert the supplied screenshot close to the relevant operating instructions;
- add a caption, source, and a short explanation of every parameter used in the conclusion;
- distinguish acquisition controls from display-only controls;
- do not replace a requested screenshot with a generic block diagram;
- if the original screenshot is unavailable, use an official vendor screenshot, cite its page, and state that it is an official interface example rather than the user's exact test configuration.

## Audit Before Delivery

Run:

```bash
python scripts/audit_test_report_docx.py path/to/report.docx
```

Fix hard failures before final delivery:

- problem words or old phrases remain
- indicator conclusions still use English `PASS/FAIL` or legacy `通过/未通过`; formal Chinese reports must use `满足/不满足/暂不能判定/未测试`
- table cell indentation not explicit zero
- table content is not explicitly centered horizontally and vertically
- expected formulas are plain text or unstructured Office Math
- formula subscripts, fractions, radicals, or integral limits render incorrectly
- requested software screenshots lack captions or parameter explanations
- expected paired figures are missing or separated
- a standalone image-inspection chapter duplicates or separates figures from their quantitative result analysis
- a final indicator-comparison table omits an applicable requirement or a no-data item
- a figure/table caption ends with `。` or `.`, or is placed on the wrong side of its object
- a visible figure caption contains `[EVIDENCE-ID]`, a source filename, a temporary screenshot name, or a space between `图` and its number
- figure count, caption count, manifest rows, evidence IDs, references, or traceability rows are not one-to-one
- a table object is not centered, its header does not repeat, or a data row can split across pages
- a requested local edit was implemented by regenerating and overwriting a hand-edited report
- a dark-blue project table header contains non-white visible text
- a surgical revision changes an untouched table fill, column width, font color, paragraph, figure, section, or page setting
- technical or English content still uses full-width Chinese parentheses, such as `（MSPS）`, `（Hz）`, `（µV/√Hz）`, or `（0 V）`; use `(MSPS)`, `(Hz)`, `(µV/√Hz)`, and `(0 V)` while retaining `（ ）` for Chinese prose
- the report uses several competing formal status vocabularies instead of `满足/不满足/暂不能判定/未测试`
- a main-body table contains paragraph-length management prose or repeats the core result summary
- an unreadable handwritten collage is used as the only formal result figure when a clear source plot is available
- a condition-specific method is separated from its result so that the reader cannot reproduce the calculation locally


## Rework-table editing mechanics (added 2026-09-27)

Hard-won rules from the 0927 rework-style campaign; apply them whenever tables are edited through raw `document.xml`:

- Use lxml element boundaries for paragraphs/runs; string searches for <w:p can match <w:pPr and create invalid nesting.
- Use the guarded plain-text cell helper for empty or split-run text; refuse rich-content cells and set the foreground color explicitly.
- Locate tables using combined cell text, section context and grid shape; require a unique match. Do not anchor only on a measured value that can legitimately recur.
- Adding a column to a two-level header table requires a `vMerge restart` header cell plus a `vMerge` continuation cell, and a matching `gridCol` insertion; keep `gridSpan` groups consistent with the new column count.
- Cell-width edits must update both `w:tcW` (prefer `pct` values) and the `tblGrid` columns; Word and LibreOffice weigh them differently.
- Concurrent editing: snapshot mtime+md5 of the authoritative file at session start; re-check both plus the `~$` Word owner lock before overwriting. If the user saved meanwhile, rebase the scripted edits onto the newest version rather than overwriting.
- Formula cells (k=…/b=…) render as two paragraphs per cell; never move a superscript character into the second paragraph's start.
