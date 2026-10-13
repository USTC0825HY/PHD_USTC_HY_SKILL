# Timing acceptance, not prediction

- Bind reports to the actual part/tool, source/IP/XDC inputs and routed run/checkpoint. A historical Complete status or existing BIT is not current-input proof.
- Review routed setup, hold and pulse-width: no failing endpoints and nonnegative applicable slack, plus the project's explicit margin requirements. Do not invent a universal margin number.
- Review clock definitions, generated clocks, clock interactions, unconstrained paths, input/output delays, timing exceptions, CDC/reset and DRC. Report untested/unconstrained interfaces explicitly; internal closure is not board-interface closure.
- Failures, missing reports or unknown coverage cannot be changed into PASS by a QoR score, process exit code, warning suppression, relaxed clock target or blanket false/multicycle paths.
- QoR assessment is predictive guidance at a particular flow stage, not permission to generate/release a bitstream. Synthesis estimates and routed signoff are distinct.
- Examine control fanout, reset/enable semantics and combinational depth before proposing implementation directives. Pipeline changes require latency/throughput/handshake agreement; keep required CDC and data-valid protections.
- Exception scope and start/end objects must exist and match the functional justification. For multicycle paths review both setup and hold implications; do not paste generic values.
- A project-specific release gate must reject absent/failed evidence and bind its decision to the current routed result. No generic callback can establish board function; program/measure only within separate task scope.

Reference: [AMD UG906 Overall Assessment Summary](https://docs.amd.com/r/2025.1-English/ug906-vivado-design-analysis/Overall-Assessment-Summary) explains the predictive nature of QoR assessment. Command availability still depends on the selected Vivado release.
