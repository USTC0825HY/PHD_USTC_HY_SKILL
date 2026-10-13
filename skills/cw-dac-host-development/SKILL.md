---
name: cw-dac-host-development
description: Develop, diagnose, test and release the linearity_automation Tk host for CW DAC/ADC, five-DDS control, generic VIO/ILA and instrument workflows. Use for host capability inventories, service/GUI failures, timed ILA capture and package verification; keep firmware and physical measurement conclusions in their own evidence workflows.
---

# CW 上位机开发与排障

先定位用户指定的 `host/linearity_automation`，读取最近的 AGENTS.md/MEMORY.md；不要回到旧 projects 开发目录。功能盘点另读 host/MEMORY.md。维护源码在项目 `skills/cw-dac-host-development`，安装目录是副本，同步遵循 skills/MAINTENANCE.md。

运行脚本前按 [运行时验证](references/runtime-validation.md) 探测实际 Python 版本和所需导入；优先复用可执行专用环境。

## 选择所需引用

- 服务、线程、手动控制或通用 ILA：[架构与接口](references/architecture.md)。
- 连接、超时、取消、探针或文件失败：[故障定位](references/diagnostics.md)。
- 回归、打包或技能同步：[测试与发布](references/test-release.md)。
- 器件能力、五路 DDS 或跨模块任务：[host 与 DDS 边界](references/host-device-boundaries.md)。
- 联合频率/幅度预采与证据用 `fpga-substitute-board-workflow-validation`；SCPI/VISA 驱动用 `sdg-dmm-automation`。不将本工程预采规则推广到所有仪器任务。

## 必守边界

1. 先核对目标源码/发布包、实际依赖、服务 hello/capabilities 和对应模式验证记录。端口、版本名称、源码存在及历史 MEMORY 均不能独立证明运行能力或实板验收。缺失能力时明确降级或停止依赖功能，不自动升级服务。
2. 主线程读取 Tk 配置并形成纯数据快照；worker 不访问 Tk，结果经队列回主线程显示。采集、发送、取消与关闭须遵守同一会话的操作归属，不能另开服务抢占板卡。
3. 区分旧同步服务、统一任务、手动免回复发送和通用 ILA。手动发送成功不等于 Tcl 成功，更不等于物理输出完成；真实采集必须确认数据与文件完成。
4. 超时保留 session_id/task_id 或手动操作编号；按可用协议查询。未知结果不自动重发烧写、控制或采集，重启/记录淘汰后不能补判成功。Vivado 同步阶段须等待返回才可处理取消。
5. 通用 ILA 只作用于选定核，不自动烧写、关联 LTX、操作 ADC/VIO/DAC 或关闭 Vivado；SDG 输出关断另行确认。完整核/探针身份不可用短名代替。
6. 默认离线 Fake VISA/Mock ILA。业务源码、离线验证、发布包、硬件观测和模拟测量分别取证。纯技能修订不触发应用打包、硬件动作或 Git 提交。
