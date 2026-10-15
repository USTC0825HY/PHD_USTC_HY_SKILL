# Laser/PDH LaTeX Rendering Rules

## Obsidian Delimiters

- Use inline math as `$...$`.
- Use display math as unindented:

```markdown
$$
formula
$$
```

- Do not use `\(...\)` or `\[...\]`; Obsidian may show those literally in this vault.
- Do not indent `$$` delimiters inside lists. Put display formulas in their own unindented block or convert short formulas to inline math.

## Absolute Values

Use `\lvert...\rvert` instead of raw pipe absolute values:

```markdown
$\lvert l_g(f)\rvert\gg1$
$S_\mathrm{error}/\lvert D(f)\rvert$
```

Avoid:

```markdown
$|l_g(f)|\gg1$
$S_\mathrm{error}/|D(f)|$
```

Raw pipes can break Markdown tables and are harder to audit.

## Tables

- Avoid complex LaTeX in Markdown tables.
- If a formula contains fractions, absolute values, aligned equations, or multi-line expressions, use a formula card or display block outside the table.
- Simple symbols such as `$D(f)$` or `$K_\mathrm{cur}(f)$` are acceptable in tables if they do not contain raw pipe characters.

## Repair Procedure

1. Inspect only the selected note for a local repair. Use audit `--root <vault-root> --file <selected.md>`; repeat --file for a selected set. A wider scan must not expand write scope.
2. If old delimiters or absolute-value pipes are reported, run `scripts/fix_laser_pdh_latex.py` without `--write` first.
3. Run the same script with `--file <selected.md> --write` within the authorized scope; repeat --file for selected notes. Explicit whole-project governance uses --all-project --write, excluding raw/history by default.
4. Re-run the audit script and inspect the most relevant note in Obsidian preview.

## Formula-safe edits

Parse code fences before headings or formulas; normalize LF/CRLF for parsing without changing source-hash meaning. Do not globally replace variable letters inside LaTeX commands, code or resource filenames. In particular, `\approx k` must not become the undefined command `\approxk`. Use `\times 10^{-5}` rather than plain scientific `e-05` inside displayed math; plain-text copyable code may use e notation. Validate rendered formulas separately from static delimiter checks.
