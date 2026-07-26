---
name: maroc-fpga-rtl-code-review
description: "MAROC adapter for FPGA RTL code review. Use when reviewing MAROC Verilog modules such as TOP_MAROC.v, CY_driver_new.v, maroc_usb_packet_parser.v, SlowControl_MAROC.v, command_MAROC.v, auto_mode_MAROC.v, data_socket_MAROC.v, and read-probe logic. Use fpga-rtl-code-review for the generic method."
---

# MAROC FPGA RTL Code Review

## Workflow

1. Apply the generic `fpga-rtl-code-review` workflow first.
2. Load MAROC paths from `maroc-hardware-dev-router/references/resource-map.md`.
3. Identify the MAROC module boundary: USB, parser, command, slow-control, trigger/acquisition, upload, read-probe, or debug support.
4. Review MAROC-specific contracts: `CY_driver_new` owns FX2 ingress/egress, `maroc_usb_packet_parser` owns packet validation and tag stripping, `SlowControl_MAROC` owns SC pin sequencing, and `command_MAROC` is legacy/manual unless promoted.
5. Report findings with file/line, behavior risk, evidence, and minimal fix direction.

## Handoffs

Use `maroc-fpga-cdc-reset-timing` for CDC/reset/timing closure, and `maroc-fpga-testbench-simulation` when fixture or XSim proof is required.

## Asset Library

- Read `C:/Users/Administrator/.codex/skills/maroc-hardware-dev-router/references/maroc-asset-map.md` for MAROC RTL module and review-template routing.
- Use `C:/Users/Administrator/.codex/hardware-assets/source-refs/maroc-rtl-assets.md` to locate current RTL modules and representative snapshots.
- Use `C:/Users/Administrator/.codex/hardware-assets/templates/rtl/rtl_module_review_checklist.md` as the reusable review structure.
