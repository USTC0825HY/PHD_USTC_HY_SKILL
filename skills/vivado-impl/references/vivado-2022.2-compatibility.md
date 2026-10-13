# Vivado 2022.2 compatibility

- Upstream source: `Shinei-Nouzen-Arch/FPGA-Agent`, commit `b8eb0e7cbcd27131bda57b7c7cbab11ac3a53297`, GPL-2.0.
- Upstream path: `skills/vivado-impl`.
- This is a historical 2022.2 compatibility record, not the workstation default. Select the actual project/tool version first; use `vivado_executable` in `<CODEX_HOME>/laser-fpga-profile.json` only as a validated fallback. These checks do not establish 2018.3 or other-version support.
- Query the worst path with `lindex [get_timing_paths -max_paths 1 -sort_by slack] 0`; `get_timing_path` is not a command.
- `report_qor_suggestions` is plural.
- Validate every directive and option against `help opt_design`, `help place_design`, `help phys_opt_design`, and `help route_design` before execution.
- Do not apply Versal-only, UltraScale-only, SLR, or ML options to a 7-series target.
