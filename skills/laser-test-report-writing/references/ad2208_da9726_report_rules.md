# AD2208 And DA9726 Report Profile

Load this profile only for the digital-lock-board AD2208/DA9726 chain or the named interfaces JG12, JG15, JG18, JG2, JG3, JG32, and JG11. Treat historical conflicts below as checks to perform, not as facts for a different board or test campaign.

## Naming And Test Object

- Use `数字锁定板`, not `数字锁定版`, when the hardware board is intended.
- Prefer the formal title `数字锁定板 AD2208/DA9726 性能测试报告`; avoid underscores in the visible report title.
- Confirm whether records use LTC2208/AD2208/YB2208 or DA9726/DAC9726/B9726 as true part names, aliases, or errors before normalizing them.

## Input Range, Saturation, And Frequency Response

- Distinguish near-full-scale input, maximum undistorted input, first-clipping input, and saturation input.
- Repeated contact with code 32767 or −32768 indicates possible clipping; a near-rail code alone does not prove maximum undistorted range.
- Require stepped input, pre/post-clipping waveforms, and preferably THD or sine-fit residuals before claiming maximum undistorted input.
- Resolve Vpeak/Vpp/Vrms and source-setting/actual-input distinctions before comparing against an amplitude requirement.
- For a frequency response measured at only 1, 5, 10, 15, 20, 25, and 30 MHz:
  - report only the measured points;
  - do not claim DC capability when DC was not tested;
  - state that 30 MHz has not reached −3 dB when supported;
  - do not extrapolate a specific cutoff frequency.
- Treat `Codepp ≈ 2|Codepk|` from a single ILA cursor as an initial screenshot-peak check. State the missing negative peak, sampling-phase error, source-flatness correction, actual ADC-pin Vpp, and sparse-point limitations.
- Prefer raw-code sine fitting `x[n]=A sin(2πfn/fs+φ)+C` and compute `H(f)=20 log10[A(f)/A(fref)]` for a formal response result.
- Treat nonmonotonic response as an anomaly. Consider source flatness, cable/connector/termination, analog front end, sampling phase, cursor error, and operating-condition changes as hypotheses to distinguish by retest.

## Vpp–Codepp Calibration

- State the reference plane: signal-generator setting, board connector, analog-front-end output, or ADC pins.
- State termination and loading. A 50 Ω source setting is not automatically the voltage at the ADC pins.
- Record any analog-front-end gain separately. If ADC-pin voltage equals connector voltage times `G_AFE`, then the connector-referred slope is the ADC-pin slope divided by `G_AFE`; do not divide twice.
- Fit `Vpp = k·Codepp + b` and report slope in `Vpp/codepp` or `µVpp/codepp`, intercept, R², residual RMS, point count, used/excluded points, and exclusion reasons.
- Do not interpret the Vpp–Codepp intercept as ADC DC offset. A constant DC code offset cancels in peak-to-peak amplitude.
- Do not remove inconsistent points solely to improve R². Distinguish a valid full-range calibration from a local high-quality fit and require a retest when the full dataset is nonmonotonic or conditionally inconsistent.

## ADC–FPGA–DAC Total-Chain Noise

When the path is AD2208 -> FPGA digital gain -> DA9726 -> PICO and DAC/PICO background is not subtracted, name the result `ADC–FPGA–DAC总链路输入端等效噪声` or equivalent. State that it includes ADC, FPGA, DAC, instrument, clock, power, connection, and environmental contributions and is not the ADC device floor.

For

`V_in = k_ADC C_ADC + b_ADC`,  
`V_out = k_DAC C_DAC + b_DAC`,  
`C_DAC = G C_ADC`,

use, after mean removal,

`S_ADC,in,eq(f) = S_out,total(f) [k_ADC/(G k_DAC)]²`

and

`A_ADC,in,eq(f) = sqrt(S_ADC,in,eq(f))`.

Record units: `k_ADC` and `k_DAC` in `Vpp/codepp` or `µVpp/codepp`, `G` in code/code, PSD in V²/Hz, and ASD in V/√Hz. Do not include `b_ADC` or `b_DAC` in mean-removed PSD/ASD scaling.

Never shorten an ADC–FPGA–DAC total-chain equivalent-input result to `AD2208 器件本底`, `AD9245 器件本底`, or `ADC 本底`. Device-floor language requires an independently established subtraction or isolation method and sufficient records for every downstream contribution.

Use `conservative upper bound` only after confirming linearity, no clipping/overflow, correct gain, appropriate response correction, no obvious aliasing, and approximately uncorrelated contributions. Otherwise call it the current configuration's total-chain equivalent-input result.

## Sampling And Spectral Coverage

- Compute acquisition duration as `N/fs` and Nyquist frequency as `fs/2`; reconcile every conflicting point-count, sample-rate, and duration statement.
- A 10 MSPS record covers at most approximately 0–5 MHz and cannot judge a 10–25 MHz noise requirement.
- For a 1 Hz ASD requirement, record duration, frequency resolution, mean removal, detrending, window, segment length, overlap, NFFT, estimator stability, and instrument background. Mark the item `暂不能判定` when these do not support a reliable 1 Hz value.
- For integrated noise, use `V_rms = sqrt(∫ S_v(f) df)` and report the band and unit `µVrms`.
- A single-segment Hann estimate or a single 1 Hz bin requires an explicit variance and drift limitation.

## DA9726 Results

- Separate 0 V, +1 V, and −1 V noise conditions. Completion of 0 V alone does not complete the full DC-noise item.
- Do not infer −3～+3 V range, 200 Ω load operation, ≥15 mA drive, or four-channel consistency from a local scale fit.
- Require four-channel full-code scans, unloaded and 200 Ω measurements, voltage/current, linearity, positive/negative endpoints, and clipping/current-limit observations for output-range and load conclusions.
- For 1 MHz phase-noise tests, record channel, carrier frequency and power, configured and actual duration, sample count, mode, bandwidth, reference source, and calibration state.
- When several channels show the same far-offset value, consider analyzer-floor limitation. A result below the indicator may support `满足`, but do not claim the displayed difference as true device margin without a background trace.
- Describe common spurs by channel, frequency, and amplitude. Treat power, clock, analyzer, and environment as hypotheses; distinguish them by background, supply, carrier-frequency, clock-configuration, and connection-state comparisons.

## Historical Conflict Checklist

For the 2026 digital-lock-board report family, explicitly search source text, tables, captions, and images for:

- JG12 input-power records that disagree;
- JG18 records that mix 1.2 Vpeak, 2.4 Vpp, and 1.2 Vpp;
- an unverified JG15 input-power note;
- point count, sample rate, and duration inconsistency in DA DC-noise data;
- shortened JG11 phase-noise acquisition;
- missing independent JG3 phase-noise evidence;
- missing analyzer calibration, source flatness, PICO configuration, firmware version, Welch parameters, DC point, ±1 V noise, load/drive, 10–25 MHz ADC noise, 1 Hz JG18 noise, and AD2208 temperature drift.

If the source artifacts close a conflict, cite the resolving artifact. Otherwise keep the value out of formal determination and record `暂不能判定` or `未测试` as appropriate.
