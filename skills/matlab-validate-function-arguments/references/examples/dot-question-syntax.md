# Property import and name-value forwarding

Use this only when constructor/property forwarding is in scope and the target release supports the syntax. Exposing every public-settable property is a contract choice; list a subset explicitly when needed. Adding a property later can expand the constructor API.

```matlab
classdef SensorConfig
    properties
        SampleRate (1,1) double {mustBePositive} = 1000
        Label (1,1) string = "unnamed"
    end
    methods
        function obj = SensorConfig(nvArgs)
            arguments
                nvArgs.?SensorConfig
            end
            names = fieldnames(nvArgs);
            for k = 1:numel(names)
                obj.(names{k}) = nvArgs.(names{k});
            end
        end
    end
end
```

Test omitted values, supplied overrides, property validation and unknown names. The options struct contains supplied fields; omitted properties retain object defaults. Do not assume a class such as onCleanup exposes useful settable properties merely because the import parses.

For forwarding a selected options struct, use `pairs = namedargs2cell(options); obj = SensorConfig(pairs{:});` when supported. Preserve the caller's precedence and do not forward unrelated options. Validate actual block combinations and inherited/overridden property constraints in the target release rather than using an unverified universal composition rule.

Copyright 2026 The MathWorks, Inc.
