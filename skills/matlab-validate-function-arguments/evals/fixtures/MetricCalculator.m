classdef MetricCalculator
    properties
        Threshold = 0.5
        Name = "default"
    end

    methods
        function obj = MetricCalculator(threshold, name)
            obj.Threshold = threshold;
            obj.Name = name;
        end

        function results = compute(obj, data)
            results = struct('value', mean(data), 'name', obj.Name);
        end

        function normalize(~, results) %#ok<INUSL>
            for n = 1:length(results)
                res = results(n);
                fprintf('Result %d: %s = %.4f\n', n, res.name, res.value);
            end
        end
    end
end

% Copyright 2026 The MathWorks, Inc.
