---
name: hardware-datasheet-to-schematic
description: "Datasheet-to-schematic translation workflow. Use when converting ASIC, ADC, DAC, USB, clock, regulator, op-amp, connector, or reference-design requirements into schematic checks, pin mapping tables, bias/termination recommendations, and board-design review items."
---

# Hardware Datasheet To Schematic

## Workflow

1. Extract only the datasheet sections needed for the target circuit: absolute maximums, recommended operating conditions, pin functions, timing, reference circuits, and layout cautions.
2. Build a requirement table: parameter, datasheet source, schematic net/component, expected value, current value, and review status.
3. Mark assumptions that require user confirmation or measurement.
4. When mapping pins to FPGA or ASIC control signals, hand off to `rtl-schematic-xdc-alignment`.
5. Do not turn typical/reference values into mandatory requirements unless the datasheet says so.

## Outputs

Produce a checklist, pin/net mapping, discrepancy list, or schematic change recommendation with source page references.

## Handoffs

Use project-specific adapter skills only for local signal names, board revisions, or repository paths. MAROC-specific mapping belongs in `maroc-rtl-schematic-xdc-alignment`.

## Asset Library

- Use `C:/Users/Administrator/.codex/hardware-assets/templates/reports/rtl_xdc_schematic_alignment_table.md` when datasheet pins must be tied to RTL/XDC/schematic nets.
- Use project `source-refs/` files to locate prior datasheet-to-schematic notes and review artifacts.
