---
name: matlab-validate-function-arguments
description: Design or review MATLAB function input contracts, arguments blocks, name-value or repeating arguments; migrate inputParser or validateattributes while preserving accepted inputs, defaults, conversions and errors.

license: MathWorks BSD-3-Clause
metadata:
  author: MathWorks
  version: "1.1"
---

# MATLAB Function Argument Validation

Read [runtime and compatibility](../matlab-clean-code/references/runtime-and-compatibility.md). Determine whether the task preserves an existing contract or intentionally changes it. Prefer the smallest correct change; valid manual validation/inputParser need not be migrated.

## Contract before syntax

Read callers and current validation. Record accepted classes, sizes/orientation, real/complex values, sparse/empty/missing inputs, defaults including explicit [] sentinels, name matching, output effects and documented error identifiers. Preserve Chinese comments and public names.

- Class declarations such as `double` or `logical` can convert compatible inputs before validators run. A numeric 1 can become logical true; `(1,1) logical` is not equivalent to `@islogical` and also imposes a new size constraint.
- Size declarations can reshape compatible vectors or expand scalars. `(1,:)` is not a strict row rejection check. Validate original input without a converting declaration when rejection is required.
- Preserve integer-storage requirements. `isinteger` is not equivalent to “numeric with integer-valued elements”; do not silently admit double(5) where only integer classes were accepted.
- Defaults can reference earlier passed values; replacing an explicit [] sentinel with an omitted-argument default can change behavior. Check both omitted and explicitly empty calls.
- Keep `validatestring` canonicalization/prefix/case behavior where callers rely on it; exact membership alone is not equivalent.
- Preserve unused `~` placeholders. Do not add names/pragmas solely for style. Check actual release support for argument-block syntax and validators.
- Validator semantics can change by release: local R2025b `mustBeInteger(1+2i)` rejects the input, while MathWorks documents removal of its real/type restrictions in R2026a. Preserve real/type restrictions explicitly when migrating that contract across releases; do not claim that every release accepts complex integers. See the version note in [validator semantics](references/validators-reference.md).

Use [migration guide](references/migration-guide.md) for conversions from existing validation, [validator semantics](references/validators-reference.md) for strict versus converting checks, [repeating examples](references/examples/repeating-args.md) for repeated inputs/outputs, and [property import](references/examples/dot-question-syntax.md) only for constructor/property forwarding tasks.

## Verification

Compare old/new accepted and rejected calls, output values/classes/shapes, omitted/empty defaults, error identifiers and name-value behavior. A generic validator may change error IDs; retain a local custom validator or the old code when IDs are contractual. For unfamiliar block combinations, write a minimal function and run it in the target release instead of inventing a restriction or claiming parse success.

For `.mlx`/`.mlapp`, use supported MATLAB editing/export facilities when available. Do not manually rewrite ZIP internals. Search for source/export or an available native editing route before asking the user for a plain `.m` copy. Preserve runtime invariant guards unrelated to input validation.

Copyright 2026 The MathWorks, Inc.
