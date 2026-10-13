---
name: matlab-review-code
description: Review MATLAB code for demonstrated correctness, numerical, compatibility, performance and maintainability issues. Use for read-only review, audits and handoff checks; distinguish defects from optional style changes.

license: MathWorks BSD-3-Clause
metadata:
  author: MathWorks
  version: "1.1"
---

# MATLAB Code Review

Read [runtime and compatibility](../matlab-clean-code/references/runtime-and-compatibility.md). Establish requested scope, supported releases, callers and project rules before analysis. Review is read-only unless fixes were requested.

## Evidence-led review

1. Inspect changed code and enough call sites/data contracts to understand behavior. Identify units, array orientation, precision, missing-value handling, error behavior and external side effects.
2. Run available static analysis: MATLAB MCP if exposed, otherwise local `checkcode(file,'-struct')`. Use `codeIssues` only when supported and useful. Optional coding-guideline resources supplement project rules; their absence does not block review. Report diagnostics as diagnostics, not proof of correctness.
3. Inspect risks static analysis misses: wrong dimensions or implicit expansion, unit/gain mistakes, PSD versus ASD, dropped errors, state leakage, path assumptions, unsupported syntax and parser conversions. Where execution is authorized and useful, reproduce the suspected failure in a minimal fixture.
4. Assess performance only against relevant data size and actual cost. Profile when required and available; growing arrays or loops alone do not establish a user-visible performance defect. A measured regression merits stronger priority than an unmeasured preference.
5. Report actionable findings with file/line, trigger, impact, evidence/confidence and a narrow remedy. State checks run and gaps; if no defects are found, say so without inventing style findings.

## Severity and compatibility

- **Defect / high priority:** reproducible wrong result, failure, data loss, release incompatibility, or a demonstrated unsafe input-to-execution path. Explain the actual trigger.
- **Risk / needs verification:** plausible failure with incomplete evidence, such as an unresolved shape assumption or external dependency. State how to verify it.
- **Optional improvement:** readability, naming or an unmeasured performance opportunity. Do not label it an error or mix it into the defect count.

`eval`, `assignin`, shadowed names and platform paths require context. For example, untrusted input reaching `eval` is different from a fixed controlled expression; a Windows-only acquisition script need not be portable. Missing `arguments`, char arrays, matrices, `subplot`, loops, long functions and input/output counts are not errors by themselves. Preserve valid legacy interfaces and project naming.

Use `matlab-modernize-code` for a proven release/API migration, `matlab-testing` for requested regression tests, and `matlab-validate-function-arguments` for parser semantics. Debug a runtime report by inspecting its trace and inputs; do not depend on a missing `matlab-debugging` skill. Laser measurement conclusions require the domain skill and measured evidence.

Copyright 2026 The MathWorks, Inc.
