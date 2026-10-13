# Stage template usage

Read `<CODEX_HOME>/hardware-assets/templates/vivado/vivado_project_build_skeleton.tcl` before use. It is a library, not a script that starts builds when sourced. Adapt a project-owned launcher, then call `native_project::run $cfg`.

Required dict keys: `project_name`, `project_dir`, `part`, `top`, `sources`, `constraints`, `sim_sources`. The last two lists may be explicitly empty during creation; that is not constraint/timing acceptance. Paths in lists are absolute or project-directory-relative final locations. For first creation supply a reviewed project-owned `prepare_sources` procedure receiving the config dict: AFTER native create_project, it writes only the requested new inputs to those final folders. Do not precreate .srcs in Vivado 2018.3 or use -force to bypass its refusal. Preparation is never rerun for an existing project. Existing inputs must exist. Use `sim_top` when TB sources exist. `external_sources` is an explicit allowlist for reviewed external libraries, never task-temporary dependencies.

`stage` defaults to `create`. `create` writes/reopens XPR with native layout and verifies membership; existing compatible projects are checked, not reconfigured. `check` runs syntax checks; inspect messages, not only Tcl completion. `synth` and `impl` require authorized stages and `report_dir` under the project's docs/logs run directory. `impl` stops at route/reports. Stale or failed runs stop; no automatic resets.

`bit` requires an already completed current routed run and a project-owned `acceptance_gate` Tcl procedure. It receives config dict and report directory; return exactly `1` only after evaluating matching input/checkpoint identity, setup/hold/pulse-width, clock/IO coverage, exceptions, CDC/reset and DRC. Never implement it as `return 1` or infer acceptance from QoR prediction. Missing/failed evidence blocks BIT. Read [timing acceptance](../../fpga-cdc-reset-timing/references/timing-acceptance.md).

Existing source/IP mismatches and unsupported properties deliberately stop rather than silently modify membership or switch tool versions. Interrupted first creation is a partial project, not delivery; audit before explicitly completing it.

Launch batch Vivado with explicit `-log`/`-journal` and working directory `docs/logs/<unique-run>/`. Use target-version help for command support. Do not change global GUI preferences. Native API creation/reopening, visible GUI interaction and full synth/route/bit validation are separate test results.

## IP and repeat contract

Optional `ip_sources` defaults to `{}` and lists final native XCI/XCIX files. IPs in legacy `sources` are normalized separately; duplicate entries across both lists are errors. See [IP and repeat validation](ip-and-repeat-validation.md). First-create preparation may import external IP via Vivado, then verify final paths, configuration, associated assets and OOC. Existing projects only verify membership/identity; no re-import or unconditional output generation.
