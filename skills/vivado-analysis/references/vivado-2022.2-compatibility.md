# Vivado 2022.2 compatibility

- Upstream source: `Shinei-Nouzen-Arch/FPGA-Agent`, commit `b8eb0e7cbcd27131bda57b7c7cbab11ac3a53297`, GPL-2.0.
- Upstream path: `skills/vivado-analysis`.
- This is a historical 2022.2 compatibility record, not the workstation default. Select the actual project/tool version first; use `vivado_executable` in `<CODEX_HOME>/laser-fpga-profile.json` only as a validated fallback. These checks do not establish 2018.3 or other-version support.
- Exact-command audit: 83 of 95 extracted names are commands in 2022.2. The remainder include option names/placeholders plus four later commands.
- Unavailable as commands in 2022.2: `create_dataflow_design`, `get_dataflow_paths`, `get_qor_assessment`, `report_slr_crossing`.
- Use `report_qor_assessment -file ...` instead of `get_qor_assessment`.
- Use schematic/object queries and `report_design_analysis` instead of the dataflow commands.
- Use `report_utilization -slr` and targeted object queries instead of `report_slr_crossing`.
- Treat all Versal-only and ML strategy material as non-applicable unless the target device and local command help prove otherwise.
