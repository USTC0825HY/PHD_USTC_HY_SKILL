# Multi-board topology and closure rules

## Physical boards versus evidence sets

A physical board is a graph node. A DSN/PDF/PST/SchDoc directory is an evidence set for that node, not automatically a separate board. Record public, internal, historical, and alternate exports separately and select at most one current set before tracing.

Boards without PST remain visible as E0 nodes. PDF may support device pin/function and visual intent; SchDoc/PcbDoc may establish source availability; neither establishes exact PST net membership.

## Graph construction

Declare directed edges and end-to-end chains before querying signals. A chain path such as `A -> BASE -> B` creates candidate topology only. Close each boundary independently:

```text
A connector contact | BASE input/contact/net/output | B connector contact
```

Acceptable closure sources are selected-board PST, controlled connector maps, explicit schematic mating definitions, and continuity records. Similar net names and equal contact numbers remain `网络链路推断`.

Multiple chains may traverse the same physical boards with different edge types. Keep a control signal, status return, clock, power rail, and ground return separate even when they use the same connectors.

## Power distribution

Trace power from source to each load as a separate branch. Record rail/domain, nominal voltage, current/rating only when evidenced, return ground, connectors, fuses, protection, switching, filters, straps, assembly state, and unclosed points. A source board being connected to the baseboard does not prove every load branch is powered.

Do not require RTL/XDC for `power_rail` or `ground_return`. If FPGA or another controller drives enable, reset, sequencing, or monitor signals, trace those as separate `fpga_control` or `status_return` chains and correlate them to the power branch by ID.

## Electrical availability

Physical reachability and electrical availability are separate. Mark a path unavailable when OE disables a translator, DIR opposes the required direction, a switch is open by fixed state, a fuse/link is absent, or a traversed part is DNP/TSD*/NC. Record fixed pull-up/down and assembly-option resistors explicitly.

A branch such as D120 whose OE state holds the channel disabled is `硬件禁用/电气不可用`; do not downgrade it to `可选功能`, and do not claim usability from an FPGA ball or XDC LOC alone.

## Functional classification

Classify each completed or candidate chain as exactly one of:

- `必需控制`: software/RTL must actively drive it for the required function;
- `硬件默认`: fixed pull, strap, or power-on state supplies the required behavior without FPGA action;
- `可选功能`: intentionally unused capability that remains electrically available;
- `状态输出`: device/board-to-controller observation, fault, ready, or telemetry path.

Do not use `可选功能` for NC, DNP, TSD*, open, wrong-direction, or OE-disabled paths.

## Deliverable ordering

Report in this order:

1. board/evidence registry and selected versions;
2. declared graph and priority chains;
3. board-local PST evidence;
4. cross-board closure evidence;
5. electrical-availability analysis;
6. RTL/XDC/Vivado alignment where applicable;
7. conflicts, unclosed points, and physical checks.
