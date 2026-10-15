# PST signal tracing

## Evidence sources

- Use `pstxnet.dat` for exact network membership: `NET_NAME` followed by `NODE_NAME <refdes> <pin>`.
- Use `pstxprt.dat` to bind a concrete reference designator to its part name and hierarchy.
- Use `pstchip.dat` to resolve the primitive `VALUE` and assembly markers.
- Use the PDF for page, zone, visual intent, and signal semantics. Do not claim a PDF page from PST alone.
- Treat binary DSN as a source artifact. Export PST natively from OrCAD; do not parse DSN as text.

## Required procedure

1. Run `inventory` and select one version-consistent evidence set. Record relative path, timestamp, SHA-256, PSTWRITER header, and missing files.
2. Start from an exact network or `refdes.pin`. Exact network matching is the default; enable regex only for deliberate discovery.
3. Record every node on the returned net. Do not delete apparently irrelevant nodes before reviewing loading, pulls, test points, and branches.
4. At a series resistor, jumper, translator, buffer, or isolator, query the component's other pin separately. The nets on its two pins remain separate graph edges.
5. At a connector, record board, connector, pin, net, and source line. Stop the confirmed path at the board boundary.
6. Continue on a backplane or next board only when a PST net, controlled interface table, explicit schematic pairing, or continuity record supplies the connector mapping.
7. Resolve every traversed component through `pstxprt.dat` and `pstchip.dat`. Preserve TSD/DNP markers separately from current population. PST output reports `fitted_state=unknown`; the closure record may supply a version/refdes-scoped assembly confirmation. No marker also does not prove physical population.
8. Verify function, polarity, direction, and timing from the device datasheet. Net names are not datasheet evidence.

## Cross-board output

Separate results into:

- `原理图/PST 已确认`: individual board nets, nodes, components, and connector pins explicitly present in PST.
- `网络链路推断`: cross-board pairing supported only by naming, equal pin numbers, mechanical expectation, or incomplete interface evidence.
- `待实物/线缆导通确认`: actual slot, orientation, cable, fitted option, and continuity.
- `资料不完整，无法继续`: a required connection has no usable evidence. Missing PST alone blocks PST queries, not inspection of explicit selected-schematic connections.

Never merge boards automatically. `multi-query` groups independent board results; it does not assert that those results form a continuous electrical path.

## PDF-only child-board connector tracing

Use this procedure when the child board has a readable schematic PDF but no selected, version-consistent PST export.

1. Extract the child-board connector with spatial coordinates. For rotated connector drawings, pair each signal label with the nearest explicit connector pin number; do not trust plain PDF text order.
2. Preserve separate columns for parent-board connector/pin and child-board connector/pin. Mating connectors can be mirrored or renumbered, so equal pin numbers are not continuity evidence.
3. Pair the parent PST edge to the child PDF edge through explicit interface definitions or schematic mating evidence. This can establish a design pairing without proving physical continuity; matching signal labels alone remains inference. A child PST alone does not prove cable mapping. Keep each evidence dimension separate per the shared closure method.
4. Continue from the child connector to the device pin through every series resistor, 0-ohm link, level translator, buffer, switch, and strap. Record reference designator, pin, value, population marker, and both adjacent net names.
5. For each level translator, record A/B channel, DIR net and pull state, OE/OE* net and pull state, supply domains, and whether the channel is actually enabled. A reachable FPGA ball is not a controllable output when OE disables the channel or DIR points the wrong way.
6. Classify each child-board pin as FPGA-driven control, FPGA input/status, hardware strap, fixed rail/GND, shared/variant-only, or unconnected. Do not add straps, returns, or disabled paths to XDC as outputs.
7. Compare the traced chain with the active RTL top and active XDC. Report `已驱动`, `缺少RTL/XDC`, `硬件禁用`, `方向冲突`, or `待装配/实物确认` separately.
8. For spreadsheet-style delivery, include at least: function, child connector pin, child device/refdes.pin, parent connector pin, parent net, intermediate components, translator channel/DIR/OE, FPGA net, FPGA ball, RTL port, XDC state, evidence class, source path/line or PDF page, and residual risk.
