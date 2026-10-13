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

- Use independent expected values/models or cycle-by-cycle pre/post comparison. Cover applicable arithmetic boundaries, continuous/busy requests, backpressure, reset interruption, stop and restart; simplification must preserve latency and throughput as well as values.
- Require actual checks, an explicit PASS/FAIL result and watchdog timeout. Inject a known error when creating/changing a checker or wrapper; reuse that validation for unchanged infrastructure. A zero exit or completion alone is not PASS. Wrappers must reject FAIL, timeout, zero checks and missing actual simulator PASS; a parent-script echo is insufficient.
- For new projects read [native layout](../fpga-vivado-tcl-automation/references/native-project-layout.md): TB/fixtures in sim_1 functional folders, never synthesis sources. Run standalone simulators in a dedicated run directory, not the project root. Do not migrate existing projects automatically.

- A passing simulation proves behavior only inside the modeled DUT, fixture, and timing assumptions.
- Same-clock or simplified testbenches can hide CDC and board timing failures.
- Host-export replay must preserve provenance: original export, flattening/packing transform, fixture hash/count, parser input, and checker result.

## Asset Library

- Use `<CODEX_HOME>/hardware-assets/templates/rtl/tb_skeleton.v` for a minimal testbench starting point.
- Use `<CODEX_HOME>/hardware-assets/templates/rtl/fixture_manifest_template.md` for fixture provenance.
- Use project `source-refs/` files to find existing TBs, fixtures, replay scripts, and run wrappers.
- Read simulation wrappers before running them and use dry-run behavior when available. Simulation proves only modeled DUT behavior.
- The shared XSim wrapper requires a fresh run directory and a simulator transcript inside it (`-TranscriptPath`, default `xsim.log`), with one `TB_PASS checks=N` where N>0. Set `-TimeoutSeconds` for longer tests (default 600). See [audit helper usage](../fpga-vivado-tcl-automation/references/audit-helper-usage.md) for runtime and evidence boundaries.
