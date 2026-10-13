---
name: fpga-cdc-reset-timing
description: "Generic FPGA CDC, reset, and timing closure workflow. Use for clock-domain crossings, reset assertion/deassertion, async FIFO use, generated clocks, timing reports, XDC/SDC constraints, false/multicycle paths, IO clocks, and bring-up timing risks."
---

# FPGA CDC Reset Timing

## Workflow

1. Identify every clock: external input clocks, PLL/MMCM outputs, divided clocks, bus clocks, recovered clocks, and testbench simplifications.
2. Mark each data/control crossing and classify it as single-bit sync, pulse handshake, async FIFO, gray counter, dual-clock RAM, or unsafe multi-bit transfer.
3. Check reset assertion and deassertion per domain, including reset release order and state-machine readiness.
4. Compare RTL clocks with constraint files and timing reports before proposing changes.
5. Never use broad false paths or smoke overrides to hide CDC/timing failures. Every formal exception needs path-specific functional justification. Diagnostic exceptions, if explicitly requested, stay isolated and cannot support formal acceptance.
6. Read [timing acceptance](references/timing-acceptance.md) before a closure claim. Multi-bit configuration needs coherency, pulses need event delivery and reset release needs per-domain analysis; independent bit synchronizers are not a bus protocol.

## Outputs

Produce a CDC/reset/timing risk table with source domain, destination domain, signal group, mechanism, evidence, risk, and required fix or constraint.

## Asset Library

- Use `<CODEX_HOME>/hardware-assets/templates/rtl/cdc_reset_timing_checklist.md` for CDC/reset/timing review structure.
- Use project `source-refs/` files to locate XDC, timing notes, and build reports before making closure claims.
