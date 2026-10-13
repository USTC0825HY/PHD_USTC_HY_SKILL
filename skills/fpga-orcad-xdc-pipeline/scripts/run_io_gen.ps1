param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$IoGenArgs
)

$ErrorActionPreference = 'Stop'
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$ioGen = Join-Path $codexHome 'tools\io-gen-c852b04\.venv\Scripts\io-gen.exe'
if (-not (Test-Path -LiteralPath $ioGen)) {
    throw "Pinned io-gen executable not found: $ioGen"
}

& $ioGen @IoGenArgs
exit $LASTEXITCODE
