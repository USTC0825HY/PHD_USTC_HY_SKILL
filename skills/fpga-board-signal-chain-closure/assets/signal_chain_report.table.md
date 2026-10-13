# Multi-board signal-chain closure report

## Input authority

| Item | Selected source | Version/hash/time | Completeness | Notes |
|---|---|---|---|---|
| XPR |  |  |  | actual fileset/top/part |
| Active XDC |  |  |  | `UsedIn` and disabled state |
| Board registry |  |  |  | schema v2 |

## Physical boards and evidence sets

| Board ID | Role | Selected evidence set | Alternatives not mixed | PST/DSN/PDF/SchDoc | Level | Gaps |
|---|---|---|---|---|---|---|
|  |  |  |  |  | E0/E1 |  |

## End-to-end chains

| Chain ID | Kind | Functional class | Ordered boards | Electrical availability | Evidence level | Status |
|---|---|---|---|---|---|---|
|  | fpga_control/status_return/board_signal/clock_reference/power_rail/ground_return | 必需控制/硬件默认/可选功能/状态输出/电源分配 |  | 可用/电气不可用/待确认 | E0-E4 |  |

## Ordered segments

| Chain | Seq | Board | From | Net | Components/channel | Connector contact | To | DIR/OE/pulls | Assembly | Evidence | Status |
|---|---:|---|---|---|---|---|---|---|---|---|---|
|  | 1 |  |  |  |  |  |  |  | fitted/DNP/TSD*/NC | path:line/page |  |

## FPGA alignment (FPGA chains only)

| Chain | RTL port | Direction/owner | Active XDC:line | PACKAGE_PIN | IOSTANDARD | SZSD refdes.ball | `report_io` | Result |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  | reviewed/not reviewed |  |

For `power_rail` and `ground_return`, enter `不适用` here. Record power enable and power-good/fault as separate FPGA chains.

## Power distribution branches

| Chain | Source rail/voltage | Source connector | Protection/fuse | Switch/enable | Filter | BASE entry/exit | Load connector | Load board | Return ground | Assembly | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |  |  |

## Conflicts

| ID | Chain/segment | Type | Evidence A | Evidence B | Impact | Resolution |
|---|---|---|---|---|---|---|
| EXAMPLE_DIR |  | 方向冲突 | required A→B | fixed DIR gives B→A | electrically unusable | verify assembly/design intent |
| EXAMPLE_OE |  | disabled branch | FPGA/XDC reaches D120 | OE holds D120 disabled | `硬件禁用/电气不可用` | do not classify as optional |

## Unclosed points

| ID | Chain/edge | Missing evidence | Current level | Next proof required |
|---|---|---|---|---|
| EXAMPLE_CONN |  | connector contacts on both boards and BASE mapping（跨板待确认） | E0/E1 | connector table, BASE PST, or continuity measurement |

## Physical checks

| ID | Board/refdes | Check | Expected | Result | Evidence |
|---|---|---|---|---|---|
| EXAMPLE_ASSEMBLY |  | fitted/DNP/TSD*/NC and option resistor population |  | pending | photo/BOM/measurement |
