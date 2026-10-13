param(
    [switch]$Help,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$TraceArgs
)

$ErrorActionPreference = 'Stop'
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$profilePath = Join-Path $codexHome 'laser-fpga-profile.json'
$python = $null
$bundled = 'C:\Users\86183\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (Test-Path -LiteralPath $bundled) { $python = $bundled }
if (-not $python -and (Test-Path -LiteralPath $profilePath)) {
    $profile = Get-Content -LiteralPath $profilePath -Raw | ConvertFrom-Json
    if ($profile.python_executable -and (Test-Path -LiteralPath $profile.python_executable)) { $python = $profile.python_executable }
}
if (-not $python) { $pinned = Join-Path $codexHome 'tools\io-gen-c852b04\.venv\Scripts\python.exe'; if (Test-Path -LiteralPath $pinned) { $python = $pinned } }
if (-not $python) { $command = Get-Command py -ErrorAction SilentlyContinue; if ($command) { $python = $command.Source } }
if (-not $python) { $command = Get-Command python -ErrorAction SilentlyContinue; if ($command) { $python = $command.Source } }
if (-not $python) { throw 'Python interpreter not found.' }

$script = Join-Path $PSScriptRoot 'pst_signal_trace.py'
if ($Help) {
    & $python $script --help
} else {
    & $python $script @TraceArgs
}
exit $LASTEXITCODE
