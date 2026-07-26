---
name: maroc-host-rtl-alignment
description: "MAROC adapter for host-to-RTL alignment. Use when QT_MUON exports, register_mapping.txt, bits_829, raw_104B, packet_250, USB byte order, MAROC RTL fixtures, parser testbenches, and XSim replay must match exactly. Use host-rtl-alignment for the generic method."
---

# MAROC Host RTL Alignment

## Workflow

1. Apply the generic `host-rtl-alignment` workflow first.
2. Identify the MAROC host artifact: GUI setting, `DeviceConfig`, `MarocConfigurationManager` export, `bits_829`, `register_mapping.txt`, `raw_104B`, or `packet_250`.
3. Compare against MAROC RTL fixtures and parser/TB consumers listed in `maroc-hardware-dev-router/references/resource-map.md`.
4. Classify mismatches as UI binding, MAROC3A model bit order, packet framing, USB wire transform, parser, or TB fixture issue.
5. Do not call the alignment done until `bits_829/register_mapping -> raw_104B -> packet_250 -> fixture -> parser/TB` provenance is clear.

## MAROC Boundaries

- `bits_829.txt` and `register_mapping.txt` are MAROC slow-control configuration intent.
- `packet_250.hex` is transport/parser framing, not the ASIC register map itself.
- Host/RTL replay is digital evidence, not board or chip-behavior proof.

## Asset Library

- Read `C:/Users/Administrator/.codex/skills/maroc-hardware-dev-router/references/maroc-asset-map.md` before choosing host export, fixture, parser, or report assets.
- Use `C:/Users/Administrator/.codex/hardware-assets/source-refs/maroc-qt-host-assets.md` for QT_MUON exporters and payload transforms, and `C:/Users/Administrator/.codex/hardware-assets/source-refs/maroc-rtl-assets.md` for parser/TB fixture consumers.
- Use `C:/Users/Administrator/.codex/hardware-assets/templates/reports/host_rtl_alignment_table.md` as the standard alignment record.
- Use `C:/Users/Administrator/.codex/hardware-assets/hooks/maroc-hook-map.md` for `rtl.fixture.prepare.maroc` and related fixture/replay hooks. Keep hook run logs as provenance, not as board evidence.
