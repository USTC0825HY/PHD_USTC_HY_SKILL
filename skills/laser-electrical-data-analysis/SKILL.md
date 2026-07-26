---
name: laser-electrical-data-analysis
description: Analyze Laser/PDH electrical-test data and produce traceable evidence bundles from Vivado ILA CSV, PicoScope MAT, counter CSV/TXT, calibration CSV/XLSX, and existing MATLAB results. Use for PSD/ASD, integrated noise, ADC/DAC Vpp-Codepp calibration, input-equivalent noise, total-chain/noise-separation analysis, 1 Hz noise, Allan stability, spectral-band indicator decisions, or when a report needs reproducible numerical results before DOCX editing.
---

# Laser Electrical Data Analysis

Use measured artifacts as the only technical source. Never infer an unrecorded sampling rate, reference plane, termination, gain, calibration, or test condition.

## Start Every Task

1. Read `references/workspace-map.md`, then run `scripts/inventory_workspace.py` to refresh paths and current artifacts.
2. Read `references/script-routing.md` and select the narrowest existing MATLAB entry that matches the data and indicator.
3. Read `references/psd-asd-workflow.md` for spectrum/noise work or `references/calibration-workflow.md` for ADC/DAC calibration. Read both for input-equivalent noise.
4. Record source paths, sizes, modification times, SHA-256 hashes, channel, acquisition condition, coding, sampling rate, duration, termination/load, and requirement band before calculation.
5. Preserve raw data. Write complete analysis outputs below the applicable `G:\01_laser\202607_电2test` campaign directory unless the user explicitly chooses another result root.

## Core Workflow

Follow this order:

`discover -> verify acquisition -> choose script -> resolve calibration/reference plane -> calculate -> quality-check -> judge coverage -> package evidence -> synchronize report`

- Reject or downgrade a result when the data format, code decoding, sample rate, frequency coverage, calibration reference plane, gain, or unit cannot be established.
- Prefer task-specific validated scripts over a generic script. Do not rewrite a new PSD or fit implementation when an applicable current script exists.
- Treat configured values, direct measurements, calculated values, and formal indicator conclusions as different evidence classes.
- Use only `满足`, `不满足`, `暂不能判定`, and `未测试` as formal conclusion states.
- Keep hypotheses separate from observations. State the controlled retest that distinguishes each plausible cause.

## Analysis Bundle Contract

Create one self-contained result directory per task. It must contain or identify:

- analysis parameters CSV;
- summary CSV;
- channel-level full PSD/ASD CSV when spectral analysis is performed;
- ASD and PSD figures, plus spur/residual/stability figures when applicable;
- a reproducible MAT result or an equivalent machine-readable result;
- source file path, size, modification time, and SHA-256;
- script path/version, all processing parameters, calibration source, reference plane, gain treatment, exclusions, and formal conclusion.

Use `scripts/audit_analysis_bundle.py <result-dir>` before report handoff. A report must consume the audited bundle; do not recalculate values inside a DOCX-editing script.

## Report Handoff

- Use `laser-test-report-writing` to place verified results in a report and `laser-electrical-test-report-standard` for the project DOCX contract.
- Keep complete data products in the data tree. Keep formal DOCX/PDF files in `01_正式报告`; keep historical or review copies in `02_过程报告`.
- If Word has a `~$` lock file, do not overwrite, refresh, export, or hash the open report. Wait for closure or create a separate revision only when authorized.
- State unresolved coverage, calibration quality, and evidence limitations next to the corresponding result and in the final indicator table.

## Resources

- `references/workspace-map.md`: current roots, folder responsibilities, active report/requirement files, and calibration-source precedence.
- `references/script-routing.md`: `s01` through `s16` task routing, inputs, outputs, and limitations.
- `references/psd-asd-workflow.md`: PSD/ASD, integrated-noise, equivalent-input, spur, coverage, and result rules.
- `references/calibration-workflow.md`: Vpp-Codepp fitting, 50 ohm source conversion, reference planes, gain, intercepts, exclusions, and datasheet checks.
- `scripts/inventory_workspace.py`: read-only workspace inventory; prints JSON unless `--output` is supplied.
- `scripts/audit_analysis_bundle.py`: evidence-bundle structure and metadata audit.
