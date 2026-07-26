---
name: gf-plan
description: Plan Verilog/SystemVerilog FPGA features and subsystems before implementation. Use when Codex needs a decision-complete architecture covering module hierarchy, interfaces, clocks, resets, CDC, FSMs, pipelines, register maps, XDC responsibilities, verification, Vivado build stages, and acceptance criteria.
---

# FPGA Design Planner

Produce a decision-complete plan grounded in the current repository and target board. Do not generate RTL unless the user also requests implementation.

## Workflow

1. Inspect existing RTL, `.fpga-map`, XDC, Vivado Tcl/project files, schematics, part number, clocks, and interfaces.
2. Use `gf-architect` if the repository structure is not already mapped.
3. Lock functional requirements, throughput, latency, target frequency, resource constraints, external protocols, error behavior, and integration ownership.
4. Define module hierarchy, parameters, ports, ready/valid or bus semantics, clock/reset domains, CDC structures, FSMs, pipelines, buffering, register maps, and debug observability.
5. Separate physical XDC ownership from timing XDC ownership. Never propose a timing exception without a path-specific functional justification.
6. Define implementation phases with verification gates: lint/elaboration, unit simulation, CDC/reset review, integration simulation, synthesis, implementation, timing/DRC, and ILA or board bring-up where applicable.

## Required plan content

- Problem statement, success criteria, target device/tool version, and explicit assumptions.
- Mermaid block diagram and module tree.
- Interface/parameter tables with widths, direction, protocol, and ownership.
- Clock/reset table and CDC table with selected synchronization method.
- FSM state/transition tables and pipeline latency/backpressure behavior when applicable.
- Register map and command framing when applicable.
- XDC plan: package pins, IOSTANDARD/bank evidence, clocks, I/O delays, and separately reviewed exceptions.
- File-level implementation phases, dependencies, tests, and measurable acceptance criteria.

## Routing

- Existing code structure: `gf-architect`.
- RTL correctness: `fpga-rtl-code-review`.
- CDC/reset/timing: `fpga-cdc-reset-timing` and `vivado-constraints`.
- Simulation: `fpga-testbench-simulation`.
- Vivado build automation: `fpga-vivado-tcl-automation`.
- Board/RTL/XDC alignment: `rtl-schematic-xdc-alignment` or `fpga-orcad-xdc-pipeline`.

Read the matching file under `references/` only when the design needs its patterns. Read `references/upstream-provenance.md` when auditing or updating this adapted skill.
