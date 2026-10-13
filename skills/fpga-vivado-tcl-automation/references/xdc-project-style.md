# Personal Vivado XDC writing convention

Apply when creating a project or when constraint reorganization is explicitly authorized. Do not use this preference as permission to refactor unrelated projects.

- Use user-owned `pins.xdc` and, only when needed, `xilinx_debug.xdc`; do not create an empty debug file. For new projects place them in `.srcs/constrs_1/new/` per [native layout](native-project-layout.md). IP-owned scoped XDCs remain enabled as required and are not counted in this pair.
- Group every device's pins together. Explain the device, instance, channels and any evidenced assembly/cable assumptions in nearby comments.
- For normal fabric IO, put PACKAGE_PIN and IOSTANDARD on one line per port, using `set_property -dict`. Expand buses per bit and brace names containing brackets.
- Derive actual pin numbers and IO standards from the project's reviewed evidence. A style example is not a board pin authority; no pin, voltage or GTH line rate is a universal default.
- Example syntax only:

```tcl
set_property -dict {PACKAGE_PIN AP40 IOSTANDARD LVCMOS18} [get_ports {device_addr[0]}]
```

- For dedicated transceiver/reference-clock pads, assign the package pin without inventing a fabric IOSTANDARD.
- Keep clocks, timing exceptions and configuration properties in separately labeled sections of `pins.xdc`. Preserve property semantics, scoped constraints and required processing order during organization.
- Keep GUI-generated debug constraints in `xilinx_debug.xdc`; enable the applicable user XDCs and set the debug file as Target when present, otherwise pins.xdc. Being Target does not disable the other file.
- Place `if`, loops, validation and error handling in project Tcl, not an XDC that Vivado parses with restricted command support.
- Save XPR changes with native Vivado Tcl. Reopen and verify file membership, target constraint file, resolved ports/clocks and absence of duplicate bindings. Do not hand-edit XPR XML.
- Do not weaken timing constraints, add unsupported clock groups, or suppress errors merely to satisfy the two-file layout.
