# New Vivado Project Build Defaults

Use these defaults when creating a new Vivado project. Existing projects remain evidence-driven: inspect their XPR, runs, IP, and local instructions before changing settings.

## Safe project creation

Follow [native layout](native-project-layout.md) and [stage usage](stage-template-usage.md). Create the native empty project before writing final .srcs inputs; Vivado 2018.3 refuses pre-existing .srcs without force. Never use force to bypass this. Stage defaults to create only. Check property/IP/run support in the selected version; stop for an explicit exception when unsupported rather than silently changing policy.

Do not use an unconditional `create_project -force`. If the expected XPR already exists, open it and verify the project name, part, top, and source roots before resuming. If the target directory is nonempty but no compatible XPR exists, stop with a clear error instead of overwriting files.

```tcl
if {[file exists $xpr]} {
    open_project $xpr
    if {[get_property PART [current_project]] ne $expected_part} {
        error "Existing project part mismatch"
    }
} else {
    create_project $project_name $project_dir -part $expected_part
}
```

## XCI OOC synthesis

After all IP is added or created, require at least one XCI when the design is expected to contain IP. A generic template may diagnose an empty set without failing.

```tcl
set xci_files [get_files -quiet *.xci]
if {[llength $xci_files] == 0} {
    puts "WARNING: no XCI files found; OOC policy has no targets"
} else {
    set_property GENERATE_SYNTH_CHECKPOINT true $xci_files
    foreach xci $xci_files {
        if {![get_property GENERATE_SYNTH_CHECKPOINT $xci]} {
            error "Failed to enable OOC synthesis for $xci"
        }
    }
}
```

`GENERATE_SYNTH_CHECKPOINT=false` is an explicit diagnostic or rollback operation only. Do not make it the new-project default.

## Project-mode incremental implementation

Require `impl_1` and enable automatic checkpoint handoff. Vivado 2018.3 accepts the integer form `1`; use integer `0/1` when supporting that release.

```tcl
set impl_run [get_runs -quiet impl_1]
if {[llength $impl_run] != 1} {
    error "Expected implementation run impl_1"
}
set_property AUTO_INCREMENTAL_CHECKPOINT 1 $impl_run
if {![get_property AUTO_INCREMENTAL_CHECKPOINT $impl_run]} {
    error "AUTO_INCREMENTAL_CHECKPOINT readback failed"
}
```

The first implementation normally has no reference DCP. That is not an error; a completed run becomes the automatic reference for a later implementation.

## Manual DCP override

Manual mode has higher priority for that run only. Before setting `INCREMENTAL_CHECKPOINT`, verify that the path exists and open the checkpoint to check at minimum the FPGA part plus project-specific interface/topology signatures. Prefer checking the expected top hierarchy, external port count/names, and any critical interface cells. Reject an unvalidated or placeholder path.

```tcl
open_checkpoint $validated_dcp
# Project-specific compatibility assertions go here.
close_design
set_property AUTO_INCREMENTAL_CHECKPOINT 0 [get_runs impl_1]
set_property INCREMENTAL_CHECKPOINT $validated_dcp [get_runs impl_1]
```

After the manual build and release evidence are captured, clear the manual reference and restore the project default:

```tcl
set_property INCREMENTAL_CHECKPOINT {} [get_runs impl_1]
set_property AUTO_INCREMENTAL_CHECKPOINT 1 [get_runs impl_1]
```

If validation fails, stop before resetting or launching implementation. Do not silently fall back to a different DCP.

## Non-project mode injection point

Validate the checkpoint before opening the implementation flow. The injection point is fixed:

```tcl
opt_design
read_checkpoint -incremental $validated_dcp
place_design
```

Do not move `read_checkpoint -incremental` before `opt_design` or after `place_design`.

## Release evidence

Record whether the run used no reference, automatic incremental reuse, or a validated manual DCP. Preserve timing, DRC, utilization, IO, incremental-reuse, bus-skew (when present), routed DCP, bitstream, probes, and an input manifest. A reused checkpoint does not relax timing or DRC acceptance criteria.
