# Static hierarchy scanner

- `python -X utf8 -B scripts/rtl_hierarchy_scan.py <root> --project <xpr>` derives active synthesis members and top. It does not launch Vivado. XPR membership is not expanded IP/BD dependency or elaborated hierarchy evidence.
- `--filelist <file> --top <name>` accepts one literal path per line, relative to the filelist. Blank/comment lines are ignored; options, nested lists and variable substitution are rejected, not executed.
- Without either input, scan an inventory and label uninstantiated modules as candidate roots. Do not classify an unreachable module as safe to delete.
- No `--output`: JSON to stdout only. With an explicit output directory: the existing seven-file architecture bundle. Review existing outputs before overwriting.
- Schema 2 retains modules/edges/unresolved/top_modules and adds configured_top, mode, duplicate definitions, review items and source hashes. Exit 2 means incomplete/ambiguous static mapping, not necessarily broken RTL; exit 0 means a complete *static map*, not successful elaboration.
- Duplicate definitions are unresolved rather than last-file-wins. Macros, generate, symbolic widths, encrypted/IP sources and scoped/dynamic XDC require tool/source review. Simple ANSI/non-ANSI Verilog is supported; this is not a complete SV/VHDL frontend.
- Before reusing a map, match its selected XPR/filelist, TOP, input hashes and schema. Inspect current membership too: a new file can invalidate an inventory even when old hashes match. Old schema/no hashes is historical evidence until rechecked.
- Port/XDC name matches are static candidates only. Use the alignment audit for pin coverage and Vivado read-only review for applied properties; clocks/reset names do not prove CDC safety.
