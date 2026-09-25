# Skill 分类规范

分类按主要功能确定，每个逻辑 Skill 只属于一个主类。跨领域任务在分类页说明组合关系。

| 主分类 | 数量 | 用途 |
|---|---:|---|
| [FPGA/RTL/EDA 与硬件](categories/fpga-hardware/README.md) | 25 | 处理通用 RTL、Vivado、板级连接、调试及证据闭环。 |
| [MAROC 项目适配](categories/maroc/README.md) | 19 | 把通用硬件与文档流程应用到 MAROC 工程。 |
| [Laser/PDH 与精密测量](categories/laser-pdh/README.md) | 11 | 覆盖 Laser/PDH 电测、CW 板卡、仪器协同和操作报告。 |
| [学术研究与论文](categories/research/README.md) | 17 | 支持选题、文献、研究设计、论文结构和投稿检查。 |
| [演示文稿与视觉表达](categories/presentations/README.md) | 15 | 制作与检查学术汇报、项目演示和可编辑图示。 |
| [文档/PDF/表格办公](categories/documents/README.md) | 7 | 制作、检查和整理 Word、PDF、表格及办公资料。 |
| [图像与媒体](categories/media/README.md) | 7 | 处理图像、截图、照片、语音、转写及媒体产物。 |
| [知识库与 Obsidian](categories/knowledge-base/README.md) | 3 | 维护笔记结构、Obsidian 内容与独立知识工具。 |
| [Codex/Skill 元管理](categories/codex-skill-management/README.md) | 4 | 管理 Codex 运行状态、技能创建及相关辅助工具。 |
| [浏览器与自动化](categories/browser-automation/README.md) | 2 | 通过可观察的浏览器会话执行或调试页面任务。 |
| [MATLAB](categories/matlab/README.md) | 6 | 编写、审查、测试和迁移 MATLAB 代码。 |
| [软件与应用开发](categories/app-development/README.md) | 4 | 实现 ASP.NET、ChatGPT App、网页游戏和 WinUI 应用。 |
| [云部署与 Git 工作流](categories/cloud-git/README.md) | 6 | 处理站点部署、GitHub 审查与 CI 故障。 |
| [安全与系统维护](categories/security-system/README.md) | 4 | 分析软件安全风险和 Windows 系统性能。 |

合计 **130 个逻辑 Skill**、**123 个顶层目录**。分类与数量以 `registry/skills.json` 为准。

通用 FPGA／硬件能力与 MAROC 项目适配分开；Laser/PDH 分类包含 CW 上位机及仪器自动化。`ppt-maker` 的 7 个子 Skill 保留原路径，按各自用途分类，随父技能装载。
