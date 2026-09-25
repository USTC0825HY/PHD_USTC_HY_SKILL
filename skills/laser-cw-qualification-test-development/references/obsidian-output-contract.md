# Obsidian and spreadsheet output contract

## Scope

The formal CW notes live under:

`D:\obsidian_hy\ustc_hy\ustc_hy\01_科研主系统\03_超稳激光系统工程\06_FPGA数字稳频逻辑\513_test_鉴定测试顶层`

Keep original schematic screenshots. Do not leave temporary repair artifacts in the formal note directory.

## Markdown

- Use YAML frontmatter for formal notes.
- Keep current implementation, schematic evidence, inference, and pending confirmation visibly separate.
- Repair wikilinks before deleting a note.
- Keep every Mermaid `.mmd` and `.html` pair synchronized.

## CSV encoding and structure

This is mandatory because a prior export opened in Excel as mojibake and shifted fields across columns.

- Encode every formal CSV as UTF-8 with BOM.
- Use CRLF line endings.
- Quote every field, including headers and empty strings.
- Escape embedded quotes as doubled quotes.
- Do not allow accidental line breaks inside a cell.
- Re-read every file after writing and verify a fixed column count on every record.
- Scan for mojibake markers: `�`, `锟`, `鎴`, `绔`, `鏄`, `妯`, `缁`, `瀹`, `闂`.
- Do not keep `.bak`, `before_*`, `*.inspect.ndjson`, or duplicate “修复版” files in the formal directory.

## XLSX

- Generate XLSX from the final CSV; never maintain both manually.
- Compare every CSV cell with the exported first worksheet.
- Render a representative range and visually inspect Chinese text, headers, wrapping, and column alignment.
- If Excel has the destination workbook open, do not discard unsaved user work. Write a temporary replacement, report the lock, and replace only after the workbook can be safely closed.

