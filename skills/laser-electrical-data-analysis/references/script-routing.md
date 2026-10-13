# MATLAB 入口路由

当前权威库见workspace-map；先读实际入口、器件README和审计台账。目录或版本记录不能替代采样率、码制、增益、参考面及限值证据。

| 任务 | 入口 |
|---|---|
| AD2208/AD9245 SFDR、带宽、隔离度、输入刻度、INL/DNL | 2208_hy / 9245_hy 内对应 adc_*_analysis.m |
| AD2208 ILA/PICO噪声 | 2208_hy/adc_ila_noise_analysis.m 与 adc_pico_noise_1hz_analysis.m，均四参数 |
| AD9245 PICO噪声 | 9245_hy/adc_input_noise_analysis.m：dataFolder, outputFolder, runOptions；文件及接口在选项内 |
| AD677 ILA/PICO噪声 | 677_hy/adc_ila_noise_analysis.m 与 adc_pico_noise_1hz_analysis.m，均四参数 |
| AD677 输入刻度、带宽、输入噪声 | 677_hy 当前入口，板卡/接口校准显式指定 |
| AD128 带宽 | 128_hy 当前入口 |
| DA9726/DA766 刻度、噪声、隔离度、输出范围 | 9726_hy / 766_hy 当前 dac_* 入口 |
| 多通道Pico切分 | 9726_hy/split_dac_isolation_channels.m，CH位置/显式channelMapping |
| DAC隔离度内核 | _shared/+converter/+dac/runIsolation.m、fitTone.m；IO为+io/loadPicoMat.m |

每次从实际README确认参数顺序，尤其766hex频率数值参数、2208 INL多参数和不同PICO入口差别。不固定入口数量。legacy、旧laser_analysis/01_workflows及发布ZIP不作新分析首选。

执行前记录输入哈希、采样率/时长、通道/列、码制、频带、校准来源/参考面、全部增益与输出目录。数据不足、通道歧义或参数不明时保留待确认，不猜值。
复用适用且已验证的算法；本技能维护不授权修改MATLAB源码。涉及方法修改时遵循MATLAB项目AGENTS的公式、文档、测试和台账同步要求。

2026-10-13项目有26个正式入口，完整清单见库内docs/20261013_structure_governance/STRUCTURE.md；运行时仍核对磁盘。DA9726的dac_output_voltage_analysis.m为直流台阶分析，保留CSV/PNG/MAT布局。677审计/批处理/FFT、切分工具及Phase_delay单独分类。

需要内置刻度的五个ADC噪声入口使用boardType和calibrationState；无电压刻度换算的指标不增加板型弹窗。PICO选择同板ADC和DA9726 JG18；详见calibration-workflow。
