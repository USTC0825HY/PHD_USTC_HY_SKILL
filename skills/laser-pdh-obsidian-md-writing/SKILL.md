---
name: laser-pdh-obsidian-md-writing
description: Laser/PDH Obsidian Markdown writing, repair, and governance workflow. Use when creating, revising, auditing, or repairing Laser_PDH_Study notes, source maps, formula indexes, chapter study notes, experiment methods, derivations, LaTeX rendering, Mermaid diagrams/viewers, schematic screenshot crops, table layout/wide table repairs, long-text table conversion, CSS/frontmatter, wikilinks, or coverage of web/PDF/PPT learning sources.
---

# Laser/PDH Obsidian Markdown Writing

Before consuming profile-derived inputs, read [path validation](../hardware-dev-router/references/profile-path-resolution.md) and run its read-only validator for the required keys only (or validate an explicit task path). Missing inputs stop dependent work; do not create obsolete directories or guess replacement campaigns. Keep existing CLI/environment overrides ahead of profile defaults.

运行脚本前按 [运行时验证](../hardware-dev-router/references/runtime-validation.md) 探测实际 Python 版本和所需导入；优先复用可执行专用环境。

先区分指定文件写作/修复与明确授权的全项目治理。单篇任务只检查和修改目标文件，不因全库问题扩展任务。公式工具默认预览；写入必须提供可重复的 --file，或在全项目治理时提供 --all-project。备份、哈希复核与原子替换由工具执行；默认排除原始摘录/历史目录。Mermaid 仍保留内嵌与 .mmd/.html 配套习惯，只对本次新建/修改的图应用，不给仅修公式的旧笔记补图。

## Portable Configuration

Read `<CODEX_HOME>/laser-fpga-profile.json` before resolving any path. Resolve `<CODEX_HOME>` from the environment, falling back to the current user's `.codex` directory. Treat `<obsidian_vault_root>` below as the profile value. Use `<CODEX_HOME>/tools/laser-fpga-runtime/.venv/Scripts/python.exe` for bundled Python dependencies.

## Canonical Paths

- Research system root: `<obsidian_vault_root>/01_科研主系统`
- Theory / literature: `<obsidian_vault_root>/01_科研主系统/02_理论学习` / `03_文献阅读`
- Modeling / RTL: `<obsidian_vault_root>/01_科研主系统/04_建模与算法` / `05_RTL与系统实现`
- Experiment / analysis: `<obsidian_vault_root>/01_科研主系统/06_实验测试` / `07_数据分析`
- Source/asset indexes: `<obsidian_vault_root>/01_科研主系统/09_资料与工具`
- Governance root: `<obsidian_vault_root>/01_科研主系统/99_系统治理/02_Laser资料治理`
- Note template: `<obsidian_vault_root>/模板/科研流程/Laser_PDH_Study_科研学习笔记模板.md`
- CSS snippet: `<obsidian_vault_root>/.obsidian/snippets/laser-pdh-study.css`
- Required note class: `cssclasses: [laser-pdh-note]`

## Workflow

本地科研主系统AGENTS.md/MEMORY.md优先于任何示例目录。2026-10-12前旧目录只作历史线索，不自动重建。单篇遥测笔记读[遥测笔记模式](references/telemetry-note-layout.md)；技术记录来自`telemetry-route-workbook`，跨板方法来自`fpga-board-signal-chain-closure`。该模式不套用于普通论文或理论笔记。

1. Classify the task before writing: source import, lecture-note rewrite, experiment method, derivation, index/map update, formula repair, or coverage audit.
2. Use the canonical directory for the note type. Read `references/laser_pdh_obsidian_rules.md` before creating or reorganizing notes.
3. Keep raw sources in their locally confirmed evidence location (large originals outside the vault); use `09_资料与工具` for indexes. Do not turn raw web/PDF text into formal notes by dumping it unchanged.
4. Write formal notes in lecture style: core conclusion, physical picture, math expression, experiment implementation, common pitfalls, source/evidence boundary, and related questions.
5. Use Obsidian `[[wikilinks]]` for knowledge links. Use absolute filesystem paths only in source/evidence sections.
6. For LaTeX work, read `references/latex_rendering_rules.md` and run `scripts/audit_laser_pdh_md.py` after edits.
7. When the user explicitly asks to fix formula rendering, run `scripts/fix_laser_pdh_latex.py --file <指定笔记.md> --write`, then re-run the audit script.
8. For table layout, wide table, screenshot-metadata table, engineering-list table, or long-text table repairs, read `references/table_layout_rules.md` before editing:
   - Split unreadable long-text tables into smaller comparisons or field-list cards; preserve deliberately requested concise node/parameter/result tables.
   - Keep numeric comparison tables, signal matrices, and short record templates as tables.
   - Skip `01_Raw` and `_旧版.md`; preserve values, evidence IDs, image paths, and `needs_check`.
9. For Mermaid 图，读 `references/mermaid_rendering_rules.md` 后再产出/修改：
   - 正式 Markdown 必须至少内嵌一张可直接渲染的 Mermaid 图；不能只提供 `.mmd/.html` 链接。
   - 多图索引默认内嵌总览或代表图；明确要求逐路图时逐路内嵌，用章节折叠，不擅自改为仅链接。
   - 禁止在 Mermaid 节点内使用 `/n`、`\n`、`<br/>` 强制换行。
   - 节点标签尽量不超过 12 字符，长文本放到正文/表格/说明中，图内只放结构名。
   - 每张图必须有同名的 `.mmd` 与 `.html` 成对文件；每个 `.html` 只加载一张图的源码，支持独立调试。
   - 在相关 Markdown 中给出 `.mmd` 图源链接与 `.html` 缩放入口。
10. For 原理图截图/电路截图，读 `references/schematic_screenshot_rules.md` 后再产出/修改：
   - 不要用整页原理图截图替代说明；截图必须是可读的局部证据。
   - 围绕单一对象裁剪：接口、输入前端、核心芯片、输出级、电源支路、控制线或反馈链路。
   - 一张图放不下时拆成多张局部图，并在正文按“接口 -> 前端 -> 核心 -> 输出”解释。
   - 每张截图附近说明来源、页码/文件、对应功能块、测试关注点和易错点。
11. For CSV mapping tables intended for Microsoft Excel, read `references/csv_excel_compatibility_rules.md` before delivery:
   - Write UTF-8 with BOM, CRLF line endings, and RFC 4180 quoting; quote every field by default.
   - Round-trip the final CSV and assert a fixed column count for every row.
   - Scan decoded cells for replacement characters or common mojibake before handoff.
   - When practical, provide a formatted `.xlsx` companion for direct Excel use.

## Validation Commands

局部任务优先：`audit_laser_pdh_md.py --root <科研主系统> --file <指定笔记.md>`，可重复`--file`。此模式只审计目标笔记及其引用资源；索引其他文件仅用于解析链接。`--project`全项目审计保留，但不扩大修改范围。静态审计、实际Mermaid/公式渲染与视觉检查分别记录。

Run from any working directory:

```powershell
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
& "$codexHome/tools/laser-fpga-runtime/.venv/Scripts/python.exe" "$codexHome/skills/laser-pdh-obsidian-md-writing/scripts/audit_laser_pdh_md.py" --project Laser_PDH_Study
```

Use dry-run before writing formula fixes:

```powershell
& "$codexHome/tools/laser-fpga-runtime/.venv/Scripts/python.exe" "$codexHome/skills/laser-pdh-obsidian-md-writing/scripts/fix_laser_pdh_latex.py" --project Laser_PDH_Study
```

Run Mermaid-focused auditing after rendering-related edits:

```powershell
& "$codexHome/tools/laser-fpga-runtime/.venv/Scripts/python.exe" "$codexHome/skills/laser-pdh-obsidian-md-writing/scripts/audit_laser_pdh_md.py" --project Laser_PDH_Study
```

Expected Mermaid checks are included in `MERMAID_*` counters:

```text
MERMAID_LABEL_ESCAPES
MERMAID_LABEL_LEN
MERMAID_PAIR_CHECK
MERMAID_SINGLE_VIEWER
MERMAID_LINK_TARGET
MERMAID_INLINE_DISPLAY
```

Expected schematic screenshot checks are included in `SCHEMATIC_IMAGE_*` counters:

```text
SCHEMATIC_IMAGE_EXISTS
SCHEMATIC_IMAGE_SCOPE
SCHEMATIC_IMAGE_CONTEXT
```

Expected table layout reports are included in `TABLE_*` counters:

```text
TABLE_WIDE
TABLE_SEVERE
TABLE_SCREENSHOT_METADATA
```

`TABLE_*` counters are report-only. They identify table layout risk; do not require them to be zero when remaining tables are numeric comparisons, matrices, or record templates.

Apply formula fixes only when requested:

```powershell
& "$codexHome/tools/laser-fpga-runtime/.venv/Scripts/python.exe" "$codexHome/skills/laser-pdh-obsidian-md-writing/scripts/fix_laser_pdh_latex.py" --file <指定笔记.md> --write
```

## Evidence Rules

- Mark uncertain claims as `needs_check`.
- Keep paper facts, PPT facts, web answer summaries, user questions, and Codex derivations separate in `source_origin` or source/evidence sections.
- Use `Web_QA_Coverage_Audit.md` and `Web_QA_to_Notes_Map.md` when checking whether web answers have been integrated.
- Update `Question_Index.md` for user-facing learning questions and `Formula_Index.md` for reusable formulas.
