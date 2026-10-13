# Vivado 2022.2 compatibility

- Upstream source: `Shinei-Nouzen-Arch/FPGA-Agent`, commit `b8eb0e7cbcd27131bda57b7c7cbab11ac3a53297`, GPL-2.0.
- Upstream path: `skills/vivado-constraints`.
- This is a historical 2022.2 compatibility record, not the workstation default. Select the actual project/tool version first; use `vivado_executable` in `<CODEX_HOME>/laser-fpga-profile.json` only as a validated fallback. These checks do not establish 2018.3 or other-version support.
- Core XDC commands in this skill were found by exact command lookup in 2022.2.
- Command availability does not validate a constraint's correctness, scope, object selection, or timing intent.
- Physical constraints require FPGA package and board evidence. Timing constraints require clock/interface timing evidence.
- Never generate timing exceptions automatically from net names.
