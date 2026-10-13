# OrCAD Capture 17.4 export

Read `orcad_capture_executable` from `<CODEX_HOME>/laser-fpga-profile.json`. If it is absent, locate `Capture.exe` from the installed Cadence SPB 17.4 tree and record the resolved path in the profile.

1. Open the `.DSN` and confirm the board revision and design root.
2. Run the native PCB/Allegro netlist export for the design.
3. Preserve `pstxnet.dat`, `pstxprt.dat`, `pstchip.dat`, and `pstxprp.dat` together with the export log.
4. Record the source `.DSN` path, modification time, FPGA reference designator, part/package, and export date.
5. Do not rename nets or pins during export. Do not infer missing package pins from screenshots.

The query parser consumes `NET_NAME` and `NODE_NAME <refdes> <pin>` from `pstxnet.dat`, part identities from `pstxprt.dat`, and primitive values such as `TSD*` from `pstchip.dat`. It does not claim page numbers; add page evidence during review.
