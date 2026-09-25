# PHD_USTC_HY_SKILL

面向科研、FPGA/硬件和软件工程的个人 Skill 仓库。`skills/` 保存规范副本，注册表记录每项技能的身份、来源、分类与哈希，profile 决定装载范围。

## 当前状态

注册表包含 **130 个逻辑 Skill**，分布在 **123 个顶层目录**；其中 `ppt-maker` 有 **7 个**嵌套场景 Skill。

GitHub 远端当前为 **Public**。本地分支已补齐 35 个此前缺失的技能，**尚未推送**。部分技能的许可证和项目内容仍待审查；遵循 [发布检查表](docs/GITHUB_UPLOAD_CHECKLIST.md) 与 [许可证策略](LICENSE_POLICY.md)，不得将这批内容直接推送到公开远端。

## 按任务选择 Skill

先进入最贴近任务的分类页，选择技能后阅读其 `SKILL.md`；涉及具体项目时，按分类页说明结合通用技能与项目适配技能。

| 功能分类 | 数量 | 适用任务 |
|---|---:|---|
| [FPGA/RTL/EDA 与硬件](docs/categories/fpga-hardware/README.md) | 25 | 处理通用 RTL、Vivado、板级连接、调试及证据闭环。 |
| [MAROC 项目适配](docs/categories/maroc/README.md) | 19 | 把通用硬件与文档流程应用到 MAROC 工程。 |
| [Laser/PDH 与精密测量](docs/categories/laser-pdh/README.md) | 11 | 覆盖 Laser/PDH 电测、CW 板卡、仪器协同和操作报告。 |
| [学术研究与论文](docs/categories/research/README.md) | 17 | 支持选题、文献、研究设计、论文结构和投稿检查。 |
| [演示文稿与视觉表达](docs/categories/presentations/README.md) | 15 | 制作与检查学术汇报、项目演示和可编辑图示。 |
| [文档/PDF/表格办公](docs/categories/documents/README.md) | 7 | 制作、检查和整理 Word、PDF、表格及办公资料。 |
| [图像与媒体](docs/categories/media/README.md) | 7 | 处理图像、截图、照片、语音、转写及媒体产物。 |
| [知识库与 Obsidian](docs/categories/knowledge-base/README.md) | 3 | 维护笔记结构、Obsidian 内容与独立知识工具。 |
| [Codex/Skill 元管理](docs/categories/codex-skill-management/README.md) | 4 | 管理 Codex 运行状态、技能创建及相关辅助工具。 |
| [浏览器与自动化](docs/categories/browser-automation/README.md) | 2 | 通过可观察的浏览器会话执行或调试页面任务。 |
| [MATLAB](docs/categories/matlab/README.md) | 6 | 编写、审查、测试和迁移 MATLAB 代码。 |
| [软件与应用开发](docs/categories/app-development/README.md) | 4 | 实现 ASP.NET、ChatGPT App、网页游戏和 WinUI 应用。 |
| [云部署与 Git 工作流](docs/categories/cloud-git/README.md) | 6 | 处理站点部署、GitHub 审查与 CI 故障。 |
| [安全与系统维护](docs/categories/security-system/README.md) | 4 | 分析软件安全风险和 Windows 系统性能。 |

## 仓库结构

```text
skills/                   Skill 规范副本；每项以 SKILL.md 为入口
docs/categories/          14 个功能分类页，提供任务入口和逐项功能说明
registry/skills.json      机器可读清单：分类、来源、许可状态和内容哈希
registry/skills.csv       供人工筛选的扁平清单
profiles/                 codex、cc_switch、all 装载名单
scripts/                  注册表校验、哈希刷新和本机装载工具
reports/                  发布前校验记录
```

`registry` 描述 Skill，`profiles` 选择需要装载的顶层目录；`ppt-maker/subskills/` 随父目录装载。系统内置 Skill、插件缓存和依赖目录不纳入仓库。

## 维护与装载

修改 `skills/` 或注册表分类后，刷新哈希并核对注册表、分类页和链接：

```powershell
python .\scripts\refresh_hashes.py --repo .
python .\scripts\validate_registry.py --repo . --write-report .\reports\preflight.json
python .\scripts\validate_readmes.py --repo .
git diff --check
```

本机装载默认预演，已有同名目录会跳过：

```powershell
.\scripts\materialize.ps1 -Profile codex -TargetRoot C:\path\to\skills
.\scripts\materialize.ps1 -Profile codex -TargetRoot C:\path\to\skills -Apply
```

分类规则见 [CLASSIFICATION.md](docs/CLASSIFICATION.md)；维护步骤见 [MAINTENANCE.md](docs/MAINTENANCE.md)。
