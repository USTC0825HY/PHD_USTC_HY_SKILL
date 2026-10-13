# Figure Identity And Mixed Typography

Use this contract for every new report and for any revision that changes figures, captions, figure references, or document-wide fonts.

## Reader-facing figure captions

Keep the visible caption natural:

```text
图N 对象/接口：图像内容
```

Examples:

```text
图1 RF射频参考：49.96 MHz，Marker 16.73 dBm
图12 DA9726 DAC2/JG20：正弦输出
```

- Do not insert a space between `图` and the sequence number.
- Do not expose an evidence ID, source filename, temporary screenshot name, or local path in the visible caption.
- Compact 513 new captions use plain-text 图N. Preserve untouched legacy fields; renumber the full document only when that is part of the authorized edit.
- Preserve stable legacy evidence IDs during surgical revision, but keep them in the task-local manifest; the data-traceability appendix is required for 513 reports.

## Evidence identity

Assign every new figure a stable ASCII evidence ID:

```text
<OBJECT>-<CHANNEL_OR_INTERFACE>-<CONTENT_TYPE>-<NN>
```

Use uppercase letters, digits, and hyphens. Use `NA` only when no channel or interface exists. Examples:

```text
RFREF-JG1-SPECTRUM-01
DA9726-DAC1-WAVE-01
AD766-X12G-ASD-01
GTH-4P5M-SPECTRUM-01
```

Maintain a task-local `figure_manifest.csv` with exactly these columns:

```text
sequence,evidence_id,object,interface,content_type,caption,source_filename,word_section
```

The evidence ID and original filename are provenance fields. Do not use either as the figure's reader-facing name.

## One-to-one mapping

Enforce all of the following:

- one inserted image -> one adjacent visible caption;
- one caption -> one image;
- one figure number -> one manifest row;
- one evidence ID -> one manifest row;
- every reader-facing `图N` or `图N～图M` reference resolves to an existing caption;
- each figure resolves to at least one row in the required data-traceability appendix; same-source figures/tables may share a row;
- the main report never uses a source filename, temporary screenshot name, or `未单独保存` as a figure reference.

An optional additional figure-only index, distinct from the required seven-column data appendix, may use this header:

```text
图号 | 报告内编号 | 对象/接口 | 图像内容 | 原始文件名（仅追溯）
```

Keep each figure next to the paragraph that interprets its result. A caption does not replace the quantitative observation or conclusion.

## Mixed-language typography

Use one run with script-specific font attributes whenever possible:

- `w:eastAsia`: Chinese font for the active profile;
- `w:ascii`, `w:hAnsi`, and `w:cs`: Times New Roman for Latin letters, digits, units, identifiers, paths, and signal names.

Profiles:

| Profile | Chinese body/table/caption | Latin/digits/units | Heading Chinese |
|---|---|---|---|
| `report` | 宋体 | Times New Roman | 微软雅黑 |
| `manual` | 微软雅黑 | Times New Roman | 微软雅黑 |

Do not split text runs merely to apply Chinese and Latin fonts. Do not rewrite field instructions, bookmarks, hyperlinks, drawings, or relationship IDs. Preserve Office Math fonts and structures; do not replace Cambria Math with body fonts.

Use a half-width space between a value and its unit. Use `( )` around Latin identifiers, formulas, version strings, or number-plus-unit spans; use `（ ）` for Chinese explanatory prose.

## Refresh and final audit order

For a saved output copy:

1. update only the applicable existing fields/cross-references on the output copy; do not introduce SEQ fields into plain-text captions;
2. save and close Word;
3. inspect scoped table, image, caption, and font properties; repair only authorized changes, preserving unrelated formatting;
4. audit the final DOCX against the figure manifest;
5. reopen the final DOCX read-only and export the PDF without saving;
6. inspect every rendered page.

Render only the final saved output copy. No automatic whole-document sanitizer is part of a local edit.
