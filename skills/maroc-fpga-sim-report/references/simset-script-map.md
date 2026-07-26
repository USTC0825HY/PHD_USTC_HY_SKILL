# Simset 与脚本地图

## 适用仓库

- Repo root:
  - `F:\01_MOUN\01_logic\02_MAROC\SPIROC_REF\01_MAROC_USB`
- 常用文档目录:
  - `C:\01_obsidian\ustc_hy\01_科研主系统\02_项目\MAROC开发\00_MAROC文档\过程开发笔记\04_仿真与验证`

## 三层验证边界

### `sim_parser`

用于：
- `maroc_usb_packet_parser`
- `SlowControl_MAROC`
- packet parsing
- `raw_sc_bytes / legacy bytes / o_sc_dout`

主入口：
- `sources_maroc/tools/prepare_vivado_parser_gui.ps1`

主 TB：
- `sources_maroc/tb/tb_maroc_usb_packet_parser.v`

常用日志：
- `MAROC_PRJ/MAROC_PRJ.sim/sim_parser/behav/xsim/xvlog.log`
- `.../compile.bat`
- `.../elaborate.bat`
- `.../simulate.log`

### `sim_sc829`

用于：
- `command_MAROC`
- `o_cfg_valid / o_cfg_data / o_sc_start`
- command-to-slowcontrol contract

主入口：
- `sources_maroc/tools/prepare_vivado_sc829_gui.ps1`

主 TB：
- `sources_maroc/tb/tb_command_slowcontrol_joint_829_csv_xsim.v`

### `top`

用于：
- `TOP_MAROC`
- USB/CY handshake
- command path 与 parser path 仲裁
- `o_ck_sc / o_din_sc`

主入口：
- `sources_maroc/tools/prepare_vivado_top_gui.ps1`

主 TB：
- `sources_maroc/tb/tb_top_maroc_command_usb.v`

### `cy-driver`

用于：
- `CY_driver_new`
- `tb_cy_driver_new_xsim`
- FX2LP Slave FIFO 模块级教学/调试

优先入口：
- 直接 CLI：

```powershell
cd F:\01_MOUN\01_logic\02_MAROC\SPIROC_REF\01_MAROC_USB
xvlog sources_maroc/CY_driver_new.v sources_maroc/tb/tb_cy_driver_new_xsim.v
xelab -debug typical tb_cy_driver_new_xsim -s tb_cy_driver_new_xsim
xsim tb_cy_driver_new_xsim
```

## 通用 Vivado/XSim 辅助脚本

- `sources_maroc/tools/enable_vivado_mem_autoload.ps1`
  - 通用 Vivado simulation configurator
- `sources_maroc/tools/configure_vivado_mem_autoload.tcl`
  - 绑定 top/TB/runtime/compile-pre-hook
- `sources_maroc/tools/stage_mem_for_vivado.tcl`
  - staging `.mem/.hex/.txt` fixture，并修正 parser `.prj` 的 `SystemVerilog` 编译问题

## 波形脚本入口

### parser

- `sources_maroc/tools/tb_maroc_usb_packet_parser_xsim_wave_manual_groups.tcl`
- `sources_maroc/tools/tb_maroc_usb_packet_parser_xsim_wave_setup_only.tcl`
- `sources_maroc/tools/tb_maroc_usb_packet_parser_xsim_wave_runall.tcl`

### cy-driver

- `sources_maroc/tools/tb_cy_driver_new_xsim_wave_runall.tcl`

## Python 工具

- `scripts/run_parser_sc_dout_compare.py`
  - 编译 parser TB，运行 3 个正例，导出 `o_sc_dout` capture，并生成 compare CSV + report
- `scripts/compare_sc_bitstream.py`
  - 通用 bit compare helper
- `scripts/build_maroc_sc_payload_from_csv.py`
  - 从 CSV 构造 829-bit payload
- `scripts/inspect_sc_field_trace.py`
  - field-level trace inspection
- `scripts/generate_maroc_parser_fixtures.py`
  - parser fixture generation

## 故障定位顺序

### `[USF-XSim-62] compile step failed`

按这个顺序查：
1. `xvlog.log`
2. `compile.bat`
3. `*_vlog.prj`
4. parser TB 是否按 `SystemVerilog` 编译
5. `stage_mem_for_vivado.tcl` 是否实际执行

### 仿真能跑但 case 行为全零

按这个顺序查：
1. `simulate.log`
2. `...sim/<simset>/behav/xsim/sources_maroc/tb/fixtures` 是否存在 fixture
3. `prepare_vivado_*_gui.ps1` 是否在改动后重新执行
4. 当前激活的 simset 是否正确
