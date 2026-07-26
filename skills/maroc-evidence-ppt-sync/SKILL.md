---
name: maroc-evidence-ppt-sync
description: "MAROC adapter for hardware evidence-to-PPT synchronization. Use when turning MAROC RTL diffs, XSim reports, ILA CSV/screenshots, Obsidian notes, schematic evidence, host logs, or board-test results into MAROC PPT claims, slide outlines, evidence tables, or screenshot placeholders. Use hardware-evidence-report-sync for the generic method."
---

# MAROC Evidence PPT Sync

## Workflow

1. Apply `hardware-evidence-report-sync` for the generic claim table and evidence boundaries.
2. Load MAROC-specific evidence wording from `maroc-hardware-dev-router/references/evidence-boundaries.md`.
3. Convert each MAROC stage into slide material: phenomenon, basis, action, verification, current conclusion, remaining boundary, and next action.
4. Use `maroc-ppt` for shared MAROC style, typography, waveform, screenshot, and PowerPoint QA rules.
5. Use the scenario skill for deck structure: `maroc-ppt-debug-report`, `maroc-ppt-progress-summary`, or `maroc-ppt-group-meeting`.

## MAROC Output Contract

Return a slide claim table with page/topic, evidence class, evidence path, observed fact, allowed conclusion, forbidden overclaim, screenshot/plot needed, repo commit/bit/ltx when available, and next action.

## Asset Library

- Read `C:/Users/Administrator/.codex/skills/maroc-hardware-dev-router/references/maroc-asset-map.md` before selecting MAROC evidence or report templates.
- Use `C:/Users/Administrator/.codex/hardware-assets/source-refs/maroc-ppt-assets.md` and `source-refs/maroc-doc-assets.md` to locate existing decks, build scripts, QA reports, and Obsidian notes.
- Use `C:/Users/Administrator/.codex/hardware-assets/templates/reports/claim_table_template.md` and `ppt_md_companion_template.md` for new evidence-to-slide synchronization records.
- Use `C:/Users/Administrator/.codex/hardware-assets/hooks/maroc-hook-map.md` when script outputs feed a slide. Preserve hook id, mode, run directory, and risk level in the claim table.
