# Engineering Report Reconstruction

Use this reference when a user supplies a reference report and a target DOCX for substantial restructuring. Use the reference only for narrative and layout lessons; never copy its facts into the target.

## Preflight

1. Locate the actual reference and target paths.
2. Record each file's path, SHA-256, size, modification time, and Word lock state.
3. Keep the original target unchanged. Create a task-specific output copy.
4. Extract and inspect:
   - body paragraphs and styles;
   - heading hierarchy and TOC;
   - tables and merged cells;
   - equations and OMML structure;
   - embedded images, diagrams, and screenshots;
   - captions, `SEQ` fields, and cross-references;
   - headers, footers, page breaks, sections, and page geometry;
   - tracked changes and comments;
   - local paths and external links.
5. Render both documents when layout or image meaning affects the comparison.

## Internal Issue Register

Create an internal table before rewriting:

`位置 | 原文或原始数据 | 问题类型 | 问题说明 | 建议处理 | 是否影响结论`

Classify at least:

- numerical or unit conflict;
- missing test condition;
- damaged or incorrect formula;
- duplicated result;
- unsupported or over-broad conclusion;
- inconsistent terminology;
- management-style or AI-style prose;
- unreadable figure or table;
- numbering, TOC, or cross-reference defect;
- traceability gap;
- instrument or chain contribution;
- uncovered band, range, duration, load, or operating condition;
- inference not supported by available data.

Do not start prose reconstruction until conclusion-affecting issues have an explicit treatment: confirm, retain with qualification, downgrade, mark untested, or move to the conflict register.

## Reference-Report Comparison

Extract transferable strengths such as:

- purpose and core indicators stated at the start;
- system and hardware state explained before results;
- actual procedures recorded rather than only requirement rows;
- results organized by date, operating condition, or hardware configuration;
- condition changes stated when results change;
- anomalies linked to controlled follow-up tests.

Do not copy weaknesses such as incomplete formulas, missing acquisition parameters, diary-style prose, unsupported conclusions, time-relative plans, or low-resolution figures.

## Required Companion Files

When the user requests a formal deep reconstruction, produce these alongside the revised DOCX unless the requested deliverables differ:

### Modification Notes

Include the objective, original problems, new structure, moved or merged content, terminology changes, conclusion changes, downgraded items, figure/table changes, formula repairs, unresolved issues, and representative before/after examples.

### Data Conflicts And Open Items

For every conflict or missing condition, record:

`原始位置 | 冲突或缺失内容 | 对结论的影响 | 推荐确认方式 | 当前处理状态`

Do not hide a conclusion-affecting conflict inside a general remarks column.

### Technical Review Record

Review test-chain validity, processing formulas, units, indicator coverage, preliminary-only results, instrument-floor limits, sample-rate/duration/resolution limits, mandatory retests, recommended methods, and release blockers.

## Preservation And Delivery

- Never delete valid measured data or select points only to make a result pass.
- Record every merged or removed duplicate in the modification notes.
- Record every conclusion downgraded because of conflict or incomplete coverage.
- Refresh fields only on an output copy; verify the original hash has not changed.
- Run both report audits, export a temporary PDF, and inspect every page for clipped tables, broken equations, detached captions, unreadable figures, orphan lines, and abnormal blank space.
- In the final handoff, list every generated file, the most important structural changes, changed conclusions, unresolved conflicts, rendering status, and any object that could not be repaired automatically.
