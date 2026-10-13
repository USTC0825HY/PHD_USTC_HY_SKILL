---
name: maroc-fpga-cdc-reset-timing
description: "MAROC adapter for FPGA CDC, reset, and timing closure. Use for MAROC usb_ifclk to system-clock crossings, async FIFO use, reset sequencing, clock generation, XDC clocks, timing reports, C17/IFCLK smoke issues, and timing-closure risk reviews. Use fpga-cdc-reset-timing for the generic method."
---

# MAROC FPGA CDC Reset Timing

## Workflow

1. Apply the generic `fpga-cdc-reset-timing` workflow first.
2. Use MAROC clocks and XDC paths from `maroc-hardware-dev-router/references/resource-map.md`.
3. Check `usb_ifclk`, system 40 MHz, C17/local clock, generated clocks, reset release, async FIFO, and any same-clock TB simplification.
4. Treat C17/`Local_FPGA_CLK` and `CLOCK_DEDICATED_ROUTE FALSE` issues as board-clock/timing risks unless formal closure evidence exists.

## MAROC Risk Pattern

Local 2FF sync of `valid + data bus` across unrelated clocks is unsafe; prefer a proper async FIFO or handshake owned at the integration boundary.

## Asset Library

- Read `<CODEX_HOME>/skills/maroc-hardware-dev-router/references/maroc-asset-map.md` for MAROC clock, reset, XDC, and timing-report assets.
- Use `<CODEX_HOME>/hardware-assets/source-refs/maroc-rtl-assets.md` to locate XDC files, timing scripts, and CDC-related RTL.
- Use `<CODEX_HOME>/hardware-assets/templates/rtl/cdc_reset_timing_checklist.md` for reusable CDC/reset/timing reviews.
