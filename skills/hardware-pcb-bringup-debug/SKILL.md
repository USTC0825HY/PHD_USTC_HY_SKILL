---
name: hardware-pcb-bringup-debug
description: "Generic PCB bring-up and hardware debug workflow. Use for power-up sequencing, current draw, clock/reset checks, USB/JTAG enumeration, FPGA programming, ILA/on-chip smoke tests, oscilloscope or logic-analyzer probing, board-level fault isolation, and packaging measured evidence for FPGA/ASIC/MCU/instrument boards."
---

# Hardware PCB Bring-Up Debug

## Workflow

1. Establish safety limits, board revision, power rails, current limit, programmed bit/ltx, and instrument setup.
2. Bring up in layers: power, clocks, resets, JTAG, USB, FPGA smoke, configuration chain, trigger/acquisition, upload/readout, analog probe.
3. Capture evidence at every layer: photos, screenshots, ILA CSV, oscilloscope settings, host logs, and repo/build identifiers.
4. Stop and classify when a layer fails; do not debug downstream behavior until the upstream layer is proven.
5. Write conclusions with explicit proof and remaining boundary.

## Evidence Rules

- Current increase is supporting evidence, not chip behavior signoff.
- ILA/on-chip debug cannot directly prove external analog waveforms.
- Configuration-chain success does not imply acquisition, ADC, upload, or analog-path success unless each layer has evidence.
- Use project-specific adapter skills only for local board names, register fields, packet formats, or established lab procedures.

## Asset Library

- Use `C:/Users/Administrator/.codex/hardware-assets/templates/reports/board_bringup_log_template.md` for layered bring-up notes.
- Use `C:/Users/Administrator/.codex/hardware-assets/templates/reports/claim_table_template.md` before converting lab results into report claims.
- Use project `source-refs/` files to locate board logs, ILA/scope evidence, and PPT/MD reporting examples.
