# 加强件测试结果结构

Default to a compact result document, not a long engineering narrative.

Opening: title, object, update date, and relevant board modification/state. Level 1 identifies board/device; level 2 identifies the indicator. Use automatic multilevel numbering.

Each indicator follows:
1. 测试/分析方法：brief actual stimulus, connection/load, acquisition and processing conditions needed to interpret results.
2. 指标要求：verified requirement with units; `未提供` when absent. Do not infer it from older reports.
3. Result table: concrete interfaces, conditions, measured/calculated values, units and necessary status.
4. 结果说明：key extrema, failed conditions, supported conclusion, and specific limitations or untested items.
5. Only applicable formal result images, each followed immediately by its caption, at the subsection end.

Do not force a `尚未测试内容：无` sentence, empty image, repeated value narrative, opening summary matrix, or extra traceability chapter. The trailing data-traceability appendix is required. Entirely untested items retain their indicator position and state `未测试`, without fabricated table values or figures. Optional pending summaries contain actual unfinished tests, not completed results awaiting judgment.

Formal states: `满足` requires adequate coverage and a passing result; `不满足` requires a valid failing comparison; `暂不能判定` applies when data exist but conditions, requirements, calibration, or coverage are insufficient; `未测试` means no applicable measurement. A missing requirement is `未提供`; `无独立指标` is reserved for explicitly confirmed absence of an independent requirement.

Keep configured, measured, calculated, and judgment values distinct. Hypotheses are not established causes. Put any necessary retest next to the affected result.

Formal long reports are an explicit alternative handled by laser-electrical-test-report-standard. Their cover, contents, summary, conditions and appendix architecture must not be imposed on compact reports. Local edits preserve the current document architecture.
