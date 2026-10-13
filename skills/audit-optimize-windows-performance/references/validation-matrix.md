# Validation matrix

Select checks that match the changed subsystem. Keep pre/post conditions comparable.

## Core system

| Check | Evidence | Pass condition |
|---|---|---|
| CPU | 10–30 second counter sample and per-process delta | No sustained regression; processor queue remains low |
| Memory | Available MB, commit %, page-file usage | No new pressure or paging spike |
| Storage | Disk time, queue, latency, health | No new error; latency and queue remain low |
| Stability | WHEA and storage events since change | No new hardware/storage critical event |
| Target state | Registry/service/package/process query | Exact approved target changed; nothing broader |

## Startup and services

- Confirm the backed-up Run value or task before removal.
- Confirm the optional UI is absent after a clean sign-in.
- Confirm the preserved service remains in its original start mode and state.
- For Manual services, launch the owning application once and verify on-demand behavior.
- Recheck SCM 7000/7001/7009/7011 events after the next boot.

## Proxy, VPN, and networking

| Check | Pass condition |
|---|---|
| DNS | A/AAAA lookup succeeds |
| HTTPS | Known official endpoint returns a valid HTTP response |
| Proxy port | Intended executable path owns the configured TCP/UDP port |
| System proxy | Matches the documented pre-change state |
| WinHTTP proxy | Matches the documented pre-change state |
| Tailscale service | Running with intended start type |
| Tailscale backend | `Running`, self online, IPs present |
| Peer test | At least one required peer responds |
| Wi-Fi | Adapter Up, gateway reachable, no material latency/loss regression |
| Driver/binding | Only approved service, driver, or adapter binding changed |

Do not treat DERP relay use as failure unless direct connectivity was a requirement. Report it.

## Virtualization

- Check `HypervisorPresent`.
- Query `Win32_DeviceGuard` VBS and security-service states.
- Test WSL2, Docker, Sandbox, Hyper-V VMs, or emulators the user requires.
- Re-run a comparable memory/CPU benchmark.
- Verify Tailscale, sleep/wake, and network adapters after reboot.

## Power

- Record AC/DC source.
- Verify active base scheme and power-mode overlay separately.
- Query processor maximum state, boost mode, and PCIe ASPM indices.
- Compare sustained workload, not only a short burst.
- Do not claim thermal success without temperature or throttling evidence.

## Camera and sensing

- Confirm physical RGB and IR camera devices remain Present/OK.
- Confirm optional enhancement services have the approved mode.
- Ask the user to test camera preview, conferencing, blur, framing, gaze correction, and presence lock.
- Restore when a required feature fails.

## Drivers

- Confirm device status is OK and driver version/date changed as intended.
- Test the device's primary workflow.
- Test restart and sleep/wake.
- Inspect new WHEA, DeviceSetupManager, display, WLAN, Bluetooth, or storage events.
- Keep the exported prior driver until the validation window closes.

## Firmware

- Verify firmware version after reboot.
- Recheck power, virtualization, boot order, Secure Boot/BitLocker state, memory performance, thermals, and device enumeration.
- Reapply only previously documented settings that firmware reset.

## Reporting

Record:

- Timestamp and baseline type.
- Approved action codes.
- Exact before/after values.
- Backup and rollback locations.
- UAC/restart/sign-out requirements.
- Tests passed, failed, skipped, or awaiting user validation.
- Residual processes or services that require the next login/reboot.

