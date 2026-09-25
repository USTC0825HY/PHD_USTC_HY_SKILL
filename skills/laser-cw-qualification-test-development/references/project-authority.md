# Project authority

## Select the FPGA implementation

Start from the user's requested project and its nearest AGENTS.md/MEMORY.md. Under the current workspace, locate the project in `F:/01_Laser/code/fpga/projects`; do not select a similarly named directory or the newest BIT by timestamp.

| Project | Identity and scope |
|---|---|
| `05_CW_TEST_HY` | Current integrated target when explicitly selected: `CW_TEST_HY.xpr`, top `cw_top`, Vivado 2018.3, `xc7vx690tffg1761-2L`; reread its current XPR and local rules |
| `01_CW_TEST_MAIN` | CW mother project; discover its XPR below `AD766_RF_test` and preserve its own top/constraints |
| `02_GS_CW_TEST_MAIN` | GS/CW mother project; discover its XPR below `jianding_szsd_ver729`, not the 05 release |
| Other dedicated targets | For example `06_JGQD` contains distinct baseline/guard/board-control targets; use that target's own rules and XPR |

The retired `cw_test_202608` path and `AD677_IO_DDS_TOP` identity describe an earlier baseline only. They cannot establish another project's active top or pin authority.

Parse the selected XPR for version, part, top/source, fileset membership, active/disabled constraints, IP and run metadata. Read matching build manifests before claiming a release. A Complete run may predate current inputs; static inspection does not establish board validation. Historical authorizations in MEMORY apply to their original task only.

## Hardware authority

- Root: `F:\01_Laser\0_20260727_513test\04_共用硬件设计资料\超稳原理图pcb_王老师`
- Board/evidence registry: `references/513-board-registry.json`
- Generic closure workflow: `fpga-board-signal-chain-closure`

The registry separates physical boards from candidate evidence sets. A similarly named folder
or another revision is not another physical board and must not be silently merged with the
selected evidence set.

| ID | Physical role | Current selected evidence |
|---|---|---|
| `SZSD` | FPGA master/controller | public DSN + PST; `CW-202401770C-J-XG（公开）` remains an alternate PDF + PST evidence set |
| `BASE` | common backplane/interconnect | public DSN + PDF + PST |
| `POWER` | power module/source | public DSN + PDF + PST |
| `YCQD` | delay-drive board | public DSN + PDF + PST; internal drawing package remains an unselected alternate |
| `PZ` | frequency-synthesis board | public review PDF + PcbDoc only; no PST, so no board-internal continuity claim |
| `LASER_DRIVE` | laser-drive load | no evidence set selected; E0 |
| `TEMP_CONTROL` | temperature-control load | review PDF only; E0 for board connectivity |
| `LOCK_DRIVE` | ultra-stable lock-drive board | SchDoc + PcbDoc only; distinct from PZ and E0 for PST connectivity |
| `ERROR_DETECT` | error-detection board and power load | DSN only; E0 until PST export exists |
| `OTHER_LOADS` | discovered future loads | placeholder; E0 |

PDF provides device-side pin evidence only. SchDoc, PcbDoc, or DSN without PST keeps the board
in the topology but cannot establish exact board-internal nets. Re-run the inventory/preflight
whenever source files change; retain source paths, hashes, timestamps, and completeness state.

## Required graph routes

- `SZSD -> BASE -> POWER`
- `SZSD -> BASE -> YCQD`
- `SZSD -> BASE -> PZ`
- `YCQD -> BASE -> PZ`
- `POWER -> BASE -> PZ / LASER_DRIVE / TEMP_CONTROL / LOCK_DRIVE / ERROR_DETECT / OTHER_LOADS`

Every boundary requires connector-pin mapping, BASE PST evidence, a controlled interface table,
or a physical continuity record. Net-name equality and equal pin numbers never close an edge.

## Disabled as current evidence

The removed `F:\01_Laser\logic\jianding_szsd\jianding_szsd.xpr` tree and historical XDC files
are `历史文件，仅供功能参考`. They cannot establish the current top, active constraint, or FPGA pin.
