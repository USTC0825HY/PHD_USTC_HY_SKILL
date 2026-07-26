# Vivado 2022.2 compatibility

- Upstream source: `Shinei-Nouzen-Arch/FPGA-Agent`, commit `b8eb0e7cbcd27131bda57b7c7cbab11ac3a53297`, GPL-2.0.
- Upstream path: `skills/vivado-synth`.
- Local executable verified: `E:/02_Xilinx/Vivado/2022.2/bin/vivado.bat`.
- `synth_design` exists in 2022.2, but option values and directives in the v2025.2 guide must be confirmed with local help.
- Validate inferred RAM/DSP/SRL behavior with synthesis reports rather than assuming an attribute took effect.
- Treat Versal, UltraRAM, block-level synthesis, and new lint features as conditional capabilities.
