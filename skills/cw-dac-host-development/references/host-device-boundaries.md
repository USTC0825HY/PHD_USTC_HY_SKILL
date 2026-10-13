# host 能力盘点与 DDS 接入边界

适用于功能盘点、DDS 开发和跨模块任务。以用户指定工程为目标，先读 host/MEMORY.md 与模块记录，再核对当前契约、执行器、包和验证；历史提取路线不自动成为新任务默认工程。

## 三个模块

1. `host/dds_vio_control` 提供五路 DDS 的 `tcl/dds15_vio.tcl` / `::dds` 接口，同时保留旧 DDS3 API。读取其 README/MEMORY/VALIDATION 及 profile，不把旧 API 的设备范围套给新库。
2. `host/linearity_automation` 已有五 DDS GUI/服务接入记录；从 `dds_control.py`、Tcl 分发、dds_v1、实际包内共享库和验证报告确认选定版本是否包含它。早期“尚未接入 GUI”仅适用于对应旧版本。
3. `host/pdh_dlock` 是独立串口软件及 HDL，其内部数字 DDS 不等于外部 AD9914 控制，也不是本 Tk 工程的默认共享模块。

## DDS 契约与生命周期

- 独立 profile 显式绑定设备、完整 CELL_NAME 和探针结构，不猜 hw_vio_N 或探针序号。换板、重烧、LTX/会话变化后按当前失效机制重新绑定。
- 当前五路库区分 DDS1/4/5 串行 AD9852、DDS2 并行 AD9852 的 48 位 FTW，与 DDS3 AD9914 的 32 位 FTW；实际 SYSCLK、倍率和量化范围从目标 profile/源码核实。不能使用 DDS3 公式假定其他通道。
- 保持 source/plan 无输出、prepare 不启动、start 明确启动的边界；stop 不关闭 RF。状态/控制字不等于芯片实际频率或电压，多路顺序 JTAG 操作不等于同步更新。
- 手动免回复控制后按当前协议主动查询最近操作；服务成功和仪器确认分别报告。旧版状态轮询不推广为新默认。
- SYNC_CLK enable 属 RTL 配置；CFR2 debug 常量不是芯片寄存器回读。频谱改善仍需 A/B 仪器证据。
- GUI、worker、服务生命周期、依赖打包和测试已经是现有集成的维护范围；新器件/新工程仍重新检查，不自动改大工程或触发硬件。

## 其他器件与证据

- CW 的 b9726/da766 与旧线性度 da9726/ad766 分属不同契约，不凭近似名称混用。
- point/sweep/scale 配置和外部自动测量分别确认；枚举、按钮或 YAML 存在不证明完整执行流程。
- 通用 ILA 不等于芯片寄存器驱动。温度、模拟噪声和校准条件由测量证据支持，交给 laser-electrical-data-analysis 处理。
- 源码、离线 Mock、包内能力、真实连接和板上电气结果分别报告，不把任一层证据替代另一层。
