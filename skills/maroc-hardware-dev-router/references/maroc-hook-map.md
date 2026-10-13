# MAROC Hook Map

Use this file after loading the generic hook rules from `hardware-dev-router/references/hook-library.md`.

Primary map:

`<CODEX_HOME>/hardware-assets/hooks/maroc-hook-map.md`

## Availability Gate

- Check that the primary map, registry, runner, and referenced source script all exist before offering a hook invocation.
- If any of them is absent, this table is descriptive only. Do not fabricate a hook command or create a replacement registry.
- Use `resource-map.md` to understand the intended scenario, then locate the current project with the user or through workspace discovery.
- Without a verified registry and runner, restrict work to read-only inspection and ordinary project commands that are already documented in the located repository.

## Scenario Hooks

| Scenario | Hook id | Risk |
| --- | --- | --- |
| Asset and registry validation | `asset.catalog.validate` | `read-only` |
| Hardware skill validation | `skill.validate.hardware` | `read-only` |
| Parser fixture preparation | `rtl.fixture.prepare.maroc` | `project-write` |
| Host export replay XSim flow | `rtl.sim.maroc.xsim` | `generated-output` |
| Hardware skill intro PPT QA/build | `ppt.qa.hardware-skill-intro` | `generated-output` |
| Current ILA core listing | `ila.capture.list` | `read-only` |
| RTL port map for XDC review | `xdc.review.maroc.port-map` | `project-write` |

## Rules

- Use dry-run first for every MAROC hook.
- Treat `rtl.fixture.prepare.maroc`, `xdc.review.maroc.port-map`, and `vivado.build.*` as project-writing operations.
- Treat ILA capture, programming, and full-auto Hardware Manager scripts as live-hardware operations unless the registry marks them read-only.
- Do not run cleanup hooks without an explicit target and user confirmation.
- Never treat a missing registry as lowering a hook's risk level.
