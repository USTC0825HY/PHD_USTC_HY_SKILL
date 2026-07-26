# Generic Hardware Evidence Boundaries

Use these boundaries whenever a task makes a technical claim.

## Evidence Classes

- Datasheet or user guide: defines intended device behavior, pin semantics, register fields, limits, and timing. It does not prove the local board or RTL implements them.
- Schematic or PCB evidence: proves intended connectivity, component values, reference circuits, and probe points. It does not prove a signal toggled.
- Host-software evidence: proves what the host intended to send or observed on its transport interface. It does not prove downstream FPGA, board, or chip behavior.
- RTL evidence: current source and diffs prove implemented logic. It does not prove physical board behavior.
- Simulation evidence: proves behavior inside a DUT, fixture, and modeled environment. It does not prove board bring-up, CDC in hardware, or analog behavior.
- On-chip debug evidence: ILA/VIO/SignalTap captures prove internal FPGA activity for the programmed image and trigger condition. They do not directly prove external analog waveforms.
- Board-level evidence: power/current, JTAG/USB enumeration, ILA captures, oscilloscope traces, logic analyzer traces, and host logs prove a tested board state under the recorded setup.
- Device/chip-behavior evidence: requires aligned configuration, control/trigger path, measured device output or readout, and explicit A/B comparison where relevant.

## Required Claim Language

- Configuration-chain success requires host intent, transport, parser/bridge, serializer/register write, and pin/internal-state evidence.
- Acquisition or readout success requires trigger/control, capture/readout, framing, transport, and host-side receive evidence.
- Analog claims require oscilloscope or ADC/readout evidence tied to the same configuration and test condition.
- Constraint/schematic alignment requires RTL port, constraint pin, schematic net, board connector/component, voltage standard, and clock/timing role.
- Reports and slides must preserve evidence path, date, repo/build/bitstream version when available, observed fact, allowed conclusion, and remaining boundary.
