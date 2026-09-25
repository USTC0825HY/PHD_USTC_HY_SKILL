[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Path,

    [switch]$SkipHash
)

$ErrorActionPreference = 'Stop'

$rootItem = Get-Item -LiteralPath $Path
if (-not $rootItem.PSIsContainer) {
    throw "Path is not a directory: $Path"
}

$root = $rootItem.FullName.TrimEnd('\')
$items = @(Get-ChildItem -LiteralPath $root -Force -Recurse | Sort-Object FullName)

$records = foreach ($item in $items) {
    $relativePath = $item.FullName.Substring($root.Length).TrimStart('\')
    $hash = $null
    if (-not $item.PSIsContainer -and -not $SkipHash) {
        $hash = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash
    }

    [PSCustomObject]@{
        relativePath = $relativePath
        kind = if ($item.PSIsContainer) { 'directory' } else { 'file' }
        extension = if ($item.PSIsContainer) { $null } else { $item.Extension.ToLowerInvariant() }
        bytes = if ($item.PSIsContainer) { $null } else { $item.Length }
        lastWriteTime = $item.LastWriteTime.ToString('o')
        sha256 = $hash
    }
}

[PSCustomObject]@{
    root = $root
    generatedAt = (Get-Date).ToString('o')
    itemCount = $records.Count
    fileCount = @($records | Where-Object { $_.kind -eq 'file' }).Count
    directoryCount = @($records | Where-Object { $_.kind -eq 'directory' }).Count
    items = $records
} | ConvertTo-Json -Depth 5
