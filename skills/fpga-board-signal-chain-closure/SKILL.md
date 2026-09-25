---
name: fpga-board-signal-chain-closure
description: Trace and close typed signal, clock, return, and power paths across an FPGA controller, a shared base/backplane, and any number of function boards while keeping physical boards, evidence-set versions, connector edges, RTL/XDC, and Vivado evidence separate.
---

# FPGA Multi-board Signal-chain Closure

Use this skill as the topology and evidence-closure layer above `fpga-orcad-xdc-pipeline` and `rtl-schematic-xdc-alignment`. Those skills remain authoritative for PST queries and RTL/XDC/Vivado checks.

## Read first

- Read [references/multi-board-topology.md](references/multi-board-topology.md) when defining boards, evidence sets, graph edges, or power distribution.
- Read [references/chain-schema.md](references/chain-schema.md) before creating a manifest or report.
- Use [assets/signal_chain_report.table.md](assets/signal_chain_report.table.md) for a reusable evidence/conflict/closure report.
- Read the PST signal-tracing reference from `fpga-orcad-xdc-pipeline` and the FPGA control-chain reference from `rtl-schematic-xdc-alignment` before making connectivity claims.

## Model

Represent the system as a typed directed graph, not a fixed three-board chain:

```text
controller board -> shared base/backplane -> zero or more function boards
function board -> shared base/backplane -> another function board
```

Keep physical boards separate from their evidence sets. Select at most one current evidence set per physical board; never merge public/internal or old/new PST, DSN, PDF, or SchDoc sources merely because their names look related.

Allowed edge/chain kinds are `fpga_control`, `status_return`, `board_signal`, `clock_reference`, `power_rail`, and `ground_return`. An edge is only a candidate until connector-to-connector mapping is supported by baseboard PST, a controlled interface definition, explicit schematic pairing, or continuity evidence.

## Workflow

1. Load a v2 board registry or create one from `assets/board_registry.template.json`. Use `assets/signal_chain_manifest.template.yaml` for the richer closure deliverable. Inventory every board, including PDF-only, SchDoc-only, DSN-only, unbound, and alternative evidence sets.
2. For FPGA control or return chains, parse the XPR before trusting top, part, source fileset, constraint set, XDC membership, `UsedIn`, `AutoDisabled`, or `UserDisabled`. `TargetConstrsFile` alone is not authority.
3. Query each selected PST independently using exact `NET_NAME` and `NODE_NAME <refdes> <pin>`. Preserve source lines and both sides of every resistor, jumper, translator, buffer, switch, or isolator.
4. Store each path as ordered `chains[].segments[]`. Keep connector contacts, FPGA balls, device pins, and nets as distinct fields. Do not infer a cross-board edge from equal pin numbers, similar net names, device suffixes, or logical group numbers.
5. For every translator, record channel/A-B pins, supply domains, DIR, OE/OE*, pull state, assembly resistors, and fitted state. A D120-like OE-disabled branch is `硬件禁用/电气不可用` even when a reachable FPGA ball and XDC entry exist.
6. For `power_rail` and `ground_return`, record source rail, voltage/domain, source connector, fuse/protection, switch, filter, baseboard entry/exit, load connector, return ground, and assembly state. RTL/XDC is `不适用` unless a separate enable or status signal exists; model that signal as its own control or return chain.
7. Use PDF only for device-side pin/function, page/zone, and visual intent. Use PST for actual net membership. Identify fixed pull-up/down, NC, DNP, and TSD*; stop electrical-availability claims at disabled or unpopulated branches.
8. Compare FPGA chains with RTL direction, active XDC PACKAGE_PIN/IOSTANDARD, and read-only Vivado `report_io` when a current synthesis run already exists. Never launch synthesis or implementation implicitly.

## Evidence and outputs

Use evidence levels E0-E4 defined in `references/chain-schema.md`. Report board-local proof, cross-board definition, physical continuity, and FPGA implementation as separate layers.

Required outputs are:

- physical board registry and selected/alternative evidence sets;
- graph edges and ordered chain segments;
- conflicts, unclosed points, disabled/DNP/TSD*/NC branches, and required physical checks;
- XPR/XDC/Vivado evidence only for FPGA-related chains.

Keep generated artifacts in staging. Do not edit user XPR, XDC, RTL, PST, DSN, PDF, SchDoc, or hardware data during an audit.

## Preflight script

Preferred v2 invocation:

```powershell
python scripts/audit_chain_inputs.py `
  --boards-file C:\staging\board_registry.json `
  --xpr C:\fpga\project.xpr `
  --xdc C:\fpga\top.xdc `
  --fpga-refdes D1 `
  --query-net CONTROL_EN `
  --output C:\staging\chain_preflight.json
```

Add or override an ad-hoc PST board with repeated `--board ID=PATH`. The legacy `--szsd-pst-dir`, `--backplane-pst-dir`, and `--child-pst-dir` interface remains supported when all three are supplied.

The script inventories boards and validates declared topology; it never joins board segments automatically.
