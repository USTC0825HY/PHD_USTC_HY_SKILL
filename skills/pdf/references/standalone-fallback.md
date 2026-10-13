# Standalone PDF fallback

## Applicability and discovery

Use only when no PDF plugin is available/enabled, not to evade a failed mandatory step of an already-selected plugin workflow. This preserves the personal skill's basic operations in other environments without requiring a plugin installation.

Discover the environment's bundled runtime, then an existing suitable local runtime. Verify the imports/commands actually needed: `pdfplumber` or `pypdf` for text/structure; `reportlab` for creation; `pdftoppm` and `pdfinfo` for rendering/inspection. Reuse available tools rather than installing a new environment. If a capability is missing, say which operation was not possible.

## Minimal workflow

1. Resolve source, task directory and separate destination from the caller's project rules. Inspect page count, encryption and whether the task involves interactive fields or signatures before edits.
2. For content questions, extract the relevant pages with an available reader. Scanned pages without a text layer need an available OCR path or visual inspection; an empty extraction is not an empty document.
3. For simple new PDFs, use ReportLab with an installed font that covers the requested Chinese, Latin and math glyphs. Register/embed a suitable font where supported. Do not silently drop or transliterate symbols to make a font pass.
4. Render the new/changed document and inspect affected pages; for a newly generated short document inspect every page. Reopen it to check page count and expected text. Text extraction alone cannot establish wrapping, clipping, glyph correctness or table layout.
5. Deliver the PDF with a concise statement of checks actually performed and any unverified scope. Preserve a useful editable source when part of the task.

Example rendering command; replace placeholders with verified paths and quote them in the current shell:

```text
<pdftoppm> -png -r 120 <input.pdf> <task-dir>/page
```

## Forms, signatures and missing capabilities

This basic fallback does not establish a complete AcroForm or signing workflow. For such a task, inspect the available library capability and relevant documentation before editing. Preserve interactivity unless a static result was explicitly requested; never flatten a signed or interactive PDF as a workaround and describe it as a successful editable result. If logical field-value/appearance verification or signature preservation cannot be supported, stop that edit and report the limitation.

If rendering is missing, extraction can still answer supported content questions, but final layout remains unverified. If a font lacks a requested glyph, choose a verified available alternative; if none exists, report the limitation instead of claiming a successful visual check.
