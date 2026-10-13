# Preserving validation during migration

The table is a decision aid, not a mechanical rewrite. Test the original predicate on representative valid/invalid inputs first. `inputParser` validation also has parsing semantics; equivalent predicates alone do not prove equivalent APIs.

| Existing intent | Behavior-preserving direction |
|---|---|
| `isnumeric` | `mustBeNumeric` without a converting class declaration; verify errors. |
| `ischar` / `isstring` / `islogical` | A non-converting class predicate/validator; preserve original shape acceptance. Do not replace with a scalar class declaration. |
| `isinteger` or integer-storage classes | Preserve the exact accepted storage classes; integer-valued double is a different contract. |
| single or double | `mustBeFloat` without a `double` declaration, if errors/subclasses remain compatible. |
| exact class / subclass-sensitive check | Preserve `class` versus `isa` semantics; `mustBeA` checks class membership and is not a universal exact-class substitute. |
| strict row/column/shape | Use non-converting predicates or a supported validator. A size declaration may reshape or expand. |
| anonymous predicate | Preserve both class and value semantics; use a local error-throwing validator if no verified equivalent exists. Array-valued predicates are not automatically equivalent to an all-elements validator. |
| `validatestring` | Preserve its canonical return and matching rules; do not replace with `mustBeMember`. |

Example: preserve integer-storage acceptance and a public error identifier:

```matlab
function y = preserveInteger(x)
    arguments
        x {requireIntegerStorage}
    end
    y = x;
end

function requireIntegerStorage(x)
    if ~isinteger(x)
        error('myAPI:IntegerClass', 'Input must use integer storage.');
    end
end
```

For inputParser, inspect CaseSensitive, PartialMatching, KeepUnmatched, StructExpand, optional-positional ambiguity and repeated/unknown names. Keep the parser when forwarding, dynamic validation, old-release support or error compatibility makes it the safer implementation. Moving an options struct to name-value inputs is an API change, not a strict-fidelity migration.

Test omitted optional arguments, explicit [], empty arrays of different shapes, scalar expansion, row/column, single/double/integer/logical/text, complex, NaN/Inf, valid/invalid abbreviations, unknown names and caller-visible errors. Select cases relevant to the actual contract; do not harden unrelated inputs by default.

[Official conversion guidance](https://www.mathworks.com/help/matlab/matlab_prog/avoid-unwanted-class-and-size-conversions.html) explains why validators without converting declarations can preserve rejection behavior.


Copyright 2026 The MathWorks, Inc.
