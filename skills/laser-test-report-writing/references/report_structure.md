# Engineering Test Report Structure

Use this reference for new reports and deep reconstruction. Treat the default architecture and core summary schema as mandatory only in those modes. During a surgical or final editorial revision, preserve the user-approved level-1 structure unless a local adjustment is required to remove a duplicate, repair a conflict, or restore a broken reference.

## Default Engineering Narrative

Use this order for a formal device or board test report:

1. **Cover and report information**
   - Report name, document number, version, test date, report date, personnel, location, author/reviewer/approver, and revision record.
2. **Test purpose and conclusion summary**
   - Identify the test object, completed items, main measured results, unresolved items, overall conclusion, and decisive limitations.
   - Keep this chapter within one or two pages when practical.
   - Use one core result table: `对象 | 测试项目 | 指标 | 测试条件 | 实测结果 | 结论 | 备注`.
3. **Test object, system connection, and shared conditions**
   - Describe board/device state, channel mapping, signal path, clocks, firmware/software, instruments, terminations, loads, cables, bandwidth, and common acquisition settings.
   - Show a system diagram that matches the actual test path. Mark unrecorded items explicitly.
4. **Result chapters by device and test item**
   - Order by hardware object, then by the reader's engineering question; do not follow file order.
   - Keep item-specific connections, procedures, and processing with the corresponding result.
5. **Anomalies and test limitations**
   - Consolidate cross-item anomalies, conflicting records, instrument limits, incomplete coverage, and conditions that weaken conclusions.
6. **Summary and follow-up tests**
   - Summarize only conclusions already established. List mandatory retests before optional improvements.
7. **Appendices**
   - Recommended: formulas; processing parameters; instrument settings/calibration; raw screenshots; data/script index; conflicts and unresolved records.

Aim for a readable main report of roughly 12–15 pages when the amount of evidence permits. Do not shrink figures or tables to meet a page target.

## Result-Item Pattern

Write each test item in this sequence:

1. **Purpose**: state the property or indicator being tested.
2. **Conditions**: state the actual connection, input, load, clock, sample rate, duration, range, and instrument settings relevant to the result.
3. **Method**: describe what was physically done, including the sequence of condition changes.
4. **Data processing**: define formulas, reference plane, exclusions, frequency resolution, windowing, fitting, and units.
5. **Result**: present a compact table and the minimum set of readable figures.
6. **Analysis**: quote exact values, trends, anomalies, residuals, failed points, and measurement limitations.
7. **Conclusion**: relate the result to the indicator using one formal state and an explicit qualification when needed.

Do not centralize every method in one early chapter. Centralize only common equipment and shared configuration; repeat neither generic theory nor full instrument descriptions inside every result item.

## Value And Conclusion Classes

Keep these classes separate:

- **Configured value**: software setting, register value, nominal source setting, or theoretical capability.
- **Direct measurement**: value obtained from the current instrument or raw record.
- **Calculated value**: value derived from measurements using a stated formula.
- **Formal conclusion**: comparison with a requirement after coverage and conditions are verified.

Use only these formal states:

- `满足`: required range, condition, band, duration, and evidence are covered and the result meets the indicator.
- `不满足`: coverage is sufficient and the result fails the indicator.
- `暂不能判定`: data exist, but conflicts, missing conditions, method limits, or incomplete coverage prevent a valid decision.
- `未测试`: no applicable measurement was performed.

Do not mix these with `通过`, `部分通过`, `待补证`, `正式通过`, `数值通过`, or `整项待补测` as formal states.

For an item with no formal requirement, write `无独立指标` in the requirement field. `仅作分析` is a non-formal disposition and is allowed only when the same row explicitly identifies `无独立指标`; otherwise place the explanation in `备注` and leave formal status out of that row.

## Figures And Tables

- Insert each quantitative figure once, in the subsection whose question it answers.
- Introduce the question before the figure; state numerical observations and the supported conclusion after it.
- Use one figure for one main conclusion. Use paired figures only when direct comparison materially helps.
- Use tables for channel mapping, conditions, measured results, requirement comparison, conflicts, and follow-up tests.
- Keep units in headers, preserve meaningful significant digits, and avoid prose paragraphs in cells.
- Keep a single core summary table. Detailed indicator rows may appear in the relevant result section or appendix, not as a duplicate summary.

## Anomalies And Limitations

Use this structure for each significant issue:

- **Observed phenomenon**: what changed, where, and under which condition.
- **Available data**: exact values, frequencies, channels, or screenshots.
- **Effect on the conclusion**: whether the issue changes, qualifies, or blocks the decision.
- **Possible causes**: list only technically plausible hypotheses supported by the context.
- **Confirmation method**: state the comparison or controlled retest that distinguishes the hypotheses.

Do not name a unique root cause unless the available test discriminates it.

## Follow-Up Test Table

Use `项目 | 当前缺口 | 后续测试 | 必须保存的数据 | 优先级`.

Every row must map to an unresolved indicator, conflict, missing operating condition, or anomaly. State the test condition and evidence that will close the item. Avoid time-relative wording such as `明天计划`.

## Traceability

Keep the main body readable. Use short data identifiers and filenames there. Put complete absolute paths in the data appendix together with a project-relative path where possible.

Use `数据编号 | 内容 | 测试日期 | 原始文件 | 处理脚本 | 版本` for the data index. Do not assume a drive letter will exist on another workstation.
