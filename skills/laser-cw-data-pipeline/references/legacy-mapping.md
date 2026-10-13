# 存量映射与移动纪律

读旧根、实际布局及对应 README 后生成 dry-run CSV。旧根本身不是删除授权，也不能凭同名判断旧 I:\CW_Data 与 v2 主库同构。

## 映射来源

v2 已执行逐目录映射位于主库 00_整理方案_20260930/逐目录映射表_v2.csv；列包括 库(JD/JQ)、现路径、目标路径、动作、原因。路径相对相应 campaign 根。辅助脚本接受此格式或 old/new/match CSV；只产生建议，不移动文件。

20261001 案例包含：KEDU/sin_scale→06_scale、DA766 NOISE→03_DCNoise、OUTPUT_AMP 归入04_OutputVoltage、AD2208 03_inputpower→03_InputPowerScale、04_INL→05_INL_DNL、Isolation→04_Isolation、06_phase_bandwidth→08_PhaseBandwidth，AD9245 加批次层、X2G INL raw归位、200290919→20260919、nosie→noise。
这些是器件/批次限定的历史映射，不是全树字符串替换表。原始 COADE_* 文件名保留并标注。

## 执行前与执行中

1. 写完整 dry-run 清单：源/目标、内容统计、冲突、原因、预计改变；有明确范围授权才执行。
2. 基线按同一长路径口径统计文件数/字节，关键源文件和保留副本记录 SHA-256。
3. 每条先持久化 move_journal 的 PENDING，再执行，再记录 OK/FAIL；禁止覆写已存在目标。
4. 续跑不能仅靠“源不存在”判断完成：核对目标、日志及基线；不一致则停止相关条目。
5. 同盘移动按成功日志逆序回退，回退前检查源位冲突和移动后修改；跨盘复制不是同盘 rename，要另设复制验证流程。
6. 完成后文件数/字节及必要哈希对账；扫描不可访问项为零才可报告完整验证。

数据整理始终零删除。去重清理另走 laser-electrical-data-analysis 的明确范围流程。
