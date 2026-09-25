param(
    [Parameter(Mandatory)]
    [string] $OutputPath,

    [ValidateRange(3, 60)]
    [int] $SampleSeconds = 10
)

$ErrorActionPreference = 'Stop'

function Invoke-AuditSafe {
    param([scriptblock] $Script)
    try {
        & $Script
    } catch {
        [pscustomobject]@{ AuditError = $_.Exception.Message }
    }
}

$resolvedOutput = [System.IO.Path]::GetFullPath($OutputPath)
$outputDirectory = Split-Path -Parent $resolvedOutput
if (-not (Test-Path -LiteralPath $outputDirectory)) {
    New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
}

$os = Get-CimInstance Win32_OperatingSystem
$computer = Get-CimInstance Win32_ComputerSystem
$deviceGuard = Get-CimInstance -Namespace root\Microsoft\Windows\DeviceGuard -ClassName Win32_DeviceGuard -ErrorAction SilentlyContinue

$counterPaths = @(
    '\Processor(_Total)\% Processor Time',
    '\Memory\Available MBytes',
    '\Memory\% Committed Bytes In Use',
    '\PhysicalDisk(_Total)\% Disk Time',
    '\PhysicalDisk(_Total)\Avg. Disk Queue Length',
    '\PhysicalDisk(_Total)\Avg. Disk sec/Transfer',
    '\System\Processor Queue Length'
)
$counterSample = Invoke-AuditSafe {
    $samples = Get-Counter -Counter $counterPaths -SampleInterval 1 -MaxSamples $SampleSeconds
    @($samples.CounterSamples |
        Where-Object Status -eq 0 |
        Group-Object Path |
        ForEach-Object {
            $values = @($_.Group.CookedValue)
            [pscustomobject]@{
                Counter = $_.Name
                Average = [math]::Round(($values | Measure-Object -Average).Average, 3)
                Maximum = [math]::Round(($values | Measure-Object -Maximum).Maximum, 3)
                Minimum = [math]::Round(($values | Measure-Object -Minimum).Minimum, 3)
            }
        })
}

$cimProcessMap = @{}
Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | ForEach-Object {
    $cimProcessMap[[int]$_.ProcessId] = $_
}
$processes = @(Get-Process -ErrorAction SilentlyContinue | ForEach-Object {
    $cim = $cimProcessMap[[int]$_.Id]
    [pscustomobject]@{
        Name           = $_.ProcessName
        Id             = $_.Id
        WorkingSetMB   = [math]::Round($_.WorkingSet64 / 1MB, 1)
        PrivateMB      = [math]::Round($_.PrivateMemorySize64 / 1MB, 1)
        CPUSeconds     = if ($null -ne $_.CPU) { [math]::Round($_.CPU, 2) } else { $null }
        Threads        = $_.Threads.Count
        ExecutablePath = $cim.ExecutablePath
        CommandLine    = $cim.CommandLine
    }
})

$runEntries = @()
foreach ($location in @(
    @{ Scope = 'HKCU'; Path = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' },
    @{ Scope = 'HKLM64'; Path = 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Run' },
    @{ Scope = 'HKLM32'; Path = 'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run' }
)) {
    if (-not (Test-Path -LiteralPath $location.Path)) {
        continue
    }
    $item = Get-ItemProperty -LiteralPath $location.Path
    foreach ($property in $item.PSObject.Properties | Where-Object Name -notmatch '^PS') {
        $runEntries += [pscustomobject]@{
            Scope   = $location.Scope
            Path    = $location.Path
            Name    = $property.Name
            Command = [string]$property.Value
        }
    }
}

$bootTime = $os.LastBootUpTime
$report = [ordered]@{
    GeneratedAt = (Get-Date).ToString('o')
    SampleType  = 'Point-in-time plus bounded counters'
    System      = [ordered]@{
        Manufacturer     = $computer.Manufacturer
        Model            = $computer.Model
        OS               = $os.Caption
        Version          = $os.Version
        Build            = $os.BuildNumber
        BootTime         = $bootTime.ToString('o')
        CPU              = @(Get-CimInstance Win32_Processor |
            Select-Object Name, NumberOfCores, NumberOfLogicalProcessors, MaxClockSpeed, LoadPercentage)
        TotalMemoryGB     = [math]::Round($computer.TotalPhysicalMemory / 1GB, 2)
        FreeMemoryGB      = [math]::Round($os.FreePhysicalMemory * 1KB / 1GB, 2)
        ProcessCount      = $processes.Count
        HypervisorPresent = [bool]$computer.HypervisorPresent
        VBSStatus         = $deviceGuard.VirtualizationBasedSecurityStatus
    }
    Counters    = $counterSample
    Processes   = [ordered]@{
        TotalWorkingSetGB = [math]::Round(($processes | Measure-Object WorkingSetMB -Sum).Sum / 1024, 2)
        TopWorkingSet     = @($processes | Sort-Object WorkingSetMB -Descending | Select-Object -First 30)
        All               = $processes
    }
    Startup     = [ordered]@{
        RegistryRun = $runEntries
        Commands    = @(Invoke-AuditSafe {
            Get-CimInstance Win32_StartupCommand |
                Select-Object Name, Command, Location, User
        })
        BootLogonTasks = @(Invoke-AuditSafe {
            Get-ScheduledTask -ErrorAction SilentlyContinue |
                Where-Object { @($_.Triggers.CimClass.CimClassName) -match 'BootTrigger|LogonTrigger' } |
                Select-Object TaskPath, TaskName, State,
                    @{n='Actions';e={@($_.Actions | Select-Object Execute, Arguments)}}
        })
    }
    Services    = @(Get-CimInstance Win32_Service |
        Select-Object Name, DisplayName, State, StartMode, ProcessId, StartName, PathName)
    Drivers     = [ordered]@{
        ProblemDevices = @(Invoke-AuditSafe {
            Get-PnpDevice -PresentOnly |
                Where-Object Status -ne 'OK' |
                Select-Object Class, FriendlyName, Status, InstanceId, Problem
        })
        SystemDrivers = @(Get-CimInstance Win32_SystemDriver |
            Select-Object Name, DisplayName, State, StartMode, PathName)
    }
    Storage     = [ordered]@{
        PhysicalDisks = @(Invoke-AuditSafe {
            Get-PhysicalDisk |
                Select-Object FriendlyName, MediaType, BusType, HealthStatus, OperationalStatus, Size, FirmwareVersion
        })
        Volumes = @(Invoke-AuditSafe {
            Get-Volume |
                Where-Object DriveLetter |
                Select-Object DriveLetter, FileSystemLabel, FileSystem, HealthStatus, Size, SizeRemaining
        })
        PageFiles = @(Get-CimInstance Win32_PageFileUsage |
            Select-Object Name, AllocatedBaseSize, CurrentUsage, PeakUsage)
        Trim = (fsutil.exe behavior query DisableDeleteNotify 2>&1) -join "`n"
    }
    Network     = [ordered]@{
        Adapters = @(Invoke-AuditSafe {
            Get-NetAdapter -IncludeHidden |
                Select-Object Name, InterfaceDescription, Status, LinkSpeed, DriverVersion, DriverDate, ifIndex, Virtual
        })
        TcpListeners = @(Invoke-AuditSafe {
            Get-NetTCPConnection -State Listen |
                Select-Object LocalAddress, LocalPort, OwningProcess
        })
        WinHttpProxy = (netsh.exe winhttp show proxy 2>&1) -join "`n"
    }
    Power       = [ordered]@{
        ActiveScheme = (powercfg.exe /getactivescheme 2>&1) -join "`n"
        Requests     = (powercfg.exe /requests 2>&1) -join "`n"
        Battery      = @(Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue |
            Select-Object BatteryStatus, EstimatedChargeRemaining, EstimatedRunTime)
    }
    Events      = [ordered]@{
        Whea = @(Get-WinEvent -FilterHashtable @{
            LogName='System'; ProviderName='Microsoft-Windows-WHEA-Logger'; StartTime=$bootTime
        } -ErrorAction SilentlyContinue |
            Select-Object TimeCreated, Id, LevelDisplayName, Message)
        ServiceControl = @(Get-WinEvent -FilterHashtable @{
            LogName='System'; ProviderName='Service Control Manager'; StartTime=$bootTime; Level=1,2,3
        } -ErrorAction SilentlyContinue |
            Select-Object -First 50 TimeCreated, Id, LevelDisplayName, Message)
    }
    PrivacyNote = 'This local report can contain executable paths, command lines, usernames, IP addresses, and event messages. Review before sharing.'
}

$report | ConvertTo-Json -Depth 9 | Set-Content -LiteralPath $resolvedOutput -Encoding UTF8
Write-Output $resolvedOutput

