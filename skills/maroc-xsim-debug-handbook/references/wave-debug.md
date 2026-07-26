# Wave Debug

## `cy-driver` Handbook-Aligned Groups

For `tb_cy_driver_new_xsim`, the preferred grouping is:

1. `GROUP_BASELINE`
2. `GROUP_READ_CHAIN`
3. `GROUP_WRITE_CHAIN`
4. `GROUP_ARBITRATION`
5. `GROUP_BUS_DIRECTION`
6. `GROUP_CASE_MARKERS`

Preferred Tcl:

- `sources_maroc/tools/tb_cy_driver_new_xsim_wave_runall.tcl`

### `cy-driver` Color Guidance

Prefer strong contrast:

- baseline/control: gray
- read-chain / command intake: magenta / pink
- write-chain / bus output: cyan
- arbitration markers: white / violet
- bus-direction / ownership: orange + green

### `GROUP_BASELINE`

- `rstn`
- `dut.state`
- `cy_fifoaddr`
- `cy_sloe`
- `cy_slrd`
- `cy_slwr`
- `cy_pktend`

### `GROUP_READ_CHAIN`

- `cy_flagc`
- `tb_fx2_drive_en`
- `cy_data`
- `usb_cmd_wr_en`
- `usb_cmd_data`
- `cmd_log_count`
- `cmd_log[0]`
- `cmd_log[1]`

### `GROUP_WRITE_CHAIN`

- `cy_flagb`
- `usb_fifo_in_empty`
- `usb_fifo_in_valid`
- `usb_fifo_in_rd_en`
- `usb_fifo_in_data`
- `cy_data`
- `cy_slwr`
- `cy_pktend`
- `ep2_capture_cnt`
- `ep2_in_log[0]`
- `ep2_in_log[1]`

### `GROUP_ARBITRATION`

- `cy_flagc`
- `cy_flagb`
- `usb_fifo_in_empty`
- `usb_cmd_wr_en`
- `usb_fifo_in_rd_en`
- `cy_slwr`
- `first_cmd_event`
- `first_rd_en_event`
- `first_slwr_event`

### `GROUP_BUS_DIRECTION`

- `cy_sloe`
- `cy_slrd`
- `cy_slwr`
- `tb_fx2_drive_en`
- `tb_bus_owner`
- `cy_data`
- `read_bus_tb_cycle_cnt`
- `read_bus_z_cycle_cnt`
- `write_bus_dut_cycle_cnt`
- `bus_contention_cnt`

### `GROUP_CASE_MARKERS`

- `tb_case_id`
- `tb_phase`

## `cy-driver` Recommended Read Order

1. `CASE1_SINGLE_READ_CMD`
2. `CASE3_SINGLE_WRITE_WORD`
3. `CASE4_SHORT_PACKET_PKTEND`
4. `CASE6_READ_PRIORITY_OVER_WRITE`
5. `CASE7_BUS_DIRECTION_CHECK`

Recommended time windows:

- `CASE0_RESET_IDLE` : `0 us ~ 0.5 us`
- `CASE1_SINGLE_READ_CMD` : `0.5 us ~ 0.875 us`
- `CASE2_TWO_READ_CMDS` : `0.875 us ~ 1.325 us`
- `CASE3_SINGLE_WRITE_WORD` : `1.325 us ~ 1.625 us`
- `CASE4_SHORT_PACKET_PKTEND` : `1.625 us ~ 1.975 us`
- `CASE5_NO_WRITE_WHEN_FLAGB_BLOCKED` : `1.975 us ~ 2.525 us`
- `CASE6_READ_PRIORITY_OVER_WRITE` : `2.525 us ~ 2.9 us`
- `CASE7_BUS_DIRECTION_CHECK` : `2.9 us ~ 3.425 us`

## `cy-driver` Common Misreads

### `cy_data`

Do not explain `cy_data` alone.

Always interpret it with:

- `cy_sloe`
- `cy_slrd`
- `cy_slwr`
- `tb_fx2_drive_en`

Correct wording:

- read window: FX2 drives `FD[15:0]`
- write window: DUT drives `FD[15:0]`
- high-Z demo: DUT released bus and FX2 did not drive it

### `PKTEND`

Do not describe `PKTEND` as:

- a third write
- an extra data beat

Preferred wording:

- short packet commit
- packet boundary
- package end submit after the last `SLWR`

### `FIFOADR`

Do not stop at the raw value.

Preferred teaching wording:

- `00 -> EP2_IN -> write -> FPGA/DUT drives FD[15:0]`
- `11 -> EP8_OUT -> read -> FX2 model drives FD[15:0]`

### `SLOE=0`

Do not describe it as “there is definitely valid data on the bus”.

Preferred wording:

- DUT released the bus
- FX2 may drive it
- if FX2 does not drive it, `FD[15:0]` can be `Z`

## Handbook-Aligned Groups

For `sim_parser`, the preferred grouping is:

1. `TB_IO`
2. `PARSER_CTL`
3. `PARSER_HEADER`
4. `PARSER_RAW`
5. `DRAIN_TO_SC`
6. `SLOWCONTROL_CTL`
7. `SERIAL_SHIFT`

Preferred Tcl:

- `sources_maroc/tools/tb_maroc_usb_packet_parser_xsim_wave_manual_groups.tcl`

### `sim_parser` Color Guidance

Prefer stable semantic colors:

- TB IO / packet ingress: brown-red
- parser control: blue
- parser header fields: teal
- raw slow-control bytes: cyan-green
- drain/start/busy/done: yellow
- slow-control internal state: gold / orange-brown
- serial dout: bright green

Do not color parser control and slow-control internal state with adjacent pale blues; they become hard to separate in long traces.

## `top` Handbook-Aligned Groups

For `tb_top_maroc_command_usb`, the preferred grouping is:

1. `GROUP_BASELINE`
2. `GROUP_USB_PACKET_INJECTION`
3. `GROUP_PARSER_COLLECT_DECODE`
4. `GROUP_COMMAND_EXECUTE`
5. `GROUP_RAW_SC_AND_DRAIN`
6. `GROUP_SLOWCONTROL_INTERNAL`
7. `GROUP_SERIAL_SHIFT`
8. `GROUP_TOP_MUX_ARB`

Preferred Tcl:

- `sources_maroc/tools/tb_top_maroc_command_usb_xsim_wave_setup_only.tcl`
- `sources_maroc/tools/tb_top_maroc_command_usb_xsim_wave_runall.tcl`
- `sources_maroc/tools/tb_top_maroc_command_usb_xsim_wave_case_sw_packet.tcl`

### `top` High-Contrast Color Guidance

Recommended palette:

- `GROUP_BASELINE`: gray / white / red / yellow
- `GROUP_USB_PACKET_INJECTION`: magenta + cyan
- `GROUP_PARSER_COLLECT_DECODE`: blue + teal + red
- `GROUP_COMMAND_EXECUTE`: purple + green + red + gold
- `GROUP_RAW_SC_AND_DRAIN`: cyan-green + pale yellow
- `GROUP_SLOWCONTROL_INTERNAL`: orange + gold + brown
- `GROUP_SERIAL_SHIFT`: bright orange + bright green
- `GROUP_TOP_MUX_ARB`: magenta + violet + white + red

Recommended implementation details:

1. create true collapsible groups with `add_wave_group`
2. add member signals with `add_wave -into <group> -color <name|#RRGGBB>`
3. before reloading layout, run:

```tcl
catch {remove_wave [get_waves -regexp .*]}
```

4. prefer absolute-path `source` when the user is inside a Vivado-generated run directory

### `top` Group Label Limitation

Important xsim behavior:

- expanded child waves show colors
- collapsed group rows usually do **not** inherit child-wave colors

If the user wants foldable groups **and** clear visible section labels after collapse, use:

- one `add_wave_divider "01_BASELINE"` style label
- followed by one real collapsible `add_wave_group "01_BASELINE"`

This is the preferred workaround for xsim’s collapsed-group color limitation.

### `top` Recommended Absolute-Path Source

```tcl
source F:/01_MOUN/01_logic/02_MAROC/SPIROC_REF/01_MAROC_USB/MAROC_PRJ/MAROC_PRJ.sim/sim_1/behav/xsim/tb_top_maroc_command_usb_xsim_wave_setup_only.tcl
restart
run all
```

### `top` Recommended Read Order

1. `GROUP_BASELINE`
2. `GROUP_USB_PACKET_INJECTION`
3. `GROUP_COMMAND_EXECUTE`
4. `GROUP_PARSER_COLLECT_DECODE`
5. `GROUP_RAW_SC_AND_DRAIN`
6. `GROUP_SLOWCONTROL_INTERNAL`
7. `GROUP_SERIAL_SHIFT`
8. `GROUP_TOP_MUX_ARB`

### `top` Common Source Failure

If the user runs:

```tcl
source tb_top_maroc_command_usb_xsim_wave_setup_only.tcl
```

and gets “no such file or directory”, prefer this diagnosis:

1. the file was never copied into `sim_1/behav/xsim`, or
2. the current xsim working directory is not `sim_1/behav/xsim`

Preferred fix:

```tcl
source F:/01_MOUN/01_logic/02_MAROC/SPIROC_REF/01_MAROC_USB/MAROC_PRJ/MAROC_PRJ.sim/sim_1/behav/xsim/tb_top_maroc_command_usb_xsim_wave_setup_only.tcl
```

## `sim_parser` Key Signals

### `TB_IO`

- `i_clk`
- `i_rst_n`
- `i_rx_word_valid`
- `i_rx_word`
- `o_packet_valid`
- `o_packet_error`
- `o_packet_error_code`

### `PARSER_CTL`

- `parser_0.r_state`
- `parser_0.r_packet_byte_count`
- `parser_0.r_collect_gap_cnt`
- `parser_0.r_drain_byte_index`
- `parser_0.r_start_pending`
- `parser_0.r_wait_seen_busy`

### `PARSER_HEADER`

- `parser_0.o_total_boards`
- `parser_0.o_board_id`
- `parser_0.o_chip_count`
- `parser_0.o_slow_rate`
- `parser_0.o_probe_mode`
- `parser_0.o_module_id`

### `PARSER_RAW`

- `parser_0.r_raw_sc_bytes[0]`
- `parser_0.r_raw_sc_bytes[1]`
- `parser_0.r_raw_sc_bytes[2]`
- `parser_0.r_raw_sc_bytes[103]`

### `DRAIN_TO_SC`

- `o_sc_frame_done`
- `o_sc_byte_valid`
- `o_sc_byte_data`
- `o_sc_start`

### `SLOWCONTROL_CTL`

- `o_sc_busy`
- `o_sc_done`
- `o_sc_rstb`
- `slowcontrol_0.r_curr_state`
- `slowcontrol_0.r_next_state`
- `slowcontrol_0.r_load_byte_cnt`
- `slowcontrol_0.r_reset_cnt`

### `SERIAL_SHIFT`

- `o_sc_clk`
- `o_sc_dout`
- `slowcontrol_0.r_bit_cnt`
- `slowcontrol_0.r_shift_data`

## Recommended Read Order

### Positive Cases

1. `i_rx_word_valid / i_rx_word`
2. `o_packet_valid / o_packet_error`
3. `parser_0.r_state / r_packet_byte_count`
4. `r_raw_sc_bytes / header decode`
5. `o_sc_byte_valid / o_sc_byte_data / r_drain_byte_index`
6. `o_sc_start`
7. `o_sc_busy / o_sc_done`
8. `o_sc_clk / o_sc_dout / r_bit_cnt`

### Negative Cases

1. `i_rx_word_valid / i_rx_word`
2. `o_packet_error / o_packet_error_code`
3. `o_packet_valid == 0`
4. `o_sc_byte_valid == 0`
5. `o_sc_start == 0`
6. `o_sc_done == 0`
7. `captured_count == 0`

## Common Misreads

### `o_sc_byte_valid`

Do not describe it as “104 independent pulses” unless that is literally what the waveform shows.

Preferred wording:

- “a valid window covering 104 bytes”
- “valid stays asserted across 104 effective byte cycles”

Correctness criteria:

1. `o_sc_byte_valid` covers the drain window
2. `o_sc_byte_data` updates each byte cycle
3. `r_drain_byte_index` advances from `0` to `103`

### `r_drain_byte_index`

Do not assume it means “current byte index on the bus”.

In current RTL it behaves more like:

- the next index / already-issued count

When `o_sc_byte_valid=1`, the current data byte often corresponds to:

- `r_drain_byte_index - 1`

## XSim Console Shortcuts

Preferred:

```tcl
source F:/01_MOUN/01_logic/02_MAROC/SPIROC_REF/01_MAROC_USB/sources_maroc/tools/tb_maroc_usb_packet_parser_xsim_wave_manual_groups.tcl
restart
run 1 us
run 5 us
run all
```

Use absolute paths for `source`.
