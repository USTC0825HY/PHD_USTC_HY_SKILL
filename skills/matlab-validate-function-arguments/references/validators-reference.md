# Validator semantics and release checks

Class/size declarations can transform inputs before validation functions see them. Validators alone inspect the supplied value; combining a validator with `double`, `logical`, `string` or size declarations can therefore defeat a rejection policy.

| Need | Candidate and caveat |
|---|---|
| Numeric class family | `mustBeNumeric`; decide logical/complex separately. |
| Float class family | `mustBeFloat`; preserves single versus double if no class declaration is added. |
| Class membership | `mustBeA` when available; preserve exact-class versus subclass intent. Local `isa`/`class` predicates remain valid. |
| Logical only | Local validator using `islogical`; do not add scalar restriction unless required. |
| Integer storage | Local `isinteger` or original class predicate; `mustBeInteger` checks values, not integer storage. |
| Real, finite, nonempty | `mustBeReal`, `mustBeFinite`, `mustBeNonempty` as required by the contract, independently. |
| Strict orientation | Supported `mustBeRow`/`mustBeColumn` or original `isrow`/`iscolumn` check; preserve scalar/empty behavior. |
| Text | Preserve char/string/array/scalar acceptance; `mustBeTextScalar` narrows a text-array contract. |
| Exact members | `mustBeMember`; no canonicalization substitute for `validatestring`. |
| Range | Supported comparison validators with explicit inclusive/exclusive endpoints; check version before choosing newer conveniences. |

Custom validators throw errors and do not return transformed values. Keep them free of side effects. To preserve a public error ID, issue that ID explicitly; built-in validator errors can differ from inputParser/validateattributes.

Do not rely on release numbers copied into old tables. Verify the selected release's `which`, `help` and official Version History for mustBeA, mustBeRow, mustBeBetween, output validation and other nonbaseline features. A validator available on the maintenance machine need not exist on the project minimum release.

## Verified release difference

Local R2025b source and the 2026-10-08 minimal runtime check reject `mustBeInteger(1+2i)`. [MathWorks Version History](https://www.mathworks.com/help/matlab/ref/mustbeinteger.html) documents that R2026a removes its real/numeric/logical restrictions; retaining the older contract on those releases requires explicit real and numeric-or-logical validation. The newer behavior was checked against documentation, not executed on a local R2026a installation.

Useful counterexamples to run in the target release: `single(2)`/`'A'` to a double declaration; numeric 1 to logical; a column to `(1,:)`; scalar 5 to `(1,3)`; double(5) to an integer-storage validator; complex values to numeric/finite/integer-value checks. Record outputs or errors rather than assuming.

Official references: [argument validation](https://www.mathworks.com/help/matlab/matlab_prog/function-argument-validation-1.html), [avoiding conversion](https://www.mathworks.com/help/matlab/matlab_prog/avoid-unwanted-class-and-size-conversions.html), [validation functions](https://www.mathworks.com/help/matlab/matlab_prog/argument-validation-functions.html).


Copyright 2026 The MathWorks, Inc.
