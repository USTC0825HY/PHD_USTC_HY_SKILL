[CmdletBinding()]
param(
    [ValidateSet("all", "codex", "cc_switch")]
    [string]$Profile = "all",

    [Parameter(Mandatory = $true)]
    [string]$TargetRoot,

    [switch]$Apply
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$registryPath = Join-Path $repoRoot "registry\skills.json"
$profilePath = Join-Path $repoRoot ("profiles\" + $Profile + ".json")

if (-not (Test-Path -LiteralPath $registryPath)) {
    throw "Registry not found: $registryPath"
}
if (-not (Test-Path -LiteralPath $profilePath)) {
    throw "Profile not found: $profilePath"
}

$registry = Get-Content -LiteralPath $registryPath -Raw | ConvertFrom-Json
$profileData = Get-Content -LiteralPath $profilePath -Raw | ConvertFrom-Json
$selected = @{}
foreach ($name in $profileData.skills) {
    $selected[$name] = $true
}

$resolvedRepo = [System.IO.Path]::GetFullPath($repoRoot)
$resolvedTarget = [System.IO.Path]::GetFullPath($TargetRoot)
if ($resolvedRepo -eq $resolvedTarget) {
    throw "TargetRoot must not be the repository root."
}

Write-Host ("Mode: " + $(if ($Apply) { "APPLY" } else { "DRY-RUN" }))
Write-Host ("Profile: " + $Profile)
Write-Host ("Target: " + $resolvedTarget)

foreach ($skill in $registry.skills) {
    if (-not $selected.ContainsKey($skill.name)) {
        continue
    }
    $source = Join-Path $repoRoot $skill.canonical_path
    $destination = Join-Path $resolvedTarget $skill.name
    if (-not (Test-Path -LiteralPath $source)) {
        Write-Warning ("Missing source: " + $source)
        continue
    }
    if (Test-Path -LiteralPath $destination) {
        Write-Host ("SKIP exists: " + $destination)
        continue
    }
    Write-Host ("COPY " + $skill.name + " -> " + $destination)
    if ($Apply) {
        New-Item -ItemType Directory -Path $resolvedTarget -Force | Out-Null
        Copy-Item -LiteralPath $source -Destination $destination -Recurse
    }
}

if (-not $Apply) {
    Write-Host "Dry-run only. Re-run with -Apply to copy missing Skill directories."
}
