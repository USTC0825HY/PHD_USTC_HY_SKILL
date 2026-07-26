# MAROC Debug Report Patterns

## Use This Reference When

Read this before creating a MAROC TransmitOn/Ctest/ADC/read-register debug report deck, especially a 40-50 page closed-loop board-debug PPT based on Obsidian notes, ILA CSV, datasheets, FEE schematic, and host logs.

## Report Structure

Use this order for long debug reports:

1. Title, one-page conclusion, task boundary, and three-chain definition.
2. Git/version, bit/ltx, Vivado/ILA, host tool, signal source, and board setup.
3. Configuration chain evidence: Host -> USB -> FIFO -> parser -> SlowControl -> MAROC SC pins.
4. Control chain evidence: START latch -> cfg gate -> auto_mode -> Hold/RST_ADC/start_ADC -> TransmitOn.
5. Upload chain evidence: TransmitOn + Out_ADC -> data_socket -> FA5A/payload/FEEE -> FIFO/USB/host.
6. Round-by-round evidence table with hypothesis, operation, evidence, judgment, and next step.
7. Datasheet/User Guide/FEE schematic comparison.
8. Root-cause classification tree and next minimum experiment.
9. Appendix: file paths, command logs, CSV list, missing screenshots, and unresolved proof gaps.

## Evidence Rules

- Use ILA CSV plots only when generated from original CSV files; label the source CSV and round.
- Do not draw fake waveforms. Use editable timing diagrams only for expected timing or conceptual explanation.
- Datasheet/User Guide/FEE schematic screenshots must include a `参考：...` footer.
- Missing scope/board images should be explicit placeholders: `待补真实截图：...`.
- Treat oscilloscope `OUT_AMP_Q/OUT_AMP_FS` images as analog evidence; treat ILA as digital control/readout evidence.
- Treat current increase as a board-level observation, not as proof of chip functional response.

## Claim Boundaries

- Configuration-chain success does not imply Ctest/ADC success.
- `w_sc_done/cfg_done_latched` proves configuration activity completed at the FPGA/SC pin level; it does not prove analog path behavior.
- `OR` proves trigger boundary only; it does not prove ADC conversion.
- `Hold/RST_ADC/start_ADC` proves FPGA control timing only; it does not prove MAROC returned data.
- `TransmitOn/Out_ADC` proves an ADC output window exists; it does not prove host receive or correct payload interpretation.
- `FA5A + 64 payload + FEEE` proves FPGA write-side frame formation; it does not prove Ctest charge response unless `Ctest_ch=0/1` A/B is shown.
- `OUT_Q/OUT_FS` claims require read-register/probe selection plus real analog-output observation.

## Ctest And Slow Shaper Pages

Include these distinctions:

- MAROC `Ctest` is the board/ASIC analog injection input. FPGA `o_ctest` is a debug output and must not be described as charge injection.
- `Ctest_chN` only enables the internal about-2 pF injection capacitor for channel N; it does not generate charge by itself.
- Official Ctest stimulus is a negative step with slow recovery ramp and attenuation; a generic 5 kHz 5 Vpp square wave is not equivalent evidence.
- Normal-channel injection is the fallback path when Ctest remains inconclusive.
- Slow shaper waveform observation should be presented as either direct `OUT_AMP_Q` oscilloscope evidence or Hold-delay scan reconstruction.

## Page Patterns

- Evidence page: large image/plot, 2-3 callouts, concise conclusion, `参考：...` footer.
- Round summary page: compact table with `假设 / 操作 / 证据 / 判断 / 下一步`.
- Root-cause page: tree with categories `RTL`, `host`, `packet/config`, `Vivado/ltx`, `ADC timing`, `datasheet interpretation`, `board connection`, `signal source`.
- Next-step page: minimum experiment only; avoid broad task lists.
- Missing-evidence page: list exact screenshots/logs to acquire and what each would prove.

## QA Checklist Additions

- Search for overclaims: `ADC/Ctest 已签核`, `TransmitOn 链路已跑通`, `MAROC 全功能`.
- Verify every screenshot/plot has a traceable file path or explicit placeholder.
- Verify the deck never equates `cfg_done` with ADC/Ctest success.
- Verify all bit/ltx/ILA claims mention the actual programmed artifact or state that it is unverified.
- Check exported PNG readability for root-cause trees and round tables; split if crowded.
