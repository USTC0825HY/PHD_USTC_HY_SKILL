[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$Project,
    [string]$Top, # Legacy parameter: expected top source FILE, not module name.
    [string[]]$Xdc,
    [string]$ExpectedTop,
    [string]$SzsdPstxnet,
    [string]$FpgaRefdes='D1',
    [string]$DedicatedPins,
    [string[]]$Ports,
    [string]$Output,
    [string]$PythonPath
)
$ErrorActionPreference='Stop'
. "$PSScriptRoot/../../fpga-vivado-tcl-automation/scripts/resolve_python.ps1"
$python=Resolve-FpgaPython -ExplicitPath $PythonPath
$projectPath=(Resolve-Path -LiteralPath $Project).Path
if($SzsdPstxnet){
    $scriptPath="$PSScriptRoot/../../rtl-schematic-xdc-alignment/scripts/rtl_xdc_pst_audit.py"
    $arguments=@('--project',$projectPath,'--pstxnet',$SzsdPstxnet,'--fpga-refdes',$FpgaRefdes)
    if($ExpectedTop){$arguments+=@('--top',$ExpectedTop)}
    if($Top){$arguments+=@('--rtl',$Top)}
    foreach($xdcPath in $Xdc){$arguments+=@('--xdc',$xdcPath)}
    if($DedicatedPins){$arguments+=@('--dedicated-pins',$DedicatedPins)}
    if($Ports){$arguments+=@('--ports')+$Ports}
} else {
    if($Top -or $Xdc -or $DedicatedPins -or $Ports){throw 'Pin/source override verification requires an explicit -SzsdPstxnet; omit overrides for membership-only validation.'}
    $scriptPath="$PSScriptRoot/../../fpga-vivado-tcl-automation/scripts/project_inputs.py"
    $arguments=@($projectPath,'--stage','implementation')
    if($ExpectedTop){$arguments+=@('--top',$ExpectedTop)}
}
if($Output){$arguments+=@('--output',$Output)}
& $python -X utf8 -B $scriptPath @arguments
exit $LASTEXITCODE
