# 维护手册

## 日常修改

1. 在 `skills/<skill-name>/` 的规范副本中修改内容。
2. 新增或删除文件后运行 `refresh_hashes.py`。
3. 运行 `validate_registry.py`，确认错误和疑似密钥均为零。
4. 检查 `git diff`，提交注册表与 Skill 内容的对应变更。

```powershell
python .\scripts\refresh_hashes.py --repo .
python .\scripts\validate_registry.py --repo . --write-report .\reports\preflight.json
git diff --check
```

不要直接修改 `staged_skill_sha256` 或 `staged_tree_sha256`。哈希代表 GitHub 规范副本，
应由工具计算。文本文件计算哈希时统一按 UTF-8/LF 规范化，因此不会因为 Windows 与
Linux 的换行符差异产生虚假漂移；二进制文件按原始字节计算。

## 新增 Skill

- 目录名和 frontmatter `name` 使用小写字母、数字与连字符；
- `SKILL.md` 必须包含 `name` 和清晰的 `description`；
- 将较长说明放入 `references/`，可执行工具放入 `scripts/`；
- 添加 `agents/openai.yaml`，其中 `default_prompt` 明确引用 `$skill-name`；
- 在 `registry/skills.json` 与相应 profile 中登记；
- 记录来源、许可证证据、所有权状态和发布策略。

## 去重与分叉

相同逻辑名称只保留一个规范路径。确实需要平台分叉时，优先采用：

- profile 控制是否装载；
- `agents/` 中保存平台元数据；
- 薄适配 Skill 调用共同的通用 Skill。

只有行为无法兼容时才维护分叉，并在注册表中标记上游、分叉原因和同步策略。

## 版本与发布

- 日常变更使用语义明确的小提交；
- 稳定快照可打 `skills-YYYY.MM` 标签；
- 发布说明列出新增、行为变化、弃用和需要人工迁移的 Skill；
- 二进制模板和大体积资产优先放 GitHub Release 或专用对象存储，不进入主仓库历史。

## 恢复演练

至少每季度在一个空目录执行一次 profile 预演和实际装载，并抽查：

- Skill 数量与注册表一致；
- `SKILL.md` 可解析且没有 UTF-8 BOM 问题；
- 相对引用和脚本路径有效；
- 本机已有目录不会被覆盖。

profile 只登记需要复制的顶层目录。嵌套逻辑 Skill 已包含在父目录中，不应再次登记为
独立装载单元。
