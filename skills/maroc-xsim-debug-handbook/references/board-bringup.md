# Board Bring-Up

## 何时读这份参考

当任务涉及以下任一项时加载：

- 恢复当前仓库的 Vivado 硬件工程入口
- 从零创建 `.xpr`
- 生成 `.bit + .ltx`
- 为首轮板上 bring-up 加轻量 ILA
- 解释为什么 `ifclk smoke override` 只能临时使用
- 排查 C17 / `Local_FPGA_CLK` 单端误接差分 N 端导致的 PLL、BUFG、ODDR、`o_cy_ifclk` 问题
- 设计“USB ingress -> parser -> slow-control”首轮板上 gate

## 默认策略

当前 MAROC USB 工程的首轮板上验证，默认只收口到**配置链**：

`USB ingress -> rx_cmd -> maroc_usb_packet_parser -> SlowControl_MAROC -> rstn_sc/o_ck_sc/o_din_sc`

不要把第一轮目标扩到完整 ADC 数据回传或 readout 链，因为当前：

- `TOP_MAROC` 中 `o_ck_r/o_d_r/o_rstn_r` 仍是绑值
- `02_io_timing.xdc` 尚未建立
- 当前仓库没有可直接复用的 `.xpr/.bit/.ltx`

## 当前仓库里的硬件工程入口

优先使用：

- `scripts/vivado/create_project.tcl`
- `scripts/vivado/build_bitstream.tcl`
- `scripts/vivado/create_maroc_cfg_bringup.ps1`
- `scripts/vivado/build_maroc_cfg_bringup.ps1`
- `scripts/vivado/smoke_build_maroc_cfg_bringup.ps1`
- `scripts/vivado/README.md`

这些入口做的事情是：

1. 以 `sources_maroc/TOP_MAROC.v` 为顶层重建 Vivado 工程
2. 导入现有 RTL
3. 导入 `MAROC_PRJ/MAROC_PRJ.srcs/sources_1/ip/data_fifo/data_fifo.xci`
4. 加载：
   - `xdc_auto/00_pins_formal.xdc`
   - `xdc_auto/00_pins_debug.xdc`
   - `xdc_auto/01_clocks.xdc`
5. 条件化插入轻量 ILA
6. 输出 `.bit + .ltx + timing/util/io report`

Windows `PS1` wrapper 默认会优先把 Vivado 工程放到短路径（例如 `%TEMP%\maroc_cfg_bringup*`），原因是：

- 当前仓库 worktree 路径较长
- 打开 ILA / `dbg_hub` 后，Vivado 在 `opt_design` 阶段会对临时路径长度非常敏感
- 若工程目录过长，可能在 debug core 生成阶段直接失败

因此：

- 要“稳妥地先出 `.bit + .ltx`”，优先用 wrapper 默认短路径
- 只有当用户明确要把 `.xpr` 固定在仓库里时，再显式传 `-ProjectDir`

## 默认器件与人工确认

当前脚本默认 part 是：

```text
xc7a200tfbg484-2L
```

原因不是“已经最终签核”，而是：

- 当前 `data_fifo.xci` 与旧工程残留更接近 `xc7a200t`
- 当前 `xdc_auto` 流程也围绕这套映射整理

但仍必须人工确认：

1. 板卡真实器件是否是 `XC7A200T` 还是 `XC7A100T`
2. `i_clk` 板级来源是否合法
3. `o_clk_maroc_p/n` 与 `CK_40M/CKb_40M` 极性
4. `o_start_adc` 与 `start_ADCb` 极性
5. `o_cy_slcsn` 与 `FLAGD/SLCS#` 共享脚接法
6. `i_trigger_64ch_or[n] -> OUTn` 位序是否接受

如果板子最终确认是 `XC7A100T`，不要只改命令行 `-part` 就直接上板；必须重新检查：

- pin/package 对应关系
- 时钟脚合法性
- IP/device 兼容性

## 轻量 ILA 策略

首轮配置链 bring-up，ILA 默认只抓关键握手，不抓大宽度数据面。

推荐 probe：

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

策略原则：

1. 先证明 USB 命令确实进 FPGA
2. 再证明 parser 收包/报错逻辑
3. 再证明 slow-control 启动与完成闭环
4. 不在第一轮把 ILA 资源浪费在完整数据面上

如果用户已经明确反馈“从 USB 模块读不到数据”，则把 USB 写侧 debug 链一并加入首轮 ILA：

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

这组信号的目的不是替代配置链主线，而是快速判断问题究竟在：

1. 上游 `data_socket_MAROC / tx fifo`
2. `CY_driver_new` 写状态机
3. FX2 标志位 / 总线方向
4. 板级 USB 物理连接

## Smoke Override 的使用边界

如果实现阶段卡在 `o_cy_ifclk` 相关的时钟专用布线检查，可以启用：

```text
-enable_ifclk_smoke_override 1
```

它会加入一个项目本地的实现期 XDC，核心内容是：

```xdc
set_property CLOCK_DEDICATED_ROUTE FALSE [get_nets -hierarchical -filter {NAME =~ *o_cy_ifclk_OBUF}]
```

必须明确：

- 这是**smoke-only** 兜底
- 作用是先让 `.bit + .ltx` 能生成，好做首轮下载和观测
- 它**不是**正式签核约束
- 后续必须回到板级时钟/IFCLK 合法性本身，不能长期依赖

## 首轮板上 Gate

### Gate 1: 下载与静态安全

- JTAG 识别正常
- 下载 `.bit` 成功
- 板卡静态电流无异常

### Gate 2: 主时钟/静态引脚

先看：

- `o_cy_ifclk`
- `o_clk_maroc_p/n`
- `rstn_sc`

目的：

- 证明主时钟域活着
- 没有明显悬空或异常翻转

### Gate 3: USB ingress

用最小命令流先验证：

- `rxf_sync_out`
- `rx_cmd`

若这里失败，优先查：

- FX2 pin
- 总线方向
- IFCLK 假设

不要继续查 parser。

### Gate 4: formal packet path

用真实 `packet_250B` 重放，确认：

- `w_parser_packet_valid`
- `w_parser_packet_error`
- `w_parser_packet_error_code`
- `w_parser_sc_valid`
- `w_parser_sc_start`

若 `packet_error` 出现，第一优先排：

- 板上 word-byte 顺序是否仍满足 `[15:8] -> [7:0]`

### Gate 5: slow-control 输出

在 parser 通过后，联合看：

- `rstn_sc`
- `o_ck_sc`
- `o_din_sc`
- `w_sc_busy`
- `w_sc_done`

当前工程预期：

- `o_ck_sc ≈ 2MHz`
- `rstn_sc` 低脉宽明显大于 `20ns`
- `w_sc_done` 在一次完整移位后出现

### Gate 6: 最小 ADC 控制补充

只补看：

- `o_rstn_adc`
- `o_start_adc`

重点：

- `o_rstn_adc` 低脉宽约 `25ns`
- `o_start_adc` 下降沿与 `o_rstn_adc` 释放关系是否一致

这不是首轮配置链 PASS 的必要条件，但决定是否进入第二阶段 ADC bring-up。

## 失败分流

- Gate 2 失败：先查时钟、复位、差分极性、约束
- Gate 3 失败：先查 FX2 / IFCLK / 总线方向
- Gate 4 失败：先查 packet replay / byte order / parser 仲裁
- Gate 5 失败：先查 mux 与 `SlowControl_MAROC`
- Gate 5 通过但 ASIC 无响应：优先查 `CK_40M` 极性、`start_ADCb` 极性、慢控物理连线、芯片供电

## 产物与话术

如果任务包含“整理上板基础设施”，优先产出：

1. 可重复执行的 `.tcl/.ps1`
2. 一个短 README
3. `.bit/.ltx` 输出路径说明
4. smoke override 的适用边界
5. 板前人工确认清单

避免把“能生成 smoke bitstream”写成“正式时序已签核”。

## C17 / i_clk 时钟链路经验

### 适用场景

当用户提到以下关键词时，优先按本节处理：

- `i_clk`
- `C17`
- `Local_FPGA_CLK`
- `o_cy_ifclk`
- `IFCLK`
- `PLL / MMCM / PLLE2_ADV`
- `CLOCK_DEDICATED_ROUTE FALSE`
- `PLCK-12 / PLCK-20`
- “单端时钟接到了差分 N 端”

当前已确认的硬件事实：

```text
FPGA: xc7a200tfbg484-2L
i_clk / Local_FPGA_CLK: C17
C17 site: IO_L12N_T1_MRCC_16
输入标准: LVCMOS33
输入频率假设: 40 MHz
USB IFCLK 输出: o_cy_ifclk -> V4
```

C17 是差分时钟对的 N 端。当前板上用单端 LVCMOS 时钟接入 C17，因此这条路径不等价于正规的单端全局时钟输入。任何通过 `CLOCK_DEDICATED_ROUTE FALSE` 放行的结果都只能写成 smoke / bring-up 结论。

### 推荐 smoke 链路

已验证的最小链路是：

```text
i_clk(C17, 40 MHz)
  -> IBUF u_ibuf_i_clk
  -> i_clk_IBUF
  -> BUFG u_bufg_clk_sys
  -> clk_sys 40 MHz
  -> ODDR
  -> o_clk_maroc / o_clk_raw 40 MHz debug output

i_clk_IBUF
  -> PLLE2_ADV u_pll_ifclk_25m
  -> BUFG u_bufg_cy_ifclk_25m
  -> cy_ifclk_25m
  -> ODDR u_oddr_cy_ifclk
  -> o_cy_ifclk 25 MHz
```

不要优先走：

```text
i_clk -> IBUF -> BUFG -> PLL/MMCM
```

原因是 C17 入口本来已经非理想，先送 BUFG 再送 CMT 会让 clock placer 问题更难定位。对当前 smoke top，使用 IBUF 输出同时驱动 40 MHz 观测 BUFG 和 PLL 输入更清晰。

### PLL 参数

40 MHz 生成 25 MHz 的已验证 `PLLE2_ADV` 参数：

```text
CLKIN1_PERIOD  = 25.000
DIVCLK_DIVIDE  = 1
CLKFBOUT_MULT  = 20
CLKOUT0_DIVIDE = 32
```

计算关系：

```text
VCO = 40 MHz * 20 / 1 = 800 MHz
CLKOUT0 = 800 MHz / 32 = 25 MHz
```

`o_cy_ifclk` 必须通过 ODDR 转发，不要直接 `assign o_cy_ifclk = cy_ifclk_25m`，否则输出时钟质量和时序建模都不清晰。

### 约束模式

基础 clock 与 pin：

```xdc
create_clock -name i_clk -period 25.000 [get_ports i_clk]

set_property PACKAGE_PIN C17 [get_ports i_clk]
set_property IOSTANDARD LVCMOS33 [get_ports i_clk]

set_property PACKAGE_PIN V4 [get_ports {o_cy_ifclk}]
set_property IOSTANDARD LVCMOS33 [get_ports {o_cy_ifclk}]
set_property SLEW FAST [get_ports {o_cy_ifclk}]
set_property DRIVE 8 [get_ports {o_cy_ifclk}]
```

C17 临时 override 只约束 IBUF 输出附近的 net：

```xdc
set_property CLOCK_DEDICATED_ROUTE FALSE [get_nets i_clk_IBUF]
set_property CLOCK_DEDICATED_ROUTE FALSE \
    [get_nets -of_objects [get_pins u_ibuf_i_clk/O]]
```

如果层级名变化，先查：

```tcl
get_nets -hier *clk*
get_pins -hier *u_ibuf_i_clk*/O
get_pins -hier *clkin1_ibufg*/O
```

不要把 override 扩展到 PLL 输出、`cy_ifclk_25m`、USB 数据控制信号或其它主链时钟。

给 ODDR 转发后的 IFCLK 建 generated clock：

```xdc
create_generated_clock -name o_cy_ifclk_25m \
    -source [get_pins u_oddr_cy_ifclk/C] \
    -divide_by 1 \
    [get_ports {o_cy_ifclk}]
```

### 已验证脚本与产物

当前 C17 smoke 工程入口：

```text
scripts/vivado/create_c17_clk_smoke_project.tcl
scripts/vivado/build_bitstream.tcl
```

已验证的临时工程名示例：

```text
vivado/c17_clk_smoke_pll_25m_check
build/c17_clk_smoke_pll_25m_check/c17_clk_smoke_pll_25m_check.bit
```

已观察到的构建结论写法：

- 综合通过
- 布局布线通过
- bitstream 生成
- timing 报告可写 `All user specified timing constraints are met`
- DRC error 为 0
- `PLCK-12`、`PLCK-20` 为预期 warning，原因是 C17 单端误接差分 N 端后 clock placer 路径非理想

不要把 `PLCK-12/PLCK-20` 写成无风险。推荐话术：

> 当前 bitstream 可用于 smoke bring-up 和示波器确认；C17 入口仍靠 `CLOCK_DEDICATED_ROUTE FALSE` 放行，不能作为长期可靠的正式时钟签核方案。

### USB 联调前 gate

进入 USB 联调前，先用示波器确认：

| 信号 | 预期 |
| --- | --- |
| `o_clk_maroc` | 40 MHz |
| `o_clk_raw` | 40 MHz |
| `o_cy_ifclk` | 25 MHz |
| `o_led` | `pll_locked & counter[25]`，应慢速闪烁 |

如果 `o_led` 不闪、`o_cy_ifclk` 不稳定、或 PLL lock 可疑，不要继续查 USB 协议层。先回到 C17 输入质量、PLL 参数、reset、ODDR 输出和 dedicated route warning。

若这些时钟点稳定，后续 USB 不通时优先查：

1. FX2 是否收到稳定 25 MHz IFCLK
2. `FLAGA / FLAGB / FLAGC`
3. `SLRD / SLWR / SLOE / FIFOADR / PKTEND`
4. `io_cy_fd[15:0]` 总线方向
5. FPGA 内部 USB reader / writer 状态机

除非观察到 `o_cy_ifclk` 不稳定或 PLL lock 异常，否则不要把后续 USB 数据不通直接归因到 PLL 分频失败。

### 长期修正建议

正式版本应优先考虑：

1. 改板或飞线，把单端板载时钟接入合适的单端 GC/MRCC 输入。
2. 或使用 FX2 `CLKOUT` 作为 USB 同步域基准。
3. 移除 C17 dedicated route override 后重新签核时序。

在任何文档或回复中，必须区分：

- “当前 smoke bitstream 能跑”
- “当前时钟链路可用于 USB 联调前验证”
- “当前 C17 时钟入口已经正式签核”

第三句话不能说，除非硬件入口和时序签核已经真正修正。
