# 架构与接口

以下统一接口是2026-09-20工作区候选实现的源码说明，不是发布或硬件验收声明。旧v7不含unified_tasks.tcl。先查包内文件、实际能力及当前项目验证报告；后续发布清单覆盖本日期快照。

| 服务 | 身份与选择依据 |
|---|---|
| 33441 | 旧DAC协议，不是联合采集协议 |
| 33442 | 旧capture-only，显式兼容 |
| 33443旧CW/v7 | 同步CW/VIO/ILA；GUI内嵌ILA冻结限制仍适用 |
| 33443统一候选 | 伴随模块齐全，hello确认所需capabilities；端口不证明版本 |

项目host/linearity_host：gui.py管理Tk/worker；unified_session.py管理共用连接、任务ID及预算；protocol.py保留旧协议和Mock；stimulus_gui.py/stimulus_runner.py负责联合采集与审批；cw_runner.py负责CW；storage.py负责SQLite。

统一33443对应tcl/cw_test_server.tcl + unified_tasks.tcl + CW契约；复用capture_only_server.tcl的指纹函数但不启动33442。旧33441是DAC协议、33442是capture-only；按发布能力选择，不互换。

候选hello返回session_id、hardware_generation及capabilities；task_submit携带唯一task_id和operation；task_status返回state/stage/elapsed_seconds/result/error；task_cancel请求停止。相同ID不应重复执行，参数不同应拒绝；行为须由当前回归证明。服务重启后旧任务结果未知。

预算：连接10秒、查询30秒、烧写600秒、LTX600秒、ILA按方案、上传导出180秒，可调整；通信覆盖阶段预算，但不能强制打断Vivado同步命令。

ILA短时限wait配合after，CW短轮询。program/refresh/upload/write仍同步。取消监视不证明硬件核已停止，SDG关断独立。协议离线通过不等于大LTX或真实ILA已验收，必须看当前验证报告。

源码入口相对项目根：host/linearity_host/unified_session.py、tcl/unified_tasks.tcl。候选测试入口host/tests/test_unified_session.py、host/tools/smoke_unified_gui.py；结果查docs内对应验证记录，缺失就写“未验收”，不沿用旧测试数量或mock板证据。
