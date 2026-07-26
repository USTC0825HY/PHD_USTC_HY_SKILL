---
name: hardware-evidence-report-sync
description: "Generic hardware evidence-to-report synchronization workflow. Use when turning RTL diffs, simulations, ILA/logic-analyzer/scope captures, host logs, schematic evidence, datasheets, board-test results, or lab notes into PPT, Markdown, report claims, evidence tables, screenshot placeholders, conclusions, and next actions."
---

# Hardware Evidence Report Sync

## Workflow

1. Collect source evidence paths first: source diff, simulation log, ILA/logic-analyzer/scope export, bitstream/probe file, host log, schematic page, datasheet page, board photo, or lab note.
2. Classify each claim using `C:/Users/Administrator/.codex/skills/hardware-dev-router/references/evidence-boundaries.md`.
3. Convert each stage into report material: phenomenon, basis, action, verification, current conclusion, remaining boundary, and next action.
4. Preserve version boundaries. Do not merge results across dates, commits, bitstreams, captures, boards, or host exports unless the source explicitly ties them together.
5. Use project-specific PPT/Markdown skills for visual style or local documentation structure.

## Output Contract

Return a claim table with topic/page, evidence class, evidence path, observed fact, allowed conclusion, forbidden overclaim, screenshot/plot needed, version/build identifiers, and next action.

## Asset Library

- Use `C:/Users/Administrator/.codex/hardware-assets/templates/reports/claim_table_template.md` for evidence-to-report claims.
- Use `C:/Users/Administrator/.codex/hardware-assets/templates/reports/ppt_md_companion_template.md` for PPT/Markdown companion notes.
- Use project `source-refs/` files to locate source evidence without moving or copying original records.
- Use `C:/Users/Administrator/.codex/hardware-assets/hooks/hardware-hook-registry.yaml` for `ppt.qa.*`, `rtl.sim.*`, `ila.capture.*`, and validation hooks when report evidence needs reproducible script outputs. Preserve hook run logs as report inputs.
