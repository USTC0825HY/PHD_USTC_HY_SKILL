# PSD, ASD, Integrated Noise, And Equivalent-Input Workflow

## 1. Establish The Acquisition

Record `N`, `fs`, duration `T=N/fs`, Nyquist `fs/2`, input channel, coding, radix, termination/load, reference plane, analog gain, digital gain, and instrument bandwidth. Verify these from data metadata or the test record; do not infer them from a filename alone.

Decode 16-bit two's-complement code `u` as:

`c=u` for `u<32768`, otherwise `c=u−65536`.

Preserve hexadecimal fields as literal text before parsing; spreadsheet import may interpret tokens such as `03e8` as scientific notation.

## 2. Convert To The Required Reference Plane

For direct ADC code noise with reviewed interface slope `k_ADC`:

`v_in[n]=(c[n]−mean(c))·k_ADC`.

For a measured ADC–FPGA–DAC output without background subtraction:

`S_ADC,in,eq(f)=S_out,total(f)·[k_ADC/(|G|·k_DAC)]²`.

`A_ADC,in,eq(f)=sqrt(S_ADC,in,eq(f))`.

After mean removal, calibration intercepts do not participate in PSD/ASD scaling. Do not divide an already interface-referred ADC slope by the front-end gain again.

If baseline separation is explicitly requested, subtract PSD, never ASD:

`S_est(f)=S_total(f)−S_baseline(f)`.

Require matched sample rate, estimator, window, NFFT, reference plane, loading, and operating condition. Report the negative-bin ratio before clipping negative bins for display.

## 3. Welch Estimate

- Remove the mean unless DC is the quantity of interest.
- Use a Hann window and record whether MATLAB `hann(...,'periodic')` or `hanning` was used.
- Record window length, overlap samples/ratio, NFFT, segment count, and frequency resolution.
- Use one-sided PSD for real input data.
- PSD unit: `V²/Hz`; ASD: `sqrt(PSD)` in `V/√Hz`.
- Convert ASD to `nV/√Hz` with `×10^9` or `µV/√Hz` with `×10^6`.

Do not compare a PSD curve with an ASD limit. For a `300 nV/√Hz` limit, the PSD threshold is `(300×10^−9)² V²/Hz`.

## 4. Band Statistics And Spurs

For every formal band, report:

- median ASD;
- mean ASD;
- 95th percentile ASD;
- maximum ASD and its frequency;
- percentage of bins at or below the limit;
- frequency resolution and bin count.

Use a full-record Hann periodogram or an equivalent high-resolution estimator to screen narrow spurs separately from the Welch floor. Do not average a spur away. State the formal rule, for example whether both the Welch band maximum and spur-screen maximum must meet the limit.

## 5. Integrated Noise

Compute:

`V_rms=sqrt(∫[f1,f2] S_v(f) df)`.

Integrate PSD, not ASD. Report the band, bin spacing/integration method, and result in `µVrms` or the required unit.

## 6. Coverage And 1 Hz Results

- Do not judge a 10–25 MHz requirement from a 10 MSPS record; its Nyquist limit is approximately 5 MHz.
- For 1 Hz ASD, report duration, bin resolution, detrending/mean removal, window, overlap, NFFT, segment count, segment-to-segment variation, and window-length sensitivity.
- A single bin or single-segment result must be qualified for estimator variance and drift.
- If the required band, duration, resolution, load, or condition is not covered, use `暂不能判定`.

## 7. Figures And Evidence

- Export separate readable ASD and PSD figures plus a combined plot only when useful.
- Mark the indicator band and limit.
- Place annotations and legends outside dense data regions; never cover curves.
- Export full-resolution numeric spectra, parameter and quality tables, a reproducible MAT result, and input hashes.
- Run `audit_analysis_bundle.py` before report synchronization.
