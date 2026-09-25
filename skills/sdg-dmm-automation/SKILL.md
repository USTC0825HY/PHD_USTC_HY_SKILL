---
name: sdg-dmm-automation
description: Develop, test and diagnose PyVISA/SCPI automation for SIGLENT SDG6052X and SDG6032X-E, SIGLENT SDM4065A and Keysight 34470A. Use for DC/sine sweeps, DAC simulation, Vpp/Vrms/dBm readback, load/offset safety, BUS-triggered measurement, VISA discovery and evidence-preserving shutdown.
---

# SDG与高精度万用表自动化

## 工作边界

- 默认只做代码分析、Fake VISA测试、协议检查和离线验证。
- 按用户已明确授权的设备、通道、范围和操作执行，不机械重复确认；超出范围时再确认。开发默认Fake VISA。
- 设备发现、`*IDN?`、配置回读和错误队列查询属于低风险实机检查；SDG输出使能、改电压、连续扫描和改变负载仍需用户明确要求。
- 不把SDG6052X当作2 mV级直流标准源；使用它模拟DAC时，结果属于硬件联调数据，不能直接形成DAC指标结论。
- 始终区分仪器规格、驱动测试、实机验证和被测件指标判定。

## 工作流

1. 清点目标工程、Python解释器、项目锁定的PyVISA版本、VISA后端、配置文件和已有驱动；1.14.0是既有参考环境，不要求无关项目降级。
2. 判断任务是驱动复用、新仪器适配、逐点扫描、连接诊断还是结果证据整理。
3. 读取相关引用：
   - 仪器命令或型号差异：`references/instrument-profiles.md`。
   - 接口实现或代码评审：`references/driver-contracts.md`。
   - 逐点测量和断点恢复：`references/scan-state-machine.md`。
   - 新设备接入：`references/extension-guide.md`。
   - 实机操作和证据：`references/evidence-and-safety.md`。
4. 先用Fake VISA覆盖成功路径、回读不一致、超时、错误队列和异常安全关闭。
5. 实机检查按“资源发现→`*IDN?`→配置→配置回读→`SYST:ERR?`→少量读数”的顺序执行。
6. 实际扫描必须保持“源电压稳定后再测量；测量读取并完成事务提交后再改变源电压”的顺序。
7. 完成、取消和异常路径都执行源安全状态；保存设备身份、配置快照、命令错误和原始数据哈希。

## 统一测量模型

电压源适配器至少提供：

`connect`、`identify`、`configure_dc`、`apply_voltage`、`output_off`、`set_safe_output`、`query_error`、`close`。

电压测量设备适配器至少提供：

`connect`、`identify`、`configure`、`measure_voltage`、`autozero_once`、`query_error`、`raise_for_error_queue`、`close`。

逐点流程固定为：

```text
设置信号源电压
→ 等待信号源完成并回读
→ 等待规定稳定时间
→ INIT
→ *TRG
→ FETC?
→ 检查读数和错误队列
→ SQLite/CSV事务提交
→ 进入下一个点
```

禁止在万用表积分期间修改信号源电压；禁止因维持目标更新频率而跳过点或覆盖未提交数据。

## 代码与证据要求

- VISA自动发现必须用`*IDN?`匹配目标型号；没有匹配设备或匹配多台时停止，不默认选择第一台。
- 设备连接、命令、回读、错误和退出都要产生可定位的日志或事件。
- 读取值必须拒绝非有限值、无法解析值和仪器过量程标志（例如`9.9E37`）。
- 每个测试任务记录型号、序列号、固件、VISA资源、量程、NPLC、输入阻抗、触发设置、源通道、映射范围和软件版本。
- 断点恢复以“已提交点”为边界：已提交点不重复测量，未提交点重新设置源电压并重新测量。
- CSV、SQLite和manifest分别保存；原始数据只追加、不覆盖；使用SHA-256追溯文件完整性。

## 可执行资源

运行前先查看脚本帮助：

```powershell
python .\scripts\check_python_visa.py
python .\scripts\list_visa_resources.py
python .\scripts\validate_driver_contract.py <driver.py>
```

这些脚本默认只读取本机Python/VISA环境或静态检查源码，不会设置SDG电压、开启输出或触发万用表测量。

## 当前参考实现

优先复用当前工程的参考实现：

`F:\01_Laser\code\fpga\host\linearity_automation\host`（迁移后以项目AGENTS/MEMORY为准）

SDG双型号使用通用工厂，按IDN型号字段精确匹配，不按VID/PID或序列号猜测。正弦回读Vpp/AMP、Vrms/AMPVRMS、dBm/AMPDBM分开；dBm仅50Ω，Vpp/Vrms允许High-Z。half_vpp仅用于符合当前实现约束的Vpp，OFST=Vpp/2是名义0～Vpp，不是实测证明。启动默认C1不覆盖主动导入YAML的C2。

统一服务/GUI问题转项目主技能；本技能继续负责独立DMM自动化，不要求所有DMM工作使用Vivado。

型号覆盖来自当前驱动/配置和测试源码，不代表两个型号及全部固件均实机验收。查对应版本回归记录与仪器身份记录。修改参考实现后先运行相关离线测试，再更新兼容说明；实机操作仍按当前任务授权。
