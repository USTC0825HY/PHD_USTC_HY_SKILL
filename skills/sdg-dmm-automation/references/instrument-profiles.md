# 仪器档案与SCPI基线

## SIGLENT SDG6052X / SDG6032X-E

当前驱动支持两者DC与正弦配置；身份保存实际型号、driver_profile、固件、序列号和资源。正弦Vpp使用AMP、Vrms使用AMPVRMS、dBm使用AMPDBM，同字段设置和回读；dBm仅50Ω，其他可50Ω/High-Z。非零偏置须校验回读、幅度及允许端口范围。half_vpp为Vpp/2名义偏置，不能代替示波器确认。

用途：将16位无符号码值映射为直流电压，模拟DAC输出或提供受控直流源。

历史SDG6052X实机参考固件：`6.01.01.37R6`；不得把此记录推广为SDG6032X-E或其他固件的实测证明。每台设备以其IDN及对应测试记录为准。不要按序列号匹配型号；序列号只用于证据记录。

通道前缀：`C1`或`C2`。

配置DC、高阻显示和输出：

```text
*IDN?
C1:OUTP OFF
C1:OUTP LOAD,HZ
C1:BSWV WVTP,DC,OFST,0
*OPC?
C1:OUTP ON
*OPC?
C1:BSWV?
C1:OUTP?
SYST:ERR?
```

改变直流值：

```text
C1:BSWV OFST,<voltage>
*OPC?
C1:BSWV?
C1:OUTP?
SYST:ERR?
```

安全退出：

```text
C1:BSWV OFST,0
*OPC?
C1:BSWV?
C1:OUTP OFF
*OPC?
C1:OUTP?
SYST:ERR?
```

要求：限制电压范围；验证DC、High-Z、输出状态和Offset回读；任何异常都尝试执行“0 V→关闭输出”。

## SIGLENT SDM4065A

用途：6½位直流电压测量，当前配置只用于硬件联调，不自动授予DAC指标资格。

当前实机参考：序列号`SDM46A0X9S0186`、固件`0.0.0.18`。不要把这些身份值写成设备选择条件。

固定配置：

```text
*IDN?
*CLS
CONF:VOLT:DC 20
VOLT:DC:RANG 20
VOLT:DC:NPLC 1
VOLT:DC:IMP 10M
SENS:VOLT:DC:ZERO:AUTO ON
TRIG:DEL 0
TRIG:SOUR BUS
TRIG:COUN 1
SAMP:COUN 1
*OPC?
```

固件`0.0.0.18`使用`SENS:VOLT:DC:ZERO:AUTO ON`；较新固件可能使用：

```text
VOLT:DC:AZ ON
```

应根据`*IDN?`固件版本和实际命令回读选择兼容形式，禁止无验证地静默切换。

配置后回读：

```text
VOLT:DC:RANG?
VOLT:DC:NPLC?
VOLT:DC:IMP?
SENS:VOLT:DC:ZERO:AUTO?
TRIG:DEL?
TRIG:SOUR?
TRIG:COUN?
SAMP:COUN?
SYST:ERR?
```

单点测量：

```text
INIT
*TRG
FETC?
```

`INIT`准备测量，`*TRG`触发一次BUS测量，`FETC?`读取结果。每点触发次数和样本数均为1。测量期间保持源电压不变。

## Keysight 34470A

用途：高精度直流测量；当前参考实现保留指标测试资格字段，但正式资格必须由具体项目的校准和不确定度要求确认。

固定配置：

```text
*IDN?
*CLS
CONF:VOLT:DC 10
SENS:VOLT:DC:NPLC 1
SENS:VOLT:DC:IMP:AUTO OFF
SENS:VOLT:DC:ZERO:AUTO OFF
TRIG:SOUR BUS
TRIG:COUN 1
SAMP:COUN 1
*OPC?
```

单点测量同样使用：

```text
INIT
*TRG
FETC?
```

周期自动调零时，由运行器按配置周期显式发送：

```text
SENS:VOLT:DC:ZERO:AUTO ONCE
*OPC?
```
