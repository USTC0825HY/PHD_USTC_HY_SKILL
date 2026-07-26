# MAROC Hardware Development Resource Map

Use this map as the shared path index for the MAROC skill family. Do not copy project scripts into skills; read or run them in place so the workflow follows the current repo state.

## Roots

- RTL repo: `F:/01_MOUN/01_logic/02_MAROC/SPIROC_REF/01_MAROC_USB`
- Qt host repo: `F:/01_MOUN/04_PC_HOST/02_QT_MUON`
- Obsidian process notes: `C:/01_obsidian/ustc_hy/01_科研主系统/02_项目/MAROC开发/00_MAROC文档/过程开发笔记`
- PPT workspace: `F:/09_ppt`
- Existing MAROC PPT template skill: `C:/Users/Administrator/.codex/skills/maroc-ppt`

## RTL Entry Points

- Top: `sources_maroc/TOP_MAROC.v`
- USB ingress/egress: `sources_maroc/CY_driver_new.v`
- Packet parser: `sources_maroc/maroc_usb_packet_parser.v`
- Legacy command path: `sources_maroc/command_MAROC.v`
- Slow control serializer: `sources_maroc/SlowControl_MAROC.v`
- Trigger/acquisition: `sources_maroc/auto_mode_MAROC.v`, `sources_maroc/data_socket_MAROC.v`
- Read-register/probe: `sources_maroc/maroc_read_probe_driver.v`
- Support/debug RTL: `sources_maroc/soft_rst.v`, `sources_maroc/fpga_sma_pulse_gen.v`, `sources_maroc/dac60508_chain_writer.v`

## Testbench And Fixtures

- TB root: `sources_maroc/tb/`
- Key TBs: `tb_top_maroc_command_usb.v`, `tb_maroc_usb_packet_parser.v`, `tb_command_slowcontrol_joint_829_csv_xsim.v`, `tb_maroc_stage2_acq_readout.v`, `tb_cy_driver_new_xsim.v`
- Fixture root: `sources_maroc/tb/fixtures/`
- Key fixture files: `bits_829.txt`, `register_mapping.txt`, `packet_250.hex`, `sw_packet_250.mem`, `sw_slow_control_104.mem`, `sw_slow_control_legacy_payload_104.mem`
- Host-export flattening: `scripts/flatten_maroc_vectors.py`
- Parser fixture generation: `scripts/generate_maroc_parser_fixtures.py`
- Serial compare: `scripts/run_parser_sc_dout_compare.py`, `scripts/compare_sc_bitstream.py`

## Vivado, XSim, ILA

- Vivado project: `MAROC_PRJ/MAROC_PRJ.xpr`
- Project automation: `scripts/vivado/create_project.tcl`, `scripts/vivado/build_bitstream.tcl`, `scripts/vivado/build_maroc_cfg_bringup.ps1`
- Simulation automation: `sources_maroc/tools/run_tb_top_maroc_command_usb_xsim.ps1`, `sources_maroc/tools/run_tb_command_slowcontrol_joint_829_csv_xsim.ps1`, `sources_maroc/tools/run_maroc_adc_cfg_gate_timeout_sim.ps1`, `sources_maroc/tools/setup_maroc_xsim_sim_sources.tcl`
- XSim wave Tcl: `sources_maroc/tools/tb_*_xsim_wave_*.tcl`, `sources_maroc/tools/maroc_xsim_wave_groups.tcl`
- Hardware ILA Tcl: `sources_maroc/tools/maroc_ila_csv_export.tcl`, `maroc_hw_ila_wave_groups.tcl`, `maroc_trig_upload_wave_groups.tcl`, `maroc_cfg_ila_full_auto.tcl`, `maroc_three_ila_debug.tcl`
- Evidence exports: `ila_exports/`

## XDC, Schematic, Board Alignment

- Formal pins: `xdc_auto/00_pins_formal.xdc`
- Debug pins: `xdc_auto/00_pins_debug.xdc`
- Clocks: `xdc_auto/01_clocks.xdc`
- USB-only smoke: `xdc_auto/10_usb_only_test.xdc`
- Constraint reviews: `xdc_auto/mapping_review.md`, `xdc_auto/constraint_review_final.md`, `xdc_auto/vivado_xdc_load_order.md`, `xdc_auto/maroc3a_timing_constraints_xdc_plan.md`
- Hardware inputs: `fpga_xlsx/`
- Constraint builders: `scripts/build_xdc_constraint_artifacts.py`, `scripts/build_rtl_port_map.py`, `scripts/rebuild_structured_xdc_from_manual.py`

## Qt Host

- Build root: `F:/01_MOUN/04_PC_HOST/02_QT_MUON`
- Main CMake: `CMakeLists.txt`, `src_ref/CMakeLists.txt`
- UI/orchestration: `src_ref/mainwindow.cpp`
- Configuration export: `src_ref/MarocConfigurationManager.cpp`
- ASIC model: `src_ref/maroc3a_model.cpp`
- Board/device config: `src_ref/device_config.cpp`
- UI binder: `src_ref/MarocUiParameterBinder.cpp`
- Direct commands: `src_ref/FpgaCommandBuilder.cpp`
- USB client: `src_ref/UsbDeviceClient.cpp`
- Byte transform: `src_ref/UsbPayloadTransform.cpp`
- Host/RTL doc: `docs/maroc_rtl_host_parameter_alignment.md`
- Probe doc: `src_ref/maroc_probe_automation.md`

## Obsidian Canonical Structure

- `00_导航`: navigation and onboarding routes
- `01_架构与手册`: architecture, host guide, RTL contracts, MAROC3A parameter pages
- `02_规划与总结`: plans, stage summaries, audits
- `03_协议与配置`: 829bit/raw_104B/legacy_104B/packet_250B, parser, Qt mapping
- `04_仿真与验证`: XSim/iverilog/TB reports and signoff
- `05_排障与修复`: repair notes and landed RTL fixes
- `06_工具与操作`: Vivado, XDC, GUI, command procedures
- `08_上板调试`: canonical board-debug directory; treat older `02_上板调试` as governance drift unless explicitly requested
- `98_模板`: note templates
- `99_doc_governance`: manifests, Base/DB/index, cleanup reports
