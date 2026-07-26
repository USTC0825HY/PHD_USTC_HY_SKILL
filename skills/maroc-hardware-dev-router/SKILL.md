---
name: maroc-hardware-dev-router
description: "MAROC application adapter for the generic hardware-development skill family and MAROC asset map. Use when a request mentions MAROC, MAROC3A, QT_MUON, TOP_MAROC, 829bit, packet_250, MAROC RTL, MAROC XDC/schematic, MAROC Obsidian notes, MAROC board bring-up, MAROC PPT reporting, or MAROC reusable assets/templates/scripts/examples. For generic hardware workflows, route through hardware-dev-router first."
---

# MAROC Hardware Development Router

## Role

This skill is a MAROC project adapter. The generic architecture lives in `hardware-dev-router` and the generic FPGA/hardware/host/report skills. This skill adds MAROC paths, terminology, scripts, evidence conventions, and routing shortcuts.

## Workflow

1. Classify the generic work type with `hardware-dev-router`.
2. Load MAROC project paths from `references/resource-map.md` when files, scripts, notes, or PPT assets matter.
3. Load MAROC-specific evidence wording from `references/evidence-boundaries.md` when claims mention configuration chain, Ctest, ADC/upload, read-probe, or analog outputs.
4. Load `references/maroc-asset-map.md` when the task asks for MAROC templates, reusable scripts, source examples, PPT assets, or asset catalog lookup.
5. Load `references/maroc-hook-map.md` when the task asks to run, wrap, validate, or automate MAROC scripts.
6. Route to the MAROC adapter skill only when MAROC-specific packet formats, modules, board names, or paths are involved.

## Generic-To-MAROC Mapping

- `fpga-rtl-code-review` -> `maroc-fpga-rtl-code-review`
- `fpga-testbench-simulation` -> `maroc-fpga-testbench-simulation`
- `fpga-ila-debug` -> `maroc-fpga-ila-debug`
- `fpga-cdc-reset-timing` -> `maroc-fpga-cdc-reset-timing`
- `fpga-register-command-parser` -> `maroc-fpga-register-command-parser`
- `fpga-vivado-tcl-automation` -> `maroc-fpga-vivado-tcl-automation`
- `qt-cpp-host-development` -> `maroc-qt-host-development`
- `host-rtl-alignment` -> `maroc-host-rtl-alignment`
- `rtl-schematic-xdc-alignment` -> `maroc-rtl-schematic-xdc-alignment`
- `hardware-evidence-report-sync` -> `maroc-evidence-ppt-sync`

## MAROC Boundaries

- Keep source artifacts in place. Do not copy RTL scripts, Qt source, Obsidian notes, or PPT templates into skills.
- Treat old `maroc-fpga-development` as a compatibility entry only.
- MAROC is an application example of the generic hardware workflow, not the generic workflow itself.
- Use `C:/Users/Administrator/.codex/hardware-assets` as the central asset library; `.cc-switch` skills should reference it rather than carrying a second asset copy.
- Use `C:/Users/Administrator/.codex/hardware-assets/hooks/maroc-hook-map.md` for MAROC script hooks. Start with dry-run and do not run project-write, hardware-write, or destructive hooks without explicit confirmation.
