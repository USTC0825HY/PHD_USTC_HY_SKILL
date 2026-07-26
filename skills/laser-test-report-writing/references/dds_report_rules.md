# DDS Report Rules

Use this reference for DDS frequency range, output power, stability, frequency-control-word, and micro-frequency-difference reports.

## Architecture By Editing Mode

For a new report or deep reconstruction, use this order unless the user supplies an approved project structure:

1. Test purpose and conclusion summary
2. Test object, system connection, shared conditions, and requirement sources
3. DDS1/DDS2 device result chapters
4. Anomalies and test limitations
5. Summary and follow-up tests
6. Appendices for formulas, processing parameters, instrument records, and data sources

State shared requirements and instrument-chain information before the result chapters. Keep item-specific acquisition and processing next to the result they produce. Result subsections must not repeat long method descriptions; present the data/table/figure, quantitative observation, conclusion, and indicator relationship directly.

For a surgical or final editorial revision, preserve the approved level-1 chapter structure and existing result order. Do not move control-word theory to the first subsection, add missing architecture chapters, or rebuild comparison tables merely to satisfy this preferred order. Repair only contradictions, duplicated content, broken references, unsupported conclusions, and local readability defects in scope.

## Methods Chapter

Record the actual instrument model, asset number, calibration state, reference source, connection, gate time, sample interval, RBW/VBW, averaging, attenuation, and cable-loss correction when available. Use `未记录` for absent factual records. Use `暂不能判定` when existing numerical data cannot support a formal conclusion because the measurement chain or requirement is incomplete.

For frequency/power tests, show the chain `DDS output -> cable/attenuator -> spectrum analyzer`, the upper-computer configuration evidence, the target frequency and FTW, the measured/corrected power, and the frequency-versus-power plot.

For stability tests, show `DDS output -> frequency counter -> exported CSV -> analysis computer`, the upper-computer configuration evidence, acquisition timing, preserved time axis, ADEV/MDEV method, drift treatment, anomaly rule, and distinguishability statistics.

## Per-DDS Result Order

Within each DDS device chapter in a new report or deep reconstruction, prefer:

1. Control-word theory
2. Data quality and time-domain result
3. Output power
4. Frequency stability
5. Micro-frequency-difference measurement and distinguishability
6. Device summary, when useful

Put control-word theory first when building or reconstructing the device chapter because it defines the configured frequency and theoretical quantization step. Do not enforce this order during a surgical revision.

## Control-Word Evidence

Keep these evidence levels separate:

- Theoretical capability: accumulator width, system clock, one-LSB frequency, integer FTW difference, and theoretical frequency difference.
- Loaded state: upper-computer transmit log, register readback, or ILA evidence.
- Measurement capability: measured group difference, uncertainty/confidence interval, and instrument/reference-chain evidence.

A theoretical LSB or calculated FTW does not prove that the value was loaded or resolved by the counter. State `实际加载状态未确认` until direct loading evidence exists; use `暂不能判定` for the corresponding formal measurement conclusion.

## Stability And Distinguishability

Calculate fractional frequency with the actual carrier for each group:

`y = (f - reference frequency) / actual carrier frequency`.

Do not use a script's default 100 MHz denominator for 90 MHz or 110 MHz results. If a script has a fixed denominator, correct the result to the actual carrier and independently recompute it.

Use Raw overlapping ADEV at 1 s for the formal stability comparison when that is the defined metric. Use detrended ADEV and Raw/Detrended MDEV as auxiliary diagnostics unless the requirement states otherwise.

ADEV/MDEV describe fluctuation level, not the static mean frequency difference. Determine micro-frequency distinguishability from the two-group mean difference, standard error, confidence interval, and sensitivity to the selected block lengths. Compare the interval with both zero and the target difference.

Do not put arbitrary implementation cross-check tolerances or internal numerical QA differences in the formal result narrative unless they are specified measurement requirements or uncertainty terms.

## DDS Figures

- Create one ADEV/MDEV figure for each baseline frequency. Put ADEV on the left and MDEV on the right; show Raw and Detrended only for that frequency.
- Create a separate ADEV/MDEV comparison for the baseline and micro-frequency-shift groups.
- Draw a red vertical dashed line at `tau = 1 s` and label the Raw and Detrended 1 s values from the calculated curves.
- Put time-domain/drift plots with data quality, power curves after time-domain results, stability plots with stability results, and block-mean/confidence-interval plots with distinguishability.
- Insert each figure once and interpret its exact values next to it.

## Final DDS Tables

For a new report or deep reconstruction, create separate DDS1 and DDS2 comparison tables with:

`测试项｜指标值｜本次实测/计算值｜测试结果｜判定`

List the requirement and measured/calculated numeric values directly. Include uncovered items instead of adding verbose evidence columns. During a surgical revision, preserve an existing useful schema and normalize only the relevant fields.

- `满足` when the requirement, range, duration, reference plane, measurement chain, and repeatability are sufficiently covered and the value meets the requirement.
- `不满足` when coverage is sufficient and the value or observed behavior fails the requirement.
- `暂不能判定` when numerical evidence exists but the requirement source, measurement chain, repeatability, loading evidence, calibration, or uncertainty is incomplete.
- `未测试` when no applicable measurement was performed.

If a DDS2 stability requirement is not confirmed, write `指标未确认` in the requirement field and `暂不能判定` in the formal status field. Do not copy a DDS1 requirement to DDS2. Keep dropouts or output discontinuities as independent observations even when the formal stability state remains `暂不能判定`.

Write theoretical capability as a numerical relation such as `1 LSB 小于 0.025 mHz`, not `理论满足`. Separate theoretical step, confirmed loading, measured frequency difference, and measured resolution.

The overall conclusion may only summarize established result rows. Map each gap to a concrete action and required evidence without using project-management labels such as `P0 阻塞项`.
