---
name: fpga-substitute-board-workflow-validation
description: Configure and validate SDG6052X or SDG6032X-E joint frequency/amplitude capture with Vivado ILA, manual GUI or YAML, full-point preflight and CSV/SQLite/manifest evidence. Use for YB2208, AD9245, AD677, ADC128, MAROC, SPIROC and substitute-board workflow tests.
---

# SDG与Vivado联合采集

先读项目AGENTS/MEMORY并发现当前工程。开发发布用cw-dac-host-development，SCPI用sdg-dmm-automation。

## 顺序

明确目标板实际采集或替代板验证→核对接线/通道/负载/上限/BIT/LTX/ILA→手动配置或模板/YAML→应用离线校验→Vivado服务监听→安全连接检查→人工确认→全点预采→检查证据→批准正式扫描。

目标板不强制写“替代”；替代板只能证明流程，不证明目标ADC性能。全点预采/正式审批是linearity_automation项目策略，不泛化为所有FPGA或仪器任务。单点/三点仅用于指定驱动调试，不强制插入日常全点预采。

服务按版本能力选择：旧capture-only33442显式兼容；33443区分已发布同步CW与统一候选。2026-09-20审计时统一模块尚未发布；核对包来源、hello/capabilities和对应模式验收。旧v7 GUI内嵌ILA冻结限制保留。source不等于监听，复用Vivado需符合实际版本限制。已有明确授权沿用，超范围才询问；开发默认离线。

SDG停止独立于ILA等待。取消/失败CSV保留，未提交点不作为有效点；续测复用原方案、目录、数据库，不覆盖。预采不等于正式批准。

读 [workflow-contract.md](references/workflow-contract.md)、[yaml-gui-contract.md](references/yaml-gui-contract.md)；[maroc-example.md](references/maroc-example.md)只是历史替代案例。ILA内部信号不证明模拟端口电压、带宽、饱和或噪声；half_vpp仅是名义范围。
