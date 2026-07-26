param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$IoGenArgs
)

$ErrorActionPreference = 'Stop'
$ioGen = 'C:\Users\Administrator\.codex\tools\io-gen-c852b04\.venv\Scripts\io-gen.exe'
if (-not (Test-Path -LiteralPath $ioGen)) {
    throw "Pinned io-gen executable not found: $ioGen"
}

& $ioGen @IoGenArgs
exit $LASTEXITCODE
