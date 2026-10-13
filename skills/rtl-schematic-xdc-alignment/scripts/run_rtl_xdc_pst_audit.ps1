param(
    [switch]$Help,
    [string]$PythonPath,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$AuditArgs
)

$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/../../fpga-vivado-tcl-automation/scripts/resolve_python.ps1"
$python = Resolve-FpgaPython -ExplicitPath $PythonPath
$script = Join-Path $PSScriptRoot 'rtl_xdc_pst_audit.py'
if ($Help) { & $python -X utf8 -B $script --help } else { & $python -X utf8 -B $script @AuditArgs }
exit $LASTEXITCODE
