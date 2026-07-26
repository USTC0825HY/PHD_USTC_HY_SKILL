---
name: laser-pdh-obsidian-md-writing
description: Laser/PDH Obsidian Markdown writing, repair, and governance workflow. Use when creating, revising, auditing, or repairing Laser_PDH_Study notes, source maps, formula indexes, chapter study notes, experiment methods, derivations, LaTeX rendering, Mermaid diagrams/viewers, schematic screenshot crops, table layout/wide table repairs, long-text table conversion, CSS/frontmatter, wikilinks, or coverage of web/PDF/PPT learning sources.
---

# Laser/PDH Obsidian Markdown Writing

## Canonical Paths

- Research system root: `C:/01_obsidian/ustc_hy/01_科研主系统`
- Knowledge root: `C:/01_obsidian/ustc_hy/01_科研主系统/02_Laser_PDH知识体系`
- System engineering root: `C:/01_obsidian/ustc_hy/01_科研主系统/03_超稳激光系统工程`
- Experiment/evidence root: `C:/01_obsidian/ustc_hy/01_科研主系统/04_实验测试与证据`
- Source/asset index root: `C:/01_obsidian/ustc_hy/01_科研主系统/07_资料源与资产索引`
- Governance root: `C:/01_obsidian/ustc_hy/01_科研主系统/99_系统治理/02_Laser资料治理`
- Note template: `C:/01_obsidian/ustc_hy/模板/科研流程/Laser_PDH_Study_科研学习笔记模板.md`
- CSS snippet: `C:/01_obsidian/ustc_hy/.obsidian/snippets/laser-pdh-study.css`
- Required note class: `cssclasses: [laser-pdh-note]`

## Workflow

1. Classify the task before writing: source import, lecture-note rewrite, experiment method, derivation, index/map update, formula repair, or coverage audit.
2. Use the canonical directory for the note type. Read `references/laser_pdh_obsidian_rules.md` before creating or reorganizing notes.
3. Keep raw sources in `07_资料源与资产索引/03_原始摘录`; do not turn raw web/PDF text into formal notes by dumping it unchanged.
4. Write formal notes in lecture style: core conclusion, physical picture, math expression, experiment implementation, common pitfalls, source/evidence boundary, and related questions.
5. Use Obsidian `[[wikilinks]]` for knowledge links. Use absolute `C:/` and `F:/` paths only in source/evidence sections.
6. For LaTeX work, read `references/latex_rendering_rules.md` and run `scripts/audit_laser_pdh_md.py` after edits.
7. When the user explicitly asks to fix formula rendering, run `scripts/fix_laser_pdh_latex.py --write`, then re-run the audit script.
8. For table layout, wide table, screenshot-metadata table, engineering-list table, or long-text table repairs, read `references/table_layout_rules.md` before editing:
   - Convert long-text explanation tables into heading + field-list cards.
   - Keep numeric comparison tables, signal matrices, and short record templates as tables.
   - Skip `01_Raw` and `_旧版.md`; preserve values, evidence IDs, image paths, and `needs_check`.
9. For Mermaid 图，读 `references/mermaid_rendering_rules.md` 后再产出/修改：
   - 禁止在 Mermaid 节点内使用 `/n`、`\n`、`<br/>` 强制换行。
   - 节点标签尽量不超过 12 字符，长文本放到正文/表格/说明中，图内只放结构名。
   - 每张图必须有同名的 `.mmd` 与 `.html` 成对文件；每个 `.html` 只加载一张图的源码，支持独立调试。
   - 在相关 Markdown 中给出 `.mmd` 图源链接与 `.html` 缩放入口。
10. For 原理图截图/电路截图，读 `references/schematic_screenshot_rules.md` 后再产出/修改：
   - 不要用整页原理图截图替代说明；截图必须是可读的局部证据。
   - 围绕单一对象裁剪：接口、输入前端、核心芯片、输出级、电源支路、控制线或反馈链路。
   - 一张图放不下时拆成多张局部图，并在正文按“接口 -> 前端 -> 核心 -> 输出”解释。
   - 每张截图附近说明来源、页码/文件、对应功能块、测试关注点和易错点。

## Validation Commands

Run from any working directory:

```powershell
python C:/Users/Administrator/.codex/skills/laser-pdh-obsidian-md-writing/scripts/audit_laser_pdh_md.py --root C:/01_obsidian/ustc_hy/01_科研主系统 --project Laser_PDH_Study
```

Use dry-run before writing formula fixes:

```powershell
python C:/Users/Administrator/.codex/skills/laser-pdh-obsidian-md-writing/scripts/fix_laser_pdh_latex.py --root C:/01_obsidian/ustc_hy/01_科研主系统 --project Laser_PDH_Study
```

Run Mermaid-focused auditing after rendering-related edits:

```powershell
python C:/Users/Administrator/.codex/skills/laser-pdh-obsidian-md-writing/scripts/audit_laser_pdh_md.py --root C:/01_obsidian/ustc_hy/01_科研主系统 --project Laser_PDH_Study
```

Expected Mermaid checks are included in `MERMAID_*` counters:

```text
MERMAID_LABEL_ESCAPES
MERMAID_LABEL_LEN
MERMAID_PAIR_CHECK
MERMAID_SINGLE_VIEWER
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
python C:/Users/Administrator/.codex/skills/laser-pdh-obsidian-md-writing/scripts/fix_laser_pdh_latex.py --root C:/01_obsidian/ustc_hy/01_科研主系统 --project Laser_PDH_Study --write
```

## Evidence Rules

- Mark uncertain claims as `needs_check`.
- Keep paper facts, PPT facts, web answer summaries, user questions, and Codex derivations separate in `source_origin` or source/evidence sections.
- Use `Web_QA_Coverage_Audit.md` and `Web_QA_to_Notes_Map.md` when checking whether web answers have been integrated.
- Update `Question_Index.md` for user-facing learning questions and `Formula_Index.md` for reusable formulas.
