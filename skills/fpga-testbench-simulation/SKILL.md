---
name: fpga-testbench-simulation
description: "Generic FPGA testbench and simulation workflow. Use for writing, running, debugging, or reporting Verilog/VHDL/SystemVerilog simulations, fixtures, host-export replay, checker rules, waveform grouping, case matrices, XSim/Questa/iverilog flows, and simulation evidence boundaries."
---

# FPGA Testbench And Simulation

## Workflow

1. Choose the verification layer: unit, parser, register/control, serializer, bus/transport, top-level integration, acquisition/readout, or host-export replay.
2. Read the testbench, DUT files, run script, fixture files, generated data, and latest logs before changing conclusions.
3. Classify failures as compile, elaborate, fixture/runtime, checker, or actual DUT behavior.
4. Prefer existing project scripts and manifests over inventing parallel flows.
5. For reports, state module boundary, signal chain, fixture source, case matrix, expected behavior, observed result, checker method, and unsupported claims.

## Evidence Rules

- A passing simulation proves behavior only inside the modeled DUT, fixture, and timing assumptions.
- Same-clock or simplified testbenches can hide CDC and board timing failures.
- Host-export replay must preserve provenance: original export, flattening/packing transform, fixture hash/count, parser input, and checker result.

## Asset Library

- Use `C:/Users/Administrator/.codex/hardware-assets/templates/rtl/tb_skeleton.v` for a minimal testbench starting point.
- Use `C:/Users/Administrator/.codex/hardware-assets/templates/rtl/fixture_manifest_template.md` for fixture provenance.
- Use project `source-refs/` files to find existing TBs, fixtures, replay scripts, and run wrappers.
- Use `C:/Users/Administrator/.codex/hardware-assets/hooks/hardware-hook-registry.yaml` for `rtl.fixture.*` and `rtl.sim.*` hooks. Dry-run first; simulation hooks prove only modeled DUT behavior.
