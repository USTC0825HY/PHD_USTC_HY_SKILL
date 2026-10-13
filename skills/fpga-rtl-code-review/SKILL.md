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

## Shared RTL contract

Read [the shared simple RTL contract](../fpga-rtl-development/references/simple-rtl-contract.md) for design simplicity and cycle-preserving changes. Review control ownership, unnecessary wrappers/states/parameters, arithmetic widths and timing-sensitive paths. Prefer concrete behavior risks over subjective line-count criticism. Review-only requests do not authorize edits; route requested implementation to `fpga-rtl-development`.

For new-project layout review, use [native project layout](../fpga-vivado-tcl-automation/references/native-project-layout.md): functional folders, one active source per file and separate simulation sources. Report legacy layout issues without moving files.

The linked contract is the sole shared formatting/simplification policy. Do not reload development merely to follow that reference; review findings do not authorize a rewrite or a build.

## Handoffs

- Use `fpga-cdc-reset-timing` for reset synchronizers, async FIFO, generated clocks, constraints, or timing closure.
- Use `fpga-testbench-simulation` when the question is best resolved by fixtures, waveforms, or checker coverage.
- Use `fpga-register-command-parser` for register fields, command words, packet tags, byte order, and parser ownership.

## Asset Library

- Use `<CODEX_HOME>/hardware-assets/templates/rtl/rtl_module_review_checklist.md` for reusable review structure.
- Treat project RTL as evidence, not as a generic template without adaptation.
