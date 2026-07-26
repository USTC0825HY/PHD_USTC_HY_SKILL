---
name: rtl-schematic-xdc-alignment
description: "Generic RTL-schematic-XDC alignment workflow. Use when FPGA ports, XDC constraints, schematic nets, PCB connectors, IO banks, voltage standards, clock pins, reset pins, debug pins, and board bring-up observations must be cross-checked."
---

# RTL Schematic XDC Alignment

## Workflow

1. Start with a table: RTL port, direction, module owner, constraint pin, IO standard, schematic net, page/component, board connector/test point, timing role, and evidence status.
2. Inspect current RTL top-level ports, constraint files, schematic source, board revision, and any generated port/pin maps.
3. Compare formal pins, debug pins, clocks, resets, and smoke constraints separately.
4. Flag mismatches as naming mismatch, direction mismatch, pin mismatch, voltage-standard risk, timing gap, missing constraint, schematic ambiguity, or debug-only exception.
5. Hand off measured board failures to `hardware-pcb-bringup-debug`.

## Boundaries

Schematic and XDC alignment proves intended digital connectivity and constraints. It does not prove that a signal toggled or met analog requirements on hardware.

## Asset Library

- Use `C:/Users/Administrator/.codex/hardware-assets/templates/reports/rtl_xdc_schematic_alignment_table.md` for the alignment table.
- Use project `source-refs/` files to locate RTL ports, XDC files, schematic inputs, and board connector notes.
