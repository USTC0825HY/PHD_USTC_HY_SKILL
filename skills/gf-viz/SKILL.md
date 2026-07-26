---
name: gf-viz
description: Visualize FPGA RTL architecture maps produced by gf-architect. Use when Codex needs to show module hierarchy, module details, FSMs, clock/reset domains, CDC candidates, unresolved IP, signal paths, or structural changes as concise Markdown, ASCII, Mermaid, or tables.
---

# FPGA Architecture Visualization

Read `.fpga-map/rtl_hierarchy.json` first. Fall back to `.fpga-map/*.md`, then legacy `.gateflow/map/` files.

## Views

- Overview: counts for modules, top modules, instances, clocks, resets, CDC candidates, unresolved modules, and warnings.
- Hierarchy: full tree plus parent/instance/module/parameter table.
- Module detail: source location, parameters, ports, child instances, clocks, resets, and parents.
- Clock/reset: group modules by clock and reset; distinguish evidence from naming inference.
- CDC: source, destination, signal, synchronizer evidence, status, and follow-up.
- Diff: added, removed, or structurally changed modules when two JSON maps are supplied.

## Rendering rules

1. Prefer Mermaid for a reusable document and compact ASCII for a terminal response.
2. Limit overview diagrams to two levels; provide focused subtrees for deeper designs.
3. Use stable node IDs and escape brackets, spaces, and punctuation in labels.
4. Never invent connections absent from the map or source.
5. Show missing data as `not detected` or `not supplied`, not as an empty success.
6. Link each nontrivial finding to its source file and line when available.

Read `references/upstream-provenance.md` when auditing or updating this adapted skill.
