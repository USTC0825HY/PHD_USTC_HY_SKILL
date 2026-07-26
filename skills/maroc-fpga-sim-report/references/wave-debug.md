# 波形分组与调试说明

## `sim_parser` 推荐分组

优先使用：
- `sources_maroc/tools/tb_maroc_usb_packet_parser_xsim_wave_manual_groups.tcl`

分组顺序：
1. `TB_IO`
2. `PARSER_CTL`
3. `PARSER_HEADER`
4. `PARSER_RAW`
5. `DRAIN_TO_SC`
6. `SLOWCONTROL_CTL`
7. `SERIAL_SHIFT`

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

## `sim_parser` 推荐观察顺序

### 正例

1. `i_rx_word_valid / i_rx_word`
2. `o_packet_valid / o_packet_error`
3. `parser_0.r_state / r_packet_byte_count`
4. `header decode / r_raw_sc_bytes`
5. `o_sc_byte_valid / o_sc_byte_data / r_drain_byte_index`
6. `o_sc_start`
7. `o_sc_busy / o_sc_done`
8. `o_sc_clk / o_sc_dout / r_bit_cnt`

### 反例

1. `i_rx_word_valid / i_rx_word`
2. `o_packet_error / o_packet_error_code`
3. `o_packet_valid == 0`
4. `o_sc_byte_valid == 0`
5. `o_sc_start == 0`
6. `o_sc_done == 0`
7. serial capture == 0

## `sim_parser` 常见误读

### `o_sc_byte_valid`

不要默认写成“104 个独立脉冲”。

优先写法：
- “覆盖 104 个 byte 的连续有效窗口”
- “valid 在 104 个有效 byte 周期内保持有效”

正确判据：
1. `o_sc_byte_valid` 覆盖 drain window
2. `o_sc_byte_data` 每个 byte 周期更新
3. `r_drain_byte_index` 从 `0` 走到 `103`

### `r_drain_byte_index`

不要直接理解成“当前总线上正在发送的 byte 编号”。

在当前 RTL 中，它更接近：
- next index
- already-issued count

因此在 `o_sc_byte_valid=1` 时，当前 `o_sc_byte_data` 往往更接近：
- `r_drain_byte_index - 1`

## `cy-driver` 推荐分组

优先使用：
- `sources_maroc/tools/tb_cy_driver_new_xsim_wave_runall.tcl`

分组顺序：
1. `GROUP_BASELINE`
2. `GROUP_READ_CHAIN`
3. `GROUP_WRITE_CHAIN`
4. `GROUP_ARBITRATION`
5. `GROUP_BUS_DIRECTION`
6. `GROUP_CASE_MARKERS`

## `cy-driver` 常见误读

### `cy_data`

不要脱离以下信号单独解释：
- `cy_sloe`
- `cy_slrd`
- `cy_slwr`
- `tb_fx2_drive_en`

### `PKTEND`

优先写成：
- 短包提交
- 包结束提交

不要写成：
- 第三次写
- 额外数据拍

### `FIFOADR`

讲解时不要停在原始数值，优先写：
- `00 -> EP2_IN -> 写 -> FPGA/DUT 驱动 FD[15:0]`
- `11 -> EP8_OUT -> 读 -> FX2 教学模型驱动 FD[15:0]`

## `xsim` 常用控制台顺序

```tcl
source F:/01_MOUN/01_logic/02_MAROC/SPIROC_REF/01_MAROC_USB/sources_maroc/tools/tb_maroc_usb_packet_parser_xsim_wave_manual_groups.tcl
restart
run 1 us
run 5 us
run all
```

写手册或指导时，优先给绝对路径 `source`。
