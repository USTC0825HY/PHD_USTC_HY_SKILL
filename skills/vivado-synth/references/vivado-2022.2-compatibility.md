# Vivado 2022.2 compatibility

- Upstream source: `Shinei-Nouzen-Arch/FPGA-Agent`, commit `b8eb0e7cbcd27131bda57b7c7cbab11ac3a53297`, GPL-2.0.
- Upstream path: `skills/vivado-synth`.
- This is a historical 2022.2 compatibility record, not the workstation default. Select the actual project/tool version first; use `vivado_executable` in `<CODEX_HOME>/laser-fpga-profile.json` only as a validated fallback. These checks do not establish 2018.3 or other-version support.
- `synth_design` exists in 2022.2, but option values and directives in the v2025.2 guide must be confirmed with local help.
- Validate inferred RAM/DSP/SRL behavior with synthesis reports rather than assuming an attribute took effect.
- Treat Versal, UltraRAM, block-level synthesis, and new lint features as conditional capabilities.
