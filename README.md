# PHD_USTC_HY_SKILL

面向科研、FPGA/硬件、Laser 精密测量、MATLAB 和文档工作的个人技能仓库。远程地址为 [USTC0825HY/PHD_USTC_HY_SKILL](https://github.com/USTC0825HY/PHD_USTC_HY_SKILL)。

## 当前清单（2026-10-13）

本次同步当前 Codex 全局个人技能 **87 项**，包括技能入口、引用、脚本、模板、许可证和已有测试材料；排除系统内置技能、插件缓存、虚拟环境和 Python 缓存。

仓库共 **117 个逻辑 Skill**、**110 个顶层目录**，其中包含 **7 个**原有嵌套技能。除当前 87 项外，原远端的 **30 项历史技能**继续保留，分类页逐项标记；它们不进入当前 Codex profile，也不据此判断为已安装或仍在使用。

15 项已移除的个人技能不进入当前注册表或装载清单，Git 历史仍可追溯。具体名单、同步哈希和历史保留项见 [快照清单](reports/global-snapshot-20261013.json)。

## 按任务选择技能

| 功能分类 | 数量 | 适用任务 |
|---|---:|---|
| [FPGA/RTL/EDA 与硬件](docs/categories/fpga-hardware/README.md) | 26 | 处理通用 RTL、Vivado、板级连接、调试及证据闭环。 |
| [MAROC 项目适配](docs/categories/maroc/README.md) | 19 | 把通用硬件与文档流程应用到 MAROC 工程。 |
| [Laser/PDH 与精密测量](docs/categories/laser-pdh/README.md) | 12 | 覆盖 Laser/PDH 电测、CW 板卡、仪器协同和操作报告。 |
| [学术研究与论文](docs/categories/research/README.md) | 17 | 支持选题、文献、研究设计、论文结构和投稿检查。 |
| [演示文稿与视觉表达](docs/categories/presentations/README.md) | 13 | 制作与检查学术汇报、项目演示和可编辑图示。 |
| [文档/PDF/表格办公](docs/categories/documents/README.md) | 6 | 制作、检查和整理 Word、PDF、表格及办公资料。 |
| [图像与媒体](docs/categories/media/README.md) | 5 | 生成图像、获取截图、转写音频及维护历史媒体工具。 |
| [知识库与 Obsidian](docs/categories/knowledge-base/README.md) | 3 | 维护笔记结构、Obsidian 内容与独立知识工具。 |
| [Codex/Skill 元管理](docs/categories/codex-skill-management/README.md) | 4 | 管理 Codex 运行状态、技能创建及相关辅助工具。 |
| [浏览器与自动化](docs/categories/browser-automation/README.md) | 2 | 通过可观察的浏览器会话执行或调试页面任务。 |
| [MATLAB](docs/categories/matlab/README.md) | 6 | 编写、审查、测试和迁移 MATLAB 代码。 |
| [云部署与 Git 工作流](docs/categories/cloud-git/README.md) | 3 | 处理 GitHub 审查意见、CI 故障与 Git 提交流程。 |
| [安全与系统维护](docs/categories/security-system/README.md) | 1 | 诊断和优化 Windows 系统性能。 |

阅读所选技能的完整 `SKILL.md` 和任务所需引用后执行。分类数量包含历史保留项；当前个人安装列表见 [Codex profile](profiles/codex.json)。插件提供的文档、演示、表格和 PDF 能力由运行会话发现，不复制插件缓存，也不绑定固定插件版本。

## 本轮维护重点

- **Laser 证据与文档：** 分析包严格验收，公式按范围修复，手册编号保护标题和列表，局部报告检查新增缺陷与图片来源，字段刷新在副本上完成。检查层通过不等于算法、仪器或硬件验证通过。
- **CW 与仪器：** 按所选源码或发布包的依赖、协议和验证记录选择流程；覆盖五路 DDS 与通用 ILA，保留旧 DDS3、v7 及未知结果不自动重试的边界。
- **MATLAB 六技能：** 保持版本、数值行为和输入契约，沿用现有测试形式；无 MCP 时发现本地运行时，准确区分已执行与静态检查。
- **中文与研究：** `qu-ai-wei` 按授权润色，保护事实与语体；构思与新颖性核查按可追溯检索证据分工，查询失败不能伪装为零结果。
- **PDF：** 个人同名技能保留为目录、运行时和插件契约的薄适配；正式输出遵守项目目录，未完成渲染不能宣称版面验收通过。

这些是已安装技能的同步，未在本次发布中改写算法、真实报告或实验资料。验证范围见 [发布记录](docs/UPDATE_2026-10-13.md)。

## 仓库结构与维护源

```text
skills/                   可恢复的技能发布副本
docs/categories/          分类导航与逐项功能说明
registry/skills.json       来源、分类、维护策略与内容哈希
registry/skills.csv        扁平清单
profiles/                 codex / cc_switch / all 装载范围
scripts/                  注册表校验、哈希刷新与本机装载
reports/                  快照及发布检查记录
```

当前维护源并非一律在本仓库：CW 上位机、仪器自动化、替代板验证三项由工程内技能目录维护，其余当前个人技能由 Codex 用户技能目录维护。本仓库保存发布快照；`registry` 的 `maintained_source`、`sync_policy` 和 `installed_in_codex` 区分来源与现状。历史保留项本次不从旧安装目录重新覆盖。

## 校验与恢复

先发现可用的 Python 3.10+，再执行；不要把系统默认 Python 可启动等同于版本与依赖满足要求。

```powershell
python .\scripts\refresh_hashes.py --repo .
python .\scripts\validate_registry.py --repo . --write-report .\reports\preflight.json
python .\scripts\validate_readmes.py --repo .
git diff --check
```

恢复当前个人技能时明确选择 `codex`，默认预演，已有同名目录会跳过：

```powershell
.\scripts\materialize.ps1 -Profile codex -TargetRoot C:\path\to\skills
.\scripts\materialize.ps1 -Profile codex -TargetRoot C:\path\to\skills -Apply
```

`cc_switch` 是历史兼容集合，`all` 包括仓库中的历史保留项；两者均不等于当前 Codex 安装列表。恢复前核对工作区路径、外部依赖及工程规则，不将本机路径视为通用默认值。

## 来源与许可

保留原许可证、来源和署名，不声明统一覆盖全部技能的开源许可证。注册表中的未确认状态不能解释为获得公开再发布许可。仓库当前公开，既有可见性也不代表许可审查完成；参见 [许可证策略](LICENSE_POLICY.md)、[发布检查表](docs/GITHUB_UPLOAD_CHECKLIST.md)及 [维护说明](docs/MAINTENANCE.md)。
