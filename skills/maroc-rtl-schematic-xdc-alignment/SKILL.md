---
name: maroc-rtl-schematic-xdc-alignment
description: "MAROC adapter for RTL-schematic-XDC alignment. Use when MAROC FPGA ports, XDC constraints, schematic nets, PCB connectors, IO standards, clock pins, debug pins, and board bring-up observations must be cross-checked. Use rtl-schematic-xdc-alignment for the generic method."
---

# MAROC RTL Schematic XDC Alignment

## Workflow

1. Apply the generic `rtl-schematic-xdc-alignment` workflow first.
2. Use MAROC paths from `maroc-hardware-dev-router/references/resource-map.md`: `xdc_auto/`, `fpga_xlsx/`, XDC review notes, and constraint builders.
3. Build the MAROC alignment table with RTL port, direction, owner, XDC pin, IO standard, schematic net, page/component, connector/test point, timing role, and evidence status.
4. Compare formal pins, debug pins, clocks, and USB-only smoke constraints separately.
5. Hand off measured board failures to `hardware-pcb-bringup-debug`.

## MAROC Boundaries

- MAROC XDC/schematic alignment proves intended digital connectivity and constraints.
- It does not prove SC pin activity, ADC upload, Ctest, OUT_Q, OUT_FS, or board-level behavior without matching measurement.

## Asset Library

- Read `C:/Users/Administrator/.codex/skills/maroc-hardware-dev-router/references/maroc-asset-map.md` for MAROC RTL, XDC, schematic-review, and board-debug asset routing.
- Use `C:/Users/Administrator/.codex/hardware-assets/source-refs/maroc-rtl-assets.md` and `source-refs/maroc-doc-assets.md` to locate XDC files, pin notes, and hardware review documents.
- Use `C:/Users/Administrator/.codex/hardware-assets/templates/reports/rtl_xdc_schematic_alignment_table.md` as the standard comparison table.
- Use `C:/Users/Administrator/.codex/hardware-assets/hooks/maroc-hook-map.md` for `xdc.review.maroc.port-map` and related XDC review hooks. Treat generated XDC artifacts as project-writing outputs unless directed otherwise.
