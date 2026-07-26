---
name: host-rtl-alignment
description: "Generic host-to-RTL alignment workflow. Use when host software exports register maps, binary packets, command streams, payload transforms, CSV/JSON/hex/mem fixtures, or readback expectations that must match RTL parsers, testbench fixtures, bus adapters, or FPGA command handlers."
---

# Host RTL Alignment

## Workflow

1. Identify the host artifact: GUI setting, config object, register map, command builder, raw payload, transport packet, fixture, or replay bundle.
2. Identify the RTL consumer: parser, bus adapter, register file, serializer, memory loader, testbench, or checker.
3. Trace one field or command end-to-end through host model, export, byte transform, packet framing, fixture generation, RTL parser, and checker.
4. Classify mismatches as UI binding, domain model, register map, byte order, packet framing, fixture generation, parser, or checker issue.
5. Preserve provenance: export path, generation script, hashes/counts, RTL commit, testbench, and run log.

## Output Contract

Produce a host/RTL alignment table with field/command, host source, wire bytes, fixture path, RTL consumer, expected behavior, observed behavior, mismatch class, and next action.

## Boundaries

Host/RTL alignment proves digital intent and simulated consumption only. Board, timing, and analog behavior require separate evidence.

## Asset Library

- Use `C:/Users/Administrator/.codex/hardware-assets/templates/reports/host_rtl_alignment_table.md` for the alignment table.
- Use project `source-refs/` files to locate host exports, fixture manifests, parser examples, and replay scripts.
- Use `C:/Users/Administrator/.codex/hardware-assets/hooks/hardware-hook-registry.yaml` for `rtl.fixture.*` hooks that flatten host exports, generate fixtures, compare payloads, or prepare replay inputs. Preserve export and fixture provenance in the output table.
