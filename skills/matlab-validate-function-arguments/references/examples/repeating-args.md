# Repeating arguments and outputs

Check the target release's [arguments documentation](https://www.mathworks.com/help/matlab/ref/arguments.html). Repeated input variables become cell arrays; groups must be complete and have no defaults. Test zero groups, one/multiple groups and incomplete groups.

```matlab
function total = sumPairs(x,y)
    arguments (Repeating)
        x (1,1) double
        y (1,1) double
    end
    total = sum([x{:}]) + sum([y{:}]);
end
```

This is a new example with intentional scalar-double conversion, not a strict migration recipe. Preserve existing parser acceptance if adapting another function.

For supported releases, repeating output validation declares one repeated output name. Allocate only requested outputs; test zero, one and several outputs. Do not fill triples past nargout unless an explicitly documented grouped-output contract validates the requested count.

```matlab
function out = numberedOutputs()
    arguments (Output,Repeating)
        out (1,1) double
    end
    out = num2cell(1:nargout);
end
```

Composition of required, optional, repeating and name-value blocks is release/syntax-sensitive. Test the actual signature and calls; do not claim a universal allowed/forbidden combination from memory. Include recognized, misspelled, unknown and abbreviated names: a repeated positional region can consume tokens that the caller intended as name-value options. Verify which values reached the body, not merely that parsing succeeded.

For `.?ClassName`, use a class with the intended public-settable properties, confirm exported names and test unknown names. See [property import](dot-question-syntax.md). Preserve intentional ignored `~` inputs and explicit [] defaults.


Copyright 2026 The MathWorks, Inc.
