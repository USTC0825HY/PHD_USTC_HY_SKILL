# Hardware Asset Library

Central asset root:

`C:/Users/Administrator/.codex/hardware-assets`

Use this library when a request asks for reusable templates, source examples, scripts, PPT layouts, QA patterns, RTL/testbench skeletons, Qt host patterns, XDC review tables, or report/Markdown structures.

## Entry Points

| Need | Use |
| --- | --- |
| Machine-readable catalog | `catalogs/hardware-assets-index.yaml` |
| Human overview | `catalogs/hardware-assets-index.md` |
| MAROC RTL/TB/fixture/XDC/scripts | `source-refs/maroc-rtl-assets.md` |
| MAROC Qt/C++ host source patterns | `source-refs/maroc-qt-host-assets.md` |
| MAROC PPT templates, decks, build scripts, QA | `source-refs/maroc-ppt-assets.md` |
| MAROC Obsidian and repo notes | `source-refs/maroc-doc-assets.md` |
| Reusable script hooks | `hooks/hook-library.md` |
| Hook registry | `hooks/hardware-hook-registry.yaml` |
| Hook runner | `hooks/invoke_hardware_hook.py` |
| Stable reusable templates | `templates/` |
| Read-only representative examples | `snapshots/` |
| Generic patterns derived from MAROC | `derived/` |

## Policy

- Prefer `stable` and `active` assets for normal recommendations.
- Treat `experimental` and `historical` assets as reference only.
- Use project source assets in place. Do not copy or edit original RTL, Qt, PPT, or Obsidian files through this library.
- Do not copy project source into generic skills. Link to the asset library or original source path.
- For copied templates and snapshots, verify `asset_path` exists before using it.
- For reusable scripts, prefer the hook registry and runner under `hooks/`; dry-run before any generated-output, project-write, hardware-write, or destructive operation.
- For project-specific packet, register, board, or report style rules, load the project adapter asset map after this generic policy.

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
| Qt/CMake/CTest | `templates/qt-cpp-host/CMakeLists_skeleton.txt` |
| Qt backend interface | `templates/qt-cpp-host/AbstractDeviceClient.h` |
| Qt fake backend | `templates/qt-cpp-host/FakeDeviceClient.h` |
| Hardware claim table | `templates/reports/claim_table_template.md` |
| Host/RTL alignment | `templates/reports/host_rtl_alignment_table.md` |
| RTL/XDC/schematic alignment | `templates/reports/rtl_xdc_schematic_alignment_table.md` |
| Board bring-up log | `templates/reports/board_bringup_log_template.md` |
| PPT/MD companion | `templates/reports/ppt_md_companion_template.md` |
