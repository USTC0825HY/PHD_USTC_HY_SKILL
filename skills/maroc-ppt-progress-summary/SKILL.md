---
name: maroc-ppt-progress-summary
description: "MAROC overall progress PPT workflow. Use for stage-summary decks covering recent work, completed verification, current status, risks, next plan, and cross-domain evidence across FPGA, host, hardware, Obsidian notes, and experiments."
---

# MAROC PPT Progress Summary

## Structure

1. Scope and directory page.
2. Stage timeline: completed, in progress, blocked.
3. Recent technical work by layer: host, RTL, simulation, ILA, hardware, documentation.
4. Evidence-backed results and what each result proves.
5. Risks and remaining boundaries.
6. Next plan with owners or experiment conditions.
7. Appendix for scripts, evidence paths, and detailed tables.

## Rules

Keep one judgment per slide. Use `$maroc-ppt` for MAROC template and `maroc-evidence-ppt-sync` for claim filtering.

## Asset Library

- Use `<CODEX_HOME>/hardware-assets/source-refs/maroc-ppt-assets.md` to find prior progress-summary decks, build scripts, PNG previews, and QA reports.
- Start new progress decks from `<CODEX_HOME>/hardware-assets/templates/ppt/MAROC科研汇报模板_20260519.pptx` unless the task names another template.
- Use `<CODEX_HOME>/hardware-assets/templates/ppt/build_ppt_skeleton.py` and `qa_ppt_checklist.md` for reproducible generation and QA.
