# fpga_io_map schema

The file is JSON-compatible YAML for deterministic parsing.

## Root

- `schema_version`: must be `1`.
- `source`: schematic and native netlist provenance.
- `fpga`: `refdes`, exact `part`, `cfgbvs`, and `config_voltage`.
- `ports`: one row per used FPGA package pin.
- `timing`: documentation only; active timing constraints are never emitted.

## Port row

- Identity: `net_name`, `fpga_pin`, `rtl_port`, `direction`.
- Electrical: `bank`, numeric `bank_vcco`, `iostandard`, optional `drive`, `slew`, `pulltype`.
- Intent: `role` such as `clock`, `reset`, `data`, `control`, or `debug`.
- Evidence: `component`, `schematic_page` or `source_ref`, and optional `datasheet`.
- Governance: `status` is `verified`, `needs_review`, or `waived`; waived rows require `waiver_reason`.

Only verified rows enter `pins.xdc`. Any needs-review row blocks generation.
