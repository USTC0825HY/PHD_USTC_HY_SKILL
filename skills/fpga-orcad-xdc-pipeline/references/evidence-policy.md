# Evidence and safety policy

- OrCAD/PST proves intended connectivity, not electrical operation.
- FPGA package data proves pin/bank capability, not the board rail voltage.
- Schematic power pages prove intended Bank VCCO, not measured voltage.
- RTL proves declared direction and design intent, not pin placement.
- XDC proves requested constraints, not that Vivado applied them to nonempty objects.
- Vivado reports prove the analyzed build only; preserve part, source list, command log, and report paths.
- Board behavior requires a matching bitstream plus JTAG/ILA/instrument evidence.

Never infer timing exceptions, clocks, I/O delays, voltage, or standards from names alone.
