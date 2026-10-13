# 513 数据目录规则：snapshot-v2 与 session-v1

先区分布局。物理目录与测量覆盖是不同证据；不能按空目录、run 时间、文件名推断测试已完成或板卡改焊状态。

## snapshot-v2：本次报告主库

根：I:\01_laser\202607-202609_513_data。
主库包含 513_CW_DATA_jianding 与 513_CW_jiaqiang。此库是截至 2026-09-19 的数据快照，2026-10-01 完成 v2 分类；该截止日期不是其他主库的默认值。现状与执行证据在根下 00_整理方案_20260930。

结构按器件/日期批次/指标/接口保留实际组织。AD9245 有批次层，例如加强件 20260915_ad9245；不强制塞入 SZSD/YCQD 板组层或重建会话目录。具体编号以器件 README、已执行映射和实际目录共同核对：

| 器件 | v2 指标 |
|---|---|
| AD2208 | 01_SFDR、02_FrequencyResponse、03_InputPowerScale、04_Isolation、05_INL_DNL、06_Noise、07_ClockSource、08_PhaseBandwidth |
| AD9245 | 批内 01_noise、02_FrequencyResponse、03_InputPowerScale、04_Isolation、05_INL_DNL、06_SFDR |
| DA766 | 01_UpdateRate、02_PhaseNoise、03_DCNoise、04_OutputVoltage、05_Isolation、06_scale |
| DA9726 | 01_Linearity、02_PhaseNoise、03_Noise、04_OutputVoltage、05_Isolation、06_scale |
| AD677 | 批内 01_noise、02_FrequencyResponse；其他项按现存 README 核验 |

ADC128→AD128、ad677→AD677 是该库器件目录标准化；报告器件称呼与原始文件名不据此批量替换。跨器件主题 PICO6000、RF_REF、GTH、遥测和时钟源按现状互链。

兼容项：results 就近留在采集数据旁，包括 raw 内 results；历史 result 单数目录只标注。已有 raw/instrument 正本位置用于逐条保留副本裁决，不是允许自动删除旁边文件的依据。_legacy_旧组织2208_勿删、_from_旧AD128_20260930 继续保留，其中是否尚有独有数据须重新核实。

## session-v1：现有新采集树

I:\CW_Data\鉴定件|加强件\SZSD|YCQD\器件\NN_指标\接口\YYYYMMDD_HHMM\
包含 raw、results 和 _session.md。闭集只对该布局生效，见 scripts/taxonomy.py，不套用到 snapshot-v2。

raw 保存采集原文件；analysis run 按 MATLAB resolveOutputBase 的实际结果位置记录。对 v2 历史组织不施加 v1 规范。新建骨架必须指定没有 snapshot/legacy 根的父目录；需要在混合父目录新增时由当前任务明确范围，勿绕过脚手架保护。

会话记录至少包含接口、采集时间、仪器与设置、板卡/固件身份、参考面、改焊状态及依据。鉴定件和加强件均可能改焊。gaihanqian/gaihanhou 作为历史显式线索保留；日期仅用于查找记录，不能把批次日期或分析 run 日期自动转成改焊状态。

## 审计解释

空脚手架不等于数据丢失。分别列覆盖矩阵、失败 run、空目录、结构问题、散件、大文件及无法访问项。覆盖矩阵中的“有文件”还需确认有效数据和要求；未发现指标目录并不能证明该项未测，可能存在跨主题路径。

大 MAT 等低频资产先原地索引；不按大小自动压缩、搬迁或删除。长路径和 SMB 错误必须进入扫描错误清单，扫描不完整时不得宣称文件数或字节数闭合。
