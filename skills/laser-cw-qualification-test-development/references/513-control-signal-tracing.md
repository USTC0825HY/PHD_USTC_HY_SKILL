# 513 multi-board chain adapter

This file contains only 513 project bindings and priorities. Read and follow `fpga-board-signal-chain-closure` for the reusable topology, evidence, connector, electrical-availability, power-chain, and output rules.

## Inputs

- Board registry: `references/513-board-registry.json`
- Current XPR/XDC/top and hardware root: `project-authority.md`
- Default FPGA refdes: `D1`, unless the selected SZSD evidence proves otherwise
- AD677 candidate groups and forbidden identity inference: `evidence-and-pin-policy.md`

Run the generic preflight with the registry before tracing an individual net. A board with no selected PST remains in the graph as E0 and cannot support a board-local net claim.

## Board identities

- `SZSD`: FPGA master/controller.
- `BASE`: shared bottom-board interconnect; all declared cross-board paths in this adapter traverse it.
- `POWER`: power source/module board.
- `YCQD`: delay-drive board.
- `PZ`: frequency-synthesis board, bound to folder `3.频综板PCB评审文件（公开）`; it is not the lock-drive board.
- `LASER_DRIVE`, `TEMP_CONTROL`, `LOCK_DRIVE`, `ERROR_DETECT`, and `OTHER_LOADS`: power or signal loads with the evidence status recorded in the registry.

## Critical chains

Control and functional paths:

```text
SZSD -> BASE -> POWER
SZSD -> BASE -> YCQD
SZSD -> BASE -> PZ
YCQD -> BASE -> PZ
```

Power distribution paths:

```text
POWER -> BASE -> PZ
POWER -> BASE -> LASER_DRIVE
POWER -> BASE -> TEMP_CONTROL
POWER -> BASE -> LOCK_DRIVE
POWER -> BASE -> ERROR_DETECT
POWER -> BASE -> OTHER_LOADS
```

Trace each destination branch independently. `POWER -> BASE` does not prove any `BASE -> load` branch. Keep power rails and return grounds separate from FPGA enable, fault, telemetry, and status signals.

## Current evidence caveats

- Selected SZSD evidence has DSN/PST but no PDF; its alternate CW public set has PDF/PST but no DSN. Do not merge them.
- Selected YCQD public evidence is complete; the internal delay-drive set is an alternative and remains unselected.
- PZ and temperature-control evidence are review/PDF-level only.
- Lock-drive evidence is Altium SchDoc/PcbDoc without PST.
- Error-detection evidence has DSN but no PST.
- Laser-drive and other-load nodes are currently unbound E0 placeholders.

For any chain without a complete selected PST set, stop exact net tracing at the last confirmed connector and report the missing evidence or required continuity check.
