param(
    [Parameter(Mandatory=$true)][string]$InputDocx,
    [Parameter(Mandatory=$true)][string]$PdfPath,
    [switch]$SaveUpdated,
    [string]$UpdatedDocx,
    [switch]$SkipSanitize,
    [switch]$RestyleTables,
    [switch]$NormalizeFonts,
    [string]$PythonExe,
    [string]$WorkDir
)
$ErrorActionPreference = 'Stop'
$inputPath = (Resolve-Path -LiteralPath $InputDocx).Path
$pdfFullPath = [IO.Path]::GetFullPath($PdfPath)
if ([IO.Path]::GetExtension($pdfFullPath) -ne '.pdf') { throw 'PdfPath must end in .pdf' }
if (Test-Path -LiteralPath $pdfFullPath) { throw 'PDF output already exists; choose a new output file' }
if (Test-Path -LiteralPath (Join-Path (Split-Path $inputPath) ('~$'+[IO.Path]::GetFileName($inputPath)))) { throw 'Source has a Word owner lock' }
if ($SaveUpdated) {
    if (-not $UpdatedDocx) { $UpdatedDocx = Join-Path (Split-Path $inputPath) ([IO.Path]::GetFileNameWithoutExtension($inputPath)+'_refreshed.docx') }
    $updatedPath = [IO.Path]::GetFullPath($UpdatedDocx)
    if ($updatedPath -eq $inputPath -or (Test-Path -LiteralPath $updatedPath)) { throw 'UpdatedDocx must be a new output copy, not the source/existing file' }
}
if ($SkipSanitize -and ($RestyleTables -or $NormalizeFonts)) { throw 'SkipSanitize conflicts with explicit normalization' }
if ($RestyleTables -or $NormalizeFonts) {
    if (-not $PythonExe -or -not (Test-Path -LiteralPath $PythonExe)) { throw 'Explicit sanitation requires a verified PythonExe' }
    & $PythonExe -B -c 'import sys, docx, lxml; assert sys.version_info >= (3,10)'
    if ($LASTEXITCODE -ne 0) { throw 'Python runtime/import probe failed' }
}
if (-not $WorkDir) {
    if ($inputPath.StartsWith('F:\01_Laser\',[StringComparison]::OrdinalIgnoreCase)) {
        $WorkDir = 'F:\01_Laser\.codex_work\'+(Get-Date -Format yyyyMMdd)+'-docx-export'
    } else { $WorkDir = Join-Path $env:TEMP 'laser-docx-export' }
}
$taskDir = Join-Path ([IO.Path]::GetFullPath($WorkDir)) ([guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $taskDir -Force | Out-Null
$copyPath = Join-Path $taskDir 'refreshed.docx'
$tempPdf = Join-Path $taskDir 'refreshed.pdf'
# An exclusive read also rejects an open source without a Word owner file.
$stream = [IO.File]::Open($inputPath,'Open','Read','None')
try {
    $hashBefore = (Get-FileHash -InputStream $stream -Algorithm SHA256).Hash
    $stream.Position = 0
    $dest = [IO.File]::Open($copyPath,'CreateNew','Write','None')
    try { $stream.CopyTo($dest) } finally { $dest.Dispose() }
} finally { $stream.Dispose() }
function With-WordDocument([string]$path,[bool]$refresh,[string]$export) {
    $app = $null; $doc = $null
    try {
        $app = New-Object -ComObject Word.Application
        $app.Visible = $false; $app.DisplayAlerts = 0
        $doc = $app.Documents.Open($path,$false,$false)
        if ($refresh) {
            $doc.Fields.Update() | Out-Null
            foreach ($range in $doc.StoryRanges) {
                $part = $range
                while ($null -ne $part) { $part.Fields.Update() | Out-Null; $part = $part.NextStoryRange }
            }
            foreach ($toc in $doc.TablesOfContents) { $toc.Update(); $doc.Repaginate(); $toc.UpdatePageNumbers() }
            $doc.Repaginate()
            $doc.Save() # Always persist refreshed fields to the private copy.
        }
        if ($export) { $doc.ExportAsFixedFormat($export,17) }
    } finally {
        if ($null -ne $doc) { $doc.Close($false); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($doc) }
        if ($null -ne $app) { $app.Quit(); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app) }
    }
}
With-WordDocument $copyPath $true ''
# No implicit whole-document sanitation for local revisions.
if ($RestyleTables -or $NormalizeFonts) {
    $sanitizeArgs = @('-B',(Join-Path $PSScriptRoot 'sanitize_docx_layout.py'),$copyPath)
    if ($RestyleTables) { $sanitizeArgs += '--restyle-tables' }
    if ($NormalizeFonts) { $sanitizeArgs += '--normalize-fonts' }
    & $PythonExe @sanitizeArgs
    if ($LASTEXITCODE -ne 0) { throw 'DOCX sanitizer failed' }
}
With-WordDocument $copyPath $false $tempPdf
if (-not (Test-Path -LiteralPath $tempPdf) -or (Get-Item -LiteralPath $tempPdf).Length -eq 0) { throw 'PDF export missing/empty' }
if ((Get-FileHash -LiteralPath $inputPath -Algorithm SHA256).Hash -ne $hashBefore) { throw 'Source changed during export; private results retained, no output published' }
New-Item -ItemType Directory -Path (Split-Path $pdfFullPath) -Force | Out-Null
if ($SaveUpdated) {
    New-Item -ItemType Directory -Path (Split-Path $updatedPath) -Force | Out-Null
    [IO.File]::Copy($copyPath,$updatedPath,$false)
}
[IO.File]::Copy($tempPdf,$pdfFullPath,$false)
[pscustomobject]@{ Pdf=$pdfFullPath; UpdatedDocx=$(if($SaveUpdated){$updatedPath}else{$null}); SourceUnchanged=$true; WorkingCopy=$copyPath; WholeDocumentSanitation=[bool]($RestyleTables -or $NormalizeFonts) } | ConvertTo-Json
