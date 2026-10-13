# FPGA/RTL/EDA 与硬件

处理通用 RTL、Vivado、板级连接、调试及证据闭环。

本类共 **26 个逻辑 Skill**。当前装载以 `profiles/codex.json` 为准；历史保留项不代表当前仍在使用。

| Skill | 主要功能 |
|---|---|
| [fpga-cdc-reset-timing](../../../skills/fpga-cdc-reset-timing/SKILL.md) | 审查 FPGA 跨时钟域、复位和时序收敛。 |
| [fpga-ila-debug](../../../skills/fpga-ila-debug/SKILL.md) | 规划并核对 Vivado ILA/VIO 探针、触发与板上调试证据。 |
| [fpga-orcad-xdc-pipeline](../../../skills/fpga-orcad-xdc-pipeline/SKILL.md) | 从 OrCAD/PST 网络提取连接并核对 FPGA 物理 XDC。 |
| [fpga-register-command-parser](../../../skills/fpga-register-command-parser/SKILL.md) | 设计或审查 FPGA 寄存器映射和命令解析链路。 |
| [fpga-rtl-code-review](../../../skills/fpga-rtl-code-review/SKILL.md) | 审查 Verilog/VHDL 模块职责、状态机和握手逻辑。 |
| [fpga-testbench-simulation](../../../skills/fpga-testbench-simulation/SKILL.md) | 编写、运行和报告 FPGA RTL 仿真测试。 |
| [fpga-vivado-tcl-automation](../../../skills/fpga-vivado-tcl-automation/SKILL.md) | 用 Tcl 重建 Vivado 工程、IP、约束与构建流程。 |
| [gf-architect](../../../skills/gf-architect/SKILL.md) | 梳理 RTL 层次、模块接口及状态机架构。 |
| [gf-plan](../../../skills/gf-plan/SKILL.md) | 在实现前规划 FPGA 功能模块、接口和验证方案。 |
| [gf-viz](../../../skills/gf-viz/SKILL.md) | 将 RTL 架构映射转成模块、状态机及时钟域图。 |
| [hardware-datasheet-to-schematic](../../../skills/hardware-datasheet-to-schematic/SKILL.md) | 把器件数据手册要求转成原理图检查项。 |
| [hardware-dev-router](../../../skills/hardware-dev-router/SKILL.md) | 为跨 RTL、板卡和报告的硬件任务选择证据与工作流程。 |
| [hardware-evidence-report-sync](../../../skills/hardware-evidence-report-sync/SKILL.md) | 把 RTL、仿真、ILA 和仪器证据同步到报告。 |
| [hardware-pcb-bringup-debug](../../../skills/hardware-pcb-bringup-debug/SKILL.md) | 按电源、时钟、接口和配置顺序排查板卡上电问题。 |
| [hardware-schematic-review](../../../skills/hardware-schematic-review/SKILL.md) | 检查混合信号电路的电源、时钟、接口和器件连接。 |
| [host-rtl-alignment](../../../skills/host-rtl-alignment/SKILL.md) | 核对上位机数据格式、寄存器与 RTL 消费逻辑。 |
| [qt-cpp-host-development](../../../skills/qt-cpp-host-development/SKILL.md) | 开发控制硬件或仪器的 Qt/C++ 桌面上位机。 |
| [rtl-schematic-xdc-alignment](../../../skills/rtl-schematic-xdc-alignment/SKILL.md) | 对齐 FPGA 顶层端口、XDC、原理图和 PCB。 |
| [sdg6052x-host-driver](../../../skills/sdg6052x-host-driver/SKILL.md) | 将 SDG6052X 主机控制模块接入 Qt/VISA/SCPI 工程。（远端历史保留，未在当前个人技能目录安装。） |
| [vivado-analysis](../../../skills/vivado-analysis/SKILL.md) | 解读 Vivado 时序、利用率、DRC 和 QoR 证据。 |
| [vivado-constraints](../../../skills/vivado-constraints/SKILL.md) | 编写和审查 FPGA 时钟及物理 XDC 约束。 |
| [vivado-impl](../../../skills/vivado-impl/SKILL.md) | 选择并分析 Vivado 布局布线与实现策略。 |
| [vivado-synth](../../../skills/vivado-synth/SKILL.md) | 选择 Vivado 综合设置并审查资源推断。 |
| [xilinx-suite](../../../skills/xilinx-suite/SKILL.md) | 处理 Vivado、Vitis HLS 等 Xilinx 工具链工程任务。（远端历史保留，未在当前个人技能目录安装。） |
| [fpga-board-signal-chain-closure](../../../skills/fpga-board-signal-chain-closure/SKILL.md) | 沿 FPGA、背板和功能板追踪信号、时钟、回流及供电链路。 |
| [fpga-rtl-development](../../../skills/fpga-rtl-development/SKILL.md) | 新增、适配或简化手写 RTL，保持项目语言、逐拍接口和必要时序保护。 |
