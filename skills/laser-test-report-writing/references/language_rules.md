# Engineering Report Language Rules

Use concise, direct, evidence-preserving Chinese. Do not invent or smooth over missing facts. For report-wide final review, repeated-channel compression, conclusion synchronization, and de-AI cleanup, also read `final_review_rules.md`.

## Sentence Logic

Prefer this order:

`object + test condition + action + numerical result + requirement relation + limitation`

Examples:

- `JG12在30 MHz输入条件下相对1 MHz下降0.891 dB。`
- `三路通道在1～30 MHz的已测频点内均未下降3 dB；DC未测试，因此完整DC～30 MHz指标暂不能判定。`
- `三个通道在100 kHz频偏处均显示约−149.5 dBc/Hz，结果可能受相噪仪底噪限制。`

Keep most paragraphs to two through five sentences. Start with the measured condition or observation, not with a generic explanation of what the section contains.

## Remove Document Self-Narration

Delete or rewrite high-confidence template language such as:

- `本流程用于……`
- `本节列出……`
- `下表用于……`
- `以下三张图用于……`
- `每幅图仅在本节出现一次……`
- `图像不在其他章节重复……`
- `结果读法……`
- `证据状态……`
- `证据链……`
- `正式判定……`
- `可形成正式通过结论……`
- `历史复算……`
- `当前方案……`
- `分析边界……`

Avoid empty transitions such as `值得注意的是`, `可以清楚地看到`, `不难发现`, `显而易见`, `综合来看`, and `综上所述` when a direct observation can replace them.

Do not ban ordinary words mechanically. Phrases such as `不能证明`, `不能替代`, `不是`, and `而是` may be technically necessary; reject them only when they form empty contrast rhetoric rather than a precise limitation.

## Conclusion Language

State the measured condition before the formal state:

- `在0 V输出条件下，四路1 kHz～100 kHz积分噪声均低于120 µVrms，0 V工况满足指标。±1 V工况未测试。`
- `现有数据仅覆盖0～5 MHz，不能用于评价10～25 MHz噪声指标，本项暂不能判定。`
- `输入幅度记录存在Vpeak/Vpp冲突，本项暂不能判定。`

Use only `满足`, `不满足`, `暂不能判定`, and `未测试` as formal states. Do not convert a local or partial numerical comparison into an overall `满足` conclusion.

## Anomaly Language

Separate observation from hypothesis:

- Observation: `JG12在20 MHz处下降2.345 dB，25 MHz和30 MHz处幅度回升。`
- Hypothesis: `该起伏可能与信号源平坦度、线缆端接、模拟前端响应或截图光标误差有关。`
- Confirmation: `需使用原始码流正弦拟合，并同步测量各频点ADC输入端Vpp。`

Use `可能`, `尚需确认`, or `需通过……区分` for unverified causes. Never change a hypothesis into `由……导致` without discriminating evidence.

## Terminology And Units

- Keep one official name for each device and interface. Do not mix `AD2208/YB2208/Y2208`, `DA9726/DAC9726/B9726`, or `数字锁定板/数字锁定版` unless a source distinction is explicitly explained.
- Distinguish `Vpeak`, `Vpp`, and `Vrms`; distinguish `dBm`, `dB`, `dBc`, and `dBc/Hz`.
- Use `PSD` for power spectral density and `ASD` for its square root. Keep `V²/Hz`, `V/√Hz`, `nV/√Hz`, `µV/√Hz`, and `µVrms` consistent.
- Use the mathematical minus sign `−` for negative quantities in formal prose and tables.
- Insert a space between a number and its unit: `1 MHz`, `300 nV/√Hz`, `10 MSPS`.
- Use consistent significant digits based on measurement resolution; do not imply precision not present in the source.

## Parentheses And Mixed-Language Typography

Apply the profile and OOXML rules in `figure-identity-typography.md`. For formal reports, use 宋体 for Chinese body/table/caption text and Times New Roman for Latin letters, digits, units, identifiers, and paths. Set East Asian and Latin font attributes on the same run; do not split fields, hyperlinks, or formulas merely to change fonts.

Use ASCII parentheses `( )` when the enclosed span contains Latin letters, identifiers, formulas, version strings, or number-plus-unit expressions:

- `采样率(MSPS)`
- `ASD@1 Hz(µV/√Hz)`
- `直流噪声(0 V)`
- `斜率k(Vpp/codepp)`

Use Chinese parentheses `（ ）` for Chinese prose, for example `后续补测（仪器型号未记录）`. Classify the enclosed content before replacing characters; never perform a blind global conversion.

## Captions And References

- Write a concise object-and-condition caption without a terminal period.
- Use the reader-facing form `图N 对象/接口：图像内容`; do not insert a space between `图` and its number.
- Keep evidence IDs and original filenames out of visible captions. Store them in the task-local figure manifest; the seven-column data appendix is required for 513 reports.
- Do not repeat `来源/内容/观察` blocks under every figure. Put paths and provenance in the data appendix.
- Cite every figure and table in the nearby body text. A caption does not replace quantitative interpretation.

## Final Language Check

Verify that the report contains no unsupported value, missing unit, unexplained estimate, over-broad conclusion, time-relative plan, repeated summary, standalone image-inspection chapter, or final conclusion absent from the core result table.
