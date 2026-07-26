---
name: academic-paper-presentation
description: Use when creating, revising, or QA-ing Chinese academic PowerPoint presentations for papers, course defenses, research reports, experiment results, or 8-15 minute seminar/classroom talks. Applies academic-pptx argument structure, MAROC-style Chinese section discipline, native PowerPoint sections, concise evidence-based wording, figure/table redesign, and strict COM-based layout QA.
---

# Academic Paper Presentation

Use this skill for PPTX decks based on academic papers or experiment reports. The goal is not to copy the paper into slides; the goal is to present one clear argument with evidence.

## Workflow

1. Read the source PDF/TeX and result artifacts before drafting slide content.
2. Extract the narrative spine: research question -> method design -> key results -> interpretation -> limitations.
3. Build a slide outline with action titles before creating or editing the PPTX.
4. Rebuild charts/tables from CSV/JSON where possible; avoid pasting small paper figures directly.
5. Export 1600x900 PNG previews and run PowerPoint COM layout checks before delivery.

## Toolchain

- Deck generation/editing: `python-pptx`; use PowerPoint COM on Windows for native sections, export, and text overflow checks.
- Source extraction: `pdftotext`, LaTeX source, CSV/JSON tables, existing figure PNGs.
- Visual QA: PowerPoint `Presentation.Export(..., 'PNG', 1600, 900)`.
- Geometry QA: check shapes stay inside slide bounds and pictures preserve native aspect ratio.
- In this project, prefer `src/create_presentation.py` as the PPT generation entrypoint.

## Deck Structure

- Cover and guide: title, author, date, directory with page ranges.
- Problem and data: research problem, classes, dataset, split, evaluation boundary.
- Methods: preprocessing, candidate ROI, model routes, metrics.
- Results and errors: core performance, confusion matrices, ROC, ablation, Grad-CAM, failure cases.
- Conclusion and Q&A: performance conclusion, applicable scenario, what cannot be inferred, anticipated questions.
- For long decks, add visible section-divider slides and native PowerPoint Sections.

## Slide Writing Rules

- Use action titles, not topic labels. A title should state the takeaway.
- Keep one judgment per slide.
- Keep body text to 3-5 short lines; slides support speech, not replace it.
- Use `现象`, `依据`, `当前结论`, `仍未说明` for result/diagnostic slides when useful.
- Avoid ambiguous shorthand. If writing `三条路线`, explicitly name them, e.g. `RBF SVM`, `MobileNetV3-Small`, `Soft Voting`.
- Use footer text `参考：...`; avoid mixed-language `Source:` unless matching a required external style.
- Do not overclaim: distinguish classification performance, probability ranking, weak ROI explanation, and clinical segmentation.

## Visual Rules

- Default to a 16:9 academic deck with white content slides and restrained dark-blue section dividers unless a user template says otherwise.
- Use one consistent Chinese font such as Microsoft YaHei for slide text.
- Prefer figure-left, interpretation-right layouts for result slides.
- Preserve image aspect ratio; do not pass arbitrary width and height unless computed from native dimensions.
- Use directory pages and section dividers to control pacing in 12+ slide decks.
- Tables should be small and readable; if dense, convert to cards or split the content.

## Native PowerPoint Sections

- Add native sections for long decks with PowerPoint COM:
  `Presentation.SectionProperties.AddBeforeSlide(slideIndex, sectionName)`.
- Verify section count, names, first slide, and slide count after writing.
- The directory slide and native sections must agree on page ranges.

## QA Checklist

- Export PNG previews for every slide at 1600x900.
- Confirm slide count, page numbers, directory, section dividers, conclusion, and Q&A.
- Run COM text overflow audit using `TextFrame2.TextRange.BoundWidth/BoundHeight` against available text-frame size.
- Check every main shape stays within slide bounds.
- Check every placed picture preserves native aspect ratio.
- Search for forbidden or low-quality wording: `Source:`, unexplained `三条路线`, overclaiming, and punctuation stranded on its own line.
- Verify key values are searchable in PPT text or table cells.
- Keep a `ppt_outline.md` or equivalent with slide title, talk track, and figure/data source.
