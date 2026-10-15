---
name: fpga-orcad-xdc-pipeline
description: Extract, query, and audit FPGA and board connectivity from OrCAD Capture/Allegro PST netlists, inventory DSN/PDF/PST evidence sets, trace networks through parts and connectors without guessing cross-board continuity, and generate deterministic physical XDC alignment artifacts. Use for pstxnet.dat/pstxprt.dat/pstchip.dat, network or refdes-pin lookup, FPGA pin maps, board/backplane/child-board signal tracing, assembly-option review, RTL/XDC alignment, and Vivado I/O validation.
---

# FPGA OrCAD to XDC Pipeline

Before consuming profile-derived inputs, read [path validation](../hardware-dev-router/references/profile-path-resolution.md) and run its read-only validator for the required keys only (or validate an explicit task path). Missing inputs stop dependent work; do not create obsolete directories or guess replacement campaigns. Keep existing CLI/environment overrides ahead of profile defaults.

Use a native OrCAD export; never parse binary `.DSN` directly. Keep the original schematic and netlist in place and write generated artifacts to a staging directory.

Read `<CODEX_HOME>/laser-fpga-profile.json` for the installed OrCAD, Vivado, and data-root paths. Resolve `<CODEX_HOME>` from the environment, falling back to the current user's `.codex` directory. The wrappers locate the pinned `io-gen` environment below `<CODEX_HOME>/tools/io-gen-c852b04`.

## Workflow

For a multi-board task use the shared [trace/evidence method](../fpga-board-signal-chain-closure/references/trace-and-evidence-method.md). This skill owns exact PST lookup, not automatic cross-board joining. An isolated query does not need a system report.

1. Read `references/orcad-export.md` and export `pstxnet.dat`; retain `pstxprt.dat`, `pstchip.dat`, and `pstxprp.dat` when available.
2. For signal lookup or cross-board tracing, read `references/signal-tracing.md`, inventory the hardware root, and select one version-consistent DSN/PDF/PST evidence set per board.
3. Query exact networks or device pins before drafting any connection chain:

```powershell
& scripts/run_pst_signal_trace.ps1 inventory --root C:\hardware --format json
& scripts/run_pst_signal_trace.ps1 query --pst-dir C:\board\allegro --net ADG526_EN
& scripts/run_pst_signal_trace.ps1 query --pst-dir C:\board\allegro --node D39.2
& scripts/run_pst_signal_trace.ps1 multi-query --board SZSD=C:\szsd --board Backplane=C:\backplane --net ADG526_EN
```

4. Keep series-component nets separate, resolve part/value/`TSD*`, stop confirmed claims at connectors, and join boards only with explicit mapping evidence.
5. For FPGA-to-XDC generation, identify the FPGA reference designator and exact AMD/Xilinx part/package from schematic and BOM evidence.
6. Create a draft map:

```powershell
& scripts/run_orcad_xdc_pipeline.ps1 extract-netlist --pstxnet C:\path\pstxnet.dat --fpga-refdes U1 --schematic C:\path\board.dsn --part xc7a35tcsg324-1 --output C:\staging\fpga_io_map.yaml
```

7. Review every row against the schematic, FPGA package data, bank VCCO, interface datasheet, and top RTL. Use `assets/fpga_io_map.template.yaml` and `references/schema.md`.
8. Set a row to `verified` only when package pin, RTL port/direction, IOSTANDARD, bank/VCCO, role, and evidence are complete. Use `waived` only with an explicit reason. Leave all other rows `needs_review`.
9. Validate and generate:

```powershell
& scripts/run_orcad_xdc_pipeline.ps1 validate --map C:\staging\fpga_io_map.yaml --rtl C:\repo\rtl\top.sv
& scripts/run_orcad_xdc_pipeline.ps1 generate --map C:\staging\fpga_io_map.yaml --rtl C:\repo\rtl\top.sv --output-dir C:\staging\generated
& scripts/run_io_gen.ps1 --validate-only C:\staging\generated\io_gen_input.yaml --top fpga_top
```

10. Review `pins.xdc`, `io_alignment_report.md`, and the inactive `timing.xdc` template. Do not copy them into the project until validation passes.
11. Run Vivado checks from `references/vivado-validation.md` when RTL, part, and source order are available.

## Hard safety rules

- Generate only `PACKAGE_PIN`, `IOSTANDARD`, and explicitly supplied `DRIVE`, `SLEW`, or `PULLTYPE` properties.
- Never generate `create_clock`, I/O delay, false path, multicycle path, clock groups, max/min delay, or bus skew from net names.
- Reject duplicate physical pins, duplicate RTL ports, incompatible Bank VCCO/IOSTANDARD, unknown verified voltage standards, incomplete evidence, or remaining `needs_review` rows.
- Do not treat schematic connectivity as proof of electrical activity or timing closure.
- Do not infer cross-board continuity from equal connector pin numbers, similar net names, or device numbering.
- Preserve TSD/DNP as source markers. PST alone cannot establish current fitted state; scoped assembly confirmation is recorded by the closure layer without erasing the marker.
- Treat `io-gen` output as a generated-wrapper option; preserve the audited `pins.xdc` as the direct top-port physical constraint source.

## Outputs

- `fpga_io_map.yaml`: auditable source of truth.
- `pins.xdc`: direct physical constraints for verified top ports.
- `timing.xdc`: comments and review placeholders only; no active timing constraints.
- `io_alignment_report.md`: schematic/netlist/RTL/XDC evidence and mismatches.
- `io_gen_input.yaml`: deterministic io-gen input for validation or wrapper generation.
- `validation.json`: machine-readable errors and warnings.

Read `references/evidence-policy.md` before making technical claims and `references/provenance.md` when auditing dependencies.
