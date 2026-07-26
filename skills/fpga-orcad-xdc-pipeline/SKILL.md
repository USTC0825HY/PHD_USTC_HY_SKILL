---
name: fpga-orcad-xdc-pipeline
description: Extract and audit FPGA I/O connectivity from OrCAD Capture/Allegro PST netlists and controlled CSV exports, then generate deterministic physical XDC and RTL/XDC/schematic alignment reports. Use for .DSN projects after native netlist export, pstxnet.dat/pstxprt.dat/pstxprp.dat, FPGA pin maps, bank/VCCO/IOSTANDARD review, top-level Verilog/SystemVerilog port alignment, and Vivado 2022.2 I/O validation.
---

# FPGA OrCAD to XDC Pipeline

Use a native OrCAD export; never parse binary `.DSN` directly. Keep the original schematic and netlist in place and write generated artifacts to a staging directory.

## Workflow

1. Read `references/orcad-export.md` and export `pstxnet.dat`; retain `pstxprt.dat` and `pstxprp.dat` when available.
2. Identify the FPGA reference designator and exact AMD/Xilinx part/package from schematic and BOM evidence.
3. Create a draft map:

```powershell
& scripts/run_orcad_xdc_pipeline.ps1 extract-netlist --pstxnet C:\path\pstxnet.dat --fpga-refdes U1 --schematic C:\path\board.dsn --part xc7a35tcsg324-1 --output C:\staging\fpga_io_map.yaml
```

4. Review every row against the schematic, FPGA package data, bank VCCO, interface datasheet, and top RTL. Use `assets/fpga_io_map.template.yaml` and `references/schema.md`.
5. Set a row to `verified` only when package pin, RTL port/direction, IOSTANDARD, bank/VCCO, role, and evidence are complete. Use `waived` only with an explicit reason. Leave all other rows `needs_review`.
6. Validate and generate:

```powershell
& scripts/run_orcad_xdc_pipeline.ps1 validate --map C:\staging\fpga_io_map.yaml --rtl C:\repo\rtl\top.sv
& scripts/run_orcad_xdc_pipeline.ps1 generate --map C:\staging\fpga_io_map.yaml --rtl C:\repo\rtl\top.sv --output-dir C:\staging\generated
& scripts/run_io_gen.ps1 --validate-only C:\staging\generated\io_gen_input.yaml --top fpga_top
```

7. Review `pins.xdc`, `io_alignment_report.md`, and the inactive `timing.xdc` template. Do not copy them into the project until validation passes.
8. Run Vivado checks from `references/vivado-validation.md` when RTL, part, and source order are available.

## Hard safety rules

- Generate only `PACKAGE_PIN`, `IOSTANDARD`, and explicitly supplied `DRIVE`, `SLEW`, or `PULLTYPE` properties.
- Never generate `create_clock`, I/O delay, false path, multicycle path, clock groups, max/min delay, or bus skew from net names.
- Reject duplicate physical pins, duplicate RTL ports, incompatible Bank VCCO/IOSTANDARD, unknown verified voltage standards, incomplete evidence, or remaining `needs_review` rows.
- Do not treat schematic connectivity as proof of electrical activity or timing closure.
- Treat `io-gen` output as a generated-wrapper option; preserve the audited `pins.xdc` as the direct top-port physical constraint source.

## Outputs

- `fpga_io_map.yaml`: auditable source of truth.
- `pins.xdc`: direct physical constraints for verified top ports.
- `timing.xdc`: comments and review placeholders only; no active timing constraints.
- `io_alignment_report.md`: schematic/netlist/RTL/XDC evidence and mismatches.
- `io_gen_input.yaml`: deterministic io-gen input for validation or wrapper generation.
- `validation.json`: machine-readable errors and warnings.

Read `references/evidence-policy.md` before making technical claims and `references/provenance.md` when auditing dependencies.
