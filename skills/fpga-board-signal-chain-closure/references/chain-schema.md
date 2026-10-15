# Multi-board chain schema v2

## Top-level sections

| Section | Meaning |
|---|---|
| `boards[]` | Physical boards or explicit unbound load placeholders. |
| `evidence_sets[]` | Versioned PST/DSN/PDF/SchDoc evidence belonging to one physical board. |
| `edges[]` | Directed board-to-board candidate edges. |
| `chains[]` | End-to-end functions expressed as ordered `segments[]` or a declared board path. |
| `conflicts[]` | Contradictory source claims. |
| `unclosed_points[]` | Missing connector, board-local, assembly, or implementation evidence. |
| `physical_checks[]` | Required continuity, orientation, population, or voltage checks. |

Each board has a stable `id`, human name, role, and zero or more evidence sets. Exactly zero or one evidence set may be selected. Multiple selected versions are an error; no selected version is E0.

## Edge and chain types

Use only:

- `fpga_control`: FPGA-driven control; requires RTL output plus active XDC and FPGA-ball evidence.
- `status_return`: board-to-FPGA return; requires RTL input plus active XDC and FPGA-ball evidence.
- `board_signal`: signal between non-FPGA boards or where FPGA ownership is not established.
- `clock_reference`: clock/reference distribution; record source, destination, frequency if proven, conditioning, and return/shield.
- `power_rail`: powered source-to-load path; RTL/XDC is not required.
- `ground_return`: return/ground path associated with power or sensitive signals.

## Ordered segments

Each `chains[].segments[]` item represents one board-local portion or one cross-board boundary and records as applicable:

| Field | Required content |
|---|---|
| `board_id` | Physical board owning this segment. |
| `from` / `to` | Exact device, connector, rail, or logical endpoint. |
| `net` | Exact selected-source net name; record whether from PST or legible schematic. Unnamed/uncertain nodes remain explicit, without invented PST IDs. |
| `connector_pin` | Connector refdes/contact, distinct from FPGA package ball. |
| `components[]` | Refdes.pin, value, channel, and adjacent nets for every traversed component. |
| `translator` | A/B channel, supply domains, DIR, OE/OE*, and effective state. |
| `assembly` | Legacy text remains readable; new records separate marker, current state, board version and scoped confirmation. |
| `evidence_level` | E0-E4 and source path/line or page. |
| `status` | `板内已确认`, `跨板待确认`, `硬件禁用`, `方向冲突`, `缺少RTL/XDC`, or `资料不完整，无法继续`. |

FPGA chains additionally record RTL port/direction/owner, active XDC file/line, PACKAGE_PIN, IOSTANDARD, FPGA refdes/ball, and Vivado status.

Power chains additionally record rail name, nominal voltage, current/rating if proven, source/load connector pins, fuse/protection, switch, filter, return ground, and assembly state. Set RTL/XDC fields to `不适用`; create separate `fpga_control` or `status_return` chains for power enable, power-good, fault, or telemetry signals.

## Evidence levels

Optional additive v2 fields: `trace_direction`, `signal_direction`, connector section/contact/view, and `verification` dimensions (`board_local`, `connector_mapping`, `assembly`, `continuity`, `rtl_xdc`, `implementation`, `measurement`). Each dimension stores status and evidence independently. Existing v2 records and E0—E4 remain supported; absent fields are unknown, not implicitly passed. Source marker does not itself confirm physical population.

- `E0 输入不完整`: board binding, selected evidence set, or required source is missing.
- `E1 原理图/PST 已确认`: a board-local node/net/component/contact is explicit in the selected evidence.
- `E2 跨板映射已定义`: connector pairing is defined but physical continuity is not measured.
- `E3 实物/线缆已确认`: continuity, orientation, or fitted option is independently recorded.
- `E4 FPGA实现已复核`: applicable E1-E3 evidence plus aligned RTL/XDC and reviewed Vivado report_io/current synthesis state.

Do not assign E2 from matching names or numbers, E3 from PST, or E4 to a power-only chain. Use `RTL/XDC静态核查完成，Vivado应用状态未复核` when no current Vivado run was reviewed.

## v1 compatibility

Normalize legacy `SZSD/backplane/child` inputs to physical board IDs `SZSD`, `BASE`, and `CHILD_LEGACY`, then emit schema v2. Do not interpret `CHILD_LEGACY` as a specific function board until the caller supplies its identity.
