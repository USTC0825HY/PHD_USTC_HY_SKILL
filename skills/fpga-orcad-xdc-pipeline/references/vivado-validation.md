# Vivado 2022.2 validation

Use the actual part and source order. Start in a staging directory.

```tcl
read_verilog -sv <ordered RTL files>
read_xdc pins.xdc
synth_design -rtl -top <top> -part <part>
report_io -file report_io.rpt
report_drc -file report_drc.rpt
check_timing -file check_timing.rpt
report_clock_interaction -file clock_interaction.rpt
```

After synthesis, run `report_cdc` when multiple clocks exist. A successful Tcl parse is insufficient: check that every `get_ports` query matched exactly one intended object and review critical warnings.
