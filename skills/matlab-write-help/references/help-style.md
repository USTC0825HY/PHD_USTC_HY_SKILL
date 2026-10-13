# Optional MATLAB help house style

This profile preserves useful formatting conventions from the original MathWorks-authored skill. It applies only when requested or required by the project; it does not define all valid MATLAB help. Keep the existing language, scope and declaration layout.

- Use `%NAME - Short purpose` for H1; a contiguous help block follows the full declaration, which may span multiple lines. Scripts start their help at the top. Match the file's indentation.
- Use `%   Y = name(X) describes ...` syntax paragraphs, with `%` blank comment lines between variants. Introduce required inputs first, then relevant optional/name-value arguments and outputs. Do not document an internal options struct as a caller argument when callers use name-value pairs.
- Where this profile's casing is wanted, uppercase all-lowercase names in descriptive syntax; preserve mixed-case/digit/underscore names. Keep `See also` targets in their actual resolvable spelling, including package qualification where needed.
- Prefer 75 columns counted from `%` for prose in projects that use that convention. Keep syntax/call examples readable; avoid breaking valid syntax to satisfy width. Chinese text follows the project's readability convention rather than ASCII-width assumptions.
- Include only useful examples and real `See also` targets. No fixed minimum count of links or universal prohibition on loops in examples. Use plain comment lines for conventional command-window help.
- Class descriptions can list relevant public methods/properties when a full class documentation task is requested. A method-only task stays method-only. Describe property defaults and access accurately; do not infer units or validation from a name.
- Preserve copyright/license text and separate it from the help block with a blank noncomment line when needed. Do not invent ownership or update dates as part of a help-only edit.

Verify actual `help` output when a runtime is available. Typography must never cause executable changes or unsupported claims.


Copyright 2026 The MathWorks, Inc.
