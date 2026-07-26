---
name: maroc-fpga-register-command-parser
description: "MAROC adapter for FPGA register-map and command-parser workflow. Use for MAROC 829bit slow-control fields, raw_104B, legacy_104B, packet_250B, FE/EE framing, AA20/direct commands, parser state machines, command_MAROC compatibility, register_mapping.txt, and host/RTL protocol alignment. Use fpga-register-command-parser for the generic method."
---

# MAROC FPGA Register Map And Command Parser

## Workflow

1. Apply the generic `fpga-register-command-parser` workflow first.
2. Establish the MAROC truth layer: datasheet field, Qt host field, `bits_829`, `register_mapping`, raw 104B, packet 250B, parser output, or legacy command word.
3. Trace one MAROC field or command end-to-end before generalizing.
4. Keep `bits_829/register_mapping` as ASIC slow-control intent and `packet_250` as transport/parser framing.
5. Keep `command_MAROC` legacy/manual path separate from the formal packet parser unless the task bridges them.

## Handoffs

Use `maroc-host-rtl-alignment` for Qt export replay and `maroc-fpga-testbench-simulation` for parser simulation proof.

## Asset Library

- Read `C:/Users/Administrator/.codex/skills/maroc-hardware-dev-router/references/maroc-asset-map.md` for MAROC register, command, packet, and fixture routing.
- Use `C:/Users/Administrator/.codex/hardware-assets/source-refs/maroc-rtl-assets.md` and `source-refs/maroc-qt-host-assets.md` to cross-locate parser RTL, fixture files, Qt exporters, and payload transforms.
- Use `C:/Users/Administrator/.codex/hardware-assets/templates/reports/host_rtl_alignment_table.md` when documenting field-to-packet-to-parser alignment.
