# CSV Excel Compatibility Rules

Use these rules for Chinese engineering mapping tables, evidence lists, interface matrices, and other CSV files expected to open directly in Microsoft Excel.

## Required output

- Encode as UTF-8 with a leading BOM (`EF BB BF`).
- Use CRLF (`0D 0A`) record endings.
- Follow RFC 4180 field escaping.
- Quote every field, including headers and empty fields.
- Escape an embedded double quote by doubling it.
- Keep one logical record per physical CSV record; remove unintended embedded newlines.

Example:

```text
﻿"board","target","pending"\r\n
"数字锁定","ADC1","待实物确认"\r\n
```

## Required validation

1. Read the completed CSV back as UTF-8 after stripping the BOM for the parser.
2. Assert the expected row count and the same column count on every row.
3. Spot-check the first, middle, and last records.
4. Reject cells containing `�` or common mojibake fragments such as `锟`, `鎴`, `绔`, `鏄`, `妯`, `缁`, `瀹`, or `闂`.
5. When the Spreadsheets skill is available, import the final CSV with `Workbook.fromCSV`, render a representative range, and visually inspect it.
6. For Excel-first users, also export a formatted `.xlsx` companion when practical; do not replace the CSV unless requested.

## Failure pattern

If Excel shows Chinese mojibake or several source rows appear in one worksheet row, do not repair cells manually in Excel. Regenerate the source file with BOM, CRLF, quote-all serialization, then repeat the round-trip and visual checks.
