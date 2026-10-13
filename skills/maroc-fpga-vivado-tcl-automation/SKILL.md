---
name: maroc-fpga-vivado-tcl-automation
description: "MAROC adapter for Vivado Tcl automation. Use for recreating MAROC_PRJ, building MAROC bitstreams, generating/checking MAROC ILA IP, applying MAROC XDC, setting simsets, configuring memory autoload, preparing XSim GUI flows, and packaging repeatable Tcl/PowerShell commands. Use fpga-vivado-tcl-automation for the generic method."
---

# MAROC FPGA Vivado Tcl Automation

## Workflow

1. Apply the generic `fpga-vivado-tcl-automation` workflow first.
2. Use MAROC Vivado, XSim, ILA, and build script paths from `maroc-hardware-dev-router/references/resource-map.md`.
3. Separate MAROC project creation, current-project build, simset preparation, ILA IP generation, XDC load order, and Hardware Manager flows.
4. Preserve formal, smoke, and debug/ILA builds as distinct flows.
5. After generated bit/ltx claims, record log, timing summary, DRC summary, utilization, IO report, bit path, and ltx path.

## MAROC Boundaries

MAROC Tcl automation proves a reproducible build or hardware-manager operation. It does not prove board behavior until the image is programmed and measured.

## Asset Library

- Read `<CODEX_HOME>/skills/maroc-hardware-dev-router/references/maroc-asset-map.md` for MAROC Vivado, XSim, ILA, and XDC script routing.
- Use `<CODEX_HOME>/hardware-assets/source-refs/maroc-rtl-assets.md` to locate current project scripts without copying generated build folders into skill directories.
- Use `<CODEX_HOME>/hardware-assets/templates/vivado/vivado_project_build_skeleton.tcl`, `ila_export_workflow_skeleton.tcl`, and `xsim_run_wrapper_skeleton.ps1` for new reproducible automation.
- Use `<CODEX_HOME>/hardware-assets/hooks/maroc-hook-map.md` and the `vivado.build.*` registry entries before running MAROC Tcl/PowerShell helpers. Treat build, mem staging, IP generation, and project creation as project-writing hooks.
