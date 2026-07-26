# MAROC ILA Workflow

## Use This Reference When

Read this before helping with MAROC Vivado ILA captures, waveform grouping, color layout, trigger presets, screenshot planning, or hardware-manager Tcl automation.

The goal is layered evidence for this chain:

`Host 250B packet`
-> `CY_driver_new`
-> `usb_cmd_fifo`
-> `w_cmd_word_valid + w_cmd_word`
-> `maroc_usb_packet_parser`
-> `w_parser_sc_*`
-> TOP mux
-> `SlowControl_MAROC`
-> `RSTn_SC / CK_SC / D_SC`.

Keep the conclusion bounded: ILA can prove the configuration-chain main line is very likely open; it does not prove ADC/readout/upload or chip field behavior unless a separate A/B field test exists.

## ILA Cores And Scope

- `hw_ila_1` / `u_ila_0`: config-chain ILA in the system clock domain. Use this for FIFO read side, parser, TOP mux, SlowControl, and SC pins.
- `hw_ila_2` / `u_ila_1`: raw USB ingress ILA in the USB IFCLK domain. Use this for FX2/CY raw word ingress.
- Do not mix the two cores when making a screenshot claim. One screenshot should prove one layer clearly.
- Never load config-chain groups (`01_USB_CMD_FIFO_CDC` through `06_SC_PINS_MAIN_EVIDENCE`, plus `90_UPLOAD_SIDE_REFERENCE_ONLY`) into `hw_ila_2/u_ila_1`.
- Because Vivado Hardware Manager `add_wave` is waveform-context-sensitive, raw USB capture should be displayed without dynamic `add_wave`; use the raw WCFG/default display on uploaded `hw_ila_2` data.
- At 40MHz and depth 16384, the config-chain ILA covers about 409.6us. The 829bit slow-control shift is about 414.5us plus reset/load overhead, so a single capture usually cannot contain the whole packet head and SC tail. Use head and tail captures.
- Before judging a waveform, confirm the programmed `.bit`, `.ltx`, and ILA probe names match the current RTL. If they do not match, stop and classify the mismatch as stale bit, stale ltx, RTL changed without rebuild, or Tcl/probe path drift.

## Trigger / Upload Focus ILA

Use this section when debugging Ctest-to-ADC readout, not the slow-control packet path.

- Keep trigger and upload write-side ILA separate from USB and slow-control ILA when resources allow.
- Trigger-chain evidence should show `OR -> edge detect -> w_start_acq -> auto_mode -> Hold/ADC start`.
- Upload-chain evidence should show `TransmitOn/Out_ADC -> data_socket shift/decode -> FIFO write`.
- A clean `OR` capture proves the chip/FPGA trigger boundary only. It does not prove ADC conversion or USB upload.
- A clean `TransmitOn` plus `Out_ADC` capture proves the MAROC ADC output window exists. It does not prove host receive.
- `FA5A + 64 payload + FEEE` proves the FPGA write side formed one ADC frame. It does not prove Ctest charge response unless the configuration has exactly the intended `Ctest_chN` A/B condition.
- `o_ctest` should be treated as a debug SMA/Hold-active marker in current builds, not as the chip Ctest signal.
- Slow/fast shaper waveforms are analog evidence from `OUT_Q/OUT_FS` board outputs. ILA can prove read-register pins and control timing, but it cannot directly show the shaper waveform.

## TransmitOn Closed-Loop Debug

Use this structure when the goal is to determine why `TransmitOn`, `Out_ADC`, or upload frames do not appear.

Keep three chains separate:

1. Config chain: Host -> USB -> `CY_driver_new` -> `usb_cmd_fifo` -> parser -> `SlowControl_MAROC` -> SC pins.
2. Control chain: START latch -> cfg-done gate -> `auto_mode_MAROC` -> OR -> Hold/RST_ADC/start_ADC -> `TransmitOn`.
3. Upload chain: `TransmitOn + Out_ADC` -> `data_socket_MAROC` -> `FA5A/payload/FEEE` -> FIFO/USB/host.

Each board-debug round should record:

- Hypothesis: the suspected layer, for example host/USB, packet, SlowControl, START gate, auto-mode, ADC timing, data_socket, board connection, or signal source.
- Operation: exact host commands, ILA arm preset, trigger/signal-source setting, and bit/ltx used.
- Evidence: CSV/screenshot/log paths, key sample indices, state values, counters, and timeout flags.
- Judgment: classify the failure with the decision table below.
- Next step: inspect RTL, adjust host packet, rebuild bit/ltx, change Tcl/probe, adjust signal source, or declare a hardware blocker.

Decision table:

| Evidence | First layer to inspect |
|---|---|
| No USB command words | Host/FX2/USB endpoint |
| Parser error | Packet tag/header/footer or 104B payload |
| No `w_sc_done` | SlowControl or SC pins |
| No `w_auto_start_acq` after config | START latch or cfg gate |
| `auto_mode` remains idle/waiting | Trigger/OR source or state machine |
| Hold/RST/start missing after OR | RTL auto-mode/control timing |
| Hold/RST/start present, no `TransmitOn` | ADC config, ADC timing, trigger validity, board or signal source |
| `TransmitOn` present, `Out_ADC` static | ADC output enable, width, bit order, sampling edge |
| `Out_ADC` present, no `FA5A/FEEE` | `data_socket_MAROC` |
| FIFO frame present, host has no frame | `CY_driver_new`, USB FIFO, or host read path |
| Host frame present but parsed incorrectly | Host payload bit order or frame parser |

Do not treat a Ctest/no-OR result as a pure RTL result until the official waveform, `Ctest_ch=0/1` A/B, threshold DAC, and board Ctest path have been checked.

### Focused Hardware Manager Helpers

For board-level cfg-gate and timeout retest, source the focused trigger/upload helper after programming the board and opening Hardware Manager:

```tcl
source {F:/01_MOUN/01_logic/02_MAROC/SPIROC_REF/01_MAROC_USB/sources_maroc/tools/maroc_trig_upload_wave_groups.tcl}
maroc_trig_wave_help
```

Use these helpers on the actual Hardware Manager ILAs. They are not XSim commands and they do not prove host receive or chip analog response by themselves.

| Helper | ILA role | Recommended scene | What it proves |
|---|---|---|---|
| `maroc_trig_arm_cfg_start` | trigger/auto-mode | Send a config packet while START is already latched, or reproduce the former "trigger during config" case | Captures the beginning of slow-control activity so `w_auto_start_acq` and ADC outputs can be checked while cfg gate is closed |
| `maroc_trig_arm_cfg_done` | trigger/auto-mode | Confirm acquisition is re-enabled only after the slow-control frame completes | Captures `w_sc_done`; use it to show `dbg_cfg_done_latched=1`, `w_auto_start_acq=1`, and no earlier ADC start in the same capture |
| `maroc_trig_arm_timeout` | trigger/auto-mode | Check whether `auto_mode` hit ADC wait or readout timeout | Captures either timeout sticky flag in the trigger ILA, with auto-mode state and control outputs nearby |
| `maroc_upload_arm_start_adc` | upload/data-socket | Preferred anchor for the "no TransmitOn" failure mode | Captures upload-side context around the active-low `o_start_adc` pulse even when `w_upload_transmit_on` never rises |
| `maroc_upload_arm_timeout` | upload/data-socket | Check timeout sticky with upload/data-socket signals visible | Captures timeout sticky alongside `w_upload_transmit_on`, `w_upload_adc_bit`, data-socket state, counters, and FIFO writes |

Basic capture pattern:

```tcl
source {F:/01_MOUN/01_logic/02_MAROC/SPIROC_REF/01_MAROC_USB/sources_maroc/tools/maroc_trig_upload_wave_groups.tcl}
maroc_trig_connect
maroc_trig_arm_cfg_start
# send one host config packet or perform the planned board action
maroc_focus_collect_grouped
```

For a missing-`TransmitOn` upload check:

```tcl
source {F:/01_MOUN/01_logic/02_MAROC/SPIROC_REF/01_MAROC_USB/sources_maroc/tools/maroc_trig_upload_wave_groups.tcl}
maroc_trig_connect
maroc_upload_arm_start_adc
# trigger one ADC attempt after configuration is complete
maroc_focus_collect_grouped
```

Export CSV evidence after capture with the CSV helper:

```tcl
source {F:/01_MOUN/01_logic/02_MAROC/SPIROC_REF/01_MAROC_USB/sources_maroc/tools/maroc_ila_csv_export.tcl}
maroc_ila_export_trigger
maroc_ila_export_upload
```

Evidence boundaries:
- `maroc_trig_arm_cfg_start` and `maroc_trig_arm_cfg_done` prove cfg-gate timing only when the capture shows `w_start_acq`, `dbg_cfg_done_latched`, `w_auto_start_acq`, `w_sc_start/w_sc_done`, and ADC control outputs together.
- `maroc_upload_arm_start_adc` is the right anchor when there is no `TransmitOn`; absence of `w_upload_transmit_on` after `o_start_adc` is board evidence for "no ADC output window", not proof of the root cause.
- Timeout helpers prove the sticky flag was set in FPGA control logic. They do not prove `data_socket_MAROC` has recovered from a physically stuck-high `TransmitOn`, and they do not prove MAROC3A analog/Ctest behavior.

## Waveform Groups

Use these groups for `u_ila_0` config-chain screenshots:

| Group | Purpose | Signals |
|---|---|---|
| `01_USB_CMD_FIFO_CDC` | System-domain command stream after CDC | `dbg_usb_cmd_fifo_rd_en`, `dbg_usb_cmd_fifo_valid`, `dbg_usb_cmd_fifo_empty`, `dbg_usb_cmd_fifo_dout` |
| `02_PARSER_PACKET_250B` | Packet validation and parser state | `dbg_parser_state`, `dbg_parser_packet_byte_count`, `dbg_parser_collect_gap_cnt`, `w_parser_packet_valid`, `w_parser_packet_error`, sticky error/code signals |
| `03_PARSER_104B_DRAIN` | Parser output into legacy slow-control format | `dbg_parser_drain_byte_index`, `w_parser_sc_data`, `w_parser_sc_valid`, `w_parser_sc_start`, `dbg_parser_sc_valid_cnt`, start-pending/wait-busy debug |
| `04_TOP_MUX_SELECTED_PATH` | Parser-vs-legacy selection at TOP | `w_parser_legacy_block`, `w_cfg_data`, `w_cfg_valid`, `w_sc_start`, `dbg_selected_cfg_valid_cnt`, legacy command reference |
| `05_SLOWCONTROL_LOAD_AND_FSM` | SlowControl byte load and FSM | `dbg_sc_state`, `dbg_sc_load_byte_cnt`, `dbg_sc_bit_cnt`, `dbg_sc_clk_div_cnt`, `w_sc_busy`, `w_sc_done`, `dbg_seen_sc_done` |
| `06_SC_PINS_MAIN_EVIDENCE` | Final MAROC pins and acceptance counters | `w_sc_rstb`, `w_sc_clk`, `w_sc_dout`, `w_sc_busy`, `w_sc_done`, `dbg_sc_bit_cnt`, `dbg_ck_sc_rise_cnt` |
| `90_UPLOAD_SIDE_REFERENCE_ONLY` | Reference only, not config-chain proof | upload/data-socket debug signals |

Use these groups for `u_ila_1` raw USB screenshots:

| Group | Purpose | Signals |
|---|---|---|
| `01_USB_RAW_INGRESS` | FX2 raw command words | `rxf_sync_out`, `rx_cmd`, `w_usb_dbg_state`, `w_usb_dbg_next_state`, `o_cy_slrd`, `i_cy_flagc_empty` |
| `02_USB_BOUNDARY_CHECK` | Packet boundaries and debug counters | raw/header/footer related debug signals available in the build |

## Color Convention

Keep colors consistent across captures:

- Yellow/gold: important pulses and handshakes, for example `valid`, `start`, `done`.
- Cyan: primary data buses, for example `dbg_usb_cmd_fifo_dout`, `w_parser_sc_data`, `w_sc_dout`.
- Blue: parser or USB state machines.
- Red: error, sticky error, and error code signals.
- Green: selected TOP path and final SC pin path.
- Orange: SlowControl FSM and counters.
- White: acceptance counters such as 104B count and 829 CK edge count.
- Gray: reference-only or unrelated upload/readout signals.

## Trigger Presets

Use one preset per screenshot objective.

| Preset | Core | Trigger | Suggested Manual Position | Expected Evidence |
|---|---|---|---:|---|
| `raw_head` | `u_ila_1` | `rxf_sync_out == 1 && rx_cmd == 16'hFFE1` | about 512 | 125 16-bit words; packet starts `FFE1 FFD0 FE01 FFF0` and ends `0500 0800 EEEE` |
| `cfg_packet_head` | `u_ila_0` | `dbg_usb_cmd_fifo_valid == 1 && dbg_usb_cmd_fifo_dout == 16'hFFE1` | about 512 | FIFO read side emits the packet once, without repeated header consumption |
| `parser_drain` | `u_ila_0` | `w_parser_packet_valid == 1` | about 512 | parser completed packet validation, `packet_error == 0`, then enters 104B drain |
| `sc_head` | `u_ila_0` | `w_sc_start == 1` | about 512 | TOP selected parser path; SlowControl begins after 104B load |
| `sc_tail` | `u_ila_0` | `w_sc_done == 1` | about 15000 | SC shift completes; `busy` falls and `done` pulses |
| `sc_tail_cnt829` | `u_ila_0` | `dbg_ck_sc_rise_cnt == 10'h33D` | about 15000 | CK rising-edge counter reaches 829 |

Set `Trigger position in window` manually in the Vivado Settings pane before arming. The current helper preserves the manual value instead of forcing the suggested defaults.

In Basic trigger mode, clear unused probes to `X`, not an empty string. Empty trigger values can leave stale or invalid comparator state in Vivado hardware manager.

## Expected Stage Phenomena

### 1. USB Raw Ingress

Expected:
- Trigger on the first word `FFE1`.
- Observe 125 16-bit words for the 250B packet.
- See a valid head and tail. A typical tail is `0300 0500 0800 EEEE` or the design-specific footer sequence.

This proves the host and FX2/CY ingress delivered the packet to the FPGA front door.

### 2. FIFO Read Side And Parser Packet

Expected:
- `dbg_usb_cmd_fifo_valid` pulses one word at a time.
- `dbg_usb_cmd_fifo_dout` starts at `FFE1` and reaches the packet footer once.
- `dbg_parser_state` progresses through collect, ready, drain, and wait-done states.
- `w_parser_packet_valid` pulses once.
- `w_parser_packet_error` remains 0.

If raw ingress is correct but FIFO/parser shows a repeated header such as `FE01` being consumed twice, suspect CDC or valid/data semantics before blaming the host packet.

If `dbg_usb_cmd_fifo_dout` changes but `dbg_usb_cmd_fifo_valid` never pulses, inspect the RTL debug assignment before judging hardware behavior. A known bad pattern is `assign dbg_usb_cmd_fifo_valid = dbg_usb_cmd_fifo_valid;`; it must be connected to `w_usb_cmd_fifo_valid`, then the bitstream must be rebuilt and reprogrammed.

### 3. Parser 104B Drain And TOP Mux

Expected:
- `w_parser_sc_valid` pulses 104 times.
- `dbg_parser_drain_byte_index` covers `0..103`.
- `w_parser_sc_start` pulses once after drain.
- `w_parser_legacy_block` selects the parser path while the parser owns the packet.
- `w_cfg_valid` mirrors the selected parser drain; `dbg_selected_cfg_valid_cnt` reaches `0x68` / 104.

It is normal for `w_cfg_data` and `w_cfg_valid` to be idle while `w_sc_clk` and `w_sc_dout` are shifting later. They are load-side signals, not serial-output signals.

### 4. SlowControl Pins

Expected:
- `w_sc_rstb` produces the reset pulse required by the design.
- `w_sc_busy` stays high during shifting.
- `w_sc_clk` toggles at the expected divided clock rate.
- `w_sc_dout` carries serial data.
- `dbg_ck_sc_rise_cnt` reaches 829 (`10'h33D`).
- `w_sc_done` pulses once at completion.

This is the main board-level evidence that the FPGA emitted a complete MAROC slow-control frame.

## Tcl Operation Rules

Prefer the project helper:

```tcl
source {F:/01_MOUN/01_logic/02_MAROC/SPIROC_REF/01_MAROC_USB/sources_maroc/tools/maroc_cfg_ila_full_auto.tcl}
```

Important behavior:
- `source` only loads Tcl procedures. It should print tool availability but does not arm, capture, upload, or add waves by itself.
- Use `maroc_cfg_arm <preset>` to set trigger and start ILA capture.
- Send exactly one host configuration packet after arming.
- Use `maroc_raw_collect` only after `raw_head`; it waits, uploads, and displays `hw_ila_2/u_ila_1` data without dynamic `add_wave`.
- Use `maroc_cfg_collect` only after config-chain presets; it waits, uploads, and displays `hw_ila_1/u_ila_0` data with the cfg-chain WCFG through `display_hw_ila_data -wcfg`.
- `maroc_ila_collect` routes by the last armed ILA, but explicit raw/cfg collect commands are clearer during board debug.

Recommended raw ingress flow:

```tcl
source {F:/01_MOUN/01_logic/02_MAROC/SPIROC_REF/01_MAROC_USB/sources_maroc/tools/maroc_cfg_ila_full_auto.tcl}
# set hw_ila_2 Trigger position in window manually first
set ila [maroc_cfg_arm raw_head]
# send one host 250B config packet from the PC application
maroc_raw_collect
```

Recommended config-chain flow:

```tcl
source {F:/01_MOUN/01_logic/02_MAROC/SPIROC_REF/01_MAROC_USB/sources_maroc/tools/maroc_cfg_ila_full_auto.tcl}
# set hw_ila_1 Trigger position in window manually first
set ila [maroc_cfg_arm parser_drain]
# send one host 250B config packet from the PC application
maroc_cfg_collect
```

Stage command map:

| Stage | Target | Arm | Collect |
|---|---|---|---|
| USB raw ingress | `hw_ila_2/u_ila_1` | `set ila [maroc_cfg_arm raw_head]` | `maroc_raw_collect` |
| FIFO packet head | `hw_ila_1/u_ila_0` | `set ila [maroc_cfg_arm cfg_packet_head]` | `maroc_cfg_collect` |
| Parser drain | `hw_ila_1/u_ila_0` | `set ila [maroc_cfg_arm parser_drain]` | `maroc_cfg_collect` |
| SC start | `hw_ila_1/u_ila_0` | `set ila [maroc_cfg_arm sc_head]` | `maroc_cfg_collect` |
| SC done | `hw_ila_1/u_ila_0` | `set ila [maroc_cfg_arm sc_tail]` | `maroc_cfg_collect` |
| CK count 829 | `hw_ila_1/u_ila_0` | `set ila [maroc_cfg_arm sc_tail_cnt829]` | `maroc_cfg_collect` |

Useful recovery flow for a captured backup:

```tcl
source {F:/01_MOUN/01_logic/02_MAROC/SPIROC_REF/01_MAROC_USB/sources_maroc/tools/maroc_cfg_ila_full_auto.tcl}
maroc_cfg_open_last_backup
```

Use `maroc_cfg_capture_now` only as a sanity check when the GUI is stable. It is not a formal configuration-chain capture because it triggers immediately and may miss the event of interest. If Vivado closes after capture-now or after a reset-style display command, avoid `display_hw_ila_data -reset` and use the backup/open-last flow.

## Wave Display Rules

Hardware-manager waveform Tcl is context-sensitive:
- Treat live `hw_ila_1/hw_ila_2` tabs as control/status views for arming triggers. Do not rely on them as the final grouped screenshot surface.
- For report screenshots, arm the ILA, send the packet, upload the captured data, then display the `hw_ila_data` object.
- For config-chain screenshots, prefer the project script path that displays `hw_ila_1` uploaded data with `F:/09_ppt/maroc_u_ila_0_cfg_chain_layout.wcfg`. This avoids depending on the active live wave tab.
- For raw USB screenshots, do not auto-add dynamic waves from the helper. Use `maroc_raw_collect` to display `hw_ila_2` capture data with the raw WCFG/default display; this avoids cfg-chain groups landing in the wrong context.
- If the WCFG path fails, script fallback may add uploaded signal names such as `dbg_usb_cmd_fifo_dout`, `w_cfg_valid`, `parser_0/r_start_pending`.
- Avoid suffixes such as `[15:0]` when the uploaded waveform database exposes only the base name.
- For CSV/XLSX export, export from the uploaded `hw_ila_data` object rather than a stale live tab when possible.
- After export, check that probe names match the current bitstream/LTX. If names drift, use probe index only as a last resort and document the mapping.
- Treat WCFG layouts as presentation helpers, not signal truth. If a WCFG binds to the wrong dataset or empty groups, re-add waves from the uploaded capture before judging the event.

Known name behavior:
- `parser_0/r_start_pending` works; `parser_0_r_start_pending` can fail.
- `command_0/o_cfg_data` works; `command_0_o_cfg_data` can fail.
- `w_parser_packet_error_code_sticky` works; `w_parser_packet_error_code_sticky[2:0]` can fail.

If WCFG loads group dividers but no signals, treat the WCFG as unbound to the active uploaded dataset. Rebuild the WCFG from a known-good displayed capture before trusting script-based `add_wave`.

## Common Symptoms

- Empty waveform after `source`: normal. The script was loaded but no capture/display command ran.
- `wait_on_hw_ila` dialog stays open: the ILA has not triggered. Recheck trigger preset and resend one packet after arming.
- Empty waveform after `maroc_cfg_collect` returns: the upload/display step did not bind the cfg-chain WCFG. Re-source the latest helper, then run `maroc_ila1_layout_force`; check the Tcl Console for `display_hw_ila_data -wcfg` warnings.
- Groups appear but contain no signals: WCFG or fallback `add_wave` names are not bound to the displayed ILA data.
- Groups appear but contain no signals in a live online tab: do not use that empty live tab as the report screenshot. Capture first, then display uploaded `hw_ila_data` with WCFG.
- `add_wave` says “Nothing was found”: wrong waveform context, wrong signal name, suffix mismatch, or a `hw_probe` object was passed instead of a waveform signal name.
- Raw stage loads or modifies config-chain groups: wrong command. Use `maroc_raw_collect` after `raw_head`; do not use `maroc_cfg_collect` for `hw_ila_2/u_ila_1`.
- `dbg_usb_cmd_fifo_valid` is flat even when FIFO data appears: check RTL for debug-net self-connection and rebuild/program after fixing.
- Trigger setup still shows stale probes: clear unused probe triggers to `X` and set `CONTROL.TRIGGER_CONDITION AND`.
- `w_cfg_data/w_cfg_valid` idle while `w_sc_clk/w_sc_dout` active: usually normal. The 104B load phase has already finished and SlowControl is serial shifting.
- Vivado GUI closes during scripted display: avoid aggressive reset/remove/rebuild commands; reopen the saved `.ila` backup and add waves conservatively.
- `TransmitOn` does not arrive after `ADC_START`: do not blame USB first. Check ADC slow-control bits, physical `Rstn_ADC/start_ADCb/Hold1/Hold2/CK_40M`, reset/start pulse width, and acquisition dead time.
- `dbg_auto_state` stuck at `ST_ADC_WAIT=6`: the FPGA is waiting for MAROC ADC readout. Add or inspect timeout/dead-time logic before expecting later triggers to be accepted.
- ADC payload appears with all `Ctest_chN=0`: this is baseline/pedestal, not Ctest charge measurement.
- `o_ctest` appears on FPGA SMA2: in current debug builds it is a Hold-active/debug marker, not the MAROC Ctest input.

## Report Language

Use screenshot captions that state exactly what the screenshot proves:

- Raw ingress proves the host packet reached FPGA USB ingress.
- FIFO/parser proves the 250B packet crossed CDC and passed parser format checks.
- Parser drain/TOP mux proves 104B config bytes selected the parser path.
- SC pins prove the FPGA emitted the 829bit slow-control frame.

Do not write that the chip register function is signed off unless a separate single-field A/B behavior verification is shown.
