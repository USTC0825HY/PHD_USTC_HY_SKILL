# Usage: vivado ... -tclargs project.xpr output-dir ?--run synth_1|impl_1? ?port-pattern ...?
# Read-only project inspection; reports write only to a NEW explicit output directory.
if {$argc < 2} {puts stderr "project.xpr output-dir ?--run name? ?port ...?"; exit 2}
set project_path [file normalize [lindex $argv 0]]
set output_dir [file normalize [lindex $argv 1]]
if {[file exists $output_dir]} {puts stderr "Output already exists; preserve prior evidence"; exit 2}
file mkdir $output_dir
set run_name synth_1
set requested_ports [lrange $argv 2 end]
if {[lindex $requested_ports 0] eq "--run"} {
    set run_name [lindex $requested_ports 1]
    set requested_ports [lrange $requested_ports 2 end]
}
proc audit_fail {message} {
    global output_dir
    set fp [open [file join $output_dir vivado_io_status.txt] w]
    puts $fp "NOT_VERIFIED: $message"
    close $fp
    catch {close_project}
    puts stderr $message
    exit 3
}
if {[catch {open_project -read_only $project_path} problem]} {audit_fail $problem}
set run [get_runs -quiet $run_name]
if {[llength $run] != 1} {audit_fail "Missing/ambiguous run $run_name"}
foreach property {PROGRESS STATUS NEEDS_REFRESH} {
    if {[catch {get_property $property $run} value] || $value eq ""} {audit_fail "Unknown run $property"}
    set run_property($property) $value
}
if {$run_property(PROGRESS) ne "100%" || ![string match "*Complete*" $run_property(STATUS)] ||
    ![string is boolean -strict $run_property(NEEDS_REFRESH)] || $run_property(NEEDS_REFRESH)} {
    audit_fail "Run is incomplete, stale or freshness unknown"
}
if {[catch {open_run $run_name} problem]} {audit_fail $problem}
set ports {}
foreach pattern $requested_ports {
    set matched [get_ports -quiet $pattern]
    if {![llength $matched]} {audit_fail "Empty port selection: $pattern"}
    set ports [concat $ports $matched]
}
if {![llength $requested_ports]} {set ports [get_ports]}
set ports [lsort -unique $ports]
if {![llength $ports]} {audit_fail "No ports"}
set fp [open [file join $output_dir vivado_io_ports.tsv] w]
puts $fp "port\tdirection\tpackage_pin\tiostandard\tbank\tpin_function"
array set pin_owner {}
set failures {}
foreach port $ports {
    set pin [get_property PACKAGE_PIN $port]
    set standard [get_property IOSTANDARD $port]
    set bank ""
    set function ""
    if {$pin eq ""} {lappend failures "Missing PACKAGE_PIN: $port"} else {
        set package_pin [get_package_pins -quiet $pin]
        if {[llength $package_pin] != 1} {lappend failures "Unknown package pin: $port/$pin"} else {
            set bank [get_property BANK $package_pin]
            if {[lsearch -exact [list_property $package_pin] PIN_FUNC] >= 0} {set function [get_property PIN_FUNC $package_pin]}
        }
        if {[info exists pin_owner($pin)] && $pin_owner($pin) ne $port} {lappend failures "Duplicate PACKAGE_PIN $pin"}
        set pin_owner($pin) $port
    }
    set dedicated [regexp {^MGT([HPX](TX|RX)|REFCLK)} $function]
    if {($standard eq "" || $standard eq "DEFAULT") && !$dedicated} {lappend failures "Missing fabric IOSTANDARD: $port (function=$function)"}
    puts $fp "$port\t[get_property DIRECTION $port]\t$pin\t$standard\t$bank\t$function"
}
close $fp
report_io -file [file join $output_dir report_io.rpt]
if {[llength $failures]} {audit_fail [join $failures "; "]}
set fp [open [file join $output_dir vivado_io_status.txt] w]
puts $fp "Vivado applied IO reviewed: project=$project_path run=$run_name tool=[version -short]"
puts $fp "Freshness: NEEDS_REFRESH=false reported by Vivado; historical input hashes and board behavior NOT proven."
puts $fp "Scope: $ports"
close $fp
close_project
exit 0
