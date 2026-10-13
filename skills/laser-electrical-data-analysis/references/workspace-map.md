# 当前路径选择与历史证据

显式任务路径优先，其次CLI/环境变量，最后经过验证的profile。不要按mtime自动选择板卡、报告或校准版本。

| 内容 | 当前入口/规则 |
|---|---|
| MATLAB库 | F:\01_Laser\code\matlab\513DIANXING_analysis\CW_analysis\CW_513_ANALYSIS；读本地AGENTS和memory |
| 513报告主库快照 | I:\01_laser\202607-202609_513_data；截至20260919、v2归类，非全部后续测量 |
| 新采集与后续复测 | I:\CW_Data及用户指定L盘批次；按实际路径核验 |
| 报告语料 | F:\01_Laser\0_20260727_513test\03_CW测试\01_Documents_文档\02_Test_Reports_测试报告；当前用户文件优先 |

保留脚本已有环境覆盖 LASER_TEST_CODE_ROOT、LASER_TEST_DATA_ROOT、LASER_TEST_REPORT_ROOT、LASER_TEST_513_CODE_ROOT、LASER_TEST_513_DATA_ROOT。只验证本次需要的键；旧profile缺失不自动创建目录。

分析输出沿用当前converter.io.resolveOutputBase：raw目录输入写同级results，其他输入通常写其下results，显式output优先；存量组织不迁移。报告留在其授权位置。

校准选择以板卡/接口/参考面/改焊状态和被审阅run为准，summary、measurements、图、参数和输入哈希必须同源。旧总表与当前run冲突时记录冲突，不静默拼接。

仅做历史对照时读 [20260816快照](workspace-history-20260816.md)，其中旧路径、JG映射和斜率不是本轮默认值。

513/CW当前配置层级和结构见项目AGENTS.md及memory/PROJECT_MEMORY.md当前摘要。代码刻度CSV在_shared/+converter/+calibration/report_calibrations_20261004.csv；同源两表单XLSX在docs/20261012_board_calibration。Word为指定来源，CSV供计算，XLSX供归档查看；不分别维护三套系数。
