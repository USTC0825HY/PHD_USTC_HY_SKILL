# MATLAB runtime and compatibility

Read before executing or changing MATLAB code. Project rules and the user's requested scope govern this workflow.

1. Identify the target files, callers, project conventions, supported MATLAB releases and required products. Preserve existing public names, numerical behavior, accepted input classes/shapes, defaults, output classes/shapes, documented errors and meaningful Chinese comments. A style improvement does not authorize changing those contracts.
2. Discover tools actually exposed in this session. Use MATLAB MCP analysis/execution tools only when available; their names in a skill or manifest do not make them callable. Do not require installation of an MCP server to proceed.
3. Otherwise discover a local MATLAB executable and verify startup, `version`, `ver` and the needed functions/products. An installed executable or a listed toolbox does not alone prove that execution/licensing succeeds. The local R2025b installation is a discovery hint, not every project's minimum supported release.
4. Use `checkcode` for static analysis and `runtests` for the selected tests, via the available MATLAB interface or a local `matlab -batch` script. Quote paths correctly, use a task-owned output directory, preserve path/RNG/warnings, and inspect startup scripts before running in an unfamiliar project. Do not add a recursive project path or rewrite global preferences unnecessarily.
5. Without an executable runtime, inspect the source and report static findings; label execution and numerical equivalence unverified. Never report successful tests merely because a command was prepared or a tool was listed.

Match syntax to the project's supported release. New `arguments`, `Name=Value`, graphics, validators and test features may have separate release gates. Verify the relevant official Version History/local help; do not infer a release from a reference table. If legacy behavior is needed, retaining `inputParser`, char arrays, numeric matrices, `subplot`, loops or existing validation can be the correct choice.

For behavior changes explicitly requested by the user, state the changed contract and test it. For behavior-preserving work compare old/new values, types, dimensions, errors and side effects using representative inputs. Don't rewrite algorithms or update numerical baselines just to make a test pass. Small comment/style fixes do not require a new regression suite; use checks proportional to the change.

State what was inspected, which runtime/commands ran, pass/fail/incomplete counts and what remains unverified. Read-only review stays read-only. When edits/tests were already requested, proceed within that scope without adding a draft-approval gate; ask only for missing decisions or new authorization outside it.

Laser electrical analysis uses `laser-electrical-data-analysis` for measurement conditions, units, calibration/reference plane, PSD/ASD and evidence handoff. These general skills govern code, not physical conclusions. Consult only the needed companion: clean-code for readability, review-code for findings, modernize-code for release migration, testing for regression, validate-function-arguments for input contracts, write-help for documentation.
