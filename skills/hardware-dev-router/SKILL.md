---
name: hardware-dev-router
description: "Route cross-domain FPGA and hardware tasks to focused engineering skills and apply shared evidence boundaries. Use when work crosses RTL, board connectivity, host/instrument control or measured-evidence reporting, or when the appropriate specialist is unclear."
---

# Hardware Development Router

## Select the work, not the whole chain

1. Classify the authorized action: explain/review, plan, edit, build or hardware operation. Use [routing table](references/routing-table.md) to choose one focused skill; combine only for genuine ownership crossings.
2. Read [evidence boundaries](references/evidence-boundaries.md) before technical claims. RTL, simulation, applied constraints, routed timing and board measurements are different evidence.
3. Select the user's actual project and nearest rules. Use current source/configuration/diffs over historical notes; old authorizations and PASS records do not authorize new builds or hardware operations.

Small module work does not require a repository map, all downstream skills or new reports. Reuse already-read unchanged evidence; verify identity/freshness before relying on saved results. Review does not authorize editing. New-project layout preferences do not authorize migrating existing projects.

## Application boundaries

- Generic skills own reusable methods. Thin Laser/MAROC adapters own project paths, board/register/packet meanings and local delivery conventions.
- For 513/CW specifics use `laser-cw-qualification-test-development`; 05_CW_TEST_HY is not the default for every Laser request. Its mother projects and dedicated targets keep separate identities.
- Host development, joint SDG/ILA operation, instrument drivers, data analysis, manuals, reports and notes have separate entries in the routing table. An RTL task does not automatically include them.
- Trace the actual transport: packet work needs framing/parser evidence; VIO/JTAG uses command/probe contracts, matching BIT/LTX and readback, not an invented packet parser.

## Conditional resources

- Templates/examples: read [asset library](references/asset-library.md). Keep original projects, board sources and report templates in their owning location.
- Reusable automation: read [hook library](references/hook-library.md) when using its registry. Inspect the chosen script and write boundary; use its dry-run where available.
- Laser paths/tools: read [profile path resolution](references/profile-path-resolution.md). Validate only current dependencies; missing optional roots must not block unrelated work.

Resolve `<CODEX_HOME>` from the environment, falling back to the user's `.codex` directory. Shared templates live in `hardware-assets/templates`; hook use requires an existing registry. Execute maintained helpers from their owning skill/project, not an untracked copy. Do not edit original source assets through the library.
