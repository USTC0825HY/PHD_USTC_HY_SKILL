---
name: maroc-fpga-development
description: MAROC USB/FPGA development workflow for RTL, bring-up, debug, verification, Obsidian notes, and PPT documentation. Use when Codex works on the MAROC project, especially files under sources_maroc, TOP_MAROC.v, CY_driver_new.v, maroc_usb_packet_parser.v, SlowControl_MAROC.v, command_MAROC, data_socket/auto_mode, XSim testbenches, FX2 USB issues, 829bit/104B/250B slow-control configuration-chain debugging, ILA evidence capture, TransmitOn/Ctest/ADC closed-loop debug, MAROC read-register/probe driver development, OUT_Q/OUT_FS slow/fast shaper observation, or MAROC stage-summary documentation/PPT updates.
---

# MAROC FPGA Development

## Start Here

1. Ground the task in the local project before changing anything:
   - RTL repo: `F:/01_MOUN/01_logic/02_MAROC/SPIROC_REF/01_MAROC_USB`
   - Obsidian notes: `C:/01_obsidian/ustc_hy/01_科研主系统/02_项目/MAROC开发/00_MAROC文档/过程开发笔记`
   - PPT workspace: `F:/09_ppt`
2. Before board debug, RTL edits, host protocol edits, or report generation, record `git status --short`, `git branch --show-current`, and `git rev-parse HEAD`; if relevant work is uncommitted, make or request a snapshot commit before proceeding.
3. Read the relevant notes and actual RTL/testbench diffs before trusting memory.
4. Keep evidence boundaries explicit. For the current bring-up stage, prefer “配置链很可能已经打通” unless a chip-behavior or single-field verification proves stronger.
5. Do not mix configuration-chain claims with ADC/USB upload-chain claims unless the task explicitly covers data readout.

For detailed lessons and checklists, read `references/maroc-debug-handbook.md`.
For Vivado ILA capture/layout/trigger work, read `references/maroc-ila-workflow.md` before proposing Tcl or judging a waveform.
For Ctest, ADC, trigger/upload, or fast/slow shaper bring-up, read the Ctest/ADC sections in those references first.
For MAROC read-register/probe driver work or OUT_Q/OUT_FS slow/fast shaper observation, read `references/maroc-read-register-probe.md`.

## Configuration Chain Mental Model

Use this as the default chain when reasoning about MAROC slow-control:

`Host 829bit / raw_104B / packet_250B`
-> `CY_driver_new` in `usb_ifclk` domain
-> `usb_cmd_fifo` crossing `25MHz -> 40MHz`
-> `w_cmd_word_valid + w_cmd_word[15:0]`
-> `maroc_usb_packet_parser`
-> `w_parser_sc_data / valid / start`
-> TOP arbitration with `command_MAROC`
-> `SlowControl_MAROC`
-> `RSTn_SC / CK_SC / D_SC`
-> MAROC3A.

Keep these responsibilities separate:
- `CY_driver_new`: FX2LP Slave FIFO ingress/egress, not business parsing.
- `usb_cmd_fifo`: the safe command-stream CDC boundary.
- `maroc_usb_packet_parser`: packet validation, tag stripping, raw 104B to legacy 104B adapter.
- `command_MAROC`: legacy/manual/debug path, still useful for bring-up but not the formal packet truth.
- `SlowControl_MAROC`: 104B load, reset, clock divide, 829bit serial output.

## Debug Workflow

1. Prove front-door ingress first: raw ILA should show the full `125` 16-bit words and correct `FFE1 ... EEEE` boundaries.
2. If raw ingress is correct but parser fails, suspect command-stream semantics before packet format.
3. Treat local 2FF sync of `valid + data[15:0]` across `25MHz -> 40MHz` as unsafe. The known fix is TOP-owned async FIFO, then parser/command consume the same system-domain word stream.
4. For parser issues, inspect state, packet byte/word count, error code, error offset, and whether `FE01` or another header word was repeated.
5. For slow-control issues, inspect `sc_start`, `sc_busy`, `sc_done`, `rstn_sc`, `o_ck_sc`, and `o_din_sc/o_sc_dout`; validate 829 serial bits when possible.
6. For board-level claims, capture and archive screenshots/photos: raw USB ingress, FIFO read side, parser state, SC state machine, SC physical pins, host send success, and current change.
7. Split board ILA captures by phase. The config-chain ILA depth is not enough to prove packet ingress, 104B drain, and the full 829bit slow-control tail in one reliable screenshot.
8. Before trusting an ILA signal, verify the RTL debug net is actually connected. Catch self-connections such as `assign dbg_usb_cmd_fifo_valid = dbg_usb_cmd_fifo_valid;`; the correct config-chain connection is `dbg_usb_cmd_fifo_valid = w_usb_cmd_fifo_valid`, followed by rebuild/program.
9. In Vivado hardware-manager waveforms, add uploaded config-chain ILA waves by signal names such as `dbg_usb_cmd_fifo_dout` or `parser_0/r_start_pending`, not by `hw_probe` objects. Avoid fragile WCFG-only flows unless they are known to bind signals on the active uploaded dataset.
10. Keep raw USB and config-chain Tcl flows separate: `raw_head` is `hw_ila_2/u_ila_1` and uses `maroc_raw_collect` with no dynamic `add_wave`; config-chain presets are `hw_ila_1/u_ila_0` and use `maroc_cfg_collect`, which should display uploaded data with the cfg-chain WCFG (`display_hw_ila_data -wcfg`) rather than relying on the active live wave tab.
11. Avoid misleading debug names when reasoning about hardware: current `o_ctest` is an FPGA SMA debug/Hold-active output, not the MAROC `Ctest` input and not ADC data.
12. For board-level cfg-gate and TransmitOn-timeout retest, use the focused Hardware Manager helper `sources_maroc/tools/maroc_trig_upload_wave_groups.tcl`: `maroc_trig_arm_cfg_start` / `maroc_trig_arm_cfg_done` prove cfg gate timing on the trigger ILA, `maroc_trig_arm_timeout` and `maroc_upload_arm_timeout` prove timeout sticky on trigger/upload ILAs, and `maroc_upload_arm_start_adc` is the preferred upload-side anchor when `TransmitOn` never arrives.
13. Treat slow/fast shaper waveforms as ASIC analog-probe evidence, not FPGA ILA evidence. ILA can prove read-register pins, Hold/ADC control, `TransmitOn`, `Out_ADC`, and `data_socket`; it cannot directly show `OUT_Q` or `OUT_FS`.

## ILA CSV Export Workflow

Use the repo script `sources_maroc/tools/maroc_ila_csv_export.tcl` to export Hardware Manager ILA captures to CSV. Source it in the Vivado Tcl console after the board is programmed and after the target ILA core has captured data:

```tcl
source {F:/01_MOUN/01_logic/02_MAROC/SPIROC_REF/01_MAROC_USB/sources_maroc/tools/maroc_ila_csv_export.tcl}
maroc_ila_csv_help
```

Preferred commands:
- `maroc_ila_export_trigger ?csv_or_dir?` exports the trigger/auto-mode ILA.
- `maroc_ila_export_upload ?csv_or_dir?` exports the ADC upload/data_socket ILA.
- `maroc_ila_export_cfg ?csv_or_dir?` exports the config/slow-control ILA.
- `maroc_ila_export_usb ?csv_or_dir?` exports the raw USB ILA.
- `maroc_ila_export_all ?out_dir?` exports every role it can identify without duplicating the same ILA.
- `maroc_ila_export_csv <role_or_hw_ila_name> ?csv_or_dir?` exports a specific role or exact Hardware Manager ILA object.
- `maroc_ila_export_current ?csv_or_dir?` writes the currently displayed `current_hw_ila_data`.

Default exports go under `ila_exports/YYYYMMDD/` with timestamped filenames. Always archive the matching `.bit`, `.ltx`, `register_mapping.txt`, and `packet_250.hex` alongside board-level CSV evidence when making timing or chip-behavior claims.

## Verification Discipline

- Prefer layered proof: module TB -> top replay -> ILA/board evidence.
- Remember that `SIM_GENERIC` or same-clock simulation can hide CDC bugs.
- Do not treat XSim pass as board completion.
- Do not treat current increase, even around `+0.2A`, as a full chip-function signoff; it is a strong stage signal that still needs behavior verification.
- Use bit-level signoff for slow-control: expected 829 bits, observed 829 bits, mismatch 0.
- Treat `FA5A + 64 payload + FEEE` as evidence that the FPGA ADC write-side frame formed; it does not by itself prove USB readout or Ctest charge response.
- If `Ctest_ch0..63` are all `0`, ADC payload is baseline/pedestal. Do not call it Ctest measurement without a `Ctest_ch=0/1` A/B comparison.

## Simulation Strategy

For configuration-gate, ADC-control, or upload-chain regressions, use the
repo flow `sources_maroc/tools/run_maroc_adc_cfg_gate_timeout_sim.ps1`.

- Treat a host-export bundle such as `Config_rtl_vectors_YYYYMMDD_HHMMSS`
  as the input truth, but first flatten it with
  `scripts/flatten_maroc_vectors.py` into readmem-friendly fixtures. The key
  outputs are `sw_packet_250.mem`, `sw_slow_control_104.mem`,
  `sw_slow_control_legacy_payload_104.mem`,
  `tb_command_slowcontrol_829_payload.mem`, and `topcfg_bits_baseline_real.txt`.
- Keep the proof layered: slow-control 829bit replay proves the configuration
  chain; `tb_maroc_stage2_acq_readout` proves ADC control/readout behavior;
  `tb_top_maroc_command_usb` proves packet replay, cfg gate, and USB upload
  integration.
- Default priority cases for the cfg-gate / TransmitOn timeout fix are
  `TOP_CFG_GATE_TRIGGER_DURING_CONFIG`,
  `CASE12_ADC_WAIT_TIMEOUT_MISSING_OBSERVED`,
  `CASE13_READOUT_TIMEOUT_MISSING_OBSERVED`,
  `CASE7_FULL_FRAME_64WORD_SIGNOFF`,
  `CASE8_REPEAT_ACQ_WITHOUT_RESET_SIGNOFF`, and
  `CASE_USB_FULL_FRAME_64WORD`.
- `CASE10_FALLING_SAME_CYCLE_NOT_SHIFT` is a known `data_socket_MAROC`
  falling-edge boundary diagnostic. Do not count it as a failure for the
  minimal configuration-gate / timeout fix unless that issue is explicitly in
  scope.
- XSim wave review should group and color signals by role: host/packet,
  config gate, trigger, ADC control, timeout/error, upload/data. Use
  `maroc_adc_xsim_cfg_gate_groups` for TOP cfg-gate inspection and
  `maroc_adc_xsim_timeout_groups` for stage2 timeout inspection.

## Documentation And PPT

When updating notes or PPT:
- Preserve evidence paths and dates.
- Separate “problem phenomenon”, “root cause”, “fix”, “verification”, and “remaining boundary”.
- Keep screenshot placeholders if the final ILA/experiment images are not available yet.
- Update generated PPT source (`.js`) and companion index (`.md`) together.
- Prefer new versioned PPT outputs over overwriting old stage-summary files.
