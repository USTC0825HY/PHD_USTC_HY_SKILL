---
name: matlab-testing
description: Create or run MATLAB tests using the existing project test style, including function-based and class-based tests. Use for behavioral regression, fixtures, tolerances, requested coverage or app tests; execute through available MCP or local MATLAB.

license: MathWorks BSD-3-Clause
metadata:
  author: MathWorks
  version: "1.1"
---

# MATLAB Testing

Read [runtime and compatibility](../matlab-clean-code/references/runtime-and-compatibility.md). State the behavior and cases to check, then proceed within the user's authorized test scope. Do not require a second approval merely because tests need writing.

## Select and implement meaningful tests

- Preserve the project's function-based, class-based or script-based suite. For new isolated behavior checks, function-based tests are sufficient; use classes when fixtures, parameterization, mocking or UI test facilities justify them. Do not convert a valid suite for style alone.
- Test public observable behavior, failure cases and important invariants using independent expected values. Avoid tests that copy implementation logic or merely match wording. Cover numeric values together with relevant class, shape, units, default and error contracts.
- Use Arrange–Act–Assert and focused cases. Prefer clear parameterization for repeated cases, but loops/conditionals in setup or a justified data-driven check are not forbidden. Do not hide failures behind broad try/catch.
- Choose exact equality for exact contracts; use AbsTol and/or RelTol based on precision, scale and algorithmic error for approximate results. Near-zero values often need an absolute bound. Explain tolerances; never increase them just to pass a regression.
- Restore RNG, path, warnings, working directory and temporary resources with teardown/fixtures. Register cleanup when acquiring a resource. Use task-owned temporary data; do not run tests that overwrite raw measurements or existing results.

## Run and report

Use an exposed MATLAB MCP runner if available, otherwise local MATLAB with `runtests` on the selected test file/suite. Check release support for runner options. Serial execution is the default; parallelize only when requested/useful, supported, and resources are isolated. UI/hardware/filesystem shared state can make parallel execution inappropriate.

```matlab
results = runtests('tests/myFunctionTest.m');
disp(results);
assert(~isempty(results) && all([results.Passed]), ...
    'Tests did not all pass or no tests were collected.');
```

Record command/runtime, collected/pass/fail/incomplete counts and output locations. Skips/incomplete tests are not passes. Static inspection is not a test run. Investigate failures before expanding coverage; once necessary checks pass, do not broaden the suite without an unresolved reason.

## Read only as needed

- [Setup, teardown and fixtures](reference/fixtures-guidance.md)
- [Tolerances and constraints](reference/constraints-guidance.md)
- [Class parameterization](reference/parameterized-tests-guidance.md)
- [Mocking](reference/mocking-guidance.md)
- [Execution, coverage and CI examples](reference/test-execution-guidance.md): retain existing CI; create coverage/buildtool integration only for an authorized need.
- [App gestures and UI testing](reference/app-testing-guidance.md): confirm target release, UI runtime and permission for visible interaction; hardware actions are a separate boundary.

[MathWorks test styles](https://www.mathworks.com/help/matlab/matlab_prog/ways-to-write-unit-tests.html) and [function-based tests](https://www.mathworks.com/help/matlab/matlab_prog/function-based-unit-tests.html) document multiple supported approaches.

Copyright 2026 The MathWorks, Inc.
