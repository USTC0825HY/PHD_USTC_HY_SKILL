# Implementation scope

## Current project boundary

- Resolve the selected target's actual top module, source, part/tool version and active XDC from its current XPR. `AD677_IO_DDS_TOP` is a historical mother-project identity, not a universal CW top.
- Preserve unrelated test functions and modules unless the user explicitly places them in scope.
- Do not hand-edit XPR XML or generated IP state.

## Multi-board boundary

- Use `references/513-board-registry.json` as the 513 physical-board/evidence mapping and the
  generic `fpga-board-signal-chain-closure` skill for graph traversal.
- Treat SZSD as the FPGA carrier and BASE as the common interconnect, not as a generic fixed
  three-board chain. A route may begin at POWER or YCQD and pass through BASE to another load.
- Keep PZ/frequency synthesis separate from LOCK_DRIVE/ultra-stable lock drive.
- Select exactly one evidence set per physical board. Never mix public/internal or revision
  variants within one trace unless a conflict record explicitly documents the reconciliation.
- Close every cross-board edge with connector contacts on both sides and BASE evidence. Preserve
  net renames per connector pin instead of joining same-name nets automatically.
- Record translator channel, A/B side, DIR, OE, fixed pulls, assembly resistors, DNP/NC/TSD*, and
  disabled branches. A D120-like branch held disabled by OE is `电气不可用`, not merely optional.

## Signal and power semantics

- `fpga_control` and `status_return` chains require RTL direction, active XDC PACKAGE_PIN and
  IOSTANDARD, and Vivado `report_io` when a valid synthesized design is available.
- `board_signal` and `clock_reference` require electrical direction/source/load and connector
  closure, but only require RTL/XDC when an FPGA endpoint actually exists.
- `power_rail` records source voltage, return ground, protection, switch, filter, connectors, and
  load endpoint. The rail itself does not require RTL/XDC.
- Power-enable controls and power-good/fault returns are separate `fpga_control` or
  `status_return` chains and receive full FPGA alignment checks.

## Output and mutation boundary

- Report evidence level, conflicts, unclosed points, and physical checks separately.
- Distinguish required control, hardware default, optional function, and status output.
- Static parsing and read-only inspection of an existing synthesis result are allowed.
- Do not launch synthesis, implementation, bitstream generation, programming, or modify user
  FPGA/schematic/PST/PDF/SchDoc data unless separately requested.
- If no valid synthesis result is reviewed, state `RTL/XDC静态核查完成，Vivado应用状态未复核`.
