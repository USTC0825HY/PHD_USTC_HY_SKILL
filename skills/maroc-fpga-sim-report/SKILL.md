---
name: maroc-fpga-sim-report
description: 生成 MAROC FPGA 仿真联合测试报告（中文、可审计、可复盘），适用于 TOP 联调、command+slowcontrol、slowcontrol 模块级报告；当用户要求“仿真测试手册/联合仿真报告/测试矩阵/case-by-case/签核结论/Mermaid流程图”时使用。
---

# MAROC FPGA Simulation Report Skill

## 何时使用
在以下请求触发：
1. 用户要求输出正式仿真测试手册或联合仿真报告。
2. 用户要求可审计、可复盘、可签核的 Markdown 报告。
3. 用户要求包含测试矩阵、case-by-case 分析、checker/counter/log 说明。
4. 用户要求在报告开头先解释信号链理论机制，并附 Mermaid 图。
5. 用户要求把 `xsim` 调试经验、脚本入口、波形分组、串行比对结果并入报告或手册。
6. 用户要求梳理 `sim_parser / sim_sc829 / top` 三层验证边界，或解释当前仿真层为什么不包含某个模块。

## 固定产出原则
1. 仅基于可验证事实：TB 文件、DUT 连接、脚本、日志、CSV、比对报告。
2. 不臆造未在 TB/RTL/脚本中出现的协议细节。
3. 显式写出 stub/mock 边界以及“不能签核什么”。
4. 理论机制、调试入口、case 实测、最终签核分章节，不混写。
5. 输出完整 Markdown 正文，不输出提纲草稿。
6. 只在确有证据时写“串行码流正确”，优先引用逐 bit CSV、汇总 CSV、独立 compare report。

## Progressive Disclosure
按任务类型最少加载：
1. 先读 `references/report-structure.md`
   - 默认报告主结构、章节顺序、附录约定
2. 再读 `references/pass-fail-rules.md`
   - PASS/FAIL、串行签核、不可签核边界
3. 如果用户涉及 `xsim`、Vivado、simset、脚本入口
   - 读 `references/simset-script-map.md`
4. 如果用户涉及波形讲解、分组、重点信号、常见误读
   - 读 `references/wave-debug.md`
5. 如果用户说“手册臃肿/流程不清/需要图”
   - 读 `references/report-writing-extensions.md`
6. 如果任务是 `CY_driver_new` 模块级 USB/FX2LP 教学或报告
   - 读 `references/cy-driver-module.md`

## 执行流程
1. 先判断验证层级：
   - `cy-driver`：`CY_driver_new + tb_cy_driver_new_xsim`
   - `sim_parser`：`maroc_usb_packet_parser + SlowControl_MAROC`
   - `sim_sc829`：`command_MAROC + SlowControl_MAROC`
   - `top`：`TOP_MAROC`
2. 读取该层的 TB、相关 DUT 文件、运行脚本、最新仿真日志。
3. 如果是 `xsim` 问题，先区分：
   - compile：`xvlog.log / compile.bat / *_vlog.prj`
   - elaborate：`elaborate.log`
   - runtime/fixture：`simulate.log / fixtures / stage_mem_for_vivado.tcl`
4. 先构建“模块定位/验证边界/信号链”，再进入测试矩阵和 case-by-case。
5. 如果用户同时要“怎么做”和“为什么这样做”，把“最前置操作”放在手册最前。
6. 如果涉及最终串行签核，优先补：
   - capture 方法
   - expected source
   - compare CSV / summary CSV / compare report
   - 最终 bit-by-bit 结论

## 报告结构（默认）
1. 最前置操作（当用户目的是跑 `xsim` 或快速上手）
2. 模块定位与接口语义
3. 信号链与理论机制
4. 三层验证边界与重点信号
5. Testbench 文件结构说明
6. 验证目标与边界
7. 测试矩阵
8. Case 设置思路与信号流检查流程
9. Case-by-case 测试分析
10. 关键检查器与自动判定逻辑
11. 关键结果总结
12. 最终串行码流签核结论（如适用）
13. 风险、边界与未覆盖项
14. 最终判定
15. 附录A/B/C...（`xsim` 操作、波形分组、截图模板、实验记录模板等）

## 强制检查清单
1. 报告开头必须先写模块定位、边界和信号链，不能直接从 case 开始。
2. 至少 2 张 Mermaid 图：总体链路图 + 流程图；用户混淆层级时，再补三层边界图。
3. 每个主回归 case 必须含：目的、激励、关注信号、理论预期、TB 检查方法、结果结论。
4. 当用户说“case 设置思路和信号流不清晰”，必须补：
   - 正例设置流程图
   - 反例设置流程图
   - 信号观察流程图
   - case 到“先看哪些信号/最终判据”的对照表
5. 当手册涉及 `xsim` 操作时，优先给仓库中真实存在的 `PS1/Tcl/Python` 入口，不要虚构工具链。
6. 当结论涉及 `o_sc_dout` 正确性时，必须写明 capture 口径和 fixture 来源。
7. 对 `o_sc_byte_valid` 的描述，默认写成“覆盖 104 个 byte 的连续有效窗口”，不要误写成“104 个独立脉冲”，除非波形确实如此。

## 写作风格
1. 中文、专业、克制。
2. 用词可审计，避免口语化与模糊表述。
3. 结论明确，避免“可能/估计/待补”。
4. 优先使用 TB/RTL 中的真实任务名、状态名、信号名。

## 参考模板
- 结构模板见 `references/report-structure.md`
- 常用判据模板见 `references/pass-fail-rules.md`
- simset 与脚本地图见 `references/simset-script-map.md`
- 波形分组与信号误读说明见 `references/wave-debug.md`
- 手册瘦身与流程图写法见 `references/report-writing-extensions.md`
- `CY_driver_new` 模块级说明见 `references/cy-driver-module.md`
