# MAROC Hook Map

Use this file after loading the generic hook rules from `hardware-dev-router/references/hook-library.md`.

Primary map:

`C:/Users/Administrator/.codex/hardware-assets/hooks/maroc-hook-map.md`

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
