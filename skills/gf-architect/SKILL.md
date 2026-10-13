---
name: gf-architect
description: Map and document Verilog/SystemVerilog repositories. Use when Codex needs to explain FPGA code hierarchy, module ownership, parameters, ports, instances, signal flow, FSMs, clocks, resets, CDC, unresolved modules, Vivado IP, compile order, or top-level RTL/XDC alignment.
---

# FPGA RTL Architect

Create an evidence-backed repository map. Work directly in the current repository; use parallel agents only when the user explicitly requests delegation and the active policy allows it.

## Workflow

1. Locate RTL, headers, filelists, Vivado project/Tcl files, IP metadata, XDC, and existing maps with `rg --files` or PowerShell.
2. Determine the configured top from project/Tcl/filelist evidence. If several tops remain plausible, map all and label the ambiguity.
3. For a full map, prefer `scripts/rtl_hierarchy_scan.py <repo> --project <selected.xpr>` or `--filelist <literal-list> --top <module>`. Default output is JSON on stdout, with no project writes. Directory-only scanning is a file inventory, not active-project authority. Read [scanner contract](references/scanner-contract.md) when running or consuming the scanner.
4. Inspect source around uncertain declarations, parameterized instances, generate blocks, macros, interfaces, FSMs, clocks, and resets. Preserve file and line evidence.
5. Select the tool version from the explicit target, nearest project rules and current XPR; use the shared profile only as a fallback. Cross-check with existing matching elaboration/synthesis evidence; run a new stage only when the task authorizes it. Report a tool/project mismatch instead of upgrading the project. Keep tool-generated and source-inferred facts separate.
6. Use `rtl-schematic-xdc-alignment` when a top-level XDC or schematic pin map is in scope.
7. Report unresolved modules as vendor IP, encrypted/black-box IP, missing source, simulation-only code, or probable parser limitation. Never silently drop them.

## Task-scaled outputs

For one-module explanations, inspect that module and necessary callers directly; do not generate the following bundle. For requested repository maps, pass `--output <explicit-directory>` to write the full bundle below. Respect no-write requests and workspace temporary-directory rules; `.fpga-map` is an option, not an implicit write destination.

- `rtl_hierarchy.md`: module tree, module/file index, instances, parameters, ports, and evidence.
- `rtl_hierarchy.json`: machine-readable modules, ports, instances, clocks, resets, and unresolved references.
- `rtl_hierarchy.mmd`: Mermaid hierarchy graph.
- `clock_reset_map.md`: clocks, derived clocks, reset polarity/style, and module scope.
- `cdc_inventory.md`: candidate crossings and synchronization evidence; label static-only conclusions as candidates.
- `top_xdc_alignment.md`: top ports versus XDC objects, or an explicit “XDC not supplied” boundary.
- `unresolved_modules.md`: missing/black-box/IP/unused design units and reasons.

## Evidence rules

- Source parsing proves text-level structure, not the final elaborated hierarchy.
- Vivado elaboration proves the selected parameters, macros, generate choices, and compile order for that run.
- A clock-like name is only a candidate until sensitivity lists, primitives, or timing constraints support it.
- A CDC claim requires source domain, destination domain, signal, and synchronization structure; otherwise mark it `needs_review`.
- Do not edit RTL while mapping unless the user separately requests implementation.

## Windows commands

```powershell
rg --files -g '*.v' -g '*.sv' -g '*.vh' -g '*.svh' -g '*.xdc' -g '*.tcl'
python scripts/rtl_hierarchy_scan.py C:\path\to\repo --output C:\path\to\repo\.fpga-map
```

Read `references/upstream-provenance.md` when auditing or updating this adapted skill.
