---
name: hardware-evidence-report-sync
description: "Generic hardware evidence-to-report synchronization workflow. Use when turning RTL diffs, simulations, ILA/logic-analyzer/scope captures, host logs, schematic evidence, datasheets, board-test results, or lab notes into PPT, Markdown, report claims, evidence tables, screenshot placeholders, conclusions, and next actions."
---

# Hardware Evidence Report Sync

## Workflow

1. Collect source evidence paths first: source diff, simulation log, ILA/logic-analyzer/scope export, bitstream/probe file, host log, schematic page, datasheet page, board photo, or lab note.
2. Classify each claim using `<CODEX_HOME>/skills/hardware-dev-router/references/evidence-boundaries.md`.
3. Convert each stage into report material: phenomenon, basis, action, verification, current conclusion, remaining boundary, and next action.
4. Preserve version boundaries. Do not merge results across dates, commits, bitstreams, captures, boards, or host exports unless the source explicitly ties them together.
5. Use project-specific PPT/Markdown skills for visual style or local documentation structure.

## Path resolution

Use scripts/resolve_evidence_paths.py --root <library> --input <utf8-path-list> --mapping <csv> --out <outside-library-csv> when path relocation or relative display is requested. --mapping is optional; multiple paths on one line use ；. The script returns original/resolved/display path, status, location and reason; it never edits the source or report. Mapping columns are old,new,match,status; exact is the default, prefix applies only at a directory boundary. Missing, inaccessible and unresolved remain distinct; failed mappings retain their original display path. Nonzero exit means some evidence remains unverified.

Only for 513 qualification/strengthened reports, read [513 traceability](references/513-traceability.md). Generic hardware reports do not inherit that project's roots, dates or appendix structure.

## Output Contract

Return a claim table with topic/page, evidence class, evidence path, observed fact, allowed conclusion, forbidden overclaim, screenshot/plot needed, version/build identifiers, and next action.

## Asset Library

- Use `<CODEX_HOME>/hardware-assets/templates/reports/claim_table_template.md` for evidence-to-report claims.
- Use `<CODEX_HOME>/hardware-assets/templates/reports/ppt_md_companion_template.md` for PPT/Markdown companion notes.
- Use project `source-refs/` files to locate source evidence without moving or copying original records.
- Preserve the command, tool version, stdout, stderr, and output hashes whenever a script result is used as report evidence.

映射状态缺失的旧 CSV 仍可读取，但视为草稿，不能自动参与路径替换。仅 OK/confirmed/已确认为已确认状态；与 laser-cw-data-pipeline 共用 mapping_status。
