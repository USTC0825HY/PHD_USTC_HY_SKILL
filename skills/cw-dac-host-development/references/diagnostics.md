# 故障定位

取证顺序：EXE来源/commit→监听端口及进程→Vivado Console→GUI日志→task_id与阶段→BIT/LTX摘要。旧“已连接”标签不证明当前在线。

先区分已发布同步服务和统一候选。只有确认任务协议可用时才使用task_id恢复；旧v7不能因重新source候选文件就被称为已验收升级。复用GUI前检查对应模式的验收和旧版冻结限制。

- 10061：Loaded不是READY；在已打开Vivado source对应包脚本后执行 `::cw_hy::start_server_bg 33443`。
- busy：查活动任务，不新开第二套服务抢板卡。
- 大LTX/烧写：区分TCP、PROGRAM、refresh和CW契约；预算延长不是成功证明。
- 超时/迟到：废弃socket和残留buffer，同session按任务ID恢复；服务重启/任务不存在则结果未知，不重发。
- ILA冻结：核对是否旧同步wait；新版短轮询仍不能中断同步上传。reset_hw_ila重置配置，不是停止命令。
- CSV：查路径长度、partial、非空、样本数、SHA、manifest与SQLite提交。保留失败文件。
- GUI：进程内真实点击路径冒烟，拦截messagebox和硬件工厂，不能只猜截图。

换板、烧写、LTX关联后重新检查和预采，不能用旧内部波形证明模拟端口。
