---
name: maroc-fpga-ila-debug
description: "MAROC adapter for FPGA ILA debug. Use for MAROC Vivado Hardware Manager captures, config-chain ILA, trigger/upload ILA, TransmitOn/Ctest/ADC debug, read-probe captures, bit/ltx matching, CSV export, and board evidence packaging. Use fpga-ila-debug for the generic method."
---

# MAROC FPGA ILA Debug

## Workflow

1. Apply the generic `fpga-ila-debug` workflow first.
2. Record MAROC git state, bitstream, ltx, programmed board, host export bundle, and capture date.
3. Choose one MAROC role: raw USB, config/slow-control, trigger/control, upload/data, or read-probe.
4. Use MAROC Hardware Manager Tcl helpers from `maroc-hardware-dev-router/references/resource-map.md` when current for the selected bit/ltx.
5. Interpret captures with MAROC evidence boundaries. ILA cannot directly prove OUT_Q, OUT_FS, or analog behavior.

## Preferred Capture Order

Config chain -> trigger/control -> upload/data -> read-probe.

## Asset Library

- Read `C:/Users/Administrator/.codex/skills/maroc-hardware-dev-router/references/maroc-asset-map.md` for MAROC ILA and Hardware Manager routing.
- Use `C:/Users/Administrator/.codex/hardware-assets/source-refs/maroc-rtl-assets.md` to locate ILA scripts, bit/ltx-related notes, and capture helpers.
- Use `C:/Users/Administrator/.codex/hardware-assets/templates/vivado/ila_export_workflow_skeleton.tcl` as the reusable capture/export starting point.
- Use `C:/Users/Administrator/.codex/hardware-assets/hooks/maroc-hook-map.md` for `ila.capture.*` hooks such as `ila.capture.list`. Do not run live capture, arm, or programming hooks without explicit hardware confirmation.
