# ADC/DAC Calibration Workflow (display unit: V/code)

## 1. Define The Quantities

For AD input calibration, fit one amplitude point per capture in the fixed
forward direction:

`Vpp=a·CodePp+b`.

`CodePp` is the sine-fit peak-to-peak ADC code (`2 × fitted sine amplitude`).
The operational inverse is:

`CodePp=(Vpp−b)/a`.

The formal fit axis is never dBm. If a source level is recorded in dBm, convert
it to Vpp before fitting and retain the original dBm only as traceability
metadata.

Record `a` (display unit V/code), `b` (V), `R²`, residual RMS, maximum absolute
residual, point count, used/excluded points, and each exclusion reason.

State the voltage reference plane explicitly: signal-generator setting, board connector, analog-front-end output, ADC pins, or DAC output. State whether `CodePp` comes from sine fitting, peak averaging, or min/max.

## 2. Input Level And 50 Ohm Source

For a sine specified in dBm into a known resistance `R`:

`Vrms=sqrt(R·1e−3·10^(dBm/10))`.

`Vpp=2·sqrt(2)·Vrms`.

The default is `R=50 ohm`. An explicit manifest/configuration resistance
overrides the default. If the resistance or reference plane is not known, do
not infer a Vpp value.

A signal-generator 50 ohm setting is not automatically the voltage at the board connector or ADC pins. Record output mode, termination, cable/load, and whether the displayed amplitude assumes a matched load.

High-impedance source captures may be reported as a “50 ohm equivalent” Vpp
conversion only when that assumption is explicitly recorded. They are not a
direct board-input power measurement.

Keep `Vpeak`, `Vpp`, and `Vrms` distinct.

## 3. Front-End Gain And Reference Plane

If ADC-pin amplitude is `V_ADC=G_AFE·V_connector`, then:

`k_connector=k_ADCpin/G_AFE`.

Historical example only: the reviewed AD2208 2026-07-16 slopes were external-connector-referred. The 1.8 factor belongs to that recorded front end; apply it only for that batch and reference-plane conversion. New batches require their own recorded conditions.

For mean-removed PSD/ASD, use only the CodePp-to-Vpp slope. A Vpp intercept
is an amplitude-fit extrapolation and is not ADC DC offset.

## 4. Point Estimation And Screening

- Prefer raw-code sine fitting `c[n]=A sin(2πfn/fs+φ)+C` and use `CodePp=2|A|`.
- Check sine-fit R², residual RMS, peak/rail contact, monotonicity, source level, and acquisition consistency before fitting the calibration line.
- Exclude clipped/near-rail points and demonstrably invalid captures with explicit reasons.
- Do not exclude points solely to improve R².
- A nonmonotonic full dataset cannot be converted into a formal full-range calibration by retaining only a convenient subset. Label the result `局部拟合` and require retest.
- Preserve excluded points visibly in the fit plot and measurement table.

## 5. Datasheet Cross-Check

Use the datasheet only as a plausibility check, not as a substitute for measured calibration. Confirm converter mode, PGA/reference configuration, bit width, and true full-scale definition.

For LTC2208:

- PGA low: 2.25 Vpp ADC-pin range, ideal `2.25/65536=34.3323 µV/code`.
- PGA high: 1.5 Vpp ADC-pin range, ideal `22.8882 µV/code`.
- With an exact 1.8 front-end gain and PGA low, ideal connector scale is `19.0735 µV/code`.

Differences of several percent cannot be explained by the datasheet's few-LSB INL/DNL alone. Check actual front-end gain, termination, source amplitude at the connector, reference/PGA state, clipping, and code-path scaling.

## 6. Output Contract

Export:

- measurement CSV with every source level, estimated CodePp, quality metrics, fit-use flag, and exclusion reason;
- fit-summary CSV with definition, reference plane, gain, slope, intercept, R², residuals, and formulas;
- fit/residual figure with used and excluded points; ensure annotation boxes do not cover data;
- reproducible MAT result and source hashes.

The formal calibration figure must show `CodePp` on the horizontal axis and
`Vpp` on the vertical axis. The shared exporter must explicitly normalize the
figure and axes to white, use black text/axes, and use light-gray grids and
legend borders so output is independent of MATLAB Desktop dark-theme settings.
Inspect representative PNGs before handoff and reject black-background or
low-contrast exports.

Never combine the summary from one timestamp with measurements or plots from another timestamp. Treat central calibration workbooks as secondary until their method and source run match the reviewed Vpp-Codepp evidence.

## 7. Current 513/CW board catalog and archive

Use the project catalog and CALIBRATION.md for current coefficients; do not copy numeric defaults into this skill. Built-in records distinguish boardType=jianding/jiaqiang, device, interface and calibrationState. current prefers after, otherwise uses the unique original record; explicit before/after requires that version. Interactive calibrated-noise calls select the board each time; explicit files require boardType. Do not infer it from a folder name.

The two 20261004 report calibration tables are the designated sources for this catalog and take priority over old coefficients in report noise prose. Source hashes/table locations are recorded. PICO uses the same board's ADC and DA9726 JG18; explicit custom calibration is labelled user and competing sources are rejected. DAC voltage noise applies voltage/gain only; scan calibration remains a fit to selected captures.

Display slopes in V/code while preserving ADC CodePp, DA9726 set-code and DA766 code-amplitude definitions and existing API field names. Complete fit details belong in evidence; report-derived missing R² stays empty. The daily summary may omit R².

CSV is the code configuration, the two-sheet XLSX is a generated archive, and the Word tables are the bound source evidence. Editing the archive does not update code. Regenerate from CSV and verify all rows, numeric types, version flags, missing fields and source hashes before handoff.
