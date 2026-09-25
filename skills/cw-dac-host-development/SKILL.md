---
name: cw-dac-host-development
description: Develop, diagnose, test and release the linearity_automation Tk host for CW DAC, generic VIO/ILA and SDG joint capture. Use for shared Vivado sessions, large LTX/programming timeouts, GUI workers, cancellation, evidence recovery and packaging.
---

# CW DAC与联合采集开发

先读工作区和项目AGENTS/MEMORY，再核对Git。发现当前 `host/linearity_automation`，不要使用旧projects路径。当前工作区在 `F:/01_Laser/code/fpga`，迁移时以实际目录为准。

- 架构、协议、任务ID：读 [architecture.md](references/architecture.md)。
- 超时、连接、取消、CSV故障：读 [diagnostics.md](references/diagnostics.md)。
- 测试与发布：读 [test-release.md](references/test-release.md)。
- host 功能盘点、DDS 共享库接入或跨模块边界：读 [host-device-boundaries.md](references/host-device-boundaries.md)，并核对 `host/AGENTS.md` 与 `host/MEMORY.md`。
- 联合采集操作用 `fpga-substitute-board-workflow-validation`；SCPI用 `sdg-dmm-automation`。

## 约束

先核对EXE/服务包、当前源码和验证报告。2026-09-20技能审计时，已发布v7仍用同步ILA等待，工程内unified_session.py/unified_tasks.tcl是未发布候选。端口33443或源码存在不证明升级成功。旧v7 GUI内嵌ILA冻结限制保留，采集采用其已记录的无头流程；只有包内依赖齐全、hello/capabilities确认且对应模式验收后，才使用统一任务流程。后续状态由新发布清单覆盖本日期快照。

主线程捕获Tk变量→纯数据context→worker→消息队列→主线程弹窗。状态刷新不得调用有弹窗副作用的检查。

统一候选模式优先复用已打开Vivado，受上述版本与验收门槛约束；source不等于监听。上位机关闭只断连，不关闭用户Vivado。BIT烧写、LTX关联、CW专用契约分别报告；普通ADC不要求CW VIO。

具备任务协议时，超时按同session的task_id查结果，不重发烧写/采集；旧服务无此接口，结果未知时保留现场，不伪造任务恢复。同步阶段取消待返回，不能虚报已停止。SDG安全关断独立执行。未提交CSV保留，不作有效点。

已有明确授权沿用，超出设备/范围/动作再询问。开发默认Fake VISA/Mock ILA。发布递增目录，不能覆盖运行EXE。Mock、实机流程、模拟端口实测结论分别报告。

技能源码维护在工程skills/，用户目录为安装副本；不硬编码测试数量和最新EXE版本。
