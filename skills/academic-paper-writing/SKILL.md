---
name: academic-paper-writing
description: Use when creating, revising, or QA-ing Chinese academic papers, course reports, experiment reports, LaTeX/PDF reports, or research writeups from experiment artifacts. Applies a reproducible Python/LaTeX toolchain, academic paper structure, natural scholarly wording, metric consistency checks, and anti-AI/anti-engineering-expression scans.
---

# Academic Paper Writing

Use this skill for academic paper-style reports, especially when the deliverable is editable LaTeX plus a compiled PDF. The priority order is: source evidence -> academic argument -> editable structure -> PDF rendering.

## Workflow

1. Read source materials first: paper brief, PDF/TeX, experiment tables, JSON summaries, figures, and existing generation scripts.
2. Build or update the editable LaTeX source before treating the PDF as final.
3. Generate figures and tables from experiment artifacts; do not hand-fill core metrics.
4. Compile with XeLaTeX when Chinese text is involved.
5. Extract PDF text and render selected pages before delivery.

## Preferred Toolchain

- Experiments and tables: Python, pandas, scikit-learn, PyTorch, matplotlib, seaborn.
- Report source: LaTeX with `ctexart` for Chinese, `amsmath` for formulas, `booktabs`/`longtable`/`adjustbox` for tables, `graphicx` for figures.
- Compilation: `xelatex -interaction=nonstopmode -halt-on-error`.
- Verification: `pdftotext` for searchable text, `pdftoppm` for page rendering, `pdfinfo` for page count and metadata.
- In this project, prefer `src/report_academic.py` and `src/pipeline_academic_report.py` as the report generation entrypoints.

## Paper Structure

- Cover: title, author, date, experiment platform. Avoid tool-production wording such as `生成日期`.
- Abstract: background, dataset, methods, core results, ablation, explainability, limitations. For formal Chinese course papers, put the abstract on its own page when the user asks for thesis-like formatting.
- Main text: `1 引言`, `2 数据与方法`, `3 实验设计`, `4 结果`, `5 讨论`, `6 结论`.
- Methods: explain preprocessing, segmentation/candidate ROI, classical model, deep model, fusion, and metrics.
- Results: compare core methods, confusion matrices, ROC, ablation, visual examples, and failure cases.
- Discussion: interpret why methods perform differently and state limitations explicitly.
- Appendix: reproducibility commands, main program files, per-class metrics, exploratory methods.

## LaTeX Layout Rules

- Keep the `.tex` source as the editable deliverable; treat PDF as the compiled submission preview.
- Use native LaTeX equations for formulas. Do not use screenshots or plain-text formulas.
- Start major sections on new pages when the requested style is thesis/course-paper-like.
- Constrain figures with `max width=\textwidth`, `max totalheight`, and `keepaspectratio`; split large galleries instead of letting images overflow.
- Use `booktabs`, `tabularx`, `longtable`, or `adjustbox` for tables. Do not shrink important tables until unreadable.
- Keep captions analytic: state what the table or figure shows, not only its object name.

## Writing Style

- Write in academic prose: problem definition, method motivation, comparable experiment design, error analysis, and conclusion boundaries.
- Avoid engineering/process residue: `本作业的课程要求`, `生成日期`, `自动完成`, `正式开发链路`, `报告重构`, `Python 结果生成`, `历史版本`.
- Avoid AI-sounding traces: do not write `本文完成了……重构`, `报告正文保留……`, or process-centered self-commentary. Prefer `本文比较……方法`, `实验表明……`, `结果提示……`.
- Explain metrics naturally: Accuracy for overall correctness, Macro-F1 for class-balanced performance, Macro ROC-AUC for probability ranking.
- Keep claims bounded: state weak segmentation errors, image-level rather than patient-level split, and lack of 3D context when applicable.
- Add method motivation and result interpretation before listing metrics. A report that only lists pipeline steps and scores reads like an engineering memo, not a paper.
- Include representative failure cases when results are high; use them to explain error sources and limits.

## Content Rules

- First occurrence of technical terms may use `中文（English）`; later use concise Chinese or established abbreviation.
- Formulas should be native LaTeX equations, not plain-text approximations or screenshots.
- Captions must describe what the figure/table proves, not just name the object.
- Do not overstate clinical value. If segmentation lacks pixel-level labels, call it weakly supervised candidate ROI, not clinical-grade segmentation.
- Use appendix for exploratory or secondary models; keep the main narrative focused.

## QA Checklist

- Text scan finds zero hits for obvious machine/process phrases such as `生成日期`, `本作业`, `课程要求`, `自动完成`, `历史版本`, `正式开发`, `训练链路`, `Python 结果生成`, `报告重构`.
- Core numeric values in text, tables, and figures match CSV/JSON artifacts.
- `pdftotext` confirms author, section anchors, and key values are searchable.
- XeLaTeX log has no fatal errors, missing images, or serious overfull boxes.
- Render and visually inspect at least cover, abstract, introduction, methods, result-figure page, and appendix.
- Check rendered pages for figure/table overflow, broken English terms, crowded captions, and formula images accidentally replacing LaTeX math.
- Deliver both editable `.tex` and compiled `.pdf`.
