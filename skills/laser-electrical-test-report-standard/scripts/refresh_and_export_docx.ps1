param(
    [Parameter(Mandatory = $true)]
    [string]$InputDocx,
    [Parameter(Mandatory = $true)]
    [string]$PdfPath,
    [switch]$SaveUpdated,
    [switch]$SkipSanitize
)

$ErrorActionPreference = 'Stop'
$inputPath = (Resolve-Path -LiteralPath $InputDocx).Path
$pdfFullPath = [System.IO.Path]::GetFullPath($PdfPath)
$pdfDir = Split-Path -Parent $pdfFullPath
if (-not (Test-Path -LiteralPath $pdfDir)) {
    New-Item -ItemType Directory -Path $pdfDir -Force | Out-Null
}

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $null
try {
    $doc = $word.Documents.Open($inputPath, $false, $false)
    $doc.Fields.Update() | Out-Null
    foreach ($toc in $doc.TablesOfContents) {
        $toc.Update()
        $doc.Repaginate()
        $toc.UpdatePageNumbers()
    }
    if ($SaveUpdated) {
        $doc.Save()
    }
    $wdExportFormatPDF = 17
    $doc.ExportAsFixedFormat($pdfFullPath, $wdExportFormatPDF)
    Write-Output $pdfFullPath
}
finally {
    if ($null -ne $doc) {
        $doc.Close($false)
    }
    if ($null -ne $word) {
        $word.Quit()
    }
}

if ($SaveUpdated -and -not $SkipSanitize) {
    $sanitizer = Join-Path $PSScriptRoot 'sanitize_docx_layout.py'
    & python $sanitizer $inputPath | Out-Null
}
