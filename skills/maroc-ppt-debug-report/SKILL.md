---
name: maroc-ppt-debug-report
description: "MAROC debug-problem PPT workflow. Use for presentations focused on one technical failure or bring-up blocker, including phenomenon, root cause, RTL/host/hardware fix, XSim/ILA/board evidence, remaining boundary, and next debug action."
---

# MAROC PPT Debug Report

## Structure

1. Cover: problem name, date, tested build/board.
2. Problem phenomenon: what failed, how observed, what was not yet proven.
3. Chain boundary: host, USB, parser, slow-control, trigger/control, upload, analog path.
4. Root-cause candidates and eliminated branches.
5. Fix or experiment design.
6. Verification evidence: XSim, ILA, host log, oscilloscope, schematic, with paths.
7. Current conclusion and remaining boundary.
8. Next action checklist.

## Rules

Use `$maroc-ppt` for visual style and QA. Use `maroc-evidence-ppt-sync` before writing conclusions.

## Asset Library

- Use `<CODEX_HOME>/hardware-assets/source-refs/maroc-ppt-assets.md` to find existing debug decks, build scripts, previews, and QA reports.
- Start new MAROC debug-report decks from `<CODEX_HOME>/hardware-assets/templates/ppt/MAROC科研汇报模板_20260519.pptx` when no newer project template is specified.
- Use `<CODEX_HOME>/hardware-assets/templates/reports/claim_table_template.md` before turning debug evidence into slide conclusions.
