---
name: maroc-xsim-debug-handbook
description: 总结 MAROC USB 工程里已验证的 XSim 调试方法、波形分类、Vivado Tcl/PS1/Python 脚本入口，以及首轮板上 bring-up 所需的 Vivado 工程重建、bitstream/ILA 生成、C17/i_clk 时钟链路调试、PLL/ODDR 生成 o_cy_ifclk、smoke override 策略；当用户要求调试 `tb_cy_driver_new_xsim`、`sim_parser`、`sim_sc829`、`top`，排查 C17 单端误接差分 N 端、IFCLK/PLL/BUFG/ODDR、整理波形窗口、修复 XSim 编译/路径问题、导出 `o_sc_dout` 逐bit比对，或恢复当前仓库的上板工程基础设施并把经验沉淀成手册/流程图/skill 时使用。
---

# MAROC XSim Debug Handbook

## Overview

这个 skill 面向当前 MAROC USB 仓库，沉淀四类内容：

1. `tb_cy_driver_new_xsim` 模块级 USB/FX2LP Slave FIFO 调试路径
2. `sim_parser / sim_sc829 / top` 三层仿真边界与调试顺序
3. `xsim` 波形分组、脚本入口、常见编译/路径故障定位
4. 仿真测试手册、对比报告、case 流程图的写法
5. 首轮板上 bring-up 所需的 Vivado 工程重建、bitstream/ILA 生成、C17 时钟链路验证、以及 smoke-only 约束兜底策略

只在当前工程或结构高度相近的克隆仓库中使用。如果仓库根目录 `F:\01_MOUN\01_logic\02_MAROC\SPIROC_REF\01_MAROC_USB` 不存在，先说明该 skill 依赖当前项目布局。

## Core Workflow

1. 先判断用户所在层级：
   - `cy-driver`：`CY_driver_new + tb_cy_driver_new_xsim`
   - `sim_parser`：`maroc_usb_packet_parser + SlowControl_MAROC`
   - `sim_sc829`：`command_MAROC + SlowControl_MAROC`
   - `top`：`TOP_MAROC`
2. 优先使用仓库里现成的 `PS1/Tcl/Python` 脚本；如果 `cy-driver` 这一层没有完整 GUI 入口，就优先给 `xvlog/xelab/xsim + source ...tcl` 的命令行闭环。
3. 如果是 `xsim` 问题，先区分：
   - compile 问题：看 `xvlog.log / compile.bat / *.prj`
   - elaborate 问题：看 `elaborate.log`
   - runtime/fixture 问题：看 `simulate.log / stage_mem_for_vivado.tcl / fixtures`
4. 如果是波形观察，优先使用手册一致的分组脚本：
   - `tb_maroc_usb_packet_parser_xsim_wave_manual_groups.tcl`
   - `tb_cy_driver_new_xsim_wave_runall.tcl`
   - `tb_top_maroc_command_usb_xsim_wave_setup_only.tcl`
   - 每次重新加载波形布局前，优先清旧窗口：`catch {remove_wave [get_waves -regexp .*]}`
5. 如果要验证最终串行码流，优先使用：
   - `scripts/run_parser_sc_dout_compare.py`
6. 如果要写文档或手册，先按“最前置操作 -> 模块/接口语义 -> 信号链 -> 边界 -> 测试矩阵 -> case-by-case -> checker -> 结果 -> 风险 -> 最终判定”的主结构组织，再补 Mermaid 图。
7. 如果任务是“上板前整理 Vivado 工程入口 / 生成 `.bit + .ltx` / 补轻量 ILA / 定位首轮 bring-up gate / 排查 C17 或 IFCLK 时钟链路”，优先使用：
   - `scripts/vivado/create_project.tcl`
   - `scripts/vivado/build_bitstream.tcl`
   - `scripts/vivado/create_maroc_cfg_bringup.ps1`
   - `scripts/vivado/build_maroc_cfg_bringup.ps1`
   - `scripts/vivado/smoke_build_maroc_cfg_bringup.ps1`
   - `scripts/vivado/create_c17_clk_smoke_project.tcl`
   并把 `C17/i_clk` 与 `ifclk smoke override` 明确写成 smoke-only 临时兜底，不得包装成正式签核约束。

## What To Read Next

- 脚本入口、simset 路由、工具用途：
  - 读 [references/script-map.md](references/script-map.md)
- 波形分层、重点信号、`o_sc_byte_valid`/`r_drain_byte_index` 这些易混点：
  - 读 [references/wave-debug.md](references/wave-debug.md)
- 仿真测试手册、case 设置思路、流程图、串行签核写法：
  - 读 [references/report-writing.md](references/report-writing.md)
- 如果任务是 `CY_driver_new` 模块级 USB/FX2LP 调试或教学手册：
  - 先读 [references/cy-driver-module.md](references/cy-driver-module.md)
- 如果任务是板上 bring-up、Vivado 硬件工程恢复、bitstream/ILA 生成、C17/IFCLK/PLL 时钟链路调试：
  - 先读 [references/board-bringup.md](references/board-bringup.md)

## Non-Negotiables

1. 只基于仓库里的 TB、DUT、脚本和日志写结论，不臆造协议细节。
2. 写手册时，必须把“case 怎么设”和“先看哪些信号”分开写清楚。
3. 写 `xsim` 指南时，优先给绝对路径 `source ...tcl`，不要假设当前目录正确。
4. 遇到 `[USF-XSim-62]`，不要只复述 GUI 弹窗；必须下钻到 `xvlog.log` 第一处真实报错。
5. 对 `o_sc_dout` 的结论，优先引用逐 bit CSV/汇总 CSV/Markdown 报告，而不是口头说“看起来一致”。
6. 对 `o_sc_byte_valid` 的描述，使用“连续有效窗口覆盖 104 个 byte/104 个有效时钟周期”，不要误写成“104 个独立脉冲”，除非波形确实如此。
7. 对 `CY_driver_new` 的描述，必须明确区分：
   - `00 -> EP2_IN -> 写 -> FPGA/DUT 驱动 FD[15:0]`
   - `11 -> EP8_OUT -> 读 -> FX2 教学模型驱动 FD[15:0]`
8. 解释 `PKTEND` 时，必须写成“包结束提交/短包提交”，不要写成“第三次写”。
9. 写 `CASE7_BUS_DIRECTION_CHECK` 时，必须拆成“读窗口 / 写窗口 / high-Z demo”三段，不要当作一个连续业务事务。
10. 如果同一 TB 同时有“报告”和“手册”，必须先决定分工，再写；不要让两份文档重复承载测试结果、XSim 操作和附录清单。
11. 给波形脚本做配色时，优先使用“高对比 + 语义稳定”方案，不要把 parser / command / slow-control / mux 仲裁都做成相邻浅色。
11.1 优先在 `add_wave` 时直接传 `-color`，不要优先依赖事后 `set_wave_prop CustomSignalColor`；后者在部分 xsim 会话里不稳定。
12. 写 top GUI 指南时，必须显式区分：
    - `prepare_vivado_*_gui.ps1` 负责配置 simset / stage mem / 复制 wave Tcl
    - `source *.tcl` 只负责在 xsim 里创建波形分组，不负责创建仿真目录。
12.1 若 `source tb_top_maroc_command_usb_xsim_wave_setup_only.tcl` 报“no such file or directory”，优先改成绝对路径 `source F:/.../sim_1/behav/xsim/tb_top_maroc_command_usb_xsim_wave_setup_only.tcl`。
13. 遇到 `elaborate` 时报 `Module <...> not found`，优先怀疑 active simset 缺少 RTL 源，而不是先怀疑 DUT 代码本身。
14. xsim 的折叠后 group 行通常不继承子波形颜色；如果用户要求“折叠后仍有明显分层标签”，优先采用 `divider + group` 混合布局。
15. 如果当前仓库没有 `.xpr/.bit/.ltx`，不要默认用户会手工在 GUI 里补工程；优先恢复可重复执行的 Vivado Tcl/PS1 工程入口。
16. `CLOCK_DEDICATED_ROUTE FALSE` 这类 override 只可作为 smoke bring-up 临时兜底；必须显式注明“非正式签核约束”。
16.1 对 C17 / `Local_FPGA_CLK` 时钟问题，必须明确 C17 是 `IO_L12N_T1_MRCC_16` 差分时钟对 N 端被单端 LVCMOS 使用；推荐 smoke 链路为 `i_clk -> IBUF -> PLLE2_ADV -> BUFG -> ODDR -> o_cy_ifclk`，并把 `PLCK-12/PLCK-20` 解释为预期风险而非正式通过。
17. 若板上目标是“首轮只打通配置链”，ILA 观测应优先抓：
    - `rxf_sync_out`
    - `rx_cmd`
    - `w_parser_packet_valid`
    - `w_parser_packet_error`
    - `w_parser_packet_error_code`
    - `w_parser_sc_valid`
    - `w_parser_sc_start`
    - `w_parser_legacy_block`
    - `w_sc_start`
    - `w_sc_busy`
    - `w_sc_done`
    若用户反馈“USB 模块读不到数据”，再把 USB 写侧链路一并抓上：
    - `w_usb_dbg_tx_data`
    - `w_usb_dbg_state`
    - `w_usb_dbg_next_state`
    - `txf_data`
    - `txf_valid`
    - `txf_rden`
    - `txf_empty`
    - `i_cy_flaga`
    - `i_cy_flagb_full`
    - `i_cy_flagc_empty`
    - `o_cy_sloe`
    - `o_cy_slrd`
    - `o_cy_slwr`
    - `o_cy_pktend`
    - `o_fifoadr`
    - `o_cy_slcsn`

## Typical Outputs

这个 skill 典型会产出：

- 调试步骤
- `xsim` Tcl 命令
- 波形分组方案
- `CSV/Markdown` 对比报告
- 主测试手册增补章节
- Mermaid 边界图、case 设置流程图、信号观察流程图
- `CY_driver_new` 模块级 USB/FX2LP 波形解释
- `CASE0~CASE7` 的逐案时序说明
- `sim_1 / sim_parser / sim_sc829` 的建目录与 staging 命令
- 高对比颜色版 `xsim` wave Tcl
- `divider + group` 混合布局说明
- Vivado 工程重建 Tcl / PS1
- 首轮 `.bit + .ltx` 构建入口
- ILA 信号清单与 smoke override 使用边界
- C17/i_clk 到 25MHz `o_cy_ifclk` 的 smoke RTL / XDC 策略和 USB 联调前结论

## Resources

只创建了 `references/`，因为这个 skill 的价值主要是复用方法和入口，不需要额外脚本副本。
