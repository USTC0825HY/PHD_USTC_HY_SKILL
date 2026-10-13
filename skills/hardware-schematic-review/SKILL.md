---
name: hardware-schematic-review
description: "Generic hardware schematic review workflow for mixed digital/analog FPGA, ASIC, MCU, instrument, and carrier boards. Use when reviewing power, clocks, resets, connectors, analog front ends, FPGA IO banks, USB/JTAG, signal direction, pullups, termination, protection, and design-rule risks in schematics."
---

# Hardware Schematic Review

## Workflow

1. Identify board revision, schematic source, page, net names, components, and intended test objective.
2. Review by subsystem: power, clocks, reset, USB/JTAG, FPGA IO banks, ASIC control pins, analog input/probe path, connectors, and test points.
3. For each issue, record page/net/component, expected behavior, observed mismatch, risk, and verification method.
4. Cross-check FPGA-connected nets against XDC and RTL when the board drives or receives FPGA signals.
5. Separate schematic intent from board-measured behavior.

## Handoffs

Use `rtl-schematic-xdc-alignment` when a schematic signal must match FPGA RTL and constraints. Use `hardware-pcb-bringup-debug` when the question is about measured board behavior. Use project-specific adapters, such as `maroc-rtl-schematic-xdc-alignment`, only for local paths, names, and board conventions.

## Asset Library

- Use `<CODEX_HOME>/hardware-assets/templates/reports/rtl_xdc_schematic_alignment_table.md` when FPGA-connected schematic nets need RTL/XDC correlation.
- Use project `source-refs/` files to locate schematic review notes, XDC inputs, and board documentation.
