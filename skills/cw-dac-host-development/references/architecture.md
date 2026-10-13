# 架构与接口

## 按目标包与能力分流

| 模式 | 识别与限制 |
|---|---|
| 33441 旧 DAC / 33442 capture-only | 显式旧版兼容；不可互换协议或顺手修改冻结服务。 |
| 33443 旧同步 CW（如旧 v7） | 按旧包说明运行；GUI 内嵌同步 ILA wait 的冻结限制仍适用。 |
| 33443 统一任务 | 检查包内伴随脚本、hello 的会话/代次/能力和该模式验证记录；不再一律称为候选。 |
| 五 DDS、手动操作、通用定时 ILA | 分别核实 dds_v1、manual_result_v1、ila_capture_v2 及当前服务实际返回；能力之间不互相替代。 |

工程已记录五 DDS GUI 集成、手动主动查询及通用定时 ILA；这是查证入口，不是任意旧 EXE 的能力声明。查 `docs/CW_DDS_INTEGRATION_V21.md`、`CW_MANUAL_CONTROL_V22.md`、`CW_V22_VALIDATION.md`、`GENERIC_ILA_PERIODIC_V23.md`、`ILA_V23_VALIDATION.md` 及选定包清单。后续版本仍重新核实，不固定“最新版本”或历史测试数量。

## 实现入口（相对项目根）

- `host/linearity_host/gui.py`：主线程快照、worker、消息回收和控件恢复。
- `unified_session.py` / `protocol.py`（同一 Python 目录）：共享连接、操作归属、预算、真实后端及 Mock。
- `manual_operations.py` / `dds_control.py`：手动操作身份/收尾与 DDS 参数边界。
- `ila_runner.py` / `ila_csv.py`：定时调度、采集证据、完整路径与流式格式化。
- `cw_runner.py`、`stimulus_gui.py`、`stimulus_runner.py`、`storage.py`：CW、联合采集与 SQLite；修改前检查当前实际入口。
- `tcl/cw_test_server.tcl` 按能力依赖 `unified_tasks.tcl`、`manual_control.tcl`、`ila_capture_v2.tcl`、DDS 库及契约/配置。引用 capture-only 指纹函数不等于启动 33442。

优先按目标模式复用已打开的 Vivado；source 只加载定义，不等于监听就绪。GUI 后台监听使用 start_server_bg，旧前台 vwait 不能当成后台模式。不要在活动硬件命令尚未结束时重载脚本。关闭上位机不等于关闭用户 Vivado。

## 任务与手动控制

统一任务采用会话身份与唯一 task_id；提交、查询、取消分别取证。重复 ID 的幂等和参数冲突拒绝须由对应版本回归证明；服务重启或任务淘汰后旧结果未知。连接、查询、烧写/LTX、等待、上传分别设置有限预算，从当前实现/配置读取，不用一个 TCP 超时代表所有阶段。

手动免回复发送后只表示请求已发送，用户主动查询最近结果（当前协议 manual_result_v1）；旧版自动轮询只保留为对应版本历史行为。服务查询成功也不证明芯片模拟输出。CW 自动业务命令序列、取消和恢复保持自身契约，不套用手动“发送即收尾”模式。

## 通用 ILA 定时采集

- 使用 Hardware Manager 已选设备与已识别 ILA，不要求 CW 专用核或指定 BIT/LTX；命名调试信息仍需匹配。启动前与武装前核对会话、设备、关联属性、完整 CELL_NAME、探针结构及深度。
- 开始时固定参数快照；一个执行线程负责整计划，等待阶段仍占用硬件，不为每个点新增心跳线程。首轮立即，后续按单调时钟固定时点；错过的周期跳过，不补抓、不重叠。
- 每轮按核顺序采集，同核多探针共享一次整核采集；不同核不宣称同步。指定次数只统计所有核均成功保存的完整轮次，跳过/部分轮次不算成功。
- 立即触发与采集条件分别设置；当前 ila_capture_v2 的 trigger position、ALWAYS 和 trigger_now 细节查模式文档。正常或确认取消后仅在身份仍一致时恢复原软件属性，不重新武装；未知结果不补发恢复。
- 停止只取消本次 ILA；同步上传/导出须等 Vivado 返回。不可把取消监视、reset_hw_ila 或 GUI 空闲当作核已停止。
- 原始 CSV 保留、格式化副本流式生成；完整路径优先，短名歧义报错。转换读取 Radix 行/源 DISPLAY_RADIX，旧导出才走明确兼容规则；auto/digital 可保留文本。analog 归一化不等于电压校准，1 位信号保留 0/1。
- 索引逐项追加，manifest 原子更新；只消费 completed 数据，核对样本数、SHA 和终态。partial、失败或未提交文件不能计入成功。armed_at 是软件时间，不是硬件采样沿时间戳。
