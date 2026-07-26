# MAROC Debug Handbook

## Use This Reference When

Read this file when the task needs concrete MAROC project memory: RTL edits, USB/FX2 bring-up, slow-control bit order, XSim case design, ILA capture planning, or stage-summary documentation.

For detailed Vivado ILA grouping, colors, trigger presets, and Tcl workflow, use `maroc-ila-workflow.md`.
For read-register/probe driver and `OUT_Q/OUT_FS` analog-output work, use `maroc-read-register-probe.md`.

## Project Evidence Map

- RTL repo: `F:/01_MOUN/01_logic/02_MAROC/SPIROC_REF/01_MAROC_USB`
- Active RTL files: `sources_maroc/TOP_MAROC.v`, `sources_maroc/CY_driver_new.v`, `sources_maroc/maroc_usb_packet_parser.v`
- Key testbenches: `sources_maroc/tb/tb_top_maroc_command_usb.v`, `sources_maroc/tb/tb_maroc_stage2_acq_readout.v`
- Run helper: `sources_maroc/tools/run_tb_top_maroc_command_usb_xsim.ps1`
- Process notes: `C:/01_obsidian/ustc_hy/01_科研主系统/02_项目/MAROC开发/00_MAROC文档/过程开发笔记`
- Current PPT chain: `F:/09_ppt/MAROC阶段性总结_配置链闭环续更版_20260506.js`

Important recent notes:
- `20260506 MAROC配置链阶段性调试总结.md`
- `20260506-USB解码层问题总结.md`
- `20260505 时钟架构与复位信号修复总结.md`
- `20260505 250Byte到829bit全流程追踪.md`
- `20260503-MAROC配置链仿真与829bit主链签核手册.md`
- `20260604 MAROC3A TransmitOn抓波形闭环调试记录.md`
- `20260605 MAROC3A normal-channel注入与FEE输入重设计分析.md`

## Current Stage Conclusion

Use this wording unless stronger evidence exists:

> MAROC 配置链主线很可能已经打通，核心风险已经从“链路是否成立”收敛到“芯片行为是否按配置生效”。

Do not write:
- “MAROC 全部功能已经完成板级签核”
- “ADC/USB 回传链已经完整闭环”
- “电流上涨等价于寄存器位功能生效”

## MAROC3A Ctest / ADC Bring-up Lessons

Use this section for Ctest charge injection, trigger/upload, ADC readout, and fast/slow shaper questions.

### Ctest Terms

Keep these separate:
- Board Ctest SMA / MAROC `Ctest` pin: external analog stimulus input to the chip.
- `Ctest_chN`: slow-control bit that connects channel N to the internal Ctest injection capacitor, about `2 pF`. Use `Ctest_chN -> SC# = 765 + (63 - N)`.
- FPGA `o_ctest`: current board-debug output on FPGA SMA2, used as Hold-active/debug marker. It is not the MAROC Ctest source and not ADC data.

The ADC data path is:

`Ctest SMA -> MAROC Ctest pin -> enabled Ctest_chN capacitor -> preamp/shaper/SCA -> Hold/ADC -> TransmitOn + Out_ADC -> FPGA i_tranmision/i_adc_out -> data_socket -> FIFO/USB`.

Current stable Ctest interpretation:
- The `2 pF` injection capacitor is internal to MAROC3A; do not add an external 2 pF to explain missing Ctest response unless board redesign is explicitly being considered.
- `Ctest_chN=1` opens the selected channel injection path only. It does not generate charge without an external waveform on the MAROC `Ctest` pin.
- The official setup uses a negative voltage step with slow recovery ramp and attenuation. A generic 5 kHz 5 Vpp square wave is not equivalent proof.
- If Ctest remains inconclusive, normal-channel injection is the next independent path to test preamp/fast-shaper/OR and slow-shaper/ADC behavior.

### Ctest Quantitative Checks

- Estimate injected charge with `Qinj ~= Ctest_internal * DeltaV_Ctest`. With `2 pF`, `Qinj[pC] ~= 2 * DeltaV_Ctest[V]`.
- `R160=50 ohm` is an SMA transmission-line termination, not a MAROC functional requirement. Open input can still inject charge, but the chip pin voltage can differ from the function-generator display and can have reflection/overshoot.
- For quantitative Ctest calibration, install or externally add a 50 ohm termination at the board end, set the generator load mode consistently, and measure the actual Ctest voltage at the board.
- For qualitative trigger/debug, open input is acceptable if the Ctest waveform at the board is measured and kept within safe chip limits.
- If increasing waveform amplitude changes DC supply current, treat it as a board-level anomaly to investigate. It may reflect protection structures, ground return, bias coupling, or overdrive rather than valid chip response.

### ADC And Readout Evidence

- In 12-bit mode, `TransmitOn` high for `768` cycles at 40 MHz is the expected order: `12 bit * 64 ch = 768 bit`, about `19.2 us`.
- One frame of `FA5A + 64 payload + FEEE` proves the FPGA write side formed a 64-channel ADC frame. It does not prove USB host receive stability.
- If the active configuration has all `Ctest_ch0..63 = 0`, the payload is baseline/pedestal. It is not Ctest charge response.
- A real Ctest claim needs `Ctest_ch=0` baseline versus single-channel `Ctest_chN=1` A/B under fixed pulse amplitude and Hold timing.
- If acquisition reaches `ST_ADC_WAIT=6` and no further `TransmitOn` arrives, do not start with USB. First inspect MAROC ADC timing, `Rstn_ADC/start_ADCb/Hold1/Hold2/CK_40M`, ADC slow-control bits, reset/start pulse width, and post-readout dead time.

### Slow-Control And Analog Probes

- `small_dac` affects `VTH0/DAC0 -> tp_vth0` only. `VTH1/DAC1 -> tp_vth1` should not move when only `small_dac` changes.
- `tp_vth0/tp_vth1` threshold DAC A/B is a reliable first chip-behavior check before Ctest charge injection.
- `out_fs/out_Q` are analog read-register multiplexed outputs. They need `RSTb_R/CK_R/D_R` Read Register selection before stable channel/probe observation.
- Slow-control success and Ctest pulses do not prove fast/slow shaper waveforms unless the read register and analog measurement path are configured and observed.
- On the current FEE, slow shaper waveform observation should use `OUT_AMP_Q` or a Hold-delay scan. Do not claim a slow shaper waveform from FPGA ILA alone.

## Known Architecture Lessons

### Configuration Chain

Canonical path:

`Host 829bit / raw_104B / packet_250B`
-> `CY_driver_new`
-> `usb_cmd_fifo`
-> `w_cmd_word_valid + w_cmd_word[15:0]`
-> `maroc_usb_packet_parser`
-> `w_parser_sc_data / w_parser_sc_valid / w_parser_sc_start`
-> TOP mux / `w_parser_legacy_block`
-> `SlowControl_MAROC`
-> `RSTn_SC / CK_SC / D_SC`
-> MAROC3A.

Responsibilities:
- Host owns `bits_829`, `raw_104B`, and `packet_250B` generation.
- `packet_250B` includes transport headers/tags/footer; it is not the chip SC truth.
- parser strips `0x03` tags and converts raw 104B into legacy 104B for the existing shifter.
- `legacy_104B` is a compatibility payload, not the host protocol source of truth.
- `o_sc_dout` / `D_SC` is the final slow-control serial truth and should be bit-compared.

### CDC Fix

The old failure mode:
- `CY_driver_new` generated `usb_cmd_wr_en + usb_cmd_data[15:0]` in `usb_ifclk` 25MHz.
- parser/command consumed in 40MHz.
- Local 2FF synchronization of `valid` and 16 independent data bits was unsafe.
- ILA showed raw ingress was correct, but parser consumed `FE01` twice after valid stretch.
- Failure looked like parser/header logic but root cause was CDC valid/data semantics.

The intended architecture:
- Keep `CY_driver_new` in USB IFCLK domain.
- Cross the complete 16-bit command stream with `usb_cmd_fifo` in `TOP_MAROC`.
- Feed both parser and `command_MAROC` from system-domain `w_cmd_word_valid + w_cmd_word`.
- Remove parser-local CDC of `i_rx_word_valid/i_rx_word`.
- Gate `CY_driver_new` release until FIFO ready so the first command is not lost during reset-busy.

### Reset And Clock Naming

Treat reset polarity explicitly:
- Board/top `i_rst`: active-high physical reset.
- `w_rst_soft`: active-high internal reset, suitable for PLL reset.
- `w_rst_n`: active-low internal reset for submodules with `rstn` conventions.
- Do not infer polarity from stale `_n` names without checking board mapping and code.

USB IFCLK lesson:
- Separate smoke bring-up from formal timing signoff.
- A working 25MHz-ish IFCLK path enables USB debugging, but does not close all clock constraints or IO timing.

## Debug Procedure

### 1. USB Front Door

First prove whether bytes enter FPGA:
- Raw ingress ILA should show full 250B packet as 125 16-bit words.
- Look for correct boundaries such as `FFE1 ... EEEE`.
- If raw ingress is correct, do not start by blaming host packet generation.

Capture:
- `rxf_sync_out`
- `rx_cmd`
- FX2 state/debug signals
- endpoint or host send log if available

### 2. FIFO And Parser

Then prove system-domain command stream:
- `dbg_usb_cmd_fifo_rd_en`
- `dbg_usb_cmd_fifo_valid`
- `dbg_usb_cmd_fifo_dout[15:0]`
- `dbg_usb_cmd_fifo_empty`
- parser current state / next state
- packet byte/word count
- error code and offset

Good signs:
- FIFO read side emits one word per read.
- parser leaves IDLE and enters COLLECT/DRAIN/WAIT_DONE as expected.
- parser `packet_valid=1`, `packet_error=0` for valid packets.

Bad signs:
- Same header word appears twice at parser input.
- `FE01` consumed as a later header field.
- error code points at header field even raw packet is correct.

### 3. Slow-Control Execution

Prove that parser output reaches shifter:
- `w_parser_sc_data`
- `w_parser_sc_valid`
- `w_parser_sc_start`
- selected config mux output
- `w_sc_start`
- `w_sc_busy`
- `w_sc_done`
- `rstn_sc`
- `o_ck_sc`
- `o_din_sc` / `o_sc_dout`

Signoff target:
- 104B accepted.
- SC start asserted.
- Busy/done completes once.
- 829 bits emitted.
- Expected bitstream and observed serial bits match exactly.

### 4. Board Evidence

Stage evidence:
- Configuration downlink after fix.
- Power current rises around `+0.2A` after configuration.
- This is a strong positive signal but not final register-function signoff.

Next proof level:
- Pick one slow-control field with observable chip behavior.
- Toggle it and observe a deterministic change.
- If available, use readback or a single-field A/B comparison.

## Verification Strategy

Layer tests by what they prove:
- Parser unit tests: packet format, tag stripping, negative cases.
- SlowControl tests: load, reset, shift count, bit order.
- Top replay: CY/TOP/parser/SlowControl interaction and arbitration.
- Board ILA: real USB timing, real FIFO CDC, real chip pins.

Known blind spot:
- Same-clock or `SIM_GENERIC` tests can hide real CDC failures. Do not use them as CDC proof.

Useful case categories:
- Valid packet baseline.
- Header/tag/footer negative cases.
- Parser over legacy arbitration.
- Busy/backpressure behavior.
- Packet replay from host-generated vector bundle.
- 829bit serial compare.

## Code Change Rules

Prefer these ownership boundaries:
- Put CDC ownership in `TOP_MAROC`, not inside parser or command modules.
- Keep parser focused on packet semantics and adapter conversion.
- Keep `command_MAROC` as legacy/manual/debug path.
- Keep `SlowControl_MAROC` as an executor, not a parser.
- Keep ADC/readout/upload-chain edits separate from configuration-chain fixes unless requested.

When touching RTL:
- Inspect existing debug probes before adding new ones.
- Preserve user changes in a dirty worktree.
- Update or add testbench cases matching the changed behavior.
- Update run scripts only when the case list or compile inputs change.

## Documentation And PPT Pattern

For each issue, document five blocks:

1. Problem phenomenon: what failed, with screenshot/log placeholder.
2. Root cause: what signal/code path proves the cause.
3. Fix: what changed and why it is the right ownership boundary.
4. Verification: XSim, ILA, board observation, or compare result.
5. Boundary: what still cannot be claimed.

Recommended screenshot slots:
- raw USB ingress full packet
- FIFO read-side valid+dout
- parser state/error/offset
- SC start/busy/done
- SC physical pins
- host send success or endpoint snapshot
- power current before/after
- Vivado IP/source inclusion

PPT rules from recent work:
- Keep a versioned output; do not overwrite the latest stable deck unless asked.
- Keep `.js`, `.pptx`, and `.md` companion index aligned.
- Use native PPT shapes for flows and placeholders so later replacement is easy.
- Add screenshot placeholders when evidence images are not ready.
- Phrase conclusions according to evidence level, not optimism.
