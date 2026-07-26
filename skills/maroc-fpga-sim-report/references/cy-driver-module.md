# `CY_driver_new` 模块级说明

## 适用范围

当任务直接围绕：
- `sources_maroc/CY_driver_new.v`
- `sources_maroc/tb/tb_cy_driver_new_xsim.v`
- FX2LP Slave FIFO 模块级教学/仿真报告

## 推荐入口

优先使用 CLI：

```powershell
cd F:\01_MOUN\01_logic\02_MAROC\SPIROC_REF\01_MAROC_USB
xvlog sources_maroc/CY_driver_new.v sources_maroc/tb/tb_cy_driver_new_xsim.v
xelab -debug typical tb_cy_driver_new_xsim -s tb_cy_driver_new_xsim
xsim tb_cy_driver_new_xsim
```

进入 `xsim` 后：

```tcl
source sources_maroc/tools/tb_cy_driver_new_xsim_wave_runall.tcl
```

## 报告里必须早写的接口语义

- `00 -> EP2_IN -> 写 -> FPGA/DUT 驱动 FD[15:0]`
- `11 -> EP8_OUT -> 读 -> FX2 教学模型驱动 FD[15:0]`
- `FLAGC=1`：存在可读命令
- `FLAGB=1`：存在可写空间
- `PKTEND`：短包提交/包结束提交，不是另一拍数据写入

## 波形优先阅读顺序

1. `CASE1_SINGLE_READ_CMD`
2. `CASE3_SINGLE_WRITE_WORD`
3. `CASE4_SHORT_PACKET_PKTEND`
4. `CASE6_READ_PRIORITY_OVER_WRITE`
5. `CASE7_BUS_DIRECTION_CHECK`

## `CASE7_BUS_DIRECTION_CHECK` 的固定写法

必须拆成三段：
1. 读窗口：FX2 驱动总线
2. 写窗口：DUT 驱动总线
3. high-Z demo：DUT 释放总线，FX2 也不驱动，因此 `FD[15:0]=Z`

## 截图解释顺序

每张图优先按这个顺序写：
1. 当前 case
2. 当前是读/写/high-Z 哪一段
3. 状态迁移
4. 哪个边沿才算真实读/写
5. 谁在驱动 `FD[15:0]`
6. 最容易误读的点
