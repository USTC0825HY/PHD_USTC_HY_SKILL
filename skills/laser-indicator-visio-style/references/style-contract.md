# Approved indicator Visio style contract

## Page structure

- Page: A4 landscape, native editable Visio.
- Title: one centered line only, for example `YB2208｜通道隔离度测试`.
- Omit the evidence-status subtitle, bottom explanatory footer, and separate gate/stop banner.
- Main flow: six horizontal stages with straight left-to-right connectors and no crossings.
- Detail table: `对象 | 具体信号与设置值 | 记录要求`.
- Add a white borderless page-sized background shape behind all content so Visio exports the full page bounds after small footer objects are removed.

## Main flow geometry

Use these values as the starting template for an A4 landscape page. Adjust individual body height only when the text line count requires it.

| Element | Approved value |
|---|---|
| Stage centers X | `1.00, 2.94, 4.88, 6.82, 8.76, 10.70 in` |
| Heading Y / size | `6.41 in`; `1.45 × 0.27 in` |
| Body center Y | `5.77 in` |
| Body width | `1.45 in` |
| Body heights | `0.56–0.88 in`, based on 2–4 lines |
| Heading font | `9.3 pt`, bold |
| Body font | `9.2 pt`, regular |
| Connector | `1.4 pt`, end arrow size `4` |
| Connector color | `RGB(116,128,140)` |

Keep connector gaps visually longer than the previous `0.08 in` layout. Do not expand a short two-line box to the height of a four-line box.

## Color and border rules

Only the first stage retains a colored fill.

| Element | Fill | Line | Text |
|---|---|---|---|
| `01 测试项` heading | `RGB(224,234,244)` | `RGB(142,163,183)`, `0.8 pt` | `RGB(39,65,87)` |
| `01 测试项` body | `RGB(246,249,252)` | `RGB(142,163,183)`, `0.8 pt` | `RGB(39,55,69)` |
| Headings `02–06` | white | `RGB(202,209,216)`, `0.65 pt` | `RGB(79,91,103)` |
| Bodies `02–06` | white | `RGB(194,202,210)`, `0.65 pt` | `RGB(47,55,63)` |
| Table header | `RGB(248,249,250)` | `RGB(205,211,217)`, `0.65 pt` | `RGB(57,65,73)` |
| Table body | white | `RGB(214,219,224)`, `0.55 pt` | `RGB(57,65,73)` |

Use no shadows, gradients, 3D effects, saturated status colors, colored row labels, or poster-like warning panels.

## Typography and writing

- Title: `18 pt`, dark neutral `RGB(43,56,69)`, Microsoft YaHei for Chinese and Times New Roman for Latin text.
- Chinese: Microsoft YaHei.
- English, digits, formulas, signal names, probe names, and filenames: Times New Roman.
- Center the six flow headings and bodies vertically and horizontally.
- Center the table's first column; left-align the second and third columns with `0.11 in` left margin.
- Prefer three or four short lines over one compressed long line.
- Use real line breaks. Never leave literal `` `n `` or `\n` in a shape.
- The third column heading is exactly `记录要求`; each body cell starts with `记录：` and states only what must be recorded.

## Table geometry

| Element | Approved value |
|---|---|
| Header center Y / height | `4.55 in / 0.30 in` |
| Row centers Y | `4.20, 3.78, 3.36, 2.94 in` |
| Row height | `0.40 in` |
| Header font | `9.1 pt`, bold |
| Row label font | `8.8 pt`, bold |
| Row body font | `8.5 pt`, regular |

Keep the table compact. Do not use extra row height merely to fill the page.

## Export and QA

- Export through Visio at 200 dpi using custom pixels-per-inch resolution.
- Target A4 landscape output is approximately `2339 × 1654 px`; small differences from Visio margins are acceptable.
- Inspect every PNG at original resolution for clipping, overlap, inconsistent heading frames, tiny arrows, and excessive padding.
- Compare VSDX text with PNG text after every export.
- Use [../assets/approved-style-reference.png](../assets/approved-style-reference.png) as the visual reference for spacing and tone.

