# YAML与GUI

- frequency_sweep固定幅度扫频，amplitude_sweep固定频率扫幅，精确拼写；显式不等间隔点表或范围互斥。
- 联合采集GUI纯数字频率以kHz解释，0.1=100Hz；YAML/协议仍Hz。其他页按标签，不泛化。
- 启动默认C1；主动导入YAML channel: 2保留C2，按实物接线确认。
- source.model为auto/sdg6052x/sdg6032x_e；auto仅唯一受支持仪器可用，显式地址也校验IDN。
- Vpp/Vrms支持ohm_50/high_z，dBm仅ohm_50；源/ADC上限同单位，切换不换算。maximum_path_gain_db为最坏通路增益，不是幅度单位。
- half_vpp仅适用实现允许的Vpp，名义OFST=Vpp/2、0～Vpp，不宣称实测。零幅度需显式许可。
- 完整CELL_NAME优先，后缀必须唯一；NAME/PROBE_PORT、位宽和CONTROL.DATA_DEPTH以当前Hardware Manager为准。LTX辅助核对不证明已烧写，不用hw_ila_N固定序号。
- preflight由完整点表生成1..N。旧部分预采转换后核对SHA；修改后重新应用/检查/预采。
- SQLite填写完整文件名如任务根/stimulus.sqlite；不存在时运行创建，目录本身不是数据库。续测不移动数据。
- 方案来源是当前工程config/engineering_plans，旧release内SPIROC目录不作为长期入口。模板副本编辑不覆盖正式模板。

2208/9245/677/128共用流程而不共用点表、ILA映射或安全值；查当前清单，不硬编码只启用2208。
