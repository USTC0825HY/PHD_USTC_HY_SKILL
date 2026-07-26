---
name: fpga-ila-debug
description: "Generic FPGA ILA/on-chip debug workflow. Use for Vivado ILA/VIO captures, trigger planning, probe selection, bitstream/LTX matching, Hardware Manager Tcl, CSV export, waveform interpretation, and packaging FPGA internal evidence without overclaiming board or analog behavior."
---

# FPGA ILA Debug

## Workflow

1. Record repository revision, build output, bitstream, LTX/probe file, board state, capture date, and programmed device.
2. Verify each debug signal is connected in RTL and present in the active probe file before trusting the waveform.
3. Choose one capture role at a time: transport, parser, register/control, serializer, trigger/control, acquisition/readout, memory, or debug probe.
4. Use project Hardware Manager Tcl helpers when present; otherwise keep capture, upload, and CSV export steps explicit.
5. Interpret captures using evidence boundaries. ILA proves internal FPGA activity for that image and trigger condition, not external analog behavior by itself.

## Outputs

Produce a capture plan, trigger condition, probe list, bit/ltx check, CSV/export path, observed fact, allowed conclusion, and next action.

## Asset Library

- Use `C:/Users/Administrator/.codex/hardware-assets/templates/vivado/ila_export_workflow_skeleton.tcl` for a generic Hardware Manager export starting point.
- Use project `source-refs/` files to find existing ILA trigger presets, wave groups, and CSV export scripts.
- Use `C:/Users/Administrator/.codex/hardware-assets/hooks/hardware-hook-registry.yaml` for `ila.capture.*` hooks. Listing or inspecting may be read-only; programming, arming, live capture, and live CSV export are hardware operations unless proven otherwise.
