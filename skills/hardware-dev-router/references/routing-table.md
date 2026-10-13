# Generic Hardware Skill Routing Table

Prefer the most specific leaf skill. Use `hardware-dev-router` when the request spans domains or the user is unsure where to start.

| Request pattern | Use skill |
|---|---|
| Write, adapt or simplify hand-written RTL while preserving cycle-level interfaces | `fpga-rtl-development`; review-only stays with `fpga-rtl-code-review` |
| Create a native GUI-style project with functional RTL folders | `fpga-vivado-tcl-automation`; existing projects are not automatically migrated |
| Map existing RTL / plan new RTL / visualize an existing map | `gf-architect` / `gf-plan` / `gf-viz` respectively |
| Choose synthesis / implementation strategy / interpret QoR / edit constraints | `vivado-synth` / `vivado-impl` / `vivado-analysis` / `vivado-constraints`; execution uses `fpga-vivado-tcl-automation` |
| Extract exact PST nets / close multi-board topology | `fpga-orcad-xdc-pipeline` / `fpga-board-signal-chain-closure` |
| Develop or diagnose linearity_automation Tk GUI, service sessions, workers or packaging | `cw-dac-host-development` |
| Operate the project's joint SDG/ILA capture workflow | `fpga-substitute-board-workflow-validation` |
| Develop SCPI drivers or independent source/DMM measurements | `sdg-dmm-automation` |
| 513/CW project paths, board evidence and project-specific implementation limits | `laser-cw-qualification-test-development` |
| Calculate Laser measured results / write reports / write operator manuals | `laser-electrical-data-analysis` / `laser-test-report-writing` / `laser-cw-operation-manual-writing` |
| Apply an explicitly selected formal report template | `laser-electrical-test-report-standard` with the report-content skill |
| Laser notes / schematic screenshot repair / approved Visio layouts | `laser-pdh-obsidian-md-writing` / `laser-schematic-screenshot-repair` / `laser-indicator-visio-style` |
| Review Verilog/VHDL/SystemVerilog logic, module boundaries, state machines, handshakes, muxing, debug nets | `fpga-rtl-code-review` |
| Write/run/debug testbenches, XSim/Questa/iverilog flows, fixtures, replay logs, simulation reports | `fpga-testbench-simulation` |
| Plan or interpret Vivado ILA/VIO/on-chip captures, triggers, bit/ltx matching, CSV export | `fpga-ila-debug` |
| Review CDC, reset release, async FIFO, clock constraints, timing reports, generated clocks | `fpga-cdc-reset-timing` |
| Analyze register maps, command parsers, packet framing, byte order, field ownership | `fpga-register-command-parser` |
| Build or audit Vivado Tcl/PowerShell automation, IP generation, bitstreams, simsets, XDC load order | `fpga-vivado-tcl-automation` |
| Align host exports, binary packets, CSV/JSON/hex fixtures, parser/TB inputs, replay, and checkers | `host-rtl-alignment` |
| Build or review generic Qt/C++ host applications, device clients, workers, fake backends, and CTest | `qt-cpp-host-development` |
| Align FPGA RTL ports, XDC constraints, schematic nets, connectors, and board observations | `rtl-schematic-xdc-alignment` |
| Review schematic pages and board-level intent | `hardware-schematic-review` |
| Translate datasheet requirements into schematic checks | `hardware-datasheet-to-schematic` |
| Bring up or debug a PCB with instruments, power, clocks, JTAG/USB, FPGA smoke, or lab evidence | `hardware-pcb-bringup-debug` |
| Convert RTL/sim/ILA/scope/log/schematic evidence into report, PPT, or Markdown claims | `hardware-evidence-report-sync` |
| Work on MAROC-specific paths, 829-bit maps, packet formats, board names, Qt host, RTL/XDC, notes, or PPT | Start with `maroc-hardware-dev-router`, then use its focused `maroc-*` adapter |
