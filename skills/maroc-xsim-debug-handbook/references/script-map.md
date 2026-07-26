# Script Map

## Repo Roots

- Repo root:
  - `F:\01_MOUN\01_logic\02_MAROC\SPIROC_REF\01_MAROC_USB`
- Main docs directory:
  - `C:\01_obsidian\ustc_hy\01_科研主系统\02_项目\MAROC开发\00_MAROC文档\过程开发笔记\04_仿真与验证`

## Simset Routing

### `cy-driver`

Use when the problem is in:

- `CY_driver_new`
- `tb_cy_driver_new_xsim`
- FX2LP Slave FIFO module-level teaching TB
- `FIFOADR / FLAGB / FLAGC / SLOE / SLRD / SLWR / PKTEND / FD[15:0]`
- USB module-level report/manual writing for `CY_driver_new`

Primary entry:

- direct CLI, not GUI-first:
  - `xvlog sources_maroc/CY_driver_new.v sources_maroc/tb/tb_cy_driver_new_xsim.v`
  - `xelab -debug typical tb_cy_driver_new_xsim -s tb_cy_driver_new_xsim`
  - `xsim tb_cy_driver_new_xsim`

Primary wave/helper Tcl:

- `sources_maroc/tools/tb_cy_driver_new_xsim_wave_runall.tcl`

Secondary/generated Tcl:

- `xsim.dir/tb_cy_driver_new_xsim/xsim_script.tcl`
  - only a generated replay entry, not the preferred teaching入口

Related docs:

- `C:\01_obsidian\ustc_hy\01_科研主系统\02_项目\MAROC开发\00_MAROC文档\过程开发笔记\04_仿真与验证\20260416-tb_cy_driver_new_xsim仿真测试手册.md`
- `C:\01_obsidian\ustc_hy\01_科研主系统\02_项目\MAROC开发\00_MAROC文档\过程开发笔记\04_仿真与验证\20260417-tb_cy_driver_new_xsim-iverilog_vvp仿真测试报告.md`

Notes:

- no dedicated `prepare_vivado_*_gui.ps1` currently exists for `cy-driver`
- no dedicated `tb_cy_driver_new_xsim.wcfg` currently exists in repo
- prefer `source .../tb_cy_driver_new_xsim_wave_runall.tcl` over `autoloadwcfg`

### `sim_parser`

Use when the problem is in:

- `maroc_usb_packet_parser`
- `SlowControl_MAROC`
- packet parsing
- `raw_sc_bytes / legacy bytes / o_sc_dout`

Primary entry:

- `sources_maroc/tools/prepare_vivado_parser_gui.ps1`

Wave scripts:

- `sources_maroc/tools/tb_maroc_usb_packet_parser_xsim_wave_manual_groups.tcl`
- `sources_maroc/tools/tb_maroc_usb_packet_parser_xsim_wave_setup_only.tcl`
- `sources_maroc/tools/tb_maroc_usb_packet_parser_xsim_wave_runall.tcl`

Common logs:

- `MAROC_PRJ/MAROC_PRJ.sim/sim_parser/behav/xsim/xvlog.log`
- `.../compile.bat`
- `.../elaborate.bat`
- `.../simulate.log`

### `sim_sc829`

Use when the problem is in:

- `command_MAROC`
- `o_cfg_valid / o_cfg_data / o_sc_start`
- command-to-slowcontrol contract

Primary entry:

- `sources_maroc/tools/prepare_vivado_sc829_gui.ps1`

Main TB:

- `sources_maroc/tb/tb_command_slowcontrol_joint_829_csv_xsim.v`

### `top`

Use when the problem is in:

- `TOP_MAROC`
- USB/CY handshake
- command path vs parser path arbitration
- `o_ck_sc / o_din_sc`

Primary entry:

- `sources_maroc/tools/prepare_vivado_top_gui.ps1`

Recommended wave Tcl:

- `sources_maroc/tools/tb_top_maroc_command_usb_xsim_wave_setup_only.tcl`
- `sources_maroc/tools/tb_top_maroc_command_usb_xsim_wave_runall.tcl`
- `sources_maroc/tools/tb_top_maroc_command_usb_xsim_wave_case_sw_packet.tcl`

Main TB:

- `sources_maroc/tb/tb_top_maroc_command_usb.v`

Top GUI notes:

- `prepare_vivado_top_gui.ps1` prepares `MAROC_PRJ.sim/sim_1/behav/xsim`
- after GUI opens, prefer absolute-path `source .../tb_top_maroc_command_usb_xsim_wave_setup_only.tcl`
- if `source tb_top_maroc_command_usb_xsim_wave_setup_only.tcl` fails, first suspect current xsim working directory mismatch and switch to absolute path

## Shared Vivado/XSim Helpers

- `sources_maroc/tools/enable_vivado_mem_autoload.ps1`
  - generic Vivado simulation configurator
- `sources_maroc/tools/configure_vivado_mem_autoload.tcl`
  - binds top/TB/runtime/compile-pre-hook
- `sources_maroc/tools/stage_mem_for_vivado.tcl`
  - stages `.mem/.hex/.txt` fixtures and patches parser `.prj` to use SystemVerilog

## Board Bring-Up / Hardware Project

When the user asks for board-validation preparation, Vivado hardware project recovery, or `.bit + .ltx` generation, prefer these entries:

- `scripts/vivado/create_project.tcl`
  - rebuilds a minimal Vivado hardware project around `TOP_MAROC`
- `scripts/vivado/build_bitstream.tcl`
  - runs synth/impl and exports `.bit + .ltx + reports`
- `scripts/vivado/create_maroc_cfg_bringup.ps1`
  - Windows wrapper for project creation
- `scripts/vivado/build_maroc_cfg_bringup.ps1`
  - Windows wrapper for bitstream build
- `scripts/vivado/smoke_build_maroc_cfg_bringup.ps1`
  - one-shot smoke flow with IFCLK route override
- `scripts/vivado/README.md`
  - usage notes, default part, ILA probes, smoke override boundary

Important:

- if implementation only passes with `-enable_ifclk_smoke_override 1`, call that out as smoke-only
- do not silently convert that override into a formal timing sign-off recommendation
- current first-pass ILA also covers USB write-side debug signals (`io_cy_fd / txf_* / FLAG* / SLOE/SLRD/SLWR/PKTEND/FIFOADR/SLCS#`) for “USB module cannot read data” cases

## XSim Directory Creation

When the user asks “how do I create the Vivado simulation directory”, prefer these prepared entries:

- top:
  - `powershell -NoProfile -ExecutionPolicy Bypass -File ..\sources_maroc\tools\prepare_vivado_top_gui.ps1`
- parser:
  - `powershell -NoProfile -ExecutionPolicy Bypass -File ..\sources_maroc\tools\prepare_vivado_parser_gui.ps1`
- sc829:
  - `powershell -NoProfile -ExecutionPolicy Bypass -File ..\sources_maroc\tools\prepare_vivado_sc829_gui.ps1`

If no `.xpr` exists, the fallback is to create:

- `MAROC_PRJ.sim/sim_1/behav/xsim`
- `MAROC_PRJ.sim/sim_parser/behav/xsim/sources_maroc/tb/fixtures`
- `MAROC_PRJ.sim/sim_sc829/behav/xsim`

and then copy the required mem / hex / txt fixtures manually.

## Python Utilities

- `scripts/run_parser_sc_dout_compare.py`
  - compile parser TB, run 3 positive cases, export `o_sc_dout` capture, generate compare CSV + report
- `scripts/compare_sc_bitstream.py`
  - generic resolved-vs-actual bit compare helper
- `scripts/build_maroc_sc_payload_from_csv.py`
  - build 829-bit payload mem from CSV
- `scripts/inspect_sc_field_trace.py`
  - field-level trace inspection
- `scripts/generate_maroc_parser_fixtures.py`
  - parser fixture generation

## CY Driver Wave/Report Helpers

- `sources_maroc/tools/tb_cy_driver_new_xsim_wave_runall.tcl`
  - adds grouped waves for `GROUP_BASELINE / GROUP_READ_CHAIN / GROUP_WRITE_CHAIN / GROUP_ARBITRATION / GROUP_BUS_DIRECTION / GROUP_CASE_MARKERS`
  - runs `3.5 us`
  - suitable for both GUI and `-tclbatch`

Typical batch check:

```powershell
cd F:\01_MOUN\01_logic\02_MAROC\SPIROC_REF\01_MAROC_USB
xvlog sources_maroc/CY_driver_new.v sources_maroc/tb/tb_cy_driver_new_xsim.v
xelab -debug typical tb_cy_driver_new_xsim -s tb_cy_driver_new_xsim
xsim tb_cy_driver_new_xsim -tclbatch sources_maroc/tools/tb_cy_driver_new_xsim_wave_runall.tcl
```

## When Something Fails

### `[USF-XSim-62] compile step failed`

Check in this order:

1. `xvlog.log`
2. `compile.bat`
3. `*_vlog.prj`
4. whether parser TB is being compiled as `SystemVerilog`
5. whether `stage_mem_for_vivado.tcl` ran

### `[USF-XSim-62] elaborate step failed`

Check in this order:

1. `elaborate.log`
2. whether the active simset contains every RTL that the selected top TB instantiates
3. whether `top` and `top_lib` are set to the intended TB / `xil_defaultlib`
4. whether `command_MAROC.v / maroc_usb_packet_parser.v / SlowControl_MAROC.v / TOP_MAROC.v` are all present in the simset for top-level runs
5. whether `data_fifo.v` exists when real FIFO IP is expected

Common real-world pattern:

- `Module <maroc_usb_packet_parser> not found while processing instance <parser_0>`
  - meaning: `sim_1` is missing parser RTL in the active fileset
  - fix: add the missing RTL to the simset, then rerun `prepare_vivado_top_gui.ps1`

### Simulation runs but case behavior is all zero

Check in this order:

1. `simulate.log`
2. whether fixtures exist under `...sim/<simset>/behav/xsim/sources_maroc/tb/fixtures`
3. whether `prepare_vivado_*_gui.ps1` was re-run after changes
4. whether the correct simset is active
