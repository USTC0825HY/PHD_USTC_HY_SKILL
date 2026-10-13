# Read-only helper contracts

Use Python >=3.10. `scripts/resolve_python.ps1` probes explicit `-PythonPath`, the app-bundled runtime, the FPGA runtime and available commands for executability/version and requested imports. It installs nothing. For direct Python CLI calls, check the chosen interpreter first; a PATH entry or existing executable does not prove it can run.

## Project membership

`python -X utf8 -B scripts/project_inputs.py <project.xpr> --stage implementation`

Optional `--top <expected>` validates, never overrides the configured top. JSON includes source/constraint set, active/disabled/UsedIn flags, constraint scope/order metadata, file hashes, unresolved inputs and run metadata. Default stdout; `--output` writes only the explicitly selected report. Exit 0 is a complete static membership check, not IP elaboration, compile-order or build acceptance. Inactive historical members are reported but are not treated as active missing inputs. Generated/IP/BD tops may require Vivado evidence. XPR Version is its schema version, not a substitute for the actual Vivado version.

`audit_native_layout.py <xpr> --legacy` relaxes layout policy only, not missing active sources or duplicate membership. Unresolved dependencies cannot pass. Neither helper saves the XPR nor migrates source directories.

## RTL/XDC/PST

Use the sibling alignment skill's `scripts/rtl_xdc_pst_audit.py`:

```text
--project <xpr> --pstxnet <selected-pst> [--top <expected>] [--ports clk bus[*]]
--rtl <top.v> --top <module> --xdc <first.xdc> --xdc <second.xdc> --pstxnet <pst>
```

Explicit files mode retains the legacy entrypoint; XDCs are processed in the supplied order. Project mode derives active implementation constraints using ProcessingOrder and file membership, but effective tool/IP/scoped ordering still needs Vivado review. Without `--ports`, check every resolvable top port bit. With it, report selected coverage and still flag global duplicate-pin ownership. Parameter expressions/macros not resolved by the lightweight parser stay unknown; do not replace them with scalar widths.

The supported static subset is literal `set_property PACKAGE_PIN/IOSTANDARD` or `set_property -dict {...}` with literal `get_ports` selections, multiline lists and bus wildcards. No Tcl is executed. Dynamic/unhandled commands remain `needs_review`. Timing/non-pin commands are inventoried as outside the pin audit; static PASS does not certify them. Schema 2 keeps rows/errors/status and adds coverage, unparsed commands, review reasons, ignored commands and input hashes. Exit 0 only for pass; fail/needs_review exits 2.

Dedicated pads need a reviewed evidence JSON with `part`, `evidence_file`, `evidence_sha256`, and `pins` mapping balls to exact MGT package-pin functions (for example `MGTHTXP0_...`, not a top signal name). Pass `--dedicated-pins <json>` with project part or explicit `--part`. The referenced evidence file must exist with the recorded hash. This checks provenance/shape, not the truth of a manually transcribed table: review the actual vendor package table or Vivado package-pin report before supplying it. Missing evidence does not authorize fabricated fabric IOSTANDARD.

`validate-cw-test-sources.ps1 -Project <xpr>` is membership-only. Add `-SzsdPstxnet` for pin audit. Legacy `-Top` means expected RTL file; `-ExpectedTop` means module. Optional `-Xdc` must agree with the derived list. No default project/board path or universal top/part is imposed. `-Output` retains JSON; otherwise stdout, no temporary report deletion.

## Applied IO and simulation

`vivado_io_audit.tcl` accepts `<xpr> <new-output-dir> [--run synth_1|impl_1] [port-pattern ...]`. It opens the project read-only, requires Complete/100%/NEEDS_REFRESH=false, and resolves each pattern independently. Tool freshness is not a historical input-hash proof. It never launches runs. For device-specific dedicated-pad exemption it queries package-pin PIN_FUNC; absent support requires review rather than name-based exemption.

The shared XSim wrapper defaults to a 600-second wall timeout. Use `-TranscriptPath` for the actual simulator log under the fresh run directory; the Tcl must arrange that output location. It requires a simulator-identifying transcript and exactly one `TB_PASS checks=N` with N>0, no TB_FAIL/FATAL/ERROR, and zero launcher exit. Console-only PASS, old logs, zero checks and timeout fail. It is a trusted-runner guard, not protection against a deliberately falsified simulator transcript. Timeout terminates only the launcher's process tree and preserves evidence. Paths with command-shell quote/newline/percent/exclamation characters are rejected.

Run `tests/test_toolchain.py` for synthetic behavior regressions. Real project reports and hardware results remain separate acceptance levels; do not launch a full build to test skill wording.

## Logical IP evidence

See [IP and repeat validation](ip-and-repeat-validation.md) for additive `logical_ips`, `active_ip_count`, `containers` and virtual-member semantics. BlockSrcs OOC associations are included. CRC/identity failures cannot pass; unknown associations return `needs_review`. Native IP layout is judged by role, not by the BlockSrcs fileset name. `--stage` controls constraint inclusion. Historical ImportPath/run metadata is not a live dependency.
