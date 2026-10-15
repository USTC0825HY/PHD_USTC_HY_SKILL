# FPGA control-signal chain

## Lock authority

Read the active XPR before trusting a top, part, source set, constraint set, or XDC. Reject `AutoDisabled` sources and commented or historical XDC as current evidence.

## Static alignment

For each scalar or bus bit, record:

| RTL port | direction | module owner | active XDC expression | PACKAGE_PIN | IOSTANDARD | FPGA refdes/ball | PST network |
|---|---|---|---|---|---|---|---|

Run `scripts/run_rtl_xdc_pst_audit.ps1` with the authoritative top RTL, XDC, SZSD `pstxnet.dat`, and FPGA reference designator. Resolve buses bit by bit. Treat these as errors:

- constrained port absent from the top or bus index outside its declared width;
- duplicate active property on a scalar port;
- duplicate PACKAGE_PIN ownership;
- missing PACKAGE_PIN or fabric IOSTANDARD; dedicated MGT pads require reviewed package-pin evidence rather than an invented fabric standard;
- XDC ball absent from the FPGA `NODE_NAME` records in PST.

Do not require the RTL port name to equal the PST net. Record the explicit mapping instead.

Check complete coverage or explicitly declare a selected-interface scope. Dictionary and separate-property syntax are both supported; dynamic/scoped commands, unresolved parameter widths and zero parsed pin records cannot establish success. Static text order is not proof of Vivado application order.

## On-board control target

Trace:

`RTL port → XDC ball → FPGA PST node → conditioning/translator → target-device pin`.

Query both pins of every series component. Confirm signal direction from RTL and device datasheets; confirm polarity and timing from datasheets, not net names.

## Cross-board control target

Trace and report each board segment independently:

`SZSD FPGA → SZSD conditioning → SZSD connector | backplane input → backplane output | child connector → child conditioning → device`.

Join connector boundaries only with explicit backplane PST, a controlled connector mapping, schematic pairing, or continuity evidence. An equal pin number or similar net name is only `网络链路推断`.

Trace return/status signals in the reverse direction and verify that the RTL direction is input.

The tracing order and electrical direction are separate: receiver-to-source lookup does not reverse RTL direction or translator DIR. Keep actual node ownership, original TSD/DNP markers and scoped population confirmations in the common closure record. NC/disabled paths cannot become controllable merely because RTL/XDC matches. Analog telemetry up to its ADC input does not require a fabricated FPGA port; any ADC digital control/readout is a separate FPGA chain.

## Vivado read-only review

After static checks pass, use `scripts/vivado_io_audit.tcl` when a complete, non-stale selected run exists. It opens the project read-only, checks each requested `get_ports` pattern, applied PACKAGE_PIN/IOSTANDARD, duplicate pins, bank, and writes `report_io.rpt` to a new explicit report directory. NEEDS_REFRESH=false is tool-reported freshness, not proof of historical source hashes.

Do not launch synthesis automatically. If the current synthesis run is absent or incomplete, report exactly: `RTL/XDC静态核查完成，Vivado应用状态未复核`.
