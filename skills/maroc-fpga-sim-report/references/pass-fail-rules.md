# PASS/FAIL 判据模板

## 1. FAIL 条件
- 出现 `[TB][ERROR]`。
- 关键计数器、关键序列、关键 checker 不满足。
- timeout 触发。
- 如果报告宣称“最终串行码流正确”，但逐 bit 对比存在 `mismatch/missing/extra`。

## 2. WARN 条件
- 调试辅助 case 或扩展 case 出现偏差，但不影响主回归合同。
- `xsim` 存在无害 warning，例如 string/dynamic type trace warning，但 compile/elaborate/simulate 仍通过。

## 3. PASS 条件
- 主回归 case 全部 PASS。
- 无 ERROR。
- 脚本侧日志解析通过（若启用）。
- 若声明了串行签核，则 compare CSV、summary CSV、compare report 三者结论一致。

## 4. 串行签核最小证据链
当结论涉及 `o_sc_dout` 正确性时，至少写清：
1. capture 方法
   - 例如：`posedge o_sc_clk` 且 `o_sc_busy=1`
2. expected source
   - 例如：`bits_829_case_*.txt`
3. 输出工件
   - timing compare CSV
   - summary CSV
   - compare report
4. 最终结论
   - `expected_bits`
   - `observed_bits`
   - `mismatch/missing/extra`

## 5. 边界声明
- 明确 stub/mock 范围。
- 明确当前 simset 层级与不在本层签核的模块。
- 明确不可签核范围：协议细节、板级时序、SI、CDC、上板行为全覆盖等。

## 6. 波形文字表述约束
- `o_sc_byte_valid` 默认描述为“覆盖 104 个 byte 的连续有效窗口”。
- `r_drain_byte_index` 不直接等价为“当前总线上正在输出的 byte 编号”。
- 对 `PKTEND`，写成“包结束提交/短包提交”，不要写成“第三次写”。
