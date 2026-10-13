# 历史快照：不作为当前默认路径或校准值

以下保留原20260816参考；使用前按当前任务复核。

# Laser Electrical Test Workspace Map

Last verified: 2026-08-16. Refresh this snapshot at the start of every task with `scripts/inventory_workspace.py`; do not select a file only because it is newest by modification time.

## Stable Roots

| Role | Root |
|---|---|
| MATLAB code | Validated `matlab_code_root` from profile, or explicit `--code-root` / `LASER_TEST_CODE_ROOT`; current workspace authority is `F:/01_Laser/code/matlab` |
| 513 test MATLAB library | `F:\01_Laser\code\matlab\513DIANXING_analysis\CW_analysis\CW_513_ANALYSIS` |
| Raw data and complete analysis results | `<test_data_root>` |
| Report corpus | `<obsidian_vault_root>\01_科研主系统\04_实验测试与证据\03_超稳激光电控箱指标测试\LASER 测试报告\202607` |

Environment overrides used by current scripts:

- `LASER_TEST_CODE_ROOT`
- `LASER_TEST_DATA_ROOT`
- `LASER_TEST_REPORT_ROOT`
- `LASER_TEST_513_CODE_ROOT` (overrides the current 513 test MATLAB library)
- `LASER_TEST_513_DATA_ROOT` (overrides the current 513 test data root)

## Current 513 Test Library

The current 513 test MATLAB library is the authoritative entrypoint for AD9245, AD2208, DA9726, and DA766 processing:

`F:\01_Laser\code\matlab\513DIANXING_analysis\CW_analysis\CW_513_ANALYSIS`

Use the device folders `9245_hy`, `2208_hy`, `9726_hy`, and `766_hy`. Shared algorithms are under `_shared\+converter`; `legacy` and the old `laser_analysis\01_workflows` implementations are historical or one-way compatibility layers and must not be selected as the primary algorithm source.

The current 513 test data root is:

`F:\01_Laser\20260727_513test\CW_Data\513_CW_DATA`

Relevant subtrees include `AD9245`, `AD2208`, `DA9726`, and `DA766`. Store generated bundles under the campaign's result directories; preserve raw files.

## Data Tree

- `测试参考文件_20260630`: requirements, board test instructions, exported design tables, and test logic notes.
- `SZSD_AD2208`: AD2208 raw ILA/Pico data, calibration campaigns, grounded/noise captures, and ADC-chain analysis.
- `SZSD_DAC9726`: DA9726 scale, DC-noise, and phase-noise data.
- `SZSD_rf_ref`: digital-lock-board RF reference and counter data.
- `YCQD_AD_9245` and `YCQD_DA766`: delayed-driver-board ADC/DAC evidence.
- `PLZH_DDS`: synthesizer-board DDS data.
- `处理结果_20260710`: audited historical processing outputs; use for traceability, not automatically as the newest truth.

Store a task's complete CSV/PNG/MAT output below the configured test-data campaign in a clearly dated analysis subdirectory. Do not write analysis output directly into `01_正式报告`.

## Report Tree

- `01_正式报告`: final DOCX/PDF and approved TODO workbooks only.
- `02_过程报告`: historical component reports, local supplement versions, review materials, and curated report-only copies.
- `04_修订过程与问题记录`: report-revision records.
- `05_历史备份与中间版本`: historical backups.
- `06_辅助清单与缺失项`: evidence manifests and missing-item lists.
- `90_临时锁文件` and `99_*`: temporary or pre-revision preservation areas; never use as the active source without explicit instruction.

Current digital-lock-board formal source:

`01_正式报告\02_SZSD_数字锁定板\数字锁定板测试报告.docx`

It is user-edited and may be open in Word. Preserve it and use surgical revisions only.

## Current Requirement Source

Primary requirement file:

`<test_data_root>\测试参考文件_20260630\超稳激光电控箱第2套电性件性能测试项_20260715.docx`

Compare its content and internal date/version with other requirement files before using it. A later filesystem timestamp alone does not establish authority.

## Current AD2208 Calibration Evidence

Primary Vpp-Codepp evidence is the latest reviewed per-channel `fit_summary` plus its matching `measurements` CSV under:

`<test_data_root>\SZSD_AD2208\20260716_AD2208_scale\<channel>\multi_sine_ad_calibrate`

Reviewed external-interface slopes from the 2026-07-16 campaign are approximately:

| Channel | Interface-referred slope | Evidence status |
|---|---:|---|
| JG12 | 17.589655 µV/code | 10-point broad-range fit; one near-rail point excluded |
| JG15 | 19.807065 µV/code | four-point local stable-region fit; limited evidence, retest required for formal full-range calibration |
| JG18 | 17.761757 µV/code | 0.3–1.0 Vpp fit; high-end point retained only as validation evidence |

These slopes already refer to the external board input. Do not divide them by the 1.8 front-end gain again.

Historical `AD_DA_calibration_table.xlsx` workbooks near or below `<test_data_root>` contain AD peak-fit entries and are not the primary source for current AD Vpp-Codepp scaling. Use them only after row definition, reference plane, method, and source file have been reconciled with the reviewed per-channel summaries.

## Current Task-Specific Evidence

### 513 Test Campaign

- AD2208 SFDR: `F:\01_Laser\20260727_513test\CW_Data\513_CW_DATA\AD2208\01_SFDR`.
- AD2208 isolation: `F:\01_Laser\20260727_513test\CW_Data\513_CW_DATA\AD2208\04_Isolation`.
- DA9726 noise: `F:\01_Laser\20260727_513test\CW_Data\513_CW_DATA\DA9726\03_Noise`.
- DA766 noise: `F:\01_Laser\20260727\CW_Data\513_CW_DATA\DA766\03_DCNoise`.
- Current MATLAB entry library: `F:\01_Laser\code\matlab\513DIANXING_analysis\CW_analysis\CW_513_ANALYSIS`.

- JG12/JG15 100 MSPS noise input: `SZSD_AD2208\20260716_AD2208_noise`.
- JG12/JG15 10–25 MHz result bundle: use the configured test-data copy generated by `s14`; a process-report copy is historical evidence.
- JG18 1 Hz total-chain data and results: `SZSD_AD2208\JG18_20s_100ksps_G100.mat` and `SZSD_AD2208\JG18_G100_JG3_1Hz_analysis_20260716`.
- DA9726 scale: `SZSD_DAC9726\20260707_dac_scale`.
- DA9726 phase noise: `SZSD_DAC9726\20260707_phase_noise`.

## Selection Rules

1. Prefer a reviewed result whose source hash and processing parameters are recorded.
2. Keep raw, measurement, summary, and plot timestamps from the same run together.
3. Never combine a fit summary from one run with measurement rows from another run.
4. If the central workbook and reviewed run differ, use the reviewed run and record the workbook conflict.
5. If the active report is locked, inventory it but do not modify or export it.
