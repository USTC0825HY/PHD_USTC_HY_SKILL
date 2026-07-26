# MAROC Asset Map

Central hardware asset root:

`C:/Users/Administrator/.codex/hardware-assets`

Use this file after classifying the generic workflow with `hardware-dev-router`. The original MAROC repositories, PPT folders, and Obsidian vault remain authoritative. The asset library provides indexes, stable templates, representative snapshots, and derived generic skeletons.

## Source Reference Files

| Domain | Asset source reference |
| --- | --- |
| RTL, TB, fixtures, Vivado/XSim/ILA scripts, XDC | `source-refs/maroc-rtl-assets.md` |
| Qt/C++ host source, CMake, CTest, fake/backend patterns | `source-refs/maroc-qt-host-assets.md` |
| PPT templates, decks, build scripts, QA reports | `source-refs/maroc-ppt-assets.md` |
| Obsidian notes and repository Markdown documents | `source-refs/maroc-doc-assets.md` |
| Script hook registry and MAROC scenario map | `hooks/hook-library.md`, `hooks/maroc-hook-map.md` |

## Recommended MAROC Asset Routes

| Request | First read |
| --- | --- |
| Find a MAROC RTL module or review example | `source-refs/maroc-rtl-assets.md` |
| Find a MAROC testbench, fixture, or replay example | `source-refs/maroc-rtl-assets.md` plus `templates/rtl/fixture_manifest_template.md` |
| Find Vivado/XSim/ILA automation | `source-refs/maroc-rtl-assets.md` plus `templates/vivado/` |
| Find Qt host architecture, backend, transform, or tests | `source-refs/maroc-qt-host-assets.md` plus `templates/qt-cpp-host/` |
| Find MAROC PPT template or build/QA pattern | `source-refs/maroc-ppt-assets.md` plus `templates/ppt/` |
| Run or dry-run a MAROC reusable script | `hooks/maroc-hook-map.md` plus `hooks/hardware-hook-registry.yaml` |
| Build a report/PPT/MD claim table | `templates/reports/claim_table_template.md` |
| Align host export to RTL fixture | `templates/reports/host_rtl_alignment_table.md` |
| Align RTL/XDC/schematic | `templates/reports/rtl_xdc_schematic_alignment_table.md` |
| Write board bring-up notes | `templates/reports/board_bringup_log_template.md` |

## Boundaries

- `reference-only` assets point to original files. Read them in place.
- `copied-template` assets are stable templates that may be copied into new work.
- `snapshot` assets are examples for inspection, not authoritative source.
- `derived-template` assets are generic skeletons extracted from repeated MAROC workflows.
- Historical and experimental assets can inform context, but do not use them as default templates.
- Hooked scripts remain in their source repositories. Use the hook registry for risk level, dry-run, and execution logs before running any script.
