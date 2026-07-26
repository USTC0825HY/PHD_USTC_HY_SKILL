# OrCAD Capture 17.4 export

Use the installed Capture executable at `C:/Cadence/Cadence/SPB_17.4/tools/bin/Capture.exe`.

1. Open the `.DSN` and confirm the board revision and design root.
2. Run the native PCB/Allegro netlist export for the design.
3. Preserve `pstxnet.dat`, `pstxprt.dat`, and `pstxprp.dat` together with the export log.
4. Record the source `.DSN` path, modification time, FPGA reference designator, part/package, and export date.
5. Do not rename nets or pins during export. Do not infer missing package pins from screenshots.

The parser consumes `NET_NAME` and `NODE_NAME <refdes> <pin>` records from `pstxnet.dat`. It does not claim page numbers; add page evidence during review.
