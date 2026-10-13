---
name: matlab-write-help
description: Write or improve MATLAB help comments for specified functions, classes or scripts. Preserve project language and formatting, document only implemented contracts, and use a strict house-style profile only when requested.

license: MathWorks BSD-3-Clause
metadata:
  author: MathWorks
  version: "1.0"
---

# MATLAB Help Text

Read [runtime and compatibility](../matlab-clean-code/references/runtime-and-compatibility.md). This skill changes documentation, not algorithms, signatures or input validation. If asked only to review or draft, return findings/text; if asked to edit, apply the scoped edit without an extra approval gate.

## Resolve and understand

Resolve the supplied file/path locally first (search the project if needed); use MATLAB `which` through an available interface when necessary. Ask for a path only after local discovery leaves a real ambiguity. Read the declaration, arguments/inputParser/manual checks, return paths, units, defaults, side effects and relevant callers. A declaration alone does not reveal the complete contract.

Preserve meaningful Chinese comments, project terminology, public names, indentation and copyright/license text. Keep the user's requested scope: help for one method does not authorize documenting every property or rewriting the class.

## Write usable help

- Put a contiguous `%` help block immediately after the complete function/class declaration (including continuation lines), or at the start of a script. Use an H1 summary and useful call syntaxes.
- Describe accepted inputs, shapes, units, defaults, outputs and important limitations supported by the implementation. Do not invent validation, performance, calibration or physical guarantees.
- Preserve established Inputs/Outputs lists, section headings and language when clear. A 75-character limit, name casing convention or mandatory hyphen is a house style, not a universal correctness requirement.
- Add small runnable examples only when useful and within task scope. Avoid examples that require real hardware/raw-data changes. `See also` should reference relevant resolvable functions; do not invent entries to meet a quota.
- For classes, document public construction/behavior relevant to scope. Do not duplicate inherited help or expand private implementation documentation unnecessarily. Preserve original copyright ownership and years.

Use [optional house-style details](references/help-style.md) only when the user requests that style or the project already requires it. Factual accuracy and compatibility take priority over typography.

## Check

Review the diff to ensure executable code and public signatures are unchanged. When MATLAB is available, inspect `help` rendering and run harmless examples appropriate to the edit. Otherwise state that rendering/examples were not executed. Fix formatting without changing behavior to match the prose. Use the argument-validation skill only if input-contract work is separately in scope.

Copyright 2026 The MathWorks, Inc.
