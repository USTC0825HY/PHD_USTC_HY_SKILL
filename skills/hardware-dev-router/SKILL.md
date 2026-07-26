---
name: hardware-dev-router
description: "Generic hardware-development skill router, evidence policy, and reusable asset entrypoint. Use when a request spans FPGA RTL, simulation, ILA/on-chip debug, CDC/reset/timing, Vivado Tcl, register maps, host software, schematic/XDC alignment, datasheet review, PCB bring-up, lab evidence, Markdown notes, PPT/reporting, reusable templates, source examples, scripts, or asset selection. MAROC is only one project example."
---

# Hardware Development Router

## Start Here

1. Classify the request with `references/routing-table.md`.
2. Use one focused leaf skill when possible; combine skills only when the task crosses ownership boundaries.
3. Load `references/evidence-boundaries.md` before making technical claims.
4. Load `references/asset-library.md` when the request asks for templates, source examples, scripts, PPT layouts, QA patterns, or reusable assets.
5. Load `references/hook-library.md` when the request asks to run, wrap, validate, or automate reusable scripts.
6. Identify the project-specific application layer, such as MAROC, only after the generic work type is clear.

## Routing Rules

- Use generic skills for common FPGA, hardware, host, and reporting workflows.
- Use project-specific skills only for project paths, register meanings, packet formats, board names, templates, or established local procedures.
- Keep source artifacts in place. Do not copy project repositories, schematics, notes, or PPT templates into generic skill folders.
- When implementation is requested, inspect current source, constraints, scripts, notes, and diffs before trusting historical summaries.

## Asset Rules

- Use the central library at `C:/Users/Administrator/.codex/hardware-assets` for reusable templates, asset catalogs, and representative snapshots.
- Use `C:/Users/Administrator/.codex/hardware-assets/hooks` for script hooks. Start with dry-run and obey the registry risk level before executing anything.
- Prefer `stable` and `active` assets. Treat `experimental` and `historical` assets as reference only.
- Use copied or derived templates from `templates/`; read `source-refs/` for original project files.
- Do not edit original source assets through the asset library.

## Cross-Domain Discipline

- Host-to-RTL tasks must prove application export, wire framing, fixture generation, parser/TB consumption, and replay/checker behavior.
- RTL-to-hardware tasks must prove RTL port, constraint pin, schematic net, board connector/test point, IO standard, and timing role.
- Lab-to-report tasks must preserve evidence path, date, build/bitstream/version, observed fact, allowed conclusion, and remaining boundary.

## Application Examples

Use MAROC skills as project adapters, not as the generic architecture:

- MAROC Qt host work -> `maroc-qt-host-development`, with common Qt structure from `qt-cpp-host-development`.
- MAROC packet/fixture replay -> `maroc-host-rtl-alignment`, backed by generic `host-rtl-alignment`.
- MAROC RTL/XDC/schematic checks -> `maroc-rtl-schematic-xdc-alignment`, backed by generic `rtl-schematic-xdc-alignment`.
