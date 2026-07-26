---
name: maroc-obsidian-md-writing
description: "MAROC Obsidian Markdown writing and governance workflow. Use for creating, revising, classifying, or auditing MAROC process notes, navigation pages, architecture docs, protocol/configuration notes, simulation reports, board-debug logs, repair records, tool guides, stage summaries, and PPT companion Markdown."
---

# MAROC Obsidian Markdown Writing

## Workflow

1. Choose the canonical directory before writing. Use `08_上板调试` for real board-debug notes; treat `02_上板调试` as historical drift unless explicitly requested.
2. Select the note type: navigation, architecture/interface, protocol/config freeze, simulation/signoff, board-debug/ILA, repair record, tool operation, parameter page, hardware review, or stage summary.
3. Add frontmatter: `title`, `project`, `status`, `created`, `updated`, `doc_date`, `category`, `note_type`, `module`, `source_origin`, `tags`, and evidence fields when applicable.
4. Use Obsidian `[[wikilinks]]` for vault knowledge links. Put absolute `C:/` and `F:/` paths only in evidence/source sections.
5. Separate phenomenon, basis, action, verification, current conclusion, and remaining boundary.
6. Update navigation or companion index only when the task asks for governance or publication readiness.

## Canonical Categories

- `00_导航`
- `01_架构与手册`
- `02_规划与总结`
- `03_协议与配置`
- `04_仿真与验证`
- `05_排障与修复`
- `06_工具与操作`
- `07_数据附件`
- `08_上板调试`
- `98_模板`
- `99_doc_governance`

## Evidence Rules

Follow router `evidence-boundaries.md`. Configuration-chain, ADC/upload, and analog/Ctest conclusions must remain separate unless the note includes evidence for each layer.

## Asset Library

- Read `C:/Users/Administrator/.codex/hardware-assets/source-refs/maroc-doc-assets.md` before citing or extending existing MAROC Obsidian notes.
- Use `C:/Users/Administrator/.codex/hardware-assets/templates/reports/claim_table_template.md`, `board_bringup_log_template.md`, and `ppt_md_companion_template.md` for reusable note structures.
- Use `C:/Users/Administrator/.codex/hardware-assets/hooks/hardware-hook-registry.yaml` when a note cites script-generated evidence. Record the hook id, mode, run directory, and risk level instead of implying broader hardware proof.
- Do not move existing Obsidian notes into the asset library; catalog source paths and write new notes only in the requested canonical vault location.
