# ADC And DAC Vpp-Codepp Calibration Workflow

## 1. Define The Quantities

Fit one amplitude point per capture:

`Vpp=k·Codepp+b`.

Report `k`, `b`, `R²`, residual RMS, maximum absolute residual, point count, used/excluded points, and each exclusion reason.

State the voltage reference plane explicitly: signal-generator setting, board connector, analog-front-end output, ADC pins, or DAC output. State whether `Codepp` comes from sine fitting, peak averaging, or min/max.

## 2. Input Level And 50 Ohm Source

For a sine specified in dBm into 50 ohm:

`Vrms=sqrt(50·10^((dBm−30)/10))`.

`Vpp=2·sqrt(2)·Vrms`.

A signal-generator 50 ohm setting is not automatically the voltage at the board connector or ADC pins. Record output mode, termination, cable/load, and whether the displayed amplitude assumes a matched load.

Keep `Vpeak`, `Vpp`, and `Vrms` distinct.

## 3. Front-End Gain And Reference Plane

If ADC-pin amplitude is `V_ADC=G_AFE·V_connector`, then:

`k_connector=k_ADCpin/G_AFE`.

The reviewed AD2208 2026-07-16 slopes are already external-connector-referred. Do not divide them by 1.8 again. Multiply by 1.8 only when presenting the corresponding ADC-pin slope.

For mean-removed PSD/ASD, use only the slope. A Vpp-Codepp intercept is an amplitude-fit extrapolation and is not ADC DC offset.

## 4. Point Estimation And Screening

- Prefer raw-code sine fitting `c[n]=A sin(2πfn/fs+φ)+C` and use `Codepp=2|A|`.
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

- measurement CSV with every source level, estimated Codepp, quality metrics, fit-use flag, and exclusion reason;
- fit-summary CSV with definition, reference plane, gain, slope, intercept, R², residuals, and formulas;
- fit/residual figure with used and excluded points; ensure annotation boxes do not cover data;
- reproducible MAT result and source hashes.

Never combine the summary from one timestamp with measurements or plots from another timestamp. Treat central calibration workbooks as secondary until their method and source run match the reviewed Vpp-Codepp evidence.
