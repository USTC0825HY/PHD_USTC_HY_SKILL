---
name: fpga-ila-debug
description: "Generic FPGA ILA/on-chip debug workflow. Use for Vivado ILA/VIO captures, trigger planning, probe selection, bitstream/LTX matching, Hardware Manager Tcl, CSV export, waveform interpretation, and packaging FPGA internal evidence without overclaiming board or analog behavior."
---

# FPGA ILA Debug

## Select the requested stage

1. **Plan/insert probes:** inspect signal widths, domains, trigger purpose and available sample clock. BIT/LTX or a connected board is not required. MARK_DEBUG preserves/selects nets; it does not itself instantiate an ILA. Keep asynchronous raw signals separate from synchronized system-domain observations; a stopped measured clock cannot sustain its ILA capture. Insertion requires an edit request, not merely a request for a signal list.
2. **Build/offline audit:** compare RTL/IP probe order and widths with the selected synthesis/implementation and matching BIT/LTX. Check ILA/VIO and debug-hub clocks. Inspect existing artifacts read-only; do not build simply to answer a review question.
3. **Live capture:** record image/probe identity, device, board state, trigger and date. Verify the programmed image before trusting waveforms. Use project Hardware Manager helpers after inspecting their side effects. Programming, arming and live capture require current authorization.

ILA proves internal FPGA activity for that image and trigger condition, not external analog behavior or pin accuracy by itself.

## Outputs

Deliver only the requested stage's evidence: a probe/trigger table for planning; contract and clock findings for offline audit; matched BIT/LTX, capture/export, observations and limitations for live capture.

## Asset Library

- Use `<CODEX_HOME>/hardware-assets/templates/vivado/ila_export_workflow_skeleton.tcl` for a generic Hardware Manager export starting point.
- Use project `source-refs/` files to find existing ILA trigger presets, wave groups, and CSV export scripts.
- Read ILA automation before running it. Listing saved data may be read-only; programming, arming, live capture, and live CSV export are hardware operations unless proven otherwise.
