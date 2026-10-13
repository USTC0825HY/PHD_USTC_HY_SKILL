# 职责与证据

GUI/Runner控制SDG、回读、稳定等待、ILA请求、CSV校验与数据库。Vivado处理BIT/LTX和JTAG。工程师确认接线、参考面、输入上限及批准。

经验证的统一版本source cw_test_server.tcl后执行 `::cw_hy::start_server_bg 33443`；旧capture-only执行start_capture_server 33442。2026-09-20的候选状态是旧包历史；当前按所选包内依赖/协议/验证记录判定。旧v7不具备任务协议，GUI内嵌ILA冻结只作用于对应版本。33441不是联合采集协议。核对包来源、监听、hello/capabilities和当前验证报告；没有报告不称已验收。

单点：安全校验→设置源→OPC/回读→稳定→ILA→CSV校验→SQLite事务→manifest。正式任务全点预采，检查回读、位宽、深度、样本数和削顶后人工批准。改板、方案或指纹需重新验证。

新联合采集每次运行一个目录，CSV平铺，前缀/固定条件/扫描值/微秒时间戳命名；cap/attempt区分多组与重采。run_manifest.json固定，旧任务保留旧布局。

中止独立请求SDG OFF；未提交CSV为aborted_uncommitted。具备任务协议时超时按同session的task_id查询，不自动重发；旧服务结果未知时保留现场，不伪造task_id恢复。同步上传/导出取消待返回。OFF不证明端口0V。

保存方案、源型号/固件/资源/通道/回读、BIT/LTX摘要、ILA指纹、CSV/样本数/SHA、SQLite和manifest。Mock、实机流程、目标器件指标分别报告。
