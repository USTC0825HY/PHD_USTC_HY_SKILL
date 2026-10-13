param(
    [string] $OutputPath,
    [ValidateRange(1, 65535)]
    [int] $ProxyPort,
    [string] $ExpectedProxyPathPattern,
    [string] $TailscalePeer,
    [string] $TestHost = 'www.microsoft.com',
    [string] $TestUrl = 'https://www.microsoft.com'
)

$ErrorActionPreference = 'Stop'

function Invoke-ValidationSafe {
    param([scriptblock] $Script)
    try {
        & $Script
    } catch {
        [pscustomobject]@{ Success = $false; Error = $_.Exception.Message }
    }
}

$proxyValidation = $null
if ($PSBoundParameters.ContainsKey('ProxyPort')) {
    $listeners = @(Get-NetTCPConnection -State Listen -LocalPort $ProxyPort -ErrorAction SilentlyContinue)
    $owners = @($listeners | ForEach-Object {
        $process = Get-CimInstance Win32_Process -Filter "ProcessId=$($_.OwningProcess)" -ErrorAction SilentlyContinue
        [pscustomobject]@{
            Address        = $_.LocalAddress
            Port           = $_.LocalPort
            Pid            = $_.OwningProcess
            Name           = $process.Name
            ExecutablePath = $process.ExecutablePath
            PathMatches    = if ($ExpectedProxyPathPattern) {
                $process.ExecutablePath -like $ExpectedProxyPathPattern
            } else {
                $null
            }
        }
    })
    $proxyValidation = [ordered]@{
        Port      = $ProxyPort
        Listeners = $owners
        Pass      = $owners.Count -gt 0 -and (
            -not $ExpectedProxyPathPattern -or
            @($owners | Where-Object PathMatches).Count -gt 0
        )
    }
}

$tailscale = $null
$tailscaleExe = 'C:\Program Files\Tailscale\tailscale.exe'
if (Test-Path -LiteralPath $tailscaleExe) {
    $status = Invoke-ValidationSafe {
        & $tailscaleExe status --json 2>$null | Out-String | ConvertFrom-Json
    }
    $ping = $null
    if ($TailscalePeer) {
        $ping = Invoke-ValidationSafe {
            (& $tailscaleExe ping --c 3 $TailscalePeer 2>&1 | Out-String).Trim()
        }
    }
    $service = Get-Service -Name Tailscale -ErrorAction SilentlyContinue
    $tailscale = [ordered]@{
        ServiceStatus = [string]$service.Status
        StartType     = [string]$service.StartType
        BackendState  = $status.BackendState
        SelfOnline    = $status.Self.Online
        IPs           = $status.TailscaleIPs
        Ping          = $ping
        Pass          = $service.Status -eq 'Running' -and
            $status.BackendState -eq 'Running' -and
            $status.Self.Online -eq $true
    }
}

$cameras = @(Get-PnpDevice -PresentOnly -ErrorAction SilentlyContinue |
    Where-Object Class -eq 'Camera' |
    Select-Object FriendlyName, Status, InstanceId)

$result = [ordered]@{
    Timestamp = (Get-Date).ToString('o')
    DNS = Invoke-ValidationSafe {
        $answer = Resolve-DnsName $TestHost -Type A -ErrorAction Stop
        [pscustomobject]@{
            Success   = @($answer | Where-Object IPAddress).Count -gt 0
            Host      = $TestHost
            Addresses = @($answer | Where-Object IPAddress | Select-Object -ExpandProperty IPAddress)
        }
    }
    HTTPS = Invoke-ValidationSafe {
        $response = Invoke-WebRequest -Uri $TestUrl -Method Head -UseBasicParsing -TimeoutSec 15 -ErrorAction Stop
        [pscustomobject]@{
            Success = $response.StatusCode -ge 200 -and $response.StatusCode -lt 500
            Url     = $TestUrl
            Status  = $response.StatusCode
        }
    }
    Proxy = $proxyValidation
    Tailscale = $tailscale
    Cameras = [ordered]@{
        Devices = $cameras
        Pass    = $cameras.Count -eq 0 -or @($cameras | Where-Object Status -ne 'OK').Count -eq 0
    }
    WinHttpProxy = (netsh.exe winhttp show proxy 2>&1) -join "`n"
    PrivacyNote = 'This local result can contain IP addresses and executable paths. Review before sharing.'
}

$json = $result | ConvertTo-Json -Depth 7
if ($OutputPath) {
    $resolvedOutput = [System.IO.Path]::GetFullPath($OutputPath)
    $outputDirectory = Split-Path -Parent $resolvedOutput
    if (-not (Test-Path -LiteralPath $outputDirectory)) {
        New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
    }
    $json | Set-Content -LiteralPath $resolvedOutput -Encoding UTF8
    Write-Output $resolvedOutput
} else {
    Write-Output $json
}
