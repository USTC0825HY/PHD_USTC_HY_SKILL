---
name: maroc-fpga-development
description: "Legacy compatibility router for historical MAROC USB/FPGA development requests. Use when a user invokes the old MAROC FPGA skill name, or when a request mentions MAROC RTL, USB, configuration chain, ILA, XSim, board bring-up, host protocol, Obsidian notes, or PPT but does not specify a newer leaf skill. This is a MAROC application adapter over the generic hardware-dev-router family."
---

# MAROC FPGA Development Compatibility Router

This is the legacy MAROC FPGA skill entry. Keep it as a compatibility layer. Generic hardware method belongs to `hardware-dev-router`; MAROC-specific paths and packet/register meanings belong to the MAROC adapter skills.

## Route First

1. Read `C:/Users/Administrator/.codex/skills/hardware-dev-router/references/routing-table.md` for the generic work type.
2. Read `C:/Users/Administrator/.codex/skills/maroc-hardware-dev-router/references/routing-table.md` for the MAROC adapter.
3. Load the selected MAROC leaf skill for project-specific paths, scripts, and terminology.
4. Use `C:/Users/Administrator/.codex/skills/maroc-hardware-dev-router/references/resource-map.md` for MAROC paths and scripts.
5. Use `C:/Users/Administrator/.codex/skills/maroc-hardware-dev-router/references/evidence-boundaries.md` before making MAROC conclusions.

## Legacy Detail

The pre-split workflow is preserved in `references/legacy-full-workflow.md`. Load it only when a historical rule is needed and no newer leaf skill covers the detail.

## Asset Library

- Use `C:/Users/Administrator/.codex/skills/hardware-dev-router/references/asset-library.md` for the generic reusable asset policy.
- Use `C:/Users/Administrator/.codex/skills/maroc-hardware-dev-router/references/maroc-asset-map.md` for MAROC RTL, Qt host, PPT, Obsidian, XDC, and script asset routing.
- Do not attach new reusable source templates to this legacy skill; route them through the generic or MAROC leaf skill that owns the work type.

## Default Routing

- RTL review -> `maroc-fpga-rtl-code-review`
- XSim/TB/report inputs -> `maroc-fpga-testbench-simulation`
- ILA/Hardware Manager -> `maroc-fpga-ila-debug`
- CDC/reset/timing/XDC clocks -> `maroc-fpga-cdc-reset-timing`
- Parser/register/command map -> `maroc-fpga-register-command-parser`
- Vivado Tcl/build automation -> `maroc-fpga-vivado-tcl-automation`
- Qt host -> `maroc-qt-host-development`
- Host/RTL replay -> `maroc-host-rtl-alignment`
- RTL/schematic/XDC -> `maroc-rtl-schematic-xdc-alignment`
- Obsidian notes -> `maroc-obsidian-md-writing`
- PPT evidence -> `maroc-evidence-ppt-sync` plus a PPT scenario skill
