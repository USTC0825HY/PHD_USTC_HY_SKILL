---
name: gf-viz
description: Visualize FPGA RTL architecture maps produced by gf-architect. Use when Codex needs to show module hierarchy, module details, FSMs, clock/reset domains, CDC candidates, unresolved IP, signal paths, or structural changes as concise Markdown, ASCII, Mermaid, or tables.
---

# FPGA Architecture Visualization

Read the supplied map first, otherwise `.fpga-map/rtl_hierarchy.json`; fall back to Markdown/legacy maps only as historical context. Check selected project/top, current input membership and hashes before calling a map current. For scanner schema/limits see [scanner contract](../gf-architect/references/scanner-contract.md). Missing provenance means freshness unverified, not an automatic full rescan or write.

## Views

- Overview: counts for modules, top modules, instances, clocks, resets, CDC candidates, unresolved modules, and warnings.
- Hierarchy: the requested subtree or compact overview; full tree only when useful/requested.
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
