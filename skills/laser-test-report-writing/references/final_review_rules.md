# Final Editorial Review Rules

Use this reference for a final editorial pass, de-AI cleanup, conclusion synchronization, or a format-preserving revision of an existing Chinese engineering test report.

## Editing Boundary

- Treat final review as a surgical revision. Preserve the source, level-1 chapter structure, measured values, tables, formulas, images, styles, and conclusion-affecting limitations.
- Create a separate output unless replacement is explicitly authorized. Record the source path, SHA-256, size, modification time, and Word lock state.
- Do not invent an instrument model, reference plane, board-end voltage, termination, cable loss, loaded control word, calibration state, or unrecorded test condition.
- Do not convert `未测试` to `暂不能判定`, or a numerical comparison to `满足`, without the required coverage and measurement-chain information.

## Engineering De-AI Pass

Keep the formal engineering register. Do not make the report conversational.

Delete text that carries no test information:

- document self-narration such as `本报告汇总`, `本报告涉及`, `正文保留`, or descriptions of how the report was assembled;
- review-system language such as `当前证据`, `证据边界`, `证据覆盖`, `形成可追溯`, `核心结果`, or `判定与问题` when a direct test statement can replace it;
- project-management labels such as `P0 阻塞项`, `当前测试状态`, or `优先级闭环`;
- empty transitions such as `值得注意的是`, `可以清楚地看到`, `综合来看`, and `综上所述`;
- mechanical labels such as consecutive `测试条件：`, `结果分析：`, `定量观察：`, and `结论：` when natural paragraphs carry the same structure.

Do not ban ordinary words mechanically. Keep a term when it provides technical meaning. Apply three checks before deleting or rewriting: density, information load, and register. A phrase is a de-AI target when it repeats, can be moved to another report unchanged, and can be removed without losing a condition, value, anomaly, or limitation.

Prefer direct engineering sentences:

- `在……条件下，测得……。`
- `实测值为……，低于/高于……指标。`
- `由于……未记录，本项暂不能判定。`
- `现有数据只能说明……，不能用于判断……。`

Keep most paragraphs to two through four sentences. Replace abstract audit language with the actual object, action, value, missing condition, or next discriminating test. Do not add personal voice or invented detail to make technical prose sound human.

## Repetition And Figure Commentary

- When a table already lists every channel value, state only the range, maximum, minimum, channel spread, failed points, anomalies, and effect on the conclusion.
- Compress repeated channel paragraphs into a horizontal comparison. Keep a per-channel sentence only for a channel-specific anomaly or exclusion.
- After a figure, state the most important numerical result, the anomaly, and its effect on the conclusion. Do not repeat the legend or all table values.
- Remove broad references such as `见表 9～表 13 及图 4～图 6`. Cite only an adjacent figure or table when the reference helps the reader.
- Make each report self-contained. Replace `具体流程同另一份报告` with the minimum complete connection, acquisition, processing, and conversion method.

## Conclusion Matrix

Before saving, build an internal matrix:

`报告 | 测试项目 | 摘要结论 | 正文结论 | 最终结论 | 是否一致`

Apply these rules:

- Use only `满足`, `不满足`, `暂不能判定`, and `未测试` as formal states.
- Keep a numerical comparison separate from the formal state. `低于指标限值` does not by itself mean `满足`.
- Use `暂不能判定` when data exist but the duration, band, range, reference plane, method, instrument chain, loading proof, repeatability, calibration, or uncertainty is incomplete.
- Use `未测试` only when no applicable measurement was performed.
- For a row with no formal requirement, write `无独立指标` in the requirement field. `仅作分析` may appear as a non-formal disposition only when that row explicitly contains `无独立指标`; otherwise omit the conclusion cell or move the note to `备注`.
- Distinguish a screening observation from a formal state. State the risk in prose and keep the formal state `暂不能判定` when the screening method cannot support a pass/fail decision.
- Ensure the summary, body, result tables, figure annotations, and final conclusion use the same state and the same measured value.

## Terminology, Numbers, And Units

- Use one official device, board, channel, interface, and instrument name throughout. Use `PicoScope` at first mention; an established abbreviation may follow.
- Use `AD9245 器件本底`, not `裸芯片本底`. Use `剔除异常窗口后的数据段`, not `正常数据段`, when exclusion occurred.
- Distinguish frequency deviation, theoretical step, loaded control word, measured resolution, stability, and output continuity.
- Use `Vpp`, `Codepp`, and `µVpp/codepp` for peak-to-peak calibration. State `Vpp = k·Codepp + b` and the reference plane.
- Insert a space between a value and its unit: `1 MHz`, `100 kHz`, `50 Ω`, `100 kSPS`, `9.40 dBm`, `2.19 µV/√Hz`.
- Use `ASD @ 1 Hz` and `ADEV @ 1 s` consistently. Use the mathematical minus sign `−`, the Chinese range connector `～`, and a multiplication sign in scientific notation, for example `4.74×10⁻¹²`.
- Reject damaged exponent sequences such as `10 ¹² ⁻`, `10 ¹⁻ ⁰`, or `10 ⁶⁻`.
- Preserve the source precision unless it exceeds the recorded measurement resolution. Never change a measured value while normalizing typography.

## Tables, Captions, And Word Objects

- Keep formal conclusion cells limited to the four formal states, with the `无独立指标` exception above. Put anomaly details in `备注`, not in the conclusion cell.
- Do not use `—` for an unknown conclusion. Use `未记录`, `无独立指标`, or the appropriate formal state in the correct field.
- Keep units in headers where practical. Avoid AI/review headings such as `核心结果`, `正式状态`, or `证据`; prefer `测试结果`, `数据条件`, `结论`, and `备注`.
- Keep figure/table numbering continuous. Remove stale TOC entries and wrong broad cross-references, then refresh fields on the output copy.
- Preserve native Office Math, drawings, embedded objects, and existing images. Do not flatten them during text cleanup.

## Render And Delivery Check

Render the final DOCX to PDF or page images when the environment supports it. Inspect every page for:

- TOC entries, dotted leaders, and page numbers;
- table width, repeated headers, row splits, and clipped text;
- formula structure, exponents, units, subscripts, and superscripts;
- figure/table numbers, captions, image clarity, and nearby interpretation;
- page breaks, orphan headings, detached captions, abnormal blank pages, and large unexplained blank areas;
- comments, highlights, tracked insertions/deletions/moves, and the track-revisions setting.

Natural unused space on the final page is not a defect. Do not restructure a report merely to fill it.

When requested, produce modification notes, a conclusion-consistency matrix, and representative literal before/after examples. Report changed text-object counts and removed-duplicate counts only when they can be measured; otherwise use qualitative counts rather than inventing integers.
