# Dot-source this helper; returns a tested interpreter, installs nothing.
function Resolve-FpgaPython {
    param([string]$ExplicitPath, [string[]]$RequiredModules=@())
    $skillCodexRoot = if ($env:CODEX_HOME) {$env:CODEX_HOME} else {Join-Path $env:USERPROFILE '.codex'}
    $candidates = if($ExplicitPath) {@($ExplicitPath)} else {@(
        (Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'),
        (Join-Path $skillCodexRoot 'tools/laser-fpga-runtime/.venv/Scripts/python.exe'),
        (Get-Command python -ErrorAction SilentlyContinue).Source,
        (Get-Command py -ErrorAction SilentlyContinue).Source
    )}
    $probe = 'import sys,importlib; assert sys.version_info >= (3,10); [importlib.import_module(x) for x in sys.argv[1:]]'
    foreach($candidate in $candidates | Where-Object {$_} | Select-Object -Unique){
        try {
            $null = & $candidate -X utf8 -B -c $probe @RequiredModules 2>&1
            if($LASTEXITCODE -eq 0){return $candidate}
        } catch {continue}
    }
    throw 'No runnable Python >=3.10 with required modules. Supply -PythonPath; nothing was installed.'
}
