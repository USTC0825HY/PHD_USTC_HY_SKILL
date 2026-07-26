# MAROC Application Routing Table

This table maps generic hardware skill categories to MAROC project adapters. Use `hardware-dev-router/references/routing-table.md` for the generic architecture first.

| Generic category | MAROC request pattern | Use MAROC adapter |
|---|---|---|
| `fpga-rtl-code-review` | Review MAROC Verilog logic, module responsibilities, unsafe state machines, config-chain RTL | `maroc-fpga-rtl-code-review` |
| `fpga-testbench-simulation` | Run/write/debug MAROC XSim, TB, fixtures, case matrix, simulation report inputs | `maroc-fpga-testbench-simulation` |
| `fpga-ila-debug` | Program/inspect MAROC ILA, Hardware Manager Tcl, CSV export, trigger presets, bit/ltx evidence | `maroc-fpga-ila-debug` |
| `fpga-cdc-reset-timing` | MAROC clock domains, reset sequencing, timing reports, XDC clocks, async FIFO, smoke timing | `maroc-fpga-cdc-reset-timing` |
| `fpga-register-command-parser` | MAROC 829bit/raw_104B/packet_250B, parser, command words, register map, AA20/direct command | `maroc-fpga-register-command-parser` |
| `fpga-vivado-tcl-automation` | MAROC Vivado project recreation, Tcl/PS1 build entry, IP generation, bitstream automation | `maroc-fpga-vivado-tcl-automation` |
| `qt-cpp-host-development` | QT_MUON, CyAPI, MAROC packet export, GUI automation, host CTest | `maroc-qt-host-development` |
| `host-rtl-alignment` | MAROC host export bundle must replay in RTL simulation | `maroc-host-rtl-alignment` |
| `rtl-schematic-xdc-alignment` | MAROC RTL ports must match schematic/XDC/board connector | `maroc-rtl-schematic-xdc-alignment` |
| `hardware-schematic-review` | MAROC/FEE schematic audit | `hardware-schematic-review` plus `maroc-rtl-schematic-xdc-alignment` when FPGA ports matter |
| `hardware-datasheet-to-schematic` | MAROC3A, ADC, DAC, USB, clock, regulator datasheet-to-schematic checks | `hardware-datasheet-to-schematic` |
| `hardware-pcb-bringup-debug` | MAROC board power, clocks, USB/JTAG, first smoke tests, ILA/lab evidence | `hardware-pcb-bringup-debug` |
| `hardware-evidence-report-sync` | Sync MAROC RTL/ILA/Obsidian/lab evidence to slides | `maroc-evidence-ppt-sync` |
| Documentation | Create or govern MAROC Obsidian Markdown notes | `maroc-obsidian-md-writing` |
| PPT scene | Debug-problem, progress-summary, or group-meeting MAROC PPT | `maroc-ppt-debug-report`, `maroc-ppt-progress-summary`, or `maroc-ppt-group-meeting` |
