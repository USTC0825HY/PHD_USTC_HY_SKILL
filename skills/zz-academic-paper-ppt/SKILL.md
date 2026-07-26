---
name: zz-academic-paper-ppt
description: Personal workflow for creating, revising, and QA-ing Chinese academic paper presentation PPTX decks. Use when the user asks to modify or polish a research-paper/course-report PPT, improve slide logic, remove AI-like wording, revise formulas/tables/speaker notes, coordinate subagents by page, preserve manual PowerPoint edits, or update the generation script so future runs reproduce the accepted deck.
---

# ZZ Academic Paper PPT

Use this skill for academic paper presentations where the goal is a credible graduate-level Chinese oral report, not a generic template deck. Prioritize argument logic, evidence interpretation, readable formulas, and preservation of the user's manual edits.

## Core Workflow

1. **Save and inspect first.**
   - If a PPT is open in PowerPoint, save it before editing or comparing.
   - Export current slide previews or a contact sheet before judging layout.
   - If a Python/JS generation script exists, inspect both the PPT and script before changing either.

2. **Define the logic before editing a page.**
   Answer three questions:
   - What function does this section serve in the whole talk?
   - What question does this slide answer?
   - What one judgment should the audience take away?

3. **Edit the slide around one task.**
   Prefer:
   ```text
   问题句 → 核心公式 / 图示 / 表格 → 解释卡片 → 一句判断
   ```
   Avoid turning a slide into a paragraph dump or a list of loosely related facts.

4. **Update speaker notes with the slide.**
   Notes should explain how to speak the slide, not repeat every label. Keep most notes around 120-180 Chinese characters unless the user asks for a full script.

5. **Validate visually and textually.**
   - Export PNG previews after modification.
   - Check formulas are readable and not placeholders.
   - Scan for repeated AI-like labels and banned wording.
   - Compare text/notes against manual decks when the user has hand-edited slides.

## Writing Style

Keep specialist terms when needed: `VaR`, `CAViaR`, `Regression Quantile`, `DQ test`, `Hit`, `violation`, `check loss`, `conditional quantile`, `tail persistence`, `news impact`, `out-of-sample`.

Reduce template-like labels:

| Avoid overusing | Prefer |
|---|---|
| 当前结论 | 小结 / Takeaway / direct judgment |
| 本页说明 | 这里先交代 / 这一页固定 / 这一页给出 |
| 设计意图 | 样本设置的含义 / 设置目的 |
| 评价指标 | 结果怎么读 / 回测指标 / 模型比较指标 |
| Finding | 主要发现 |
| Evidence | 表 1 依据 / 论文结果 / 回测表现 |
| Interpretation | 含义 / 模型含义 / 对结果的解释 |
| 核心增量 | 主要贡献 / 方法转向 / 关键改动 |
| 可预测结构 | 可由过去信息解释的成分 |
| 参数理解 | 汇报理解 / 直观理解 |
| 副产品 | 间接得到的结果 / 间接推出的结果 |
| 证据 | 实验结果 / 表格结果 / 结果显示 |
| 边界 | 限制 / 注意 / 结论范围 |
| 仍未说明 | 仍需验证 / 后续需要补充 |
| 结果读法 | 结果分析 |
| 答辩准备 | 可能问题与回应 / 讨论问题 |
| Source: | 参考： / 页脚引用 |

Avoid:
- `不是……而是……`
- `不是为了……而是为了……`
- `当前结论`
- `证据来源`
- `其实`
- `单纯`
- `只是`
- `不太`
- `很重要`

Prefer:
- `从 A 转向 B`
- `相较于 A，B 更强调……`
- `本文将……作为主要对象`
- `该设定使……与……保持一致`
- `方法区别在于……`
- `该结果支持……`
- `这一检验进一步考察……`

Chinese titles should carry the argument. English subtitles may preserve terminology, but should not replace Chinese logic.

Examples:
- Prefer `DQ test：检验 Hit 是否还能被过去信息解释`
- Avoid only writing `Testing orthogonality between Hit and past information`
- Prefer `模型回测与结果评价`
- Avoid vague section labels like `Evidence and assessment`

## Slide Structure Patterns

### Classroom Defense Deck
For Chinese course defenses and 8-15 minute oral reports, make the deck feel like a prepared classroom presentation, not an AI summary board.

- Keep one question or judgment per slide.
- Use short action titles, usually within one line; put details in the body or speaker notes.
- Use the order `title -> figure/table/flow -> explanation -> one bottom judgment`.
- Let the main exhibit appear before the interpretation. On result slides, place the chart/table as the visual center and put explanation to the right or bottom.
- Replace repeated `现象 / 依据 / 当前结论 / 仍未说明` cards with natural labels such as `结果分析`, `限制说明`, `后续路线`, or direct judgment sentences.
- Do not use the same three-card template on many consecutive pages. Vary between flow diagrams, numbered cards, comparison cards, tables, and bottom strips.

### Motivation / Background
Show the funnel from practical need to statistical problem. Do not place practice, definition, difficulty, and research task as unrelated parallel bullets.

### Method Shift
Use a clear contrast:
```text
traditional path: volatility / distribution → tail quantile → VaR
CAViaR path: information + lagged quantile → f_t(β) → VaR
```
Use wording like `方法转向` or `建模重心转向`, not a mechanical "not A but B" construction.

### Formula Slide
Use one main formula group. Make the formula the visual center. Put variables and interpretation near it, but avoid nested frames.

Formula hierarchy:
- main formula: largest
- auxiliary definitions: smaller
- verbal explanation: short, aligned, 1-2 lines

### Model Specifications
For repeated model cards, use consistent labels:
- `进入模型的信息`
- `更新逻辑`
- `模型含义`

Avoid repeated `更新信号 / 直觉 / 限制` when it makes the page sound like a generated template.

### Estimation and Testing
Build a chain:
```text
f_t(β) → β̂ → f̂_t → I_t → Hit_t → DQ test
```
Each slide should answer one question:
- How are parameters estimated?
- Why numerical optimization?
- What theory supports inference?
- How are violations centered into Hit?
- How does DQ test operationalize the moment restriction?

### Empirical Results
Use `结果一 / 结果二` or natural Chinese finding titles. Avoid raw `Finding / Evidence / Interpretation` headings unless the user explicitly prefers English tables.

Example:
```text
实证发现一：左尾条件分位数具有持续性
表 1 依据：β₂ 在大多数规格中显著
模型含义：波动聚集可体现在左尾条件分位数中
```

## Layout Rules

- Keep the original deck style unless the user asks for redesign.
- Use deep navy + orange + light gray consistently when working on this user's CAViaR-style academic decks.
- Avoid large nested orange frames. Use one main formula box, a few explanation cards, and one bottom judgment strip.
- Do not let every slide look like the same template. Vary labels and bottom judgment wording.
- Keep text to 1-2 lines per module when possible.
- Use `微软雅黑` for Chinese academic PPT unless the source template clearly uses another accepted font. When generating PPTX, write Chinese text with `zh-CN` and set `noProof="1"` where possible to avoid red spellcheck waves.
- Center-align academic notation and metric tables horizontally and vertically by default. Use dark navy headers with white bold text; bold key metric cells.
- Convert dense bullets into numbered cards, flow cards, or side explanation cards. Card body text must stay inside the card with comfortable padding.
- Use one visual center per page: chart, table, flow, formula, or image group. Avoid splitting attention across unrelated mini-panels.
- Bottom judgment strips should be light: pale gray fill, thin orange/blue accent, and one concise sentence. Remove footers entirely when the user says the small bottom text distracts.
- Use readable table fonts, with 15 pt as the preferred target when space permits.
- If a table exceeds 6-7 dense rows, split the content into a table plus side cards or move detail to appendix.
- Preserve image aspect ratio. Use contain/crop helpers instead of passing arbitrary width and height together.
- Always export previews for modified pages and inspect thumbnails/contact sheets.

## MRI-Style PPT Lessons To Generalize

Use these rules for any experiment-result PPT with preprocessing, models, metrics, and visual examples:

- Method-flow pages should show how intermediate artifacts enter classification, interpretation, and fusion; avoid unexplained labels such as `三条路线` unless each route is named.
- Preprocessing pages work better as numbered vertical flows than long bullets. Increase card height before shrinking text.
- Result pages should highlight exact values in tables/charts first, then explain what those values mean for classification, ranking, and interpretation.
- Candidate segmentation or ROI outputs should be described as weak localization or explanation aids unless pixel-level labels support clinical segmentation claims.
- Reference slides should use numbered, compact cards. Do not let citations consume the main visual space.

## Speaker Notes

Write notes as spoken explanation:

Prefer:
```text
先从风险管理需求切入。VaR 的吸引力在于……
这里把 VaR 写成条件分位数……
表 1 中最值得关注的是……
```

Avoid repeated openers:
```text
这一页的作用是……
本页说明……
转场：下一页……
```

Use transitions naturally inside the note instead of writing a separate `转场：` line on every slide.

## Prompting and Subagent Use

When the user asks for page-specific edits, use a precise task statement:

```text
请只修改第 X 页，不要改其他页面。
当前问题：
页面目标：
标题改为：
正文/表格/公式改为：
底部小结改为：
speaker notes 改为：
排版要求：
检查清单：
```

When the user explicitly requests subagents, split by page with disjoint responsibilities. Do not let subagents edit overlapping slide ranges or overwrite each other's work.

## Protecting Manual PowerPoint Edits

When the user says they manually adjusted the PPT:

1. Save the open PowerPoint file through COM if possible.
2. Create a snapshot named like:
   ```text
   <deck>_manual_full_locked.pptx
   ```
3. Generate or locate the script baseline.
4. Compare manual vs script by:
   - slide body text
   - speaker notes
   - exported PNG visual diff
5. If many pages differ, lock the full manual deck, not only one slide.
6. Update the generation script so future runs reinsert the accepted manual pages after normal generation.
7. Export a contact sheet and a small Markdown summary of changed/locked pages.

Do not overwrite a user's manual PPT changes just because the script has an older layout.

## QA Checklist

Before final response, verify:

- The requested slide range, and only that range, was changed unless the user allowed more.
- Manual edits were saved and protected when mentioned.
- Slide titles read like real presentation titles, not topic labels.
- Formula variables remain consistent across the deck.
- `当前结论`, `证据`, `边界`, `仍未说明`, `结果读法`, `答辩准备`, `Finding / Evidence / Interpretation`, `设计意图`, and `评价指标` are not repeated mechanically.
- Speaker notes are natural spoken notes, generally 120-180 Chinese characters.
- Modified slides have PNG previews.
- Export 1600x900 previews and inspect key pages plus a contact sheet.
- Run text overflow checks when using PowerPoint COM. Reject clipped text, text outside cards, punctuation stranded on its own line, or unreadable tiny fonts.
- Check that pictures preserve aspect ratio and that table text is horizontally and vertically centered.
- Verify key numbers and method names remain searchable in PPT text.
- Check native PowerPoint Sections when the deck has visible section divider slides.
- Search PPTX XML for unintended fonts and proofing problems when users report ugly fallback fonts or red spelling waves.
- Confirm distracting left-bottom footers or `参考：...` text are removed if the user requested deletion.
- The generation script can reproduce or preserve the accepted PPT state.
