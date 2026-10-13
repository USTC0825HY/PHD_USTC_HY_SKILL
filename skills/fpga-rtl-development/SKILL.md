---
name: fpga-rtl-development
description: "Write, adapt or simplify hand-written FPGA RTL in the project's HDL and tool version. Use for implementing modules or removing unnecessary design complexity while preserving cycle-level interfaces. For review-only requests use fpga-rtl-code-review."
---

# FPGA RTL Development

1. Read nearest project rules, current sources, XPR/configuration and tests. Establish the active source, frozen/vendor boundaries, HDL dialect and authorized stages; do not edit an installed/generated copy instead of the source.
2. Read [simple RTL contract](references/simple-rtl-contract.md). For a small change, record the function, clock/reset, widths, handshake/latency and boundary tests briefly; use `gf-plan` only when architecture decisions require it.
3. For new projects read [native project layout](../fpga-vivado-tcl-automation/references/native-project-layout.md). Place each source directly in its final functional folder. Existing project layout is not migration permission.
4. Implement the smallest clear design meeting the contract. Explain any added module, state, register, parameter or pipeline by a real responsibility, reuse or timing need; do not create speculative frameworks.
5. Use existing verification entrypoints. Compare externally observable values and cycle timing, including reset, boundaries, busy/backpressure and stop behavior. State checks actually run, failures and untested conditions.
6. Self-check the changed behavior against the contract. Load `fpga-rtl-code-review` for a requested/separate review or substantial review risk, `fpga-cdc-reset-timing` for affected crossings/reset/timing, and `fpga-testbench-simulation` for simulation work. Do not recursively load every handoff skill. Static review or simulation is not routed timing or board acceptance.

Default simplification preserves ports, parameter semantics, latency, throughput, handshakes and reset behavior. Explain and obtain authorization for a contract change beyond the user's request; an explicitly requested change is already authorized. Do not remove required pipeline/CDC/FIFO protections to reduce line count.
