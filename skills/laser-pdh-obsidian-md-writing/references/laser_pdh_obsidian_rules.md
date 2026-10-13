# Laser/PDH Obsidian Rules

## Canonical Directory Roles

- `02_Laser_PDH知识体系/00_知识导航`: learning maps, question index, formula index, and glossary.
- `02_Laser_PDH知识体系/01_论文脉络`: notes following thesis chapter order, especially chapter 3/4/5.
- `02_Laser_PDH知识体系/02_基础知识`: reusable concepts such as PDH discriminator, loop gain, beat note, IQ, and noise.
- `02_Laser_PDH知识体系/03_公式推导`: equation derivations and conversion chains.
- `03_超稳激光系统工程`: project planning, product design, loops, board analysis, interfaces, and PD signal chains.
- `04_实验测试与证据`: experiment methods, executable manuals, records, results, and formal reports.
- `07_资料源与资产索引`: source maps, F/G/C asset indexes, raw exports, extracted source text, and rendered figures.
- `99_系统治理/02_Laser资料治理`: processing notes, changelog, coverage audit, generated manifests, and agent traceability.

## Required Frontmatter

Every formal Markdown note should include:

```yaml
cssclasses: [laser-pdh-note]
title:
project: Laser_PDH_Study
status: draft
created:
updated:
doc_date:
category:
note_type:
module:
source_origin:
  - 用户原始问题
  - 论文原文
  - PPT
  - Codex 整理
tags:
  - laser/PDH
```

Keep `needs_check` in tags or source status when a claim has not been verified against the thesis, PPT, or experiment script.

## Writing Pattern

Formal notes should be rewritten, not copied from raw web answers. Use this structure when it fits:

1. 本页核心结论
2. 要解决的问题
3. 物理图像
4. 数学表达 or 推导
5. 实验实现
6. 容易误解点
7. 和论文第 3/4/5 章的关系
8. 关联问题与来源

Keep explanations lecture-like: start from the logic chain, then add equations, then connect to experiment signals and later thesis use.

## Key Indexes

- `02_Laser_PDH知识体系/00_知识导航/Question_Index.md`: user-facing QID index. Add fine-grained questions instead of one large topic.
- `02_Laser_PDH知识体系/00_知识导航/Formula_Index.md`: reusable formulas. Use formula cards, not complex Markdown table formulas.
- `02_Laser_PDH知识体系/00_知识导航/Core_Logic_Chain.md`: one-page chain from locking object to feedback, IQ measurement, `D(f)`, loop gain, and noise conversion.
- `07_资料源与资产索引/02_来源映射/Web_QA_to_Notes_Map.md`: map web learning package sections to formal notes.
- `99_系统治理/02_Laser资料治理/Agent_Log/Web_QA_Coverage_Audit.md`: coverage audit; do not leave uncovered sections as `缺失` without a follow-up target.

## Source Boundaries

- Raw sources can be copied into `07_资料源与资产索引/03_原始摘录`, but formal notes must split, rewrite, and link them.
- Distinguish thesis facts, PPT facts, web-answer explanations, user questions, and Codex derivations.
- Do not imply an experimental conclusion is proven unless the note cites the relevant data, figure, or extracted source.
- Use absolute filesystem paths only in source/evidence sections; use `[[wikilinks]]` inside the vault knowledge graph.
