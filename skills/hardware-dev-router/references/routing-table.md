# Generic Hardware Skill Routing Table

Prefer the most specific leaf skill. Use `hardware-dev-router` when the request spans domains or the user is unsure where to start.

| Request pattern | Use skill |
|---|---|
| Review Verilog/VHDL/SystemVerilog logic, module boundaries, state machines, handshakes, muxing, debug nets | `fpga-rtl-code-review` |
| Write/run/debug testbenches, XSim/Questa/iverilog flows, fixtures, replay logs, simulation reports | `fpga-testbench-simulation` |
| Plan or interpret Vivado ILA/VIO/on-chip captures, triggers, bit/ltx matching, CSV export | `fpga-ila-debug` |
| Review CDC, reset release, async FIFO, clock constraints, timing reports, generated clocks | `fpga-cdc-reset-timing` |
| Analyze register maps, command parsers, packet framing, byte order, field ownership | `fpga-register-command-parser` |
| Build or audit Vivado Tcl/PowerShell automation, IP generation, bitstreams, simsets, XDC load order | `fpga-vivado-tcl-automation` |
| Review Qt/C++ host architecture, workers, device backends, fake tests, CMake/CTest | `qt-cpp-host-development` |
| Align host-generated exports or packets with RTL fixtures, parsers, and testbenches | `host-rtl-alignment` |
| Align FPGA RTL ports, XDC constraints, schematic nets, connectors, and board observations | `rtl-schematic-xdc-alignment` |
| Review schematic pages and board-level intent | `hardware-schematic-review` |
| Translate datasheet requirements into schematic checks | `hardware-datasheet-to-schematic` |
| Bring up or debug a PCB with instruments, power, clocks, JTAG/USB, FPGA smoke, or lab evidence | `hardware-pcb-bringup-debug` |
| Convert RTL/sim/ILA/scope/log/schematic evidence into report, PPT, or Markdown claims | `hardware-evidence-report-sync` |
| MAROC-specific packet, register, RTL, board, Obsidian, or PPT work | the corresponding `maroc-*` adapter skill |
