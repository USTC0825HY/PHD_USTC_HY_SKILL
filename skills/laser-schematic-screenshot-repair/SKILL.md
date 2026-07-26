---
name: laser-schematic-screenshot-repair
description: Repair and recut clear Laser/PDH schematic screenshots for Obsidian notes. Use when a user complains that schematic screenshots are blurry, too broad, from stale PDFs, or have inaccurate red boxes/highlights; when extracting local crops from Laser/PDH PDF schematics; when updating Markdown image references, source metadata, and screenshot audit results.
---

# Laser Schematic Screenshot Repair

## Overview

Use this skill to replace blurry or poorly framed schematic screenshots with high-resolution, tightly cropped, source-traceable local images. Prioritize the latest user-specified PDF source, exact target framing, and visually verified highlights.

If the task also edits Laser/PDH Obsidian Markdown, follow the Laser/PDH Markdown governance skill if available, then use this skill for screenshot-specific work.

## Workflow

1. Confirm the authoritative source PDF.
   - Prefer the newest path explicitly given by the user.
   - For this vault, the current schematic source path is often `F:/01_Laser/原理图/原理图--汇总-20260508/_输出PDF`.
   - Do not silently reuse older copied PDFs when the user has given a newer schematic directory.

2. Inventory affected screenshots.
   - Search Markdown references with `rg`.
   - Check current image dimensions and file sizes with PIL.
   - Treat images below roughly 1000 px on the important axis, images with large blank margins, full-page screenshots, and stale source metadata as repair candidates.

3. Render high-resolution source pages.
   - Use PyMuPDF at 8x or 12x scale for circuit screenshots.
   - Start with a no-highlight candidate crop to calibrate geometry.
   - Use `scripts/render_crop_highlight.py` for repeatable rendering, cropping, optional backup, and highlight boxes.

4. Crop for the actual note purpose.
   - Crop to the function block or test point, not the page.
   - Remove unrelated regions such as neighboring DAC/ADC blocks, title blocks, large whitespace, and unrelated channels.
   - Keep enough context to show signal direction, relevant network names, component designators, and the page function.
   - If a single crop becomes too broad, split it into separate local images.

5. Place highlights only after the crop is correct.
   - Red boxes must tightly enclose the specific target object, such as `JG12`, `JG15`, `JG18`, a connector body, or a chip.
   - Do not box adjacent resistors, long signal wires, labels that are not part of the target, or explanatory text unless those are the target.
   - Use a no-box candidate first, inspect it, then calculate box coordinates in the cropped image coordinate system.
   - Prefer no highlight over an inaccurate highlight.

6. Write back safely.
   - Replace images by the existing filename when the Markdown reference should remain stable.
   - Before overwriting a low-resolution image, keep a `.old_lowres.png` backup unless one already exists.
   - Do not edit schematic content to hide inconvenient details. Cropping is allowed; altering circuit evidence is not.

7. Update nearby Markdown context.
   - State the absolute source path, page number, and what the crop includes.
   - Say what the red box marks if a highlight is added.
   - Keep `needs_check` when channel mapping, firmware mapping, or test-port naming still needs cable/firmware/hardware confirmation.

8. Verify.
   - Inspect final image files, not only temporary candidates.
   - Report dimensions of replaced images.
   - Run the Laser/PDH audit when working in that vault:
     `python C:/Users/Administrator/.codex/skills/laser-pdh-obsidian-md-writing/scripts/audit_laser_pdh_md.py --root C:/01_obsidian/ustc_hy/01_科研主系统/09_博士研究主线/00_理论补充/Laser_PDH_Study`
   - Key screenshot checks should be zero: `SCHEMATIC_IMAGE_EXISTS`, `SCHEMATIC_IMAGE_SCOPE`, `SCHEMATIC_IMAGE_CONTEXT`, and `TABLE_SCREENSHOT_METADATA`.

## Script

Use `scripts/render_crop_highlight.py` when generating or replacing a crop:

```powershell
python C:/Users/Administrator/.codex/skills/laser-schematic-screenshot-repair/scripts/render_crop_highlight.py `
  --pdf "F:/01_Laser/原理图/原理图--汇总-20260508/_输出PDF/数字锁定.pdf" `
  --page 4 `
  --scale 8 `
  --crop 1260,2020,2580,3120 `
  --box 900,198,965,300 `
  --box 900,568,965,670 `
  --box 900,927,965,1029 `
  --backup-existing `
  --output "C:/path/to/assets/02N_P04_ADC接口_JG12_JG15_JG18局部.png"
```

Read `references/screenshot_workflow.md` for the detailed checklist when the task involves multiple screenshots, red-box complaints, or Obsidian source metadata.
