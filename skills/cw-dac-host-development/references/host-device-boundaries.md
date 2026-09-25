# host 能力盘点与 DDS 接入边界

适用于本工作区的功能清单、DDS 接入方案和跨模块开发，不改变用户指定的目标工程。

## 先分清三层

1. `host/dds_vio_control` 是独立 DDS3 Tcl API；读取其 README/MEMORY/VALIDATION，不因放在 host 下就声称已接入 GUI/TCP。
2. `host/linearity_automation` 是 Python/Tcl/仪器测试系统；器件能力从契约、执行器和当前发布包分别确认。
3. `host/pdh_dlock` 是独立串口软件及配套 HDL；内部数字 DDS 不能当作外部 AD9914 控制。

器件清单与状态日期以 `F:/01_Laser/code/fpga/host/MEMORY.md` 为入口，迁移后用实际仓库路径。不要在技能内复制持续变化的版本号和测试数量。

## 盘点证据

- DAC 的 CW 标识 b9726/da766 与旧线性度标识 da9726/ad766 分属不同契约；不能只凭名称相近混用命令。
- point/sweep/scale 配置与外部自动测量分开核实；枚举有某模式不代表执行器已实现完整工作流。
- ADC 工程 YAML 和通用 ILA 能力不等于芯片寄存器驱动，也不等于实际物理通道已验收。
- 仪器驱动、Mock 测试、真实连接、板上电气结果分开报告；源码存在不等于发布 EXE 包含该能力。

## DDS 接入

- 当前用户路线为先 dds3_syncclk_test 子工程，再大工程合并；目标变化以用户新指令为准。
- 复用共享库的显式 profile 与结构化 dispatch；按确切设备/CELL_NAME/信号契约绑定，不猜探针序号。
- 保持 source/plan 无输出、prepare 不启动、start 明确启动的边界；stop 不关闭 RF。GUI 与服务层不得将 stop 标成关射频。
- SYNC_CLK enable 是 RTL 构建配置；FPGA CFR2 debug 常量不是 AD9914 寄存器回读。频谱改善须另有 A/B 仪器证据。
- DDS1/2/4/5 扩展前另核器件、SYSCLK、FTW 位宽和命令契约；不要套用 DDS3 32 位假设。
- 接入 GUI 时再实施 worker/服务生命周期/依赖打包和相应测试；仅更新说明不触发硬件操作或自动改大工程。
