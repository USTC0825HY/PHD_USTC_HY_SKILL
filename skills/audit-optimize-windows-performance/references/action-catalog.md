# Action catalog

Use these patterns as templates, not automatic recommendations. Replace names, paths, estimates, and checks with current-machine evidence.

## Approval tiers

| Tier | Typical action | Approval expectation |
|---|---|---|
| Read-only | Inventory, counters, logs, package and driver versions | No mutation approval |
| Low risk | Close optional UI, remove login autorun, fix impossible service dependency | Exact action-code approval |
| A/B | Temporarily stop optional network/camera/engineering service | Exact approval plus baseline and rollback |
| High impact | Uninstall VPN/filter driver, change virtualization, update driver | Exact approval, backup, restart gate |
| Firmware | BIOS review versus flash | Separate audit and flash approvals |

## Reusable action patterns

### `PROC-1`: stop an abnormal process

- Prove sustained CPU, disk, or memory behavior over a bounded interval.
- Resolve full executable path, parent process, command line, and whether a watchdog will restart it.
- Preserve open work; prefer normal exit.
- Verify the process stays stopped and the parent application remains healthy.

### `STARTUP-UI-1`: remove UI autorun, preserve service

Examples include remote-control clients and hardware utilities.

- Identify the Run value, Startup folder entry, task, or app-internal switch.
- Prove which service provides the required background capability.
- Back up the autorun entry.
- Remove only the UI entry and verify the service remains Automatic/Running.
- If a watchdog respawns the UI in the current session, do not loop-kill it; use the app's exit command or validate after sign-out.

### `APP-HELPER-1`: disable a login helper

Examples include MathWorks Service Host or cloud helper processes.

- Confirm the main application is not currently using it.
- Remove only its user startup entry.
- Verify the main application can relaunch the helper on demand.
- Expect the first launch or sign-in to be slower.

### `SVC-FIX-1`: repair an impossible service dependency

- Prove the service is Automatic, stopped, and blocked by a Disabled dependency.
- If the service is optional, set it to Manual rather than enabling all dependencies.
- Leave related working services untouched.
- Verify the corresponding SCM error does not recur after the next boot.

### `APPX-1`: uninstall an unused packaged utility

- Confirm the exact package identity and `NonRemovable` state.
- Explain which Windows capabilities remain independent.
- Remove the package through AppX tooling or normal app UI.
- Stop/delete only an orphan service after proving no package remains for any user.
- Use the Store reinstall path as rollback.

### `FEATURE-AB`: test optional camera or sensing features

- Record packaged UI processes, services, camera devices, and feature use.
- Set optional services to Manual and stop associated UI.
- Do not disable camera devices or delete drivers.
- Verify base camera presence; have the user test conferencing, blur, framing, gaze, and presence functions.

### `PROXY-1`: remove a duplicate proxy client

- Resolve port owners for the expected TCP and UDP proxy ports.
- Match identically named engines by full path.
- Preserve the client that owns the effective port.
- Turn off autorun through the application's supported control when possible.
- Verify DNS, HTTPS, system/WinHTTP proxy state, intended port ownership, and Tailscale.

### `NET-AB`: test optional network middleware

Examples include connectivity optimizers, packet capture, VPN filters, and game accelerators.

- Inventory services, WFP/NDIS bindings, system drivers, adapters, routes, and current traffic.
- Measure latency, loss, DNS, throughput, CPU, and required VPN/Tailscale connectivity.
- Stop or unbind one layer temporarily; do not uninstall during the A/B phase.
- Reboot when driver unload semantics require it.
- Restore on regression.

### `HYP-A` and `HYP-1`: virtualization audit and change

- `HYP-A`: inventory Hyper-V, VBS, Device Guard, Memory Integrity, WSL2, Docker, Sandbox, and VM dependencies.
- `HYP-1`: back up BCD and change only the approved virtualization controls.
- Restart, then verify `HypervisorPresent`, Device Guard status, memory bandwidth, sleep, networking, and required applications.
- Treat a disabled hypervisor service device as expected only when the change was deliberate.

### `PWR-1` and `PWR-2`: power tuning

- Separate AC and DC behavior.
- Prefer Windows power-mode overlays and documented processor/PCIe settings.
- Record active scheme and relevant setting indices before mutation.
- Validate sustained performance, battery behavior, sleep, and thermal evidence.

### `DRV-A` and `DRV-1`: driver review and update

- Audit hardware IDs, installed version/date, OEM customization, and current official release.
- Download and verify signatures/hashes before installation.
- Export the current driver package.
- Update one driver family at a time and verify device state, sleep/wake, network/display, and rollback.

### `BIOS-A` and `BIOS-1`: firmware gate

- `BIOS-A`: verify model, current version, official package, signature/hash, release notes, AC power, and recovery-key availability.
- `BIOS-1`: require a separate explicit approval immediately before flashing.
- Never combine BIOS flashing with unrelated changes.

## Lessons from common component classes

- Remote-control suites: UI memory can often be removed while the service preserves unattended access.
- Math/engineering helpers: login startup is often optional, but device discovery and licensing services need functional tests.
- PC cleanup utilities: uninstalling the optional app is cleaner than disabling a service that an app update may restore.
- Camera appearance suites: preserve camera hardware and test enhancements separately.
- Corporate VPN clients: services may be small while kernel DNS/TCP/WFP drivers remain the real cost and risk.
- Duplicate Electron proxy clients: count port ownership, not windows or process names.

