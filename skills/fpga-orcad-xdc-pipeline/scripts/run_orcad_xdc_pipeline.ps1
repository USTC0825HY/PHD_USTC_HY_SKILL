param(
    [switch]$Help,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$PipelineArgs
)

$ErrorActionPreference = 'Stop'
$python = 'C:\Users\Administrator\.codex\tools\io-gen-c852b04\.venv\Scripts\python.exe'
$script = Join-Path $PSScriptRoot 'orcad_xdc_pipeline.py'

if (-not (Test-Path -LiteralPath $python)) {
    throw "Pinned io-gen Python environment not found: $python"
}

if ($Help) {
    & $python $script --help
    exit $LASTEXITCODE
}

& $python $script @PipelineArgs
exit $LASTEXITCODE
