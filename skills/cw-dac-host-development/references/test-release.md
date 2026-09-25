# 测试与发布

发现可用Python/Tcl及依赖，不默认系统python可用；构建venv可能版本不同。从host运行 `python -m pytest tests -q`，项目根运行 `tclsh tcl/cw_test_server.tcl --selftest`，报告实际数量和失败。

Fake VISA/Mock ILA覆盖延迟、断线、重复任务、取消、普通ADC、多同名ILA、失败证据。Tk在构建环境按真实按钮路径冒烟；真实缩放和实板未测就明确未测。

选择未使用vN目录，复制spec并改名，用python -m PyInstaller构建。按实际source/import依赖列出文件和SHA-256；统一候选至少核对cw_test_server.tcl、unified_tasks.tcl、capture_only_server.tcl、cw_hy_probe_contract.tcl以及JSON/YAML配置。不能只复制主Tcl。不覆盖旧release/runtime。EXE --self-check、资源哈希一致、zip、启动脚本优先新包并保留回滚。

离线开发交付记录Python/Tcl回归、适用的GUI冒烟和打包检查；纯技能修订不要求硬件业务运行。硬件验收只在当前授权覆盖设备、范围和动作时进行，分别记录大LTX、GUI响应、取消、实际采集与SDG关断；未测写未验收，不能把候选写成已发布或已修复。

更新简短MEMORY和验证报告，技能quick_validate并核对引用。Git先看暂存/未跟踪/忽略与大文件策略；提交和推送均须用户明确授权且仅含相关文件。沿用当前任务既有授权，历史任务授权不继承。实机烧写和ILA仅在当前授权范围内执行。
