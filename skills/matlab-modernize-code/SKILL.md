---
name: matlab-modernize-code
description: Migrate MATLAB APIs or syntax for a specified release while preserving behavior. Use for verified removed or not-recommended APIs and explicitly requested modernization; a valid older pattern alone is not a migration trigger.

license: MathWorks BSD-3-Clause
metadata:
  author: MathWorks
  version: "1.2"
---

# MATLAB Modernization

Read [runtime and compatibility](../matlab-clean-code/references/runtime-and-compatibility.md). Record the current and minimum supported MATLAB releases, products and user-requested migration scope.

## Decide before replacing

Classify each candidate from the exact function's official documentation/Version History or local release documentation: removed in the target release; officially not recommended; or supported with an optional newer alternative. Record the source. A replacement's introduction date is not the old API's removal date.

Static analysis may find candidates; use exposed MCP tools or local `checkcode`, then inspect actual source/callers. Neither age nor a table in this skill establishes deprecation. Do not mass-replace `subplot`, `uicontrol`, `optimset`, char arrays, matrices, loops, `varargin` or `inputParser`.

For example, `optimset` remains the options constructor for MATLAB solvers such as fminbnd/fminsearch/fzero/lsqnonneg; choose the options API by the actual solver. A graphics migration may change positions/parent objects and callbacks. `evalc` output capture is not equivalent to replacing `eval` with dynamic fields. Analyze intent before changing any of these.

## Preserve observable behavior

1. Characterize inputs, output type/shape, numeric precision, empty/missing data, defaults, warnings/errors and file/graphics side effects before edits.
2. Change the smallest applicable API boundary. Preserve existing project structure, Chinese comments, parser behavior and supported releases; contract changes require explicit task scope.
3. Compare representative old/new calls, including failure cases. I/O migrations check headers, ranges, text/mixed data, encodings, dates, missing values and output types; do not substitute a single `readtable` output for three `xlsread` outputs without adapting callers.
4. Parameter-block migration uses `matlab-validate-function-arguments`: class and size declarations can convert inputs; stricter-looking syntax can actually widen acceptance. Keep manual parsing when it preserves required semantics.
5. Report the change, documentation basis, executed comparisons and unresolved differences. If the old release/runtime is unavailable, label that compatibility unverified and retain conservative syntax where possible.

## Conditional domain references

These existing references provide migration candidates and examples, not a verified cross-release deprecation catalog. Read only the relevant domain and verify the specific API before using an example:

- [Core I/O, text, graphics and UI](reference/core-functions-guidance.md)
- [Performance](reference/performance-guidance.md)
- [Signal processing](reference/signal-processing-guidance.md)
- [Audio/video](reference/audio-video-guidance.md)
- [Optimization](reference/optimization-guidance.md)
- [Control systems](reference/control-systems-guidance.md)
- [Image processing](reference/image-processing-guidance.md)
- [Statistics/ML](reference/statistics-ml-guidance.md)
- [Simulink](reference/simulink-guidance.md)
- [Removed-function candidates](reference/removed-functions-guidance.md)
- [Communications](reference/communications-guidance.md)
- [Mapping](reference/mapping-guidance.md)

Official check examples: [optimset](https://www.mathworks.com/help/matlab/ref/optimset.html), [subplot](https://www.mathworks.com/help/matlab/ref/subplot.html). Consult the selected release's documentation, not just the current page.

Copyright 2026 The MathWorks, Inc.
