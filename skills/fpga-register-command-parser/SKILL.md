---
name: fpga-register-command-parser
description: "Generic FPGA register-map and command-parser workflow. Use for register fields, command words, packet framing, parser state machines, byte order, payload length, headers/footers/tags, address maps, direct commands, host/RTL protocol alignment, and fixture comparisons."
---

# FPGA Register Map And Command Parser

## Workflow

1. Establish the truth layer: datasheet field, host field, exported bitstream, raw payload, transport packet, parser output, register write, or legacy command path.
2. Trace one field or command end-to-end before generalizing.
3. Verify byte order, tag/header/footer stripping, payload length, error code, error offset, start/done semantics, and consumed-versus-passed metadata.
4. Use fixtures, compare scripts, and simulation replay for bit/byte claims.
5. Keep transport framing, parser output, and downstream register/serializer behavior as separate conclusions.

## Handoffs

- Use `host-rtl-alignment` when host-generated exports must match RTL fixtures or parser testbenches.
- Use `fpga-testbench-simulation` when parser behavior must be proven by simulation.
- Use project-specific adapter skills for project register meanings.

## Asset Library

- Use `<CODEX_HOME>/hardware-assets/templates/reports/host_rtl_alignment_table.md` to trace fields or commands through host bytes, fixtures, parser, and checker.
- Use project `source-refs/` files to locate register maps, packet fixtures, parser modules, and compare scripts.
