# Data And Formula Rules

Use this reference before writing PSD/ASD, integrated noise, ADC/DAC scaling, or noise-separation sections.

## PSD And ASD

Use voltage PSD:

$$
S_v(f)\ [\mathrm{V^2/Hz}]
$$

Use voltage ASD:

$$
A_v(f)=\sqrt{S_v(f)}\ [\mathrm{V}/\sqrt{\mathrm{Hz}}]
$$

For `nV/√Hz`:

$$
A_{v,\mathrm{nV}}(f)=10^9 A_v(f)
$$

Do not compare a PSD curve directly with an ASD requirement. If the requirement is `300 nV/√Hz`, the PSD threshold is:

$$
S_{\mathrm{limit}}=(300\times 10^{-9})^2\ \mathrm{V^2/Hz}
$$

## Integrated Noise

For DC/noise integration over `f1` to `f2`:

$$
V_{\mathrm{rms}}=\sqrt{\int_{f_1}^{f_2}S_v(f)\,\mathrm{d}f}
$$

State the integration band and sampling/acquisition condition near the result.

## Noise Separation

PSD can be subtracted:

$$
S_{\mathrm{AD,est}}(f)=S_{\mathrm{total}}(f)-S_{\mathrm{DA}}(f)
$$

ASD is then derived by square root:

$$
A_{\mathrm{AD,est}}(f)=\sqrt{S_{\mathrm{AD,est}}(f)}
$$

Do not directly subtract ASD values. `182 nV/√Hz - 80 nV/√Hz` is not a valid noise separation calculation.

If PSD subtraction creates negative bins, report the negative-bin ratio. A small ratio can be measurement noise; a large ratio means the separation result needs review.

## ADC/DAC Scaling

When converting codes to voltage, state:

- ADC/DAC bit width
- coding type, such as offset binary or two's complement
- full-scale input/output range
- analog front-end gain
- sampling rate

For ADC noise at a front-end input, divide the ADC voltage noise by the analog gain. For ADC-pin noise, do not divide by front-end gain.

## ADC Input-Equivalent Noise From DAC Output

Use this flow when the measured signal is DAC output noise but the target result is ADC input-equivalent noise.

First subtract the DAC fixed mid-code baseline at the PSD level:

$$
S_{\mathrm{ADC\to DACout}}(f)=S_{\mathrm{Vout,total}}(f)-S_{\mathrm{DAC,mid}}(f)
$$

Then convert PSD to ASD:

$$
A_{\mathrm{ADC\to DACout}}(f)=\sqrt{S_{\mathrm{ADC\to DACout}}(f)}
$$

Convert DAC output voltage noise to equivalent DAC input code noise:

$$
A_{\mathrm{DAC,code}}(f)=\frac{A_{\mathrm{ADC\to DACout}}(f)}{K_{\mathrm{out}}}
$$

Convert DAC input code noise to ADC code noise with the FPGA transfer:

$$
A_{\mathrm{ADC,code}}(f)=\frac{A_{\mathrm{DAC,code}}(f)}{|H_{\mathrm{FPGA}}(f)|}
$$

If FPGA behavior is only a constant gain, use:

$$
A_{\mathrm{ADC,code}}(f)=\frac{A_{\mathrm{DAC,code}}(f)}{G}
$$

Convert ADC code noise to ADC input-equivalent voltage noise:

$$
A_{\mathrm{ADC,in}}(f)=A_{\mathrm{ADC,code}}(f)\cdot L_{\mathrm{ADC}}
$$

Required parameters:

- `S_DAC,mid(f)`: DAC fixed mid-code baseline including instrument noise
- `K_out`: DAC output calibration in `V/code`
- `G` or `H_FPGA(f)`: FPGA code gain or transfer function
- `L_ADC`: ADC input calibration in `V/code`

If any required parameter is missing, the report must state `待 DAC/ADC 刻度后计算`.

## Reporting Bands

Always keep the measured band separate from the requirement band. Example:

- measured summary band: `0~5 MHz`
- requirement band: `10~25 MHz`

Do not write a requirement conclusion when these bands differ.
