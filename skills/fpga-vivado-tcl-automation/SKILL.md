---
name: fpga-vivado-tcl-automation
description: "Generic Vivado Tcl automation workflow. Use for creating or recreating Vivado projects, adding sources and constraints, generating IP/ILA cores, configuring simsets, running synth/place/route/bitstream builds, exporting reports, Hardware Manager Tcl, and reproducible PowerShell/Tcl command packaging."
---

# FPGA Vivado Tcl Automation

## Workflow

1. Choose new creation, compatible repeat, read-only audit, or explicitly authorized migration. For migration only, read [authorized migration](references/authorized-project-migration.md); ordinary creation never migrates or cleans existing projects.
   Decide whether the task targets project creation, current-project build, simset preparation, IP/ILA generation, XDC load order, report export, or Hardware Manager.
   Read [version selection](references/vivado-version-selection.md) to select the project/tool version and stage boundary before choosing commands.
2. Prefer existing Tcl/PowerShell helpers from the project before writing a parallel flow.
   For read-only membership, use `scripts/project_inputs.py <xpr> --stage synthesis|implementation|simulation`; it does not elaborate IP or execute Tcl. Read [audit helper usage](references/audit-helper-usage.md) when invoking project/layout, pin, Python-runtime or simulation helpers.
3. Keep commands reproducible: absolute or repo-root-relative paths, expected outputs, log paths, tool version, and required mode.
4. Separate formal builds, smoke builds, debug/ILA builds, and simulation setup.
5. After bitstream or probe-file claims, capture build log, timing summary, DRC summary, utilization, IO report, bit path, and probe-file path.

## New-project acceleration defaults

For newly created compatible Project Mode projects, apply and read back these defaults unless the user or project evidence explicitly requires a different flow. Check property/IP/run support in the selected version first; unsupported policy requires an explicit diagnostic and reviewed exception, not silent fallback:

- Set `GENERATE_SYNTH_CHECKPOINT=true` on every XCI and fail if any readback is false.
- Set `AUTO_INCREMENTAL_CHECKPOINT=1` on `impl_1`; a first implementation without a reference checkpoint is valid.
- Accept a manual incremental DCP only after compatibility checks. It is a one-run override, not a placeholder project setting.
- In non-project mode, inject the validated incremental DCP after `opt_design` and before `place_design`.
- Never use unconditional `create_project -force` in a new-project template.

Read [new-project build defaults](references/new-project-build-defaults.md) for exact commands, precedence, Vivado-version handling, diagnostics, and failure behavior.

## GUI Project Deliverable

For project creation or recreation, a Tcl script alone is not a complete delivery. Unless the user explicitly requests a non-project flow, always create and retain a directly openable `.xpr` for each build target.

- Put each GUI XPR at an obvious, documented, stable path; do not leave the only XPR buried in an ephemeral cache or temporary run directory.
- Read [native project layout](references/native-project-layout.md). New projects use the GUI-native `.srcs`, `.runs`, `.cache` and simulation layout, not a parallel custom build tree. Hand-written RTL lives in `.srcs/sources_1/new/<function>/`; create only needed folders and register sources once from their final location.
- Open every delivered XPR with the target Vivado version and verify the expected top, FPGA part, active constraints, and zero missing design/IP files.
- Treat "project-creation Tcl exists" and "Vivado generated an XPR that the user can open in the GUI" as separate acceptance checks.
- In the handoff, provide the exact clickable XPR path for every target.

## Boundaries

The skeleton defaults to `create`; `check`, `synth`, `impl` and `bit` are separate requested stages. Stage selection is not authorization. Require explicit project name/directory/part/top/source lists; do not adopt template/example devices. Resume existing projects only after identity/source verification, never force-create, automatically reset runs or silently migrate a legacy layout.

Read [IP and repeat validation](references/ip-and-repeat-validation.md) for optional `ip_sources`, XCIX identity, explicit simulation lists and idempotency checks. Read [stage template usage](references/stage-template-usage.md) before using the template. `impl` stops at route/report review. `bit` requires a matching routed result and an explicit project-specific acceptance gate; QoR predictions and process exit alone are insufficient. Read [timing acceptance](../fpga-cdc-reset-timing/references/timing-acceptance.md) before a closure claim.

Vivado automation can prove that a build flow ran and produced artifacts. It does not prove board behavior until the artifacts are programmed and measured.

## Asset Library

- Use `<CODEX_HOME>/hardware-assets/templates/vivado/vivado_project_build_skeleton.tcl` for a generic project/build skeleton.
- Use `<CODEX_HOME>/hardware-assets/templates/vivado/xsim_run_wrapper_skeleton.ps1` for a PowerShell XSim wrapper skeleton.
- Use project `source-refs/` files to find existing Vivado, XSim, ILA, and report-export scripts before writing a parallel flow.
- Treat project creation, bitstream builds, memory staging, and IP generation as project writes; read the wrapper and confirm the output directory before execution.

## Personal XDC style

When creating a project or when the user authorizes constraint-file organization, read [the shared XDC style reference](references/xdc-project-style.md). This is the sole style authority; do not automatically reorganize unrelated existing projects.
