[CmdletBinding()]
param(
    [string]$Project = 'F:\01_Laser\code\fpga\projects\cw_test_202608\AD766_RF_test\vivado_project\AD766_RF_test.xpr',
    [string]$Top = 'F:\01_Laser\code\fpga\projects\cw_test_202608\AD766_RF_test\src\AD677_IO_DDS_TOP.v',
    [string]$Xdc = 'F:\01_Laser\code\fpga\projects\cw_test_202608\AD766_RF_test\cons\AD677_IO_DDS_TOP.xdc',
    [string]$SzsdPstxnet = 'F:\01_Laser\0_20260727_513test\04_共用硬件设计资料\超稳原理图pcb_王老师\1.SZSD\SZSD-202401770C-JXG20260516(公开)\allegro_wang\pstxnet.dat',
    [string]$FpgaRefdes = 'D1'
)

$ErrorActionPreference = 'Stop'
$errors = [System.Collections.Generic.List[string]]::new()
$passes = [System.Collections.Generic.List[string]]::new()
function Add-Error([string]$Message) { $script:errors.Add($Message) }
function Add-Pass([string]$Message) { $script:passes.Add($Message) }

foreach ($path in @($Project, $Top, $Xdc, $SzsdPstxnet)) {
    if (-not (Test-Path -LiteralPath $path)) { Add-Error "Missing authoritative path: $path" }
}
if ($errors.Count) { $errors | ForEach-Object { Write-Host "[ERROR] $_" -ForegroundColor Red }; exit 1 }

$xprText = [IO.File]::ReadAllText($Project)
if ($xprText -match '<Option Name="Part" Val="xc7vx690tffg1761-2L"') { Add-Pass 'Vivado part matches.' } else { Add-Error 'Unexpected Vivado part.' }
if ($xprText -match '<Option Name="TopModule" Val="AD677_IO_DDS_TOP"') { Add-Pass 'Current top matches.' } else { Add-Error 'Current source-set top is not AD677_IO_DDS_TOP.' }
foreach ($sourceName in @('AD677_IO_DDS_TOP.v','module_telemetry_adg526_ad677_test.v')) {
    $sourceMatch = [regex]::Match($xprText, '<File Path="[^"]*/' + [regex]::Escape($sourceName) + '">\s*<FileInfo>(.*?)</FileInfo>', 'Singleline')
    if (-not $sourceMatch.Success) { Add-Error "Required source is absent from XPR: $sourceName" }
    elseif ($sourceMatch.Groups[1].Value -match 'Name="AutoDisabled"\s+Val="1"') { Add-Error "Required source is AutoDisabled: $sourceName" }
}
if ($xprText -notmatch 'AD677_IO_DDS_TOP\.xdc') { Add-Error 'Current target XDC is absent from the XPR.' } else { Add-Pass 'Current target XDC is in the XPR.' }

$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$bundledPython = 'C:\Users\86183\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$pinnedPython = Join-Path $codexHome 'tools\io-gen-c852b04\.venv\Scripts\python.exe'
$python = if (Test-Path -LiteralPath $bundledPython) { $bundledPython } elseif (Test-Path -LiteralPath $pinnedPython) { $pinnedPython } else { (Get-Command py -ErrorAction SilentlyContinue).Source }
if (-not $python) { $python = (Get-Command python -ErrorAction SilentlyContinue).Source }
if (-not $python) { Add-Error 'Python interpreter not found for RTL/XDC/PST audit.' }
else {
    $auditScript = Join-Path (Split-Path $PSScriptRoot -Parent) '..\rtl-schematic-xdc-alignment\scripts\rtl_xdc_pst_audit.py'
    $auditScript = [IO.Path]::GetFullPath($auditScript)
    if (-not (Test-Path -LiteralPath $auditScript)) {
        $codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
        $auditScript = Join-Path $codexHome 'skills\rtl-schematic-xdc-alignment\scripts\rtl_xdc_pst_audit.py'
    }
    if (-not (Test-Path -LiteralPath $auditScript)) { Add-Error "Static audit script not found: $auditScript" }
    else {
        $auditOutput = Join-Path ([IO.Path]::GetTempPath()) ("cw_rtl_xdc_pst_audit_{0}.json" -f [Guid]::NewGuid().ToString('N'))
        try {
            & $python $auditScript --rtl $Top --top AD677_IO_DDS_TOP --xdc $Xdc --pstxnet $SzsdPstxnet --fpga-refdes $FpgaRefdes --output $auditOutput
            if ($LASTEXITCODE -ne 0) {
                if (Test-Path -LiteralPath $auditOutput) {
                    $audit = Get-Content -LiteralPath $auditOutput -Raw | ConvertFrom-Json
                    $audit.errors | ForEach-Object { Add-Error $_ }
                } else { Add-Error 'RTL/XDC/PST audit failed without output.' }
            } else {
                $audit = Get-Content -LiteralPath $auditOutput -Raw | ConvertFrom-Json
                Add-Pass "RTL/XDC/PST static audit passed for $($audit.rows.Count) constrained ports."
            }
        } finally {
            if (Test-Path -LiteralPath $auditOutput) { Remove-Item -LiteralPath $auditOutput -Force }
        }
    }
}

Write-Host "PASS=$($passes.Count) ERROR=$($errors.Count)"
$passes | ForEach-Object { Write-Host "[PASS] $_" }
if ($errors.Count) {
    $errors | ForEach-Object { Write-Host "[ERROR] $_" -ForegroundColor Red }
    exit 1
}
Write-Host 'CW qualification-test authority and pin audit passed.' -ForegroundColor Green
exit 0
