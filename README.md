# PHD_USTC_HY_SKILL

面向个人科研与工程工作的 Codex/Claude Skill 规范仓库。本仓库将本机分散的 Skill
去重后收拢为一个可审计、可版本化、可恢复的“唯一事实源”。

> 当前采用 **private-first** 策略。部分 Skill 的来源、著作权和再发布许可尚未逐项确认，
> 在许可证复核完成前，不应把仓库改为公开可见。

## 当前清单

| 功能主体 | Skill 数量 |
|---|---:|
| FPGA/RTL/EDA 与硬件 | 43 |
| 学术研究与论文 | 16 |
| 演示文稿与视觉表达 | 14 |
| 文档/PDF/表格办公 | 6 |
| Laser/PDH 与精密测量 | 5 |
| 图像与媒体 | 4 |
| 知识库与 Obsidian | 3 |
| Skill/插件元管理 | 3 |
| 浏览器与自动化 | 1 |
| **合计** | **95** |

95 个逻辑 Skill 被保存为 88 个顶层目录和 7 个 `ppt-maker` 嵌套子 Skill。
本机重复副本不会重复入库。

## 仓库结构

```text
skills/                  唯一规范副本
registry/skills.json     完整机器可读注册表
registry/skills.csv      便于人工筛选的扁平清单
profiles/                不同运行环境的装载清单
scripts/                 校验、哈希刷新和本地装载工具
docs/                    分类、维护和发布规范
reports/                 可提交的发布前检查报告
```

注册表记录每个 Skill 的分类、规范路径、来源类型、内容哈希、许可证证据和发布策略。
它不记录本机绝对路径，也不把 Codex 系统 Skill、插件缓存或依赖目录纳入版本控制。

## 发布前验证

```powershell
python .\scripts\validate_registry.py --repo . --write-report .\reports\preflight.json
```

修改 `skills/` 后先刷新哈希，再重新校验：

```powershell
python .\scripts\refresh_hashes.py --repo .
python .\scripts\validate_registry.py --repo . --write-report .\reports\preflight.json
```

## 恢复到本机

装载脚本默认只预演，不覆盖已有目录：

```powershell
.\scripts\materialize.ps1 -Profile codex -TargetRoot C:\path\to\skills
.\scripts\materialize.ps1 -Profile codex -TargetRoot C:\path\to\skills -Apply
```

支持 `codex`、`cc_switch` 和 `all` 三种 profile。目标位置已有同名 Skill 时会跳过，
避免把本机改动静默覆盖。`ppt-maker` 的 7 个子 Skill 随父目录一起恢复，不会重复复制
为顶层目录。

## 维护原则

- 一个逻辑 Skill 只维护一个规范副本；跨平台差异由 profile 或薄适配层表达。
- 通用能力与 MAROC/Laser 等项目适配层分离，减少内容复制和长期漂移。
- 每次变更都更新注册表哈希，并保留可复现的发布前检查报告。
- 未明确授权的第三方内容保持私有，确认许可证后再逐项调整发布策略。

详细规则见 [全盘审计摘要](docs/AUDIT_2026-07-26.md)、[分类规范](docs/CLASSIFICATION.md)、
[维护手册](docs/MAINTENANCE.md)和 [GitHub 发布检查表](docs/GITHUB_UPLOAD_CHECKLIST.md)。
