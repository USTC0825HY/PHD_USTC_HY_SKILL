# Codex/Skill 元管理

管理 Codex 运行状态、技能创建及相关辅助工具。

按平台问题选择工具；具体技能安装与发布仍核对来源和许可。

本类共 **4 个逻辑 Skill**。详情以各技能的 `SKILL.md` 为准。

| Skill | 主要功能 |
|---|---|
| [codex-log-guard](../../../skills/codex-log-guard/SKILL.md) | 诊断 Codex 日志和 SQLite 写入量异常。 |
| [codex-reset-credits](../../../skills/codex-reset-credits/SKILL.md) | 查询 Codex 重置额度及到期时间。 |
| [openai-docs](../../../skills/openai-docs/SKILL.md) | 查询 OpenAI 产品与 API 官方文档并引用来源。 |
| [ppt-personal-intro](../../../skills/ppt-maker/subskills/personal-intro/SKILL.md) | 制作个人介绍、嘉宾简介或作品集 PPT。 |

`ppt-maker` 的场景子 Skill 保持在其 `subskills/` 目录，随父技能装载，不作为独立顶层目录复制。
