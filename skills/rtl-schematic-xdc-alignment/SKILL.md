---
name: rtl-schematic-xdc-alignment
description: "Generic RTL-schematic-XDC alignment and FPGA control-chain workflow. Use when top-level ports, active XDC PACKAGE_PIN/IOSTANDARD, FPGA PST balls, on-board control devices, backplane connectors, child-board devices, return signals, IO banks, clocks, resets, or debug pins must be cross-checked without guessing connectivity."
---

# RTL Schematic XDC Alignment

## Workflow

For multi-board paths read the [shared trace/evidence method](../fpga-board-signal-chain-closure/references/trace-and-evidence-method.md). Keep endpoint identity, connector mapping, assembly and evidence dimensions in that closure record; add RTL/XDC fields here rather than maintaining a second route conclusion.

1. Read `references/fpga-control-chain.md` for FPGA-to-device and cross-board control tracing.
2. Verify the active XPR top, part, source set, constraint set, XDC membership, and `AutoDisabled` state before using RTL or XDC.
3. Start with a table: RTL port, direction, module owner, active XDC expression, PACKAGE_PIN, IOSTANDARD, FPGA refdes/ball, PST net, conditioning device, connector chain, target device, and evidence status.
4. Run `scripts/run_rtl_xdc_pst_audit.ps1` for static top/XDC/FPGA-ball checks.
   Read [audit helper usage](../fpga-vivado-tcl-automation/references/audit-helper-usage.md) for project-derived input selection, selected-port coverage, dictionary syntax, dedicated-pad evidence and unsupported syntax. Zero parsed constraints or unresolved widths are not PASS.
5. Use `fpga-orcad-xdc-pipeline` to query both sides of intermediate parts and every board connector. Do not merge cross-board nets automatically.
6. Compare formal pins, debug pins, clocks, resets, control outputs, and return inputs separately.
7. Flag mismatches as naming mismatch, direction mismatch, pin mismatch, duplicate LOC, missing IOSTANDARD, voltage-standard risk, timing gap, missing constraint, schematic ambiguity, incomplete board evidence, or debug-only exception.
8. When a current synthesis run exists, execute `vivado_io_audit.tcl` read-only. Do not launch synthesis implicitly.
9. Hand off measured board failures to `hardware-pcb-bringup-debug`.

## Boundaries

Schematic and XDC alignment proves intended digital connectivity and constraints. It does not prove that a signal toggled or met analog requirements on hardware.

Use `RTL/XDC静态核查完成，Vivado应用状态未复核` whenever no current Vivado run was actually opened and reviewed.

## Asset Library

- Use `<CODEX_HOME>/hardware-assets/templates/reports/rtl_xdc_schematic_alignment_table.md` for the alignment table.
- Use project `source-refs/` files to locate RTL ports, XDC files, schematic inputs, and board connector notes.
