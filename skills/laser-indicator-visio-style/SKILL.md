---
name: laser-indicator-visio-style
description: Format, revise, and QA editable Microsoft Visio (.vsdx) indicator-test procedure pages in the user's approved light, compact style. Use for YB2208, DA9726, and related laser qualification-test Visio flows when creating pages, standardizing an existing deck, correcting layout or typography, or exporting per-indicator PNG review images.
---

# Laser Indicator Visio Style

## Required reading

Read [references/style-contract.md](references/style-contract.md) completely before editing a Visio file. Use `laser-cw-qualification-test-development` as well whenever test values, firmware evidence, interfaces, or pass/fail boundaries are involved.

## Workflow

1. Inspect the existing VSDX, page names, shape IDs, page size, fonts, and source PNG before editing.
2. Preserve the user's prior VSDX and work in the requested review version.
3. Keep each indicator on one page with the six-stage sequence defined in the style contract: test item, interface, ILA/VIO, configuration, instruments, and data export.
4. Apply the approved geometry, colors, typography, table rules, and omissions in the style contract.
5. Edit with installed Microsoft Visio through COM or equivalent native Visio automation. Keep all text and shapes editable.
6. Export each page through Visio at 200 dpi. Preserve the full A4 landscape page with a white, borderless background shape when sparse content would otherwise be cropped.
7. Inspect the exported PNG at original resolution. Correct clipping, tiny arrows, oversized boxes, awkward wrapping, literal `` `n ``/`\n`, stale colors, or missing mixed fonts before handoff.

## Content rules

- Use explicit configuration values supported by the test specification, Word procedure, or current engineering evidence. Do not invent settings.
- Keep full interface-to-channel mappings in the dedicated mapping document; show only the generic interface role on the indicator page.
- Use real line breaks and concise phrases. Match box height to line count instead of padding all boxes to one large size.
- Use the exact third-column heading and record prefix defined in the style contract. Make each cell a concrete record instruction.
- Do not add a top evidence-status subtitle, a bottom explanatory footer, or a separate gate/stop banner in this approved visual style.
- Keep uncertainty and evidence limitations in the authoritative procedure or traceability material; do not convert unverified assumptions into confirmed values.

## Output checks

- Verify the requested page count and page names.
- Verify only the first-stage test-item heading/body uses a colored fill; all other flow and table surfaces remain white or neutral near-white.
- Verify all six heading boxes are visible, arrows are long and prominent, and the content boxes fit their text.
- Verify Chinese uses Microsoft YaHei and English, numbers, formulas, file names, probes, and signal names use Times New Roman.
- Verify exported PNG dimensions retain the A4 landscape ratio and the source VSDX remains editable.
