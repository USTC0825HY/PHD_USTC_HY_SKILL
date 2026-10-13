---
name: vivado-constraints
description: Write or review Vivado physical and timing constraints using project, board and interface evidence. Use for XDC/SDC, clocks, I/O delays, exceptions and scoping; route report interpretation to vivado-analysis.
---

# vivado constraints

1. Identify the requested analysis or change and read the current project rules, XPR, constraints and matching reports.
2. Read [version selection](../fpga-vivado-tcl-automation/references/vivado-version-selection.md) before choosing commands or interpreting version-specific features. A tool mismatch is not permission to migrate the project.
3. Read the relevant section of [the strategy/reference guide](references/strategy-guide.md) for the question at hand. It contains 2025.2 material; [the 2022.2 compatibility record](references/vivado-2022.2-compatibility.md) applies only to that audited version. Do not load unrelated command tables.
4. Explain the evidence, tradeoff and smallest proposed change. Distinguish static intent, synthesis estimates, post-route reports and board measurements.
5. Use `fpga-vivado-tcl-automation` for requested execution. Existing reports may be inspected; do not start runs, reset history, generate BIT/LTX or operate hardware merely to answer a review question.

Retain upstream provenance and license information in the compatibility record and existing references. Exact commands/options require the selected version's help and actual part support; no version-independent capability claim follows from this guide.

When creating a project or organizing constraints at the user's request, read [the shared XDC style reference](../fpga-vivado-tcl-automation/references/xdc-project-style.md). Do not reorganize unrelated existing projects.
