---
name: maroc-ppt
description: Use when creating, revising, or QA-ing MAROC project PowerPoint presentations for Chinese lab meetings or research progress reports, especially decks based on MAROC configuration-chain, FPGA/USB bring-up, ILA evidence, register behavior tests, TransmitOn/Ctest/ADC timing, read-register/probe driver work, OUT_Q/OUT_FS slow/fast shaper observation, Obsidian process notes, and technical waveform/diagram drawing. Applies the user's preferred MAROC slide structure, typography, wording discipline, evidence boundaries, template style, native PowerPoint sections, and reproducible high-quality plotting rules.
---

# MAROC PPT

## Purpose

Create MAROC project slides that read as research progress reports, not debug memos. The narrative is: recent work -> how it was tested -> result -> current conclusion -> remaining boundary -> next plan.

For long TransmitOn/Ctest/read-register closed-loop debug reports, read `references/maroc-debug-report-patterns.md` before drafting the deck.

## Required style

- Use 16:9 slides with light blue-gray background `#F5F8FC`.
- Use dark navy header `#173754` and thin orange divider `#F29E2F`.
- Use footer text `参考：...`; do not use `证据来源`.
- Use Chinese font `微软雅黑`; set Latin, numbers, register names, and signal names to `Times New Roman`.
- Avoid `Consolas`, `黑体`, and `Noto Sans SC`.
- Keep one judgment per slide. Body text should usually be 3-5 short lines.
- Prefer large screenshots and large timing diagrams over dense text.
- For long MAROC decks, keep the v7 style used by `07_MAROC3A_参数解析与上位机配置说明_20260608_v7.pptx`: clear section divider slides, directory page ranges, native PowerPoint sections, and restrained visual section markers only when they do not crowd the page.

## Typography and readability

- Use readable projector typography: top slide titles 28-32 pt, section-divider titles 34 pt or larger, card/section titles 18-22 pt, normal body 14 pt or larger, and card body 14.5-16 pt.
- Use 1.15-1.25 line spacing for body text and 2-4 pt paragraph spacing. Do not use tight default line spacing for dense Chinese text.
- Table body text should normally be 10.5-12 pt or larger. If a table becomes crowded, split it into multiple slides or convert it to larger evidence cards.
- Do not solve overflow by shrinking text below the minimums. Shorten the wording, split the slide, or redraw the content as a diagram.
- Keep card body text to 3-4 lines where possible. If a card needs more than 4-5 lines, separate "overview" and "boundary/conclusion" onto different cards or slides.
- Allowed small-text exceptions are footers, page numbers, directory page ranges, and very short diagram labels only; these exceptions must not carry the main argument.
- Text must stay visually inside its card/table cell with comfortable padding. If text touches the border, overlaps another object, or extends beyond the shape in PNG export, revise the slide instead of accepting it.
- Do not hide overflow by making text tiny. Preferred fixes are: split the page, shorten wording, widen the box, increase row height, or convert dense rows into multiple cards.
- Keep table rows tall enough for Chinese and mixed signal names. Dense lookup tables should be split by field group rather than compressed into one unreadable table.
- For generated PPTX decks, add a real PowerPoint COM text-overflow audit when possible: compare `TextFrame2.TextRange.BoundWidth/BoundHeight` against the text frame's available width/height after margins. The deck must report zero main-text overflows before delivery.
- Treat repeated text overflow as a generation-system failure, not a slide-by-slide cosmetic issue. Fix common helpers first (`add_text`, card padding, title boxes, section chips, table row heights), then repair the few remaining pages.
- Do not accept single punctuation marks wrapped onto their own line or punctuation starting a new line inside cards. Shorten the sentence or enlarge the box.
- A top-right section chip must be drawn by one function only. Do not also place a subtitle or duplicate section text behind/under the chip.
- Keep normal slide titles on one line. If a title wraps or crowds the section chip, shorten the title wording instead of accepting two-line overlap.
- When card text overflows, first enlarge the card, shorten the wording, split the content, or move neighboring objects. Do not solve it only by shrinking fonts.
- For multi-node process diagrams, prefer two-row return-path layouts or grouped flows with straight horizontal/vertical connectors. Avoid diagonal connector chains and avoid forcing long signal/module names to wrap awkwardly.
- When showing source material screenshots, crop to the actual point being discussed before placing the image. Do not paste full PDF pages, full schematic sheets, logos, footers, version tables, or large blank margins unless the whole page is the object of discussion.
- Preserve screenshot and image aspect ratio. In `python-pptx`, do not pass arbitrary `width` and `height` together unless they were computed from the image's native ratio. Use a contain/cover helper and center the image in the panel; if the panel shape does not fit the source, crop the source or change the panel, never stretch the image.
- For LaTeX formulas generated with `latex` + `dvisvgm`, keep the SVG as a source asset but do not insert the raw dvisvgm SVG directly into PowerPoint unless exported PNG QA proves PowerPoint preserves glyph proportions. PowerPoint can vertically stretch path-based SVG glyphs. Preferred workflow: render `.tex -> .svg`, rasterize the SVG to a high-DPI transparent PNG (at least 600 dpi, preferably 900-1000 dpi for projected formulas), then insert the PNG with a contain helper based on the PNG's native pixel ratio. Keep both `.svg` and `.png` in the deck asset directory.
- Avoid large decorative frames around small screenshots. If a screenshot is the slide's main point, it should be large enough to inspect on a projector; otherwise split the page or use a zoomed crop. Do not place a tiny screenshot inside a large rounded frame just to fill space.
- For teaching, review, or before/after pages, prefer one comparison case per slide. Do not compress three or more source-material comparisons into thumbnail rows when the viewer needs to read the screenshots. Split FEE schematic, datasheet, and User Guide comparisons into separate slides when needed.
- For FEE schematic screenshots, isolate the relevant signal path or make a composed focus image from multiple local crops. Add small highlight boxes, arrows, and short labels for nodes such as `J15`, `R160`, and `B4/Ctest`; avoid showing unrelated bias networks just because they are on the same sheet.
- For datasheet/User Guide screenshots, crop to the table row, figure, waveform, or paragraph needed for the slide. The useful content should occupy most of the panel; if a screenshot has large whitespace, crop it first so the image can be enlarged.
- Captions for cropped source material should state both the source and the reason for the crop, for example `User Guide p17 局部：Ctest 注入参数与示例波形`.
- Layout QA must include geometry, not only text. Reject generated PPTX if any main shape extends outside the slide, if any image is visibly aspect-distorted, or if a focus screenshot is too small to read in the exported PNG.

## Teaching and workflow decks

- For teaching, review, or workflow-summary PPTs, concept slides must include a real project example. Do not use pages that only define terms such as `agent`, `prompt`, `skill`, `context`, or `tool` in a few abstract sentences.
- Teach each AI collaboration concept with this structure when space allows: `concept -> analogy -> this project's example -> reusable template/checkpoint`.
- When explaining prompts, show one complete high-quality prompt and annotate its parts: target, inputs, outputs, constraints, style, and QA. A vague "bad vs good" pair is not enough by itself.
- When explaining skills, show concrete `SKILL.md` snippets from the user's project and explain how each rule changes agent behavior, such as title shortening, screenshot cropping, aspect-ratio preservation, or QA failure handling.
- Generated bitmap images may be used for abstract analogies, but they must contain no meaningful text, numbers, fake UI labels, or watermarks. Overlay all explanations, arrows, tags, and conclusions as editable PowerPoint objects.
- For prompt-management teaching pages, distinguish `prompt`, `system prompt / preset`, and `skill`: the prompt is the current task brief, the preset is a broader behavior preference, and the skill is a reusable project capability package. Do not overclaim third-party tool features beyond what their documentation supports.
- Avoid large empty concept cards. If a page has only a few short lines, add a real example, a filled template, a before/after snippet, or split the idea into a more useful visual workflow.

## Technical Drawing And Waveforms

- Do not use rough PowerPoint polylines for important MAROC waveforms. For fast shaper, threshold crossing, Ctest response, Hold/peaking time, ADC timing, and readout windows, prefer deterministic plots made by Python/matplotlib, SVG, or carefully editable PPT shapes.
- Use image generation only for visual style exploration or non-technical decorative imagery. Do not trust an AI-generated waveform as the technical source of truth. If image generation is used, generate no text, no numbers, no units, no watermark, then redraw the actual technical curve deterministically or overlay all labels with native PPT text.
- Keep generated technical figures reproducible from the deck build script or a project-local script. Save final assets in the PPT asset directory, not only under `.codex/generated_images`. If a model-generated reference is kept, store it as a reference asset and do not present it as measured or manual data.
- Use the MAROC figure style: white rounded panel on `#F5F8FC`, navy curve `#173754`, orange comparison curve `#F29E2F`, muted baseline `#586F8B`, light grid `#C1D2E2`, 2.5-3.0 pt visual line weight at 1600x900 export.
- Use captions such as `示意：反馈 R/C 对 fast shaper 脉冲形状的影响`. Avoid captions like `Generated waveform`. Mark qualitative plots as `示意` unless they come from measured data or an exact datasheet figure.
- Preserve MAROC signal semantics in waveform sketches: FSU is unipolar; FSB1 is bipolar and crosses below baseline; FSB2 is half-bipolar with smaller undershoot; larger R/C gives a wider/slower tail; smaller R/C gives a faster/narrower pulse; Ctest larger pulse increases amplitude at the same timing; peaking-time plots need peak markers and Hold sampling context.
- For threshold diagrams, draw the threshold line, over-threshold shaded window, and distinguish short vs long crossing windows. For timing diagrams, keep `Hold`, `start_ADC`, `TransmitOn`, and `Out_ADC` visually separated.
- Prefer one strong figure per slide. If a figure needs more than three curves or more than 4-5 annotations, split it into multiple slides rather than shrinking labels.
- When revising an existing MAROC deck, search the build script for `add_polyline`, dense hand-drawn curves, or screenshot-only waveforms. Replace ugly or ambiguous curves with reusable high-resolution assets or editable timing diagrams.

## Slide structure

Use these sections when relevant:

1. 汇报范围与结构
2. 理论分析
3. 近期工作与测试对象
4. 上位机与测试输入
5. 已解决硬件问题
6. 测试方法与仿真结果
7. 单板 ILA 实测结果
8. 寄存器行为测试
9. 寄存器参数参考
10. Ctest/ADC 前置调试
11. 初步结论与后续计划
12. 附录速查

For long decks, insert visible section divider slides and keep a directory slide with page ranges.

## Native PowerPoint sections

- Add real PowerPoint sections for long decks so the left thumbnail pane can collapse by chapter, matching `04_MAROC开发进度_Qt协议闭环_20260602.pptx`.
- Native sections are required in addition to visual section divider slides. Visual badges, chapter color rails, or progress markers are optional and do not replace native sections.
- Use concise section names, usually `封面与导览`, `01 ...`, `02 ...`, and so on. Match the directory page order and start each section at the section divider slide or cover page.
- When generating PPTX programmatically on Windows, use PowerPoint COM `Presentation.SectionProperties.AddBeforeSlide(slideIndex, sectionName)` or an equivalent method after saving the deck.
- Verify native sections after generation by reading `SectionProperties.Count`, `Name(i)`, `FirstSlide(i)`, and `SlidesCount(i)`. If console output garbles Chinese, inspect `ppt/presentation.xml` inside the PPTX and confirm section names are correct UTF-8.
- Report the section list in the final response for any deck where sections were added or changed.

## Wording rules

Write in an objective engineering-review voice:

- 现象
- 依据
- 处理
- 当前结论
- 剩余问题

Avoid overclaiming. Do not call configuration-chain evidence a full MAROC signoff. Do not mix configuration-chain, Ctest, ADC readout, and USB upload conclusions unless the evidence explicitly covers each link.
Do not present configuration-chain success as ADC/Ctest success. Treat `OUT_Q/OUT_FS` slow/fast shaper claims as analog-probe evidence only when real oscilloscope or board analog-output evidence is present.
In Chinese progress decks, avoid overusing stiff report words such as `证据`, `边界`, `矩阵`, and `模型`. Prefer more natural phrasing such as `实测结果`, `已确认内容`, `依据`, `不能推出`, `仍未说明`, `对照表`, or `分层检查`, unless quoting an original file title.

Forbidden wording:

- 强信号
- 强正向
- 很自然
- 最省事
- 皆大欢喜
- 全功能签核完成
- MAROC 全功能
- 真值
- 证据来源
- “不是……而是……” style phrasing

## Evidence discipline

- Read the relevant Obsidian notes, datasheets, RTL/testbench summaries, and existing PPT before changing claims.
- Do not fabricate ILA, oscilloscope, GUI, or experiment screenshots.
- Use placeholders for missing images and say what should be inserted.
- Treat XSim PASS as RTL-flow evidence, not board signoff.
- Treat current increase as board-level supporting evidence, not chip behavior proof.
- Treat threshold-DAC voltage response as register behavior evidence, not trigger/ADC/upload completion.

## Page patterns

- Directory: two-column section cards with number, section name, page range, and one-line content.
- Section divider: navy background, large section number/title, one-line purpose.
- Theory: one datasheet object or editable timing diagram per page, 2-3 explanatory lines.
- Hardware issue: phenomenon, cause/evidence, fix, current conclusion.
- ILA/waveform: one large screenshot per page when possible; annotate only key signal windows.
- Register result: method page, curve page, conclusion/boundary page.
- Ctest timing: draw editable lanes; SCA hold levels start from HOLD1/HOLD2 sampling edges; keep `start_ADC`, `TransmitOn`, and `Out_ADC` separate.
- Conclusion: 2-3 restrained conclusions plus next action.

## Template asset

When a new deck is requested, start from the MAROC template asset if present:

`assets/MAROC科研汇报模板_20260519.pptx`

If the asset is absent, reproduce the same style manually.

## Asset Library

- Use `C:/Users/Administrator/.codex/hardware-assets/source-refs/maroc-ppt-assets.md` to locate reusable MAROC decks, build scripts, PNG previews, QA reports, and template variants.
- Use `C:/Users/Administrator/.codex/hardware-assets/templates/ppt/MAROC科研汇报模板_20260519.pptx` as the central reusable template snapshot when the local skill asset is absent or the task asks for asset-library reuse.
- Use `C:/Users/Administrator/.codex/hardware-assets/templates/ppt/build_ppt_skeleton.py` and `qa_ppt_checklist.md` for new reproducible deck generation.
- Use `C:/Users/Administrator/.codex/hardware-assets/hooks/hardware-hook-registry.yaml` for `ppt.qa.*` hooks such as `ppt.qa.hardware-skill-intro`. Dry-run first; preserve hook run logs with the deck QA report.
- Keep source decks in their original project/archive folders. Do not move PPT archive files into the skill directory.

## QA checklist

- Export PNG checks at 1600×900.
- Confirm slide count and page numbers.
- Confirm native PowerPoint section count, section names, first slide, and slide count for long decks.
- Search for forbidden wording.
- Search PPTX XML for disallowed fonts: `Consolas`, `黑体`, `Noto Sans SC`, `Microsoft YaHei UI`, `Microsoft YaHei`.
- Check shape geometry in the generated PPTX: every shape's left/top/right/bottom must stay inside the 16:9 slide bounds, allowing only a tiny numerical tolerance.
- Check all placed pictures for aspect-ratio distortion by comparing the displayed width/height ratio with the native image ratio. Any unintended distortion should fail QA.
- For formula slides, inspect exported PNGs at 1600×900 and reject formulas with vertically stretched or horizontally compressed glyphs, even when the surrounding formula image box has the correct aspect ratio.
- Check focus screenshots for minimum visible size in the exported PNG. A screenshot that technically exists but cannot be read on a projector is not acceptable.
- Check exported PNGs for body readability, loose enough line spacing, no text pressed against card edges, no title wrapping into dividers, and no crowded tables.
- Check waveform and diagram slides at full size: curves must be smooth, readable, correctly shaped for the MAROC circuit path, and free of model artifacts, random text, fake units, watermarks, or jagged hand-drawn segments.
- Check key pages visually: directory, section divider, theory diagram, hardware issue, ILA/waveform, Ctest timing, conclusion.
- Reject the output if any main text overflows, overlaps, is clipped, or is readable only because the font was reduced below the stated minimums.
- Reject technical figures if their plotted shape conflicts with the datasheet, Obsidian notes, or known RTL/FEE signal semantics, even if the image looks polished.
