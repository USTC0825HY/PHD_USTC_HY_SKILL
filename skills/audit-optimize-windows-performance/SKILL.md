---
name: audit-optimize-windows-performance
description: Audit, diagnose, plan, execute, and verify evidence-based Windows performance optimizations with explicit approval codes, reversible changes, UAC-safe elevation, and capability checks. Use for slow Windows PCs, excessive startup/background processes, memory/CPU/disk bottlenecks, power-plan tuning, Hyper-V/VBS tradeoffs, duplicate proxy/VPN stacks, service cleanup, driver or BIOS review, and before/after performance validation.
---

# Audit and Optimize Windows Performance

Use measurement, not folklore. Separate read-only diagnosis from mutation and preserve the user's required capabilities.

## Select the operating mode

- For requests to analyze, inspect, diagnose, review, or recommend: perform read-only checks only.
- For requests to change or optimize: audit first, propose bounded action codes, and execute only codes the user explicitly approves.
- Treat approval as exact-scope authorization. Do not extend `SVC-1` into unrelated services or an A/B test into uninstalling software.
- Continue independent read-only work while waiting for approval. Stop when a required choice would materially change functionality.

## Establish required capabilities

Discover or confirm capabilities that optimization must preserve:

- Remote access and unattended control.
- Tailscale, VPNs, proxies, corporate network clients, and packet capture.
- WSL2, Docker, Hyper-V virtual machines, Windows Sandbox, VBS, Memory Integrity, and Credential Guard.
- MATLAB, NI/PXI, FPGA/Cadence/Vivado, camera effects, gaming, or other specialized software.
- Battery-life versus plugged-in sustained-performance priorities.

Do not infer that an installed component is unused merely because it is idle.

## Capture the baseline

Run `scripts/collect-performance-baseline.ps1` for a bounded, read-only JSON snapshot. Store results in the active workspace, not inside the skill directory.

Interpret the snapshot at the right grain:

- Compare free physical memory, commit percentage, paging, disk latency/queue, CPU queue, and sustained CPU load.
- Treat the sum of process working sets as an upper-bound inventory; shared pages make it larger than unique physical use.
- Attribute suites by executable path and command line, not process name alone.
- Distinguish application UI, user startup helper, Windows service, scheduled task, packaged app, network filter, and kernel driver.
- Check recent WHEA and storage events before claiming hardware instability.
- Report missing sensor or firmware evidence as unknown, not healthy or throttled.

For an idle baseline, ask the user to leave the desktop untouched for three minutes, then sample. Label measurements taken during active work as active-workload snapshots.

## Diagnose bottlenecks

Prioritize evidence in this order:

1. Hardware errors, thermal throttling, storage failure, or severe paging.
2. Sustained CPU, disk latency/queue, memory pressure, or GPU saturation.
3. Duplicate functional stacks such as two active proxy clients.
4. Login UI and helpers that can be separated from required background services.
5. Broken dependencies and deterministic startup errors.
6. Optional services, network filters, drivers, and stale devices.
7. Driver and firmware currency after confirming the current official release.

Do not equate process count with a fault. Modern Windows intentionally splits services.

## Propose approval codes

For every mutable proposal, provide:

- A stable code such as `AWE-1`, `NET-AB`, or `HYP-1`.
- Exact target and exact change.
- Baseline evidence and expected benefit.
- User-visible capability impact.
- Whether UAC, sign-out, restart, or a clean boot is required.
- Validation checks and rollback steps.

Use `-A` for audit/download-only gates, `-AB` for temporary controlled tests, and `-1` for a bounded implementation when helpful. See `references/action-catalog.md` for reusable patterns.

## Execute approved changes

Before mutation:

1. Re-read current state; do not trust a stale process ID, port owner, package version, or service mode.
2. Resolve exact executable paths, registry values, service names, package identities, and drivers.
3. Back up changed registry keys, service start modes, BCD state, driver packages, or app configuration as applicable.
4. Write rollback instructions before applying the change.
5. Keep each batch small enough to attribute regressions.

For elevation:

- Prefer a bounded PowerShell script in the workspace.
- Validate its syntax before launch.
- Show the user what the UAC run will change.
- Launch with normal Windows elevation and require the user to approve UAC; never automate authentication or UAC.
- Write structured before/after results and backup paths to the workspace.

For processes:

- Close applications normally when possible.
- If forced termination is approved, select by full executable path and role. Never kill a shared name such as `clash-win64.exe` without resolving the owner path.
- Do not repeatedly kill a watchdog-managed UI; use the application's own exit flow or defer current-session cleanup until sign-out.
- If user input is detected in a target window, stop UI automation.

For services:

- Prefer removing an optional UI autorun while preserving a required service.
- Prefer Manual over Disabled for on-demand engineering or camera features.
- Repair impossible dependency configurations rather than enabling every dependency.
- Uninstall unused packaged apps instead of leaving orphaned disabled services.
- Treat network, security, storage, and hardware-enumeration services as high-risk.

## Apply A/B discipline

Use A/B testing for networking, power, camera enhancement, engineering discovery services, and similar components:

1. Capture baseline latency, loss, throughput, CPU, memory, and required capability status.
2. Change one subsystem.
3. Restart only when technically required.
4. Repeat the same measurements under comparable conditions.
5. Restore automatically when a required capability fails or results materially worsen.
6. Keep the change only when the result is measurably positive or removes a confirmed fault.

Do not claim a gain from a single transient sample.

## Validate after every batch

Run `scripts/validate-critical-capabilities.ps1` with relevant options, then perform task-specific checks from `references/validation-matrix.md`.

At minimum verify:

- Approved targets reached their intended state.
- Unapproved services, drivers, and applications remain unchanged.
- DNS and HTTPS work.
- Required proxy port ownership still matches the intended executable.
- Tailscale service, backend, self-online state, and peer reachability remain healthy when required.
- Camera devices remain present after camera-enhancement changes.
- WHEA and storage error counts do not increase.
- Memory, CPU, process count, and disk metrics are compared with the same baseline type.

Record actual results. Do not report estimated memory savings as realized savings while the old process remains alive.

## Guardrails

Do not:

- Disable Defender, Windows security components, the page file, Windows Update, or broad groups of services without specific evidence and explicit approval.
- Apply registry latency myths, HPET/timer cargo cults, unverified BCD flags, RAM cleaners, or manual NVMe defragmentation.
- Flash BIOS in the same step as downloading or reviewing it.
- Update drivers without a backup/rollback plan and current official-source verification.
- Disable Hyper-V/VBS before checking WSL2, Docker, Sandbox, VM, Credential Guard, and Memory Integrity dependencies.
- Remove VPN, proxy, packet-capture, or network-filter drivers merely because their adapter is disconnected.
- Delete application data to reduce RAM.

## Use the bundled references

- Read `references/action-catalog.md` when classifying optimization candidates or writing approval codes.
- Read `references/validation-matrix.md` before executing or verifying power, virtualization, proxy/VPN, service, driver, firmware, or camera changes.

