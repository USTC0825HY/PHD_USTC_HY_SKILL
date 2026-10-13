# 严格证据包交接

旧 CLI 和 errors/warnings/status 保留。无 --strict 仅为 legacy_structure_only，即使 PASS 也不算定量证据验收。正式引用使用 --strict；ERROR/UNVERIFIED 均非零退出，不能自动流入定量结论。允许保留暂不能判定/未测试结果。PASS 仅表示返回 checks 的检查层通过，不证明算法或真实仪器结论。

已核对 MATLAB CW_513_ANALYSIS 中 runNoise/runScale/calculatePowerScale 的字段：频谱 frequency_hz、psd_V2_per_Hz、asd_V_per_sqrtHz、可选 asd_uV_per_sqrtHz；参数 Parameter,Value；标定 code_vpp/output_vpp_v 或 CodePp/InputVoltageVpp；来源 input_path/source_sha256。不得猜测其它列含义。one-sided 频谱要求非负严格递增频率、不超过 sample_rate_hz/2、覆盖 band_start_hz..band_end_hz，并检查 PSD=ASD² 和已声明的单位转换。

缺少的证据声明可以写入派生结果目录 audit_metadata.json，不改原 MATLAB 数值输出。例：
```json
{"sample_rate_hz":1000,"band_start_hz":1,"band_end_hz":400,"formal_conclusion":"满足","source_files":[{"path":"../raw.csv","sha256":"真实64位SHA256"}],"calibration":{"direction":"input_to_output","input_unit":"code","output_unit":"V","reference_plane":"ADC输入连接器","source":"../raw.csv","valid_range":[-1,1]}}
```
示例只演示结构，实际 calibration.source 必须指向 source_files 中哈希已核实的校准记录。标定测量表协议的输入单位为 codepp/code_vpp/CodePp，输出为 Vpp/Vpp_v，方向为 input_to_output，拟合纳入点须在有效范围内。

direction 仅 input_to_output/output_to_input/identity；有效范围必须有单位、上下界且与声明输入轴一致。状态精确读取 formal_conclusion/Conclusion/conclusion，状态未知或非规范值失败；执行状态 status 不冒充测量结论。元数据冲突失败。来源必须可访问且哈希一致，PNG 必须可解码，MAT 必须可读取且有变量；v7.3 或缺 scipy 标为未验证。

allan/generic 尚无经过工程输出核对的通用数值列协议，严格检查返回未验证，不把随意猜列名当作覆盖；要交付对应定量证据须另行完成领域审查并记录限制。旧输出仍可用结构模式列问题。
