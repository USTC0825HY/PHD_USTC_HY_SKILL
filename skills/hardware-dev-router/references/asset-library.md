# Hardware Asset Library

Central asset root:

`<CODEX_HOME>/hardware-assets`

Use this library when a request asks for RTL/testbench skeletons, Vivado automation skeletons, XDC review tables, or report/Markdown structures.

## Entry Points

| Need | Use |
| --- | --- |
| RTL and verification templates | `templates/rtl/` |
| Vivado and ILA templates | `templates/vivado/` |
| Alignment, bring-up, and claim tables | `templates/reports/` |

## Policy

- Use project source assets in place. Do not copy or edit original RTL, schematics, reports, or notes through this library.
- Verify that the selected template exists before using it.
- Read automation scripts before execution and start with dry-run behavior where available.

## Common Template Paths

| Workflow | Template |
| --- | --- |
| RTL review | `templates/rtl/rtl_module_review_checklist.md` |
| Testbench | `templates/rtl/tb_skeleton.v` |
| Fixture provenance | `templates/rtl/fixture_manifest_template.md` |
| CDC/reset/timing | `templates/rtl/cdc_reset_timing_checklist.md` |
| Vivado build | `templates/vivado/vivado_project_build_skeleton.tcl` |
| ILA export | `templates/vivado/ila_export_workflow_skeleton.tcl` |
| XSim wrapper | `templates/vivado/xsim_run_wrapper_skeleton.ps1` |
| Hardware claim table | `templates/reports/claim_table_template.md` |
| Host/RTL alignment | `templates/reports/host_rtl_alignment_table.md` |
| RTL/XDC/schematic alignment | `templates/reports/rtl_xdc_schematic_alignment_table.md` |
| Board bring-up log | `templates/reports/board_bringup_log_template.md` |
| PPT/MD companion | `templates/reports/ppt_md_companion_template.md` |
