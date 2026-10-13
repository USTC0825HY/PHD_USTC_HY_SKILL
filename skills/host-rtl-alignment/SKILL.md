---
name: host-rtl-alignment
description: "Align host settings, packet/fixture exports or VIO/JTAG commands with RTL consumers and readback. Use for byte/field mismatches, parser replay, probe contracts and host-to-FPGA control evidence."
---

# Host RTL Alignment

## Workflow

1. Identify the host artifact: GUI setting, config object, register map, command builder, raw payload, transport packet, fixture, or replay bundle.
2. Identify the RTL consumer: parser, bus adapter, register file, serializer, memory loader, testbench, or checker.
3. Select the transport: for packets/fixtures, trace host model, export, transforms, framing, RTL parser and checker. For VIO/JTAG, trace host value/unit, Tcl request, exact CELL_NAME/probe direction/width, matched BIT/LTX, RTL consumer and internal readback. Packet framing and parser fixtures are not required for VIO-only work.
4. Classify mismatches as UI binding, domain model, register map, byte order, packet framing, fixture generation, parser, or checker issue.
5. Preserve provenance: export path, generation script, hashes/counts, RTL commit, testbench, and run log.

## Output Contract

Produce an alignment table with field/command, host source, transport representation, RTL consumer, expected and observed behavior, evidence, mismatch class and next action. Include wire bytes/fixtures for packet workflows or probe/bitstream identity for VIO/JTAG workflows; mark irrelevant fields as not applicable.

## Boundaries

Static and simulated alignment prove digital intent and modeled consumption. Actual VIO/ILA observations prove internal activity only for the recorded image/session. Board, timing and analog behavior require separate evidence.

## Asset Library

- Use `<CODEX_HOME>/hardware-assets/templates/reports/host_rtl_alignment_table.md` for the alignment table.
- Use project `source-refs/` files to locate host exports, fixture manifests, parser examples, and replay scripts.
- Use `rtl.fixture.*` hooks only when both `<CODEX_HOME>/hardware-assets/hooks/hardware-hook-registry.yaml` and its runner exist. Otherwise inspect and use the owning project's script within its write boundary, or report the missing dependency. Never invent a hook command. Preserve export and fixture provenance.
