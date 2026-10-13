---
name: laser-electrical-data-analysis
description: Analyze Laser electrical-test measurements into traceable evidence bundles, or audit duplicate files and archive contents by SHA-256. Use for noise, calibration, isolation, numerical report evidence, and read-only duplicate audits; keep report formatting and data moves in their dedicated workflows.
---

# Laser Electrical Data Analysis

Before consuming profile-derived inputs, read [path validation](../hardware-dev-router/references/profile-path-resolution.md) and run its read-only validator for the required keys only (or validate an explicit task path). Missing inputs stop dependent work; do not create obsolete directories or guess replacement campaigns. Keep existing CLI/environment overrides ahead of profile defaults.

Use measured artifacts as the only technical source. Never infer an unrecorded sampling rate, reference plane, termination, gain, calibration, or test condition.

Read `<CODEX_HOME>/laser-fpga-profile.json` before resolving the Laser source, Obsidian, or test-data roots. Command-line arguments and `LASER_TEST_*` environment variables override the profile. Probe the historical laser-fpga-runtime Python before use; an installed path does not prove its underlying interpreter is still available.

运行脚本前按 [运行时验证](../hardware-dev-router/references/runtime-validation.md) 探测实际 Python 版本和所需导入；优先复用可执行专用环境。

## Select the mode first

- **Numerical analysis**: use the workflow below. For DAC isolation, AD677 slope updates, channel splitting or screenshot estimates, read [analysis methods](references/qualification-analysis-methods.md). Read [dated cases](references/qualification-analysis-cases.md) only when that campaign is relevant.
- **Duplicate/content audit**: read [duplicate and archive workflow](references/duplicate-audit.md); use scripts/audit_duplicates.py --root <data> --out <outside-data> and scripts/compare_archive.py --root <data> --archive <rar> --out <outside-data> --scratch <task-temp>. This mode does not run MATLAB or require the numerical bundle contract. No deletion executor is provided.
- **PicoScope export troubleshooting**: read [local GUI case](references/picoscope-export-case.md); available computer-control capabilities govern execution, not old scripts.

Check the Python executable and imports before use. The historical venv may be unavailable; use an existing runtime with needed dependencies without rebuilding global environments. Read-only audit helpers depend on sibling hardware-evidence-report-sync/scripts/evidence_paths.py.

## Current project rules

For 513/CW tasks, first read the project AGENTS.md, memory/PROJECT_MEMORY.md current summary, and relevant device README. Historical memory entries retain their dated scope. Read [script routing](references/script-routing.md) for exact noise entry differences and [calibration workflow](references/calibration-workflow.md) for board selection. Keep project-specific coefficients in the project catalog, not in this skill.

## Start a numerical analysis task

1. Read references/workspace-map.md. Use scripts/inventory_workspace.py with explicit *-root overrides and --require-root for only the required roots; historical digital_lock_report fields are inventory hints, not current report authority.
2. Read `references/script-routing.md` and select the narrowest existing MATLAB entry that matches the data and indicator.
3. Read `references/psd-asd-workflow.md` for spectrum/noise work or `references/calibration-workflow.md` for ADC/DAC calibration. Read both for input-equivalent noise.
4. Record source paths, sizes, modification times, SHA-256 hashes, channel, acquisition condition, coding, sampling rate, duration, termination/load, and requirement band before calculation.
5. Preserve raw data. Write complete analysis outputs below the configured test-data campaign directory unless the user explicitly chooses another result root.

## MATLAB skill boundary

This skill owns measurement conditions, coding/units, calibration/reference planes, PSD/ASD methods and evidence bundles. For requested code work, select only the relevant companion: `matlab-clean-code` (readability), `matlab-review-code` (read-only findings), `matlab-modernize-code` (release/API migration), `matlab-testing` (regression), `matlab-validate-function-arguments` (input contract), or `matlab-write-help` (documentation).

General style or modernization advice must preserve established algorithms, accepted inputs, units, configuration precedence and numerical baselines. It does not authorize replacing a validated analysis method. Discover available MATLAB MCP or local runtime before execution; when only static inspection is possible, do not claim calculated results or passing MATLAB tests.

## Core Workflow

Follow this order:

`discover -> verify acquisition -> choose script -> resolve calibration/reference plane -> calculate -> quality-check -> judge coverage -> package evidence -> synchronize report`

- Reject or downgrade a result when the data format, code decoding, sample rate, frequency coverage, calibration reference plane, gain, or unit cannot be established.
- Prefer task-specific validated scripts over a generic script. Do not rewrite a new PSD or fit implementation when an applicable current script exists.
- For every AD input-level calibration, the formal axis is mandatory `CodePp -> Vpp`: convert any dBm source label to Vpp first, then fit `Vpp = a*CodePp + b`. dBm is traceability metadata, never the formal fit axis. The default conversion reference is 50 ohm; an explicit manifest/configuration impedance and reference plane take precedence. If impedance or reference plane is unknown, do not silently convert; downgrade to `暂不能判定`.
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

For an AD calibration bundle, also require `InputPowerDbm` (when present), converted
`InputVoltageVpp`, `ReferenceImpedanceOhm`, reference-plane/load definition,
`CodePp`, `SlopeVppPerCodePp`, `InterceptVpp`, fit R², residuals, valid range,
exclusion reasons, and both formulas:

```text
Vpp = a*CodePp + b
CodePp = (Vpp - b)/a
```

All formal MATLAB PNG/FIG evidence must pass through the shared light-theme
export path. The exporter must explicitly set a white figure/axes background,
black axes and text, and light-gray grids/legend borders; never rely on the
MATLAB Desktop theme. Reject a bundle whose representative figures have a
black background or insufficient contrast.

Use `scripts/audit_analysis_bundle.py <result-dir> --strict` before quantitative report handoff. A report must consume the audited bundle; do not recalculate values inside a DOCX-editing script.

## Report Handoff

- Use `laser-test-report-writing` to place verified results in a report and add laser-electrical-test-report-standard only for explicitly requested formal cover/contents/header/pagination.
- Keep complete data products in the selected campaign result tree and reports in their current authorized document directory; old directory examples are not relocation instructions.
- If Word has a `~$` lock file, do not overwrite, refresh, export, or hash the open report. Wait for closure or create a separate revision only when authorized.
- State unresolved coverage, calibration quality, and evidence limitations next to the corresponding result and in the final indicator table.

## Resources

- `references/workspace-map.md`: current roots, folder responsibilities, active report/requirement files, and calibration-source precedence.
- `references/script-routing.md`: current device/task entry routing, inputs, outputs, and limitations; verify actual entry names.
- `references/psd-asd-workflow.md`: PSD/ASD, integrated-noise, equivalent-input, spur, coverage, and result rules.
- `references/calibration-workflow.md`: CodePp-to-Vpp fitting, 50 ohm source conversion, reference planes, gain, intercepts, exclusions, and datasheet checks.
- `scripts/inventory_workspace.py`: read-only workspace inventory; prints JSON unless `--output` is supplied.
- `scripts/audit_analysis_bundle.py`: structure-only legacy audit; --strict validates declared evidence layers. Read [strict acceptance](references/strict-bundle-contract.md).
