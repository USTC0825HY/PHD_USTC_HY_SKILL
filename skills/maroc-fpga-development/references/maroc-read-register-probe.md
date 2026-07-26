# MAROC Read Register And Analog Probe

## Use This Reference When

Read this before implementing or debugging MAROC3A `RSTb_R/CK_R/D_R/QBUF_R`, `OUT_Q`, `OUT_FS`, read-register/probe selection, slow shaper waveform observation, or host/RTL probe-control commands.

## Stable Facts

- Datasheet: the read register is for debugging and reading the analog multiplexer for charge measurement.
- `out_q` is the multiplexed Slow Shaper / 2x64 SCA analog output; `out_fs` is the multiplexed Fast Shaper analog output.
- The read register is controlled by `CK_R`, `RSTb_R`, and `D_R`; `QBUF_R` is the return chain output.
- The probe shift register is 128 flip-flops. `CK_R` period is limited by analog multiplexer settling; use a conservative 1 us period unless a measured reason exists to go faster.
- `EN_otaq` enables the multiplexed analog output. On the current FEE netlist it is not an FPGA command pin; verify the board-level bias/enable state before blaming RTL.
- FPGA ILA cannot see the analog shaper waveform. It can only prove the digital control pins, trigger/hold/ADC control, `TransmitOn`, `Out_ADC`, and data-socket/upload path.

## Current FEE Board Anchors

- `OUT_Q`: MAROC `U13.A10` routes into the slow-output buffer path and then to `OUT_AMP_Q`.
- `OUT_FS`: MAROC `U13.B14` routes into the fast-output buffer path and then to `OUT_AMP_FS`.
- Board test points exist for `OUT_AMP_Q` and `OUT_AMP_FS`; use oscilloscope evidence from these nodes for analog waveform claims.
- `J15/R160` is the MAROC `Ctest` input path, not a slow shaper output.

## Current RTL Baseline

- `TOP_MAROC.v` already has `o_ck_r`, `o_rstn_r`, `o_d_r`, and `i_qbuf_r`.
- Current baseline ties the pins off: `o_ck_r=0`, `o_d_r=0`, `o_rstn_r=1`.
- `maroc_usb_packet_parser` parses `probe_mode`, but current TOP does not use it to drive the ASIC read register.
- Therefore, a slow-shaper observation task needs both RTL probe-driver work and host command alignment.

## Minimum RTL Contract

Implement a small `maroc_read_probe_driver` with:

- Inputs: `i_start`, `i_channel[5:0]`, `i_sca_sel`, `i_raw_mode`, `i_raw_index[6:0]`.
- Outputs to ASIC: `o_rstn_r`, `o_ck_r`, `o_d_r`; input from ASIC: `i_qbuf_r`.
- Status/debug: `o_busy`, `o_done`, `o_error`, `o_state`, `o_bit_cnt`, `o_shift_data`.
- Clocking: default `CK_R` period about 1 us; at 40 MHz this is about 20 cycles low + 20 cycles high.
- Behavior: ignore or flag `i_start` while busy; provide a reset/status clear path; expose enough debug for ILA.

Keep one-hot probe selection simple first:

- Default mapping candidate: `bit_index = channel + (sca_sel ? 64 : 0)`.
- Treat this mapping as provisional until `OUT_AMP_Q/OUT_AMP_FS` real board evidence confirms it against datasheet Table 13 and User Guide SCA1/SCA2 behavior.
- Preserve `raw_mode/raw_index` so board debug can sweep `0..127` without rebuilding RTL when the bit order is unclear.

## Minimum Host/RTL Command Contract

Use this default legacy command allocation unless a real address conflict is found:

| Address | Name | Data |
|---|---|---|
| `0x30` | `PROBE_CHANNEL` | `0..63` |
| `0x31` | `PROBE_SELECT` | `bit0=sca_sel`, `bit1=raw_mode` |
| `0x32` | `PROBE_RAW_INDEX` | `0..127` |
| `0x33` | `PROBE_CTRL` | `bit0=start`, `bit1=reset_status` |

If any address conflicts with existing `command_MAROC` use, stop and define a new shared address table before editing RTL or host code.

## Verification And Evidence

- Module TB: reset defaults, one complete shift, raw-index mode, busy re-entry handling, and `CK_R` period.
- TOP-level TB or replay: legacy commands update channel/select/raw/control registers and produce one read-register transaction.
- ILA probes: `probe_start`, `probe_busy`, `probe_done`, `probe_state`, `probe_bit_cnt`, `probe_channel`, `probe_sca_sel`, `probe_raw_mode`, `probe_raw_index`, `o_ck_r`, `o_d_r`, `o_rstn_r`, `i_qbuf_r`.
- Board evidence: oscilloscope screenshot from `OUT_AMP_Q` or `OUT_AMP_FS`, plus matching host command log and ILA capture of the read-register pins.
- Do not claim slow-shaper waveform success from read-register ILA alone.

## Slow Shaper Observation Paths

- Direct analog path: configure slow control, select channel/SCA with read register, inject signal, observe `OUT_AMP_Q`.
- Reconstructed path: scan `Hold1/Hold2` delay and use internal ADC payload to reconstruct the slow-shaper curve. This requires `OR -> Hold -> ADC -> TransmitOn -> Out_ADC -> data_socket` to be working first.
