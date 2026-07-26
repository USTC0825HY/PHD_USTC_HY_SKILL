# CY Driver Module-Level XSim Notes

## Scope

Use this reference when the task is specifically about:

- `sources_maroc/CY_driver_new.v`
- `sources_maroc/tb/tb_cy_driver_new_xsim.v`
- module-level FX2LP Slave FIFO teaching TB
- `tb_cy_driver_new_xsim` handbook/report writing

## Preferred Entry

Use direct CLI:

```powershell
cd F:\01_MOUN\01_logic\02_MAROC\SPIROC_REF\01_MAROC_USB
xvlog sources_maroc/CY_driver_new.v sources_maroc/tb/tb_cy_driver_new_xsim.v
xelab -debug typical tb_cy_driver_new_xsim -s tb_cy_driver_new_xsim
xsim tb_cy_driver_new_xsim
```

Then in XSim console:

```tcl
source sources_maroc/tools/tb_cy_driver_new_xsim_wave_runall.tcl
```

For batch:

```powershell
xsim tb_cy_driver_new_xsim -tclbatch sources_maroc/tools/tb_cy_driver_new_xsim_wave_runall.tcl
```

## Interface Semantics To State Explicitly

Always write these early in the report or handbook:

- `00 -> EP2_IN -> 写 -> FPGA/DUT 驱动 FD[15:0]`
- `11 -> EP8_OUT -> 读 -> FX2 教学模型驱动 FD[15:0]`

Also state:

- `FLAGC=1` means readable command exists
- `FLAGB=1` means write space exists
- `PKTEND` means short packet commit, not another data write

## Wave Read Order

Recommended first-pass order:

1. `CASE1_SINGLE_READ_CMD`
2. `CASE3_SINGLE_WRITE_WORD`
3. `CASE4_SHORT_PACKET_PKTEND`
4. `CASE6_READ_PRIORITY_OVER_WRITE`
5. `CASE7_BUS_DIRECTION_CHECK`

## Case Windows

- `CASE0_RESET_IDLE` : `0 us ~ 0.5 us`
- `CASE1_SINGLE_READ_CMD` : `0.5 us ~ 0.875 us`
- `CASE2_TWO_READ_CMDS` : `0.875 us ~ 1.325 us`
- `CASE3_SINGLE_WRITE_WORD` : `1.325 us ~ 1.625 us`
- `CASE4_SHORT_PACKET_PKTEND` : `1.625 us ~ 1.975 us`
- `CASE5_NO_WRITE_WHEN_FLAGB_BLOCKED` : `1.975 us ~ 2.525 us`
- `CASE6_READ_PRIORITY_OVER_WRITE` : `2.525 us ~ 2.9 us`
- `CASE7_BUS_DIRECTION_CHECK` : `2.9 us ~ 3.425 us`

## What Each Case Must Explain

### `CASE0_RESET_IDLE`

- `state=IDLE`
- `FIFOADR=11`
- all control lines idle
- no cmd pulse, no write pulse

### `CASE1_SINGLE_READ_CMD`

- `FLAGC` rises after queue push
- `state: 0 -> 1 -> 2 -> 0`
- `SLOE=0 / SLRD=0` in `ST_R1`
- FX2 drives `AA20`
- `usb_cmd_wr_en` pulses once

### `CASE2_TWO_READ_CMDS`

- two separate `0 -> 1 -> 2 -> 0` loops
- not burst read

### `CASE3_SINGLE_WRITE_WORD`

- `state: 0 -> 3 -> 4 -> 5 -> 0`
- `W1` takes data
- `W2` writes `1357`
- `W3` asserts `PKTEND`

### `CASE4_SHORT_PACKET_PKTEND`

- `0 -> 3 -> 4 -> 3 -> 4 -> 5 -> 0`
- two `SLWR` pulses
- one `PKTEND` after the last `SLWR`

### `CASE5_NO_WRITE_WHEN_FLAGB_BLOCKED`

- `FLAGB=0` blocked window must stay quiet
- `state` remains `IDLE`
- after `FLAGB` release, normal `0 -> 3 -> 4 -> 5 -> 0`

### `CASE6_READ_PRIORITY_OVER_WRITE`

- read and write become ready together
- command read must finish first
- write starts only after read returns to `IDLE`

### `CASE7_BUS_DIRECTION_CHECK`

Split into three sub-windows:

1. read window: FX2 drives bus
2. write window: DUT drives bus
3. high-Z demo: DUT releases bus, FX2 does not drive, so `FD[15:0]=ZZZZ`

## Writing Style For Screenshot Explanations

For each screenshot, prefer this order:

1. identify the case
2. identify whether this is read, write, or high-Z
3. explain state transitions
4. explain which edge means “actual read/write”
5. explain who drives `FD[15:0]`
6. explain what is easy to misread

Preferred sentence patterns:

- “看到数据值不等于已经写入，要以 `SLWR` 低脉冲为准”
- “`SLOE=0` 表示 DUT 释放总线，不表示总线上一定有有效数据”
- “`PKTEND` 是包结束提交，不是第三次写”
