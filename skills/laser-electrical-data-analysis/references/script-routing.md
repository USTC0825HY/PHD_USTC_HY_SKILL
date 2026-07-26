# MATLAB Script Routing

Use the code root from `workspace-map.md`. Inspect the script configuration and source data before running it; this table routes tasks but does not replace parameter verification.

| Script | Preferred task | Input | Main output/limitation |
|---|---|---|---|
| `s01_convert_ila_to_pico_mat.m` | Convert ILA codes for voltage-domain analysis | Vivado ILA CSV | MAT with `A` and `Tinterval`; verify coding and voltage scale first |
| `s02_analyze_pico_psd_asd.m` | Generic exploratory PSD/ASD | Pico/converted MAT | Welch spectrum and band statistics; not a task-specific formal judge by itself |
| `s03_calc_dac_integrated_noise_1k_100k.m` | DAC 1 kHz–100 kHz integrated noise | Voltage MAT | PSD integral in µVrms; do not integrate ASD |
| `s04_separate_ad_da_noise.m` | Optional AD/DA noise separation | Matched total and DAC-baseline MAT | Subtract PSD only; matching and negative-bin audit required |
| `s05_compare_ad_p1_p100_input_noise.m` | P=1 versus P=100 chain comparison | Two matched MAT captures | Total-chain input-referred comparison; not ADC device floor |
| `s06_calibrate_ila_single_sine.m` | Single-point ADC diagnostic | One sine ILA CSV | Local scale only; cannot establish full-range linearity |
| `s07_calibrate_ila_multi_sine.m` | Formal ADC Vpp-Codepp calibration | Multiple level-labelled ILA CSV | Fit summary, measurements, fit/residual plot, MAT |
| `s08_calibrate_dac_multi_sine.m` | Formal DAC Vpp-Codepp calibration | Multiple `code_*` Pico MAT files | Fit summary, measurements, fit/residual plot, MAT |
| `s09_analyze_ad_input_equiv_noise_new_flow.m` | ADC–FPGA–DAC total-chain equivalent-input noise | DAC-output MAT plus ADC/DAC slopes and FPGA gain | Default: no DAC/Pico baseline subtraction; optional matched PSD subtraction |
| `s10_analyze_adc_grounded_csv_input_noise.m` | Direct grounded-ADC code noise | ILA CSV | Code PSD scaled by reviewed ADC slope |
| `s11_analyze_dac_output_noise_metrics.m` | DA output ASD@1 Hz and integrated noise | Pico voltage MAT | Verify duration and 1 Hz resolution before judgment |
| `s12_batch_allan_stability_analysis.m` | ADEV/MDEV and 1 s stability | Counter CSV/TXT | Requires frequency column, cadence, nominal frequency, gap/outlier policy |
| `s13_analyze_ad9245_psd_asd_datasheet_scale.m` | AD9245 datasheet-scale cross-check | AD9245 data or audited summary | Estimate/cross-check; distinguish measured and theoretical scale |
| `s14_analyze_ad2208_jg12_jg15_10m25m_noise.m` | JG12/JG15 10–25 MHz noise indicator | 100 MSPS ILA CSV | Welch plus full-record spur screening; external-interface scale |
| `s15_analyze_dac766_c1_noise_metrics.m` | DAC766 `C1_data/C1_time` noise | Pico MAT | Guards short records that cannot resolve 1 Hz |
| `s16_analyze_jg18_jg3_g100_1hz_noise.m` | JG18–G100–JG3 1 Hz total-chain noise | Time-axis/value MAT | Window sensitivity and segment stability; no DAC/Pico subtraction |

## Priority Rules

- Use `s14`, not generic `s02`, for the JG12/JG15 10–25 MHz formal indicator.
- Use `s16`, not one arbitrary periodogram bin, for the JG18 1 Hz total-chain result.
- Use `s07`/`s08` for multi-point calibration; use `s06` only for a diagnostic point.
- Use `s10` for direct ADC code-stream noise. Use `s09` only when the observed waveform is at the DAC/Pico output of an ADC–FPGA–DAC chain.
- Use `s04` only when the user requests baseline separation and matched baseline evidence exists. The current formal total-chain scheme does not subtract DAC/Pico background.

## Preflight

Before execution, record:

- actual source files and hashes;
- sample rate, duration, channel/probe, radix, coding, data column, validity field;
- frequency band and required statistic;
- calibration slope source, reference plane, method, and quality;
- analog and FPGA gains;
- output directory and whether it is outside the formal-report directory.

Reject scripts containing merge-conflict markers. Run MATLAB `checkcode` after modification and before formal use.

Resolve reviewed per-channel scale data with `laser_latest_fit_summary(deviceType, interfaceName)`. `s09`, `s14`, and `s16` use this helper by default; do not silently fall back to the historical aggregate calibration workbook.
