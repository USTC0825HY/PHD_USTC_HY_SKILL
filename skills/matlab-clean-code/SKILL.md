---
name: matlab-clean-code
description: "Write, refactor, review, and document MATLAB .m code with clean structure, descriptive names, concise useful comments, clear units, and modern MATLAB patterns. Use for MATLAB scripts, functions, plotting code, scientific data analysis, signal processing workflows, PSD/ASD analysis, experimental scripts, and requests that ask for elegant, readable, maintainable, or well-commented MATLAB code."
---

# MATLAB Clean Code

Use this skill as a style and quality overlay when writing or refactoring
MATLAB code. Prefer practical clarity over cleverness: code should be easy to
run, easy to inspect, and hard to misuse.

## Core Workflow

1. Identify the caller's workflow: script, function, class, analysis pipeline,
   plotting routine, test, or documentation-only change.
2. Preserve existing behavior unless the user explicitly asks for a redesign.
3. Convert repeated or fragile script logic into functions when that improves
   reuse, testability, or parameter control.
4. Name variables after physical meaning, not acquisition channel or temporary
   shape alone. Keep short names only for obvious math indices or local values.
5. Put parameters near the top or in an `arguments` block. Avoid hidden magic
   numbers in the middle of analysis code.
6. Add comments only where they explain intent, assumptions, units, hardware
   conventions, domain meaning, or non-obvious choices.
7. Verify labels, units, and plotted quantities match the actual calculation.

## MATLAB Style

- Prefer functions for reusable work. Use scripts for simple one-off analysis
  only when workspace variables are intentionally part of the workflow.
- Use lowerCamelCase for variables and functions, and descriptive names such as
  `sampleRate`, `windowLength`, `overlapLength`, `gain`, `frequencyHz`,
  `powerSpectralDensity`, and `amplitudeSpectralDensity`.
- Prefer `arguments` blocks for public functions when MATLAB release support
  allows it. Validate units, sizes, and scalar parameters.
- Prefer string scalars for text in new code unless an API requires char arrays.
- Preallocate arrays before loops. Use vectorized operations where they improve
  clarity, but do not turn readable algorithms into dense puzzles.
- Use `fullfile` for paths. Avoid hardcoded Windows-only path separators inside
  reusable code.
- Avoid `eval`, `assignin`, `evalin`, `global`, and accidental shadowing of
  built-in names such as `sum`, `mean`, `table`, `length`, or `filter`.
- Use `numel` for element counts and `size` for dimensional intent. Use
  `length` only when either dimension being longest is actually intended.

## Comments and Help Text

- Comments should explain why a step exists, what unit conversion is happening,
  or what hardware/experiment assumption is being encoded.
- Do not add comments that merely restate the line, such as "divide by gain" for
  `signal = signal / gain`.
- For public functions, include MATLAB help text with an H1 line, syntax
  paragraph, concise description, and `See also` when useful.
- Keep comments close to the code they clarify. Use short section comments for
  analysis stages such as "Load data", "Estimate spectrum", and "Plot result".
- Preserve meaningful existing Chinese comments if they carry lab context. If a
  comment is corrupted by encoding, rewrite it in clear Chinese or English based
  on the surrounding file style.

## Scientific and Signal Analysis Code

- State the source and units of each signal: ADC counts, volts, normalized DAC
  data, displacement, current, phase, or another physical quantity.
- Make sampling assumptions explicit. If data comes from PICO, derive
  `sampleRate = 1 / Tinterval` when `Tinterval` is available.
- Keep acquisition gain, ADC full-scale conversion, and calibration factors as
  named parameters. Document whether a gain should be set to `1` for already
  calibrated data.
- For Welch estimates, name and document:
  - `sampleRate`
  - `windowLength`
  - `overlapLength`
  - `nfft`
  - window type
  - detrending or mean removal
- Distinguish PSD from ASD:
  - PSD is power spectral density, usually `V^2/Hz`.
  - ASD is amplitude spectral density, usually `V/sqrt(Hz)`.
  - If plotting `pwelch` output directly, label the y-axis as PSD.
  - If plotting `sqrt(pxx)`, label the y-axis as ASD or voltage noise density.
- Use names such as `pxx`, `frequencyHz`, `psdV2PerHz`, and `asdVPerSqrtHz`
  instead of ambiguous names when the distinction matters.

## Plotting Standards

- Ensure every plot has axis labels with units. Use `Frequency (Hz)`,
  `Power Spectral Density (V^2/Hz)`, or
  `Amplitude Spectral Density (V/sqrt(Hz))` as appropriate.
- Use `tiledlayout` and `nexttile` for multi-panel figures.
- Add `grid on` for spectra and analysis plots unless the surrounding style
  intentionally omits it.
- Use legends when more than one trace is present. Label traces by physical
  meaning, channel, or measurement condition.
- Keep LaTeX labels mathematically correct. Do not use a unit label that
  describes a transformed quantity that is not actually plotted.

## Refactoring Rules

- Keep changes scoped. Do not rewrite an entire lab script when the user asks
  for a unit-label fix.
- When improving a script, first make constants and assumptions clear; then
  improve names; then consider extracting functions.
- Preserve the user's data-loading workflow unless it is fragile or wrong.
- When converting a script to a function, make inputs explicit and return the
  computed data needed for reuse, such as frequency vectors and PSD/ASD values.
- Prefer behavior-preserving cleanup before algorithmic changes. If a numerical
  result changes, explain why.

## Quality Checks

Before finishing MATLAB work:

- Check that code runs in the expected workspace model or has explicit inputs.
- Check that units in labels, comments, and variable names match calculations.
- Check that comments add context rather than noise.
- Check that hardcoded constants have names or comments explaining origin.
- Check that plotting code exposes the result the user asked to inspect.
- If official MATLAB skills are available, use them for deeper review,
  modernization, help text, argument validation, or tests.
