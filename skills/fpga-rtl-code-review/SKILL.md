---
name: fpga-rtl-code-review
description: "Generic FPGA RTL code-review workflow. Use when reviewing Verilog, VHDL, or SystemVerilog modules for responsibilities, state machines, handshakes, resets, counters, muxing, interfaces, debug nets, register access, test coverage, and implementation risk before editing or signoff."
---

# FPGA RTL Code Review

## Workflow

1. Read current RTL and constraints, not only notes.
2. Identify the module boundary: transport, parser, register/control, serializer, acquisition, upload/readout, memory, debug, or top-level integration.
3. Review reset behavior, clock-domain assumptions, valid/data handshakes, state exit conditions, counters, backpressure, muxing, and debug-net wiring.
4. Check whether an existing testbench covers the module and whether that testbench models board-relevant timing.
5. Report findings in code-review style: severity, file/line, behavior risk, evidence, and minimal fix direction.

## Handoffs

- Use `fpga-cdc-reset-timing` for reset synchronizers, async FIFO, generated clocks, constraints, or timing closure.
- Use `fpga-testbench-simulation` when the question is best resolved by fixtures, waveforms, or checker coverage.
- Use `fpga-register-command-parser` for register fields, command words, packet tags, byte order, and parser ownership.

## Asset Library

- Use `C:/Users/Administrator/.codex/hardware-assets/templates/rtl/rtl_module_review_checklist.md` for reusable review structure.
- Use `C:/Users/Administrator/.codex/hardware-assets/catalogs/hardware-assets-index.yaml` or project `source-refs/` files to find RTL examples; do not treat project RTL as a generic template without adaptation.
