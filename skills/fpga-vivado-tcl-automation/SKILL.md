---
name: fpga-vivado-tcl-automation
description: "Generic Vivado Tcl automation workflow. Use for creating or recreating Vivado projects, adding sources and constraints, generating IP/ILA cores, configuring simsets, running synth/place/route/bitstream builds, exporting reports, Hardware Manager Tcl, and reproducible PowerShell/Tcl command packaging."
---

# FPGA Vivado Tcl Automation

## Workflow

1. Decide whether the task targets project creation, current-project build, simset preparation, IP/ILA generation, XDC load order, report export, or Hardware Manager.
2. Prefer existing Tcl/PowerShell helpers from the project before writing a parallel flow.
3. Keep commands reproducible: absolute or repo-root-relative paths, expected outputs, log paths, tool version, and required mode.
4. Separate formal builds, smoke builds, debug/ILA builds, and simulation setup.
5. After bitstream or probe-file claims, capture build log, timing summary, DRC summary, utilization, IO report, bit path, and probe-file path.

## Boundaries

Vivado automation can prove that a build flow ran and produced artifacts. It does not prove board behavior until the artifacts are programmed and measured.

## Asset Library

- Use `C:/Users/Administrator/.codex/hardware-assets/templates/vivado/vivado_project_build_skeleton.tcl` for a generic project/build skeleton.
- Use `C:/Users/Administrator/.codex/hardware-assets/templates/vivado/xsim_run_wrapper_skeleton.ps1` for a PowerShell XSim wrapper skeleton.
- Use project `source-refs/` files to find existing Vivado, XSim, ILA, and report-export scripts before writing a parallel flow.
- Use `C:/Users/Administrator/.codex/hardware-assets/hooks/hardware-hook-registry.yaml` for `vivado.build.*` hooks. Treat project creation, bitstream builds, mem staging, and IP generation as `project-write` unless the registry states otherwise.
