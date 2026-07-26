# MAROC Evidence Boundaries

Use these boundaries whenever a task makes a technical claim.

## Evidence Classes

- Datasheet/User Guide: defines intended chip behavior, pin semantics, register fields, and timing requirements. It does not prove the local board or RTL implements them.
- Schematic/PCB evidence: proves intended board connectivity, reference design choices, component values, and probe points. It does not prove a signal toggled.
- Host truth: `register_mapping.txt`, `bits_829.txt`, and Qt export bundles prove what the software intends to send. `packet_250.hex` proves USB/parser packet framing, not ASIC 829bit truth.
- RTL truth: current source and committed diffs prove implemented behavior. Historical notes are secondary when they disagree with source.
- Testbench/XSim: proves behavior inside the simulated DUT, fixture, and mocked environment. It does not prove board bring-up.
- ILA evidence: proves internal FPGA signal activity for the programmed bit/ltx and capture condition. It cannot directly prove analog `OUT_Q` or `OUT_FS` behavior.
- Board-level evidence: power/current, USB/JTAG status, ILA captures, oscilloscope traces, and host logs prove a board state only for the tested setup.
- Chip-behavior evidence: requires aligned configuration, trigger/control chain, analog/probe or ADC/readout observation, and explicit A/B comparison where relevant.

## Required Claim Language

- Configuration-chain success: use only after `Host -> USB -> FIFO/CDC -> parser -> SlowControl -> SC pins` is covered by simulation or ILA evidence.
- ADC/upload success: require `OR/trigger -> Hold/start_ADC/RST_ADC -> TransmitOn -> Out_ADC -> data_socket/frame -> USB readout` evidence.
- Ctest/analog claims: require Ctest field confirmation plus analog probe or ADC A/B comparison; current increase alone is supporting evidence.
- XDC/schematic alignment: require RTL port name, XDC pin, schematic net, board connector/component, voltage standard, and clock/timing role.
- PPT/Markdown summary: preserve evidence path, date, repo commit/bit/ltx when available, and explicit “cannot prove” boundary.
