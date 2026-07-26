---
name: maroc-qt-host-development
description: "MAROC-specific Qt host development workflow. Use for QT_MUON C++/Qt code when the task involves MAROC3A configuration export, DeviceConfig, MarocConfigurationManager, maroc3a_model, MarocUiParameterBinder, FpgaCommandBuilder direct commands, CyAPI UsbDeviceClient, UsbPayloadTransform, read-probe automation, MAROC host CTest targets, or host/RTL protocol alignment. For generic Qt/C++ architecture, worker threading, fake backends, CMake, or device-client patterns, use qt-cpp-host-development first."
---

# MAROC Qt Host Development

## Workflow

1. Read the Qt host root from router `resource-map.md`: `F:/01_MOUN/04_PC_HOST/02_QT_MUON`.
2. For generic Qt/C++ structure, worker threading, fake backend, CMake option, or CTest patterns, apply `qt-cpp-host-development` first.
3. Classify the MAROC-specific surface: UI binding, ASIC model, configuration export, USB/CyAPI transport, direct FPGA command, read-probe automation, or host/RTL alignment.
4. Keep MAROC protocol ownership clear: UI/binder collects intent; `maroc3a_model` and `DeviceConfig` hold MAROC state; `MarocConfigurationManager` exports configuration; `FpgaCommandBuilder` builds FPGA commands; `UsbPayloadTransform` handles wire payload transforms; `UsbDeviceClient` handles transport.
5. If a change affects `bits_829`, `register_mapping`, `raw_104B`, `packet_250`, parser fixtures, or replay behavior, invoke `maroc-host-rtl-alignment` before calling it done.
6. Validate with the relevant host CTest targets. Treat live USB or board checks as hardware evidence, separate from host-side correctness.

## MAROC Key Files

- `src_ref/mainwindow.cpp`
- `src_ref/MarocConfigurationManager.cpp`
- `src_ref/maroc3a_model.cpp`
- `src_ref/device_config.cpp`
- `src_ref/MarocUiParameterBinder.cpp`
- `src_ref/FpgaCommandBuilder.cpp`
- `src_ref/UsbDeviceClient.cpp`
- `src_ref/UsbPayloadTransform.cpp`
- `docs/maroc_rtl_host_parameter_alignment.md`
- `src_ref/maroc_probe_automation.md`

## MAROC Boundaries

- `bits_829.txt` and `register_mapping.txt` are MAROC slow-control configuration intent, not board-level proof.
- `packet_250` is USB/parser framing, not the ASIC register map itself.
- Host tests prove model/export/transform behavior under the tested build, not FPGA or ASIC behavior.
- USB/CyAPI logs prove host-side transfer observations only; use ILA, XSim, or board evidence for downstream claims.

## Handoffs

- Use `qt-cpp-host-development` for general Qt/C++ host architecture, CMake, QThread workers, fake backends, and CTest patterns.
- Use `maroc-host-rtl-alignment` for any packet/register/export fixture alignment with RTL.
- Use `maroc-fpga-register-command-parser` when parser or FPGA command semantics must be reviewed from the RTL side.

## Asset Library

- Read `C:/Users/Administrator/.codex/skills/maroc-hardware-dev-router/references/maroc-asset-map.md` before selecting reusable MAROC host artifacts.
- Use `C:/Users/Administrator/.codex/hardware-assets/source-refs/maroc-qt-host-assets.md` to locate QT_MUON source files, tests, docs, and snapshots.
- Use generic Qt skeletons from `C:/Users/Administrator/.codex/hardware-assets/templates/qt-cpp-host/` for new abstractions; keep MAROC3A fields, CyAPI endpoint details, and packet formats in the MAROC adapter layer.
