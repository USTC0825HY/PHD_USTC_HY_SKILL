---
name: vivado-impl
description: Choose Vivado implementation strategies, incremental checkpoint reuse and opt/place/phys_opt/route changes for an identified device and tool version. Use vivado-analysis for report interpretation and fpga-vivado-tcl-automation for execution.
---

# vivado impl

1. Identify the requested analysis or change and read the current project rules, XPR, constraints and matching reports.
2. Read [version selection](../fpga-vivado-tcl-automation/references/vivado-version-selection.md) before choosing commands or interpreting version-specific features. A tool mismatch is not permission to migrate the project.
3. Read the relevant section of [the strategy/reference guide](references/strategy-guide.md) for the question at hand. It contains 2025.2 material; [the 2022.2 compatibility record](references/vivado-2022.2-compatibility.md) applies only to that audited version. Do not load unrelated command tables.
4. Explain the evidence, tradeoff and smallest proposed change. Distinguish static intent, synthesis estimates, post-route reports and board measurements.
5. Use `fpga-vivado-tcl-automation` for requested execution. Existing reports may be inspected; do not start runs, reset history, generate BIT/LTX or operate hardware merely to answer a review question.

Distinguish unchanged IP OOC synthesis/cache reuse from whole-design incremental placement/routing. Check the actual run properties, selected reference and reuse report; an enabled automatic setting alone does not prove reuse. Baselines require matching device/top and compatible IP, clock and constraint structure. Major structure changes call for a full implementation when authorized; small edits can use a validated baseline, with reuse/timing/route results reviewed. Never change a live project's strategy merely because a generic skill was updated.

Retain upstream provenance and license information in the compatibility record and existing references. Exact commands/options require the selected version's help and actual part support; no version-independent capability claim follows from this guide.
