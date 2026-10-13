---
name: maroc-fpga-testbench-simulation
description: "MAROC adapter for FPGA testbench, XSim, fixture, and simulation-report workflow. Use for MAROC tb_top_maroc_command_usb, parser, slow-control, cy-driver, ADC/readout simulations, host export replay, case matrices, waveform grouping, PASS/FAIL rules, and Markdown simulation reports. Use fpga-testbench-simulation for the generic method."
---

# MAROC FPGA Testbench And Simulation

## Workflow

1. Apply the generic `fpga-testbench-simulation` workflow first.
2. Use MAROC TB, fixture, and script paths from `maroc-hardware-dev-router/references/resource-map.md`.
3. Choose the MAROC layer: `cy-driver`, `sim_parser`, `sim_sc829`, top-level config chain, ADC/readout, or host-export replay.
4. Preserve fixture provenance for `bits_829`, `register_mapping`, `packet_250`, `sw_packet_250`, and slow-control memories.
5. Keep XSim PASS as RTL-flow evidence, not board signoff.

## MAROC Rules

- Host-export bundles must be flattened before RTL replay.
- Slow-control correctness requires bit-level signoff when claiming 829bit behavior.
- Parser conclusions and slow-control serializer conclusions must remain separate.

## Asset Library

- Read `<CODEX_HOME>/skills/maroc-hardware-dev-router/references/maroc-asset-map.md` before selecting TB, fixture, XSim, or host-export assets.
- Use `<CODEX_HOME>/hardware-assets/source-refs/maroc-rtl-assets.md` to find MAROC testbenches, fixture bundles, and XSim scripts.
- Use `<CODEX_HOME>/hardware-assets/templates/rtl/tb_skeleton.v`, `fixture_manifest_template.md`, and `<CODEX_HOME>/hardware-assets/templates/vivado/xsim_run_wrapper_skeleton.ps1` for new reusable simulation scaffolds.
- Use `<CODEX_HOME>/hardware-assets/hooks/maroc-hook-map.md` for scenario hooks such as `rtl.sim.maroc.xsim`. Dry-run first and keep hook logs with the simulation report.
