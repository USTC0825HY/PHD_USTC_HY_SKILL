# Schematic Screenshot Workflow

## Source Discipline

- Treat the user-specified source directory as authoritative for the current task.
- If there are old vault copies and newer external PDFs, render from the newer PDFs and update nearby source text.
- Use absolute source paths only in source/context sections of the note; keep image links local and relative inside Markdown.

## Crop Quality Rules

- The screenshot should answer one visual question: where is the test point, what is the front-end circuit, what is the core chip, or what is the output stage.
- Avoid full-page screenshots.
- Avoid crops dominated by whitespace.
- Avoid showing neighboring repeated channels unless comparison is the purpose.
- Keep enough context for:
  - component designator or connector ID,
  - relevant network names,
  - input/output direction,
  - immediate passive network if it affects measurement,
  - page-level function block label when useful.

## Highlight Rules

- Place red boxes only after inspecting a no-box crop.
- Use coordinates relative to the cropped output image, not the full rendered page.
- The box should surround the target with a small margin.
- For connectors, include the connector label and connector symbol/body. Do not include the upstream signal line, right-side range text, or lower explanatory notes unless explicitly needed.
- For chips, include the chip outline and designator. If pins are dense, keep the full chip body and immediate named nets rather than boxing individual pins.
- If a red box covers text, moves attention to the wrong object, or makes the schematic less legible, regenerate it.

## Replacement Pattern

1. Render full page at 8x or 12x.
2. Produce a no-box candidate crop.
3. Inspect the no-box image.
4. Adjust crop until unrelated regions are excluded and target context remains.
5. Add precise red boxes only when needed.
6. Inspect the final asset file after copying it into the vault.
7. Record dimensions and source PDF/page in the final response.

## Obsidian Markdown Context

Near each image, include:

- source PDF path,
- page number,
- crop scope,
- function block,
- test focus,
- residual uncertainty or `needs_check` if mapping is not fully verified.

Example:

```markdown
![数字锁定板 ADC 接口 JG12/JG15/JG18 局部](assets/原理图截图/局部/02N_P04_ADC接口_JG12_JG15_JG18局部.png)

- 来源：`<laser_source_root>/原理图/原理图--汇总-20260508/_输出PDF/数字锁定.pdf`。
- 页码/位置：第 4 页，顶层 ADC 输入接口；本图只保留 `JG12/JG15/JG18` 三路接口局部。
- 功能块：`JG12/JG15/JG18` 分别对应图中红框标出的三处接口本体。
```

## Review Checklist

- Final image is local and referenced by a valid relative path.
- Final image is not a full-page screenshot.
- Final image is readable at normal Obsidian zoom.
- Red boxes are accurate and do not cover unrelated parts.
- Source path points to the latest PDF used for rendering.
- Old low-resolution image is backed up as `.old_lowres.png` when replacing in place.
- Audit has zero schematic image errors.
