# Report Writing

## What Good MAROC Simulation Reports Must Explain

1. Signal chain and validation boundary first
2. Which TB/topology is under test
3. Why this layer exists (`sim_parser` vs `sim_sc829` vs `top`)
4. Test matrix
5. Case-by-case purpose, stimulus, key signals, expected behavior, checker path, result
6. Risks / non-signoff boundary
7. Final signoff conclusion

For `CY_driver_new` module-level USB reports, also explain up front:

1. module定位 is bridge, not full USB stack
2. `FIFOADR` endpoint mapping
3. who drives `FD[15:0]` in read vs write
4. why `PKTEND` is commit, not data write

## Recommended Main Structure

1. 最前置操作（如果用户是为了 `xsim`）
2. 模块定位与接口语义
3. 信号链与理论机制
4. 三层验证边界与重点信号
5. Testbench 文件结构说明
6. 验证目标与边界
7. 测试矩阵
8. Case 设置思路与信号流检查流程
9. Case-by-case 测试分析
10. 关键检查器与自动判定逻辑
11. 关键结果总结
12. 最终串行码流签核结论（如果做了 `o_sc_dout` 对比）
13. 风险、边界与未覆盖项
14. 最终判定
15. 附录（xsim 操作、波形分组、截图模板、实验记录模板）

## What To Add For Case Clarity

When users say “case 设置思路和检查信号流不清晰”, add:

1. Positive-case setup flowchart
2. Negative-case setup flowchart
3. Positive signal-observation flowchart
4. Negative signal-observation flowchart
5. One table mapping each case to:
   - how the packet is built or mutated
   - which signals to check first
   - what the final pass condition is

For module-level USB/FIFO reports, also add:

1. one compact interface table:
   - `00 -> EP2_IN -> 写 -> FPGA/DUT 驱动 FD[15:0]`
   - `11 -> EP8_OUT -> 读 -> FX2 驱动 FD[15:0]`
2. one explicit “总线方向” explanation block
3. one explicit “`PKTEND` is not another write” explanation block
4. one “case signal timing explanation” bullet in each case section

## What To Add For Serial Signoff

When `o_sc_dout` correctness matters, do not stop at “TB passed”.

Add:

1. capture method:
   - sampled at `posedge o_sc_clk` while `o_sc_busy=1`
2. expected source:
   - `bits_829_case_*.txt`
3. output artifacts:
   - timing compare CSV
   - summary CSV
   - standalone compare report
4. one explicit conclusion:
   - “final `o_sc_dout` serial bitstream matches fixture bit-by-bit”

## Writing Rules

1. Prefer actual task/signal names from TB/RTL.
2. Prefer absolute clickable file links.
3. Keep conclusions auditable:
   - expected bits
   - observed bits
   - mismatch/missing/extra
4. Use Mermaid when the user is confused by structure or signal flow.
5. Keep “theory” and “measurement” separated.
6. For waveform-heavy reports, write each case in two layers:
   - concise case metadata
   - one short “信号时序解释” paragraph
7. Do not mix read chain and write chain in one overview diagram if the user is confused; split them or enforce read-first then write-second reading order.

## Handbook Slimming Rules

When both a report and a handbook exist for the same TB, do not let them become two copies of the same document.

Preferred split:

- report:
  - module定位
  - interface semantics
  - test matrix
  - screenshot-backed `CASE0~CASE7` explanations
  - signoff boundary and final conclusion
- handbook:
  - XSim entry
  - Tcl/PS1/Python usage
  - wave grouping
  - read order and time windows
  - common misreads
  - bring-up preparation questions

What to delete from a bloated handbook first:

1. repeated test matrix already present in report
2. repeated case-by-case PASS/result prose
3. long appendices that restate the same Tcl in three different ways
4. duplicated “what is the module” paragraphs
5. repeated warning/risk sections

What to keep in a slim handbook:

1. the shortest working entry commands
2. one compact module/interface semantics block
3. one compact state/read/write explanation block
4. one wave grouping table
5. one time-window table
6. one common-misreads list
7. one bring-up/precheck list

Preferred target style for a slim handbook:

- 4 to 6 main sections
- operation first
- theory second
- wave reading third
- boundary/bring-up last
- no case screenshots unless the handbook truly needs them

## Typical Flowcharts To Use

- overall signal-chain flowchart
- single-transaction sequence diagram
- positive case setup flow
- negative case setup flow
- signal inspection flow
- three-layer boundary diagram
