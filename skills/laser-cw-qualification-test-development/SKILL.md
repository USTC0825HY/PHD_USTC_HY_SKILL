---
name: laser-cw-qualification-test-development
description: Develop, audit, or document the current ultra-stable-laser 513/CW qualification-test Vivado project using its authoritative XPR/XDC, project board registry, AD677/DDS constraints, and the generic multi-board signal-chain closure workflow.
---

# Laser CW Qualification Test Development

Use this skill only as the 513/CW project adapter. Use `fpga-board-signal-chain-closure` for reusable board/evidence graphs, connector closure, power distribution, and chain schema; use `fpga-orcad-xdc-pipeline` and `rtl-schematic-xdc-alignment` for PST and RTL/XDC mechanics.

运行脚本前按 [运行时验证](../hardware-dev-router/references/runtime-validation.md) 探测实际 Python 版本和所需导入；优先复用可执行专用环境。

## Report and measurement routing

For numerical isolation/noise/calibration, use laser-electrical-data-analysis; for Word reports use laser-test-report-writing; for data paths use laser-cw-data-pipeline and hardware-evidence-report-sync. Ordinary analysis/report tasks do not enter the FPGA workflow below.

Invoke this adapter only for the affected firmware, control words, channel mapping, pin or board-connection evidence. A fitted waveform or screenshot does not verify FPGA configuration, and an XPR does not verify analog coupling. Keep dated DA766/AD677 examples in the analysis skill, not as project defaults here.

## Required reading

Before acting, read:

1. [project-authority.md](references/project-authority.md) to select the requested project; 05, mother projects and dedicated targets retain separate identities
2. [513-board-registry.json](references/513-board-registry.json) when selecting board evidence, creating a board-targeted project or tracing connectivity
3. [evidence-and-pin-policy.md](references/evidence-and-pin-policy.md) when pins, device groups or board interfaces are in scope
4. [implementation-scope.md](references/implementation-scope.md)
5. [obsidian-output-contract.md](references/obsidian-output-contract.md) only when notes/CSV/XLSX outputs are requested
6. [513-control-signal-tracing.md](references/513-control-signal-tracing.md) when tracing any board path

## Mandatory workflow

Select the task mode first: new-project creation follows [native GUI layout](../fpga-vivado-tcl-automation/references/native-project-layout.md) and the applicable board requirements below; internal RTL writing/review uses `fpga-rtl-development`/`fpga-rtl-code-review` with local frozen-source rules. Steps 2–6 are for affected board/pin/power paths, not mandatory whole-board work for an internal module edit. Legacy projects are audit-only unless migration is explicitly requested.

1. Parse the current XPR again and verify top, part, source membership, active constraint set/XDC, and disabled state. Do not trust dated adapter defaults over the XPR.
2. Run the generic multi-board preflight with `references/513-board-registry.json`; preserve selected and alternative evidence sets as separate records.
3. For FPGA chains, run the static RTL/XDC/SZSD FPGA-ball audit using the selected SZSD PST. For power-only chains, set RTL/XDC to `不适用` and trace rail/protection/return evidence instead.
4. Trace board-local nets through exact PST nodes and close every board boundary independently through the bottom-board path. Never infer continuity from similar names or contact numbers.
5. Apply the AD677/DDS pin, logical-group, CW/GS assembly, and legacy-XDC restrictions in the project references.
6. Separate current RTL/XDC, PST-confirmed segments, declared graph edges, cross-board inference, physical continuity, electrical availability, and reviewed Vivado state.
7. Make the smallest user-authorized RTL/XDC change; do not hand-edit XPR XML or generated IP state.
8. Synchronize Obsidian or formal CSV/XLSX only when those artifacts are explicitly requested; RTL implementation alone does not request them. Use the project source validator with explicit `-Project`; without `-SzsdPstxnet` it checks XPR membership only. Board pin auditing requires an explicitly selected PST/evidence set; no retired project defaults. See [audit helper usage](../fpga-vivado-tcl-automation/references/audit-helper-usage.md).

## SZSD工程创建强制项：16X245低有效使能

凡新建或重建以513/CW数字锁定主控板（SZSD）为目标的FPGA测试工程，必须显式纳入以下两路板级电平转换器使能。不得因测试逻辑未直接使用普通GPIO而省略：

```verilog
output wire F_1V8_16X245_EN21,
output wire F_1V8_16X245_EN31;

assign F_1V8_16X245_EN21 = 1'b0;
assign F_1V8_16X245_EN31 = 1'b0;
```

```tcl
set_property -dict {PACKAGE_PIN BA41 IOSTANDARD LVCMOS18} [get_ports F_1V8_16X245_EN21]
set_property -dict {PACKAGE_PIN AL32 IOSTANDARD LVCMOS18} [get_ports F_1V8_16X245_EN31]
```

两路为低有效使能，正常测试设计固定输出`0`。工程创建、综合和发布前必须检查：顶层端口存在且方向为输出；RTL存在显式低电平驱动；活动XDC包含上述LOC/IOSTANDARD；实现后`report_io`显示BA41/AL32、OUTPUT、LVCMOS18。只有原理图/PST或经批准的板卡修订明确证明该目标硬件不需要这两路使能时，才允许记录证据后豁免。

## Project-specific refusal rules

Refuse to:

- use disabled or historical XDC as current pin authority;
- merge the selected SZSD or YCQD evidence set with its public/internal alternative;
- equate AD766 groups or G1/G2/G3 with physical device instances without traced cable/connector evidence;
- claim a DNP/TSD*/NC/OE-disabled branch is electrically available;
- claim synthesis, implementation, bitstream, or hardware validation unless actually run and reviewed.

## Output

For board-connectivity outputs use the generic v2 board/edge/chain schema. Every FPGA pin conclusion includes top port/direction, active LOC/IOSTANDARD, FPGA ball/net, conditioning and connector segments, selected evidence set, assembly state, evidence level, and pending checks. Every power branch includes source/load rail, voltage when evidenced, connectors, protection/switch/filter, return ground, assembly state, and unclosed points. Internal RTL work uses the focused skill's compact behavior/test handoff instead.

Follow `obsidian-output-contract.md` for formal Markdown/CSV/XLSX outputs.

## Personal XDC style

When creating a project or when the user authorizes constraint-file organization, read [the shared XDC style reference](../fpga-vivado-tcl-automation/references/xdc-project-style.md). This is the sole style authority; do not automatically reorganize unrelated existing projects.
