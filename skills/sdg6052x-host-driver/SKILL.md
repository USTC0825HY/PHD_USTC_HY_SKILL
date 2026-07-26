---
name: sdg6052x-host-driver
description: Reusable workflow for integrating Siglent SDG6052X/SDG6000X signal-generator host-control modules via C++/Qt, NI/IVI VISA C API, and SCPI. Use when Codex needs to add, migrate, test, or refactor SDG6052X controls, shared VISA sessions, Raw SCPI consoles, output/waveform commands, fake VISA tests, or calibration/sweep orchestration in a desktop host application.
---

# SDG6052X Host Driver

## Core Workflow

Use the existing Qt_Muon implementation as the reference architecture when available. Inspect `SdgScpi.*`, `SdgVisaClient.*`, `SdgControlPanel.*`, and any `CalibrationScan*` files before changing or reusing the module.

Build the integration in layers:

1. **SCPI builder**: pure command generation and validation, independent of Qt widgets and VISA.
2. **VISA backend**: small interface around `viOpenDefaultRM`, `viFindRsrc`, `viOpen`, `viWrite`, `viRead`, and `viClose`.
3. **Worker client**: QObject living in a `QThread`, emitting status/progress signals and never blocking the UI thread.
4. **UI or orchestration layer**: manual control panel, calibration scan page, or another host workflow that talks to the worker through queued signals.
5. **Tests**: pure SCPI tests, fake VISA backend tests, and sweep-sequence tests.

## Integration Rules

- Discover resources with `USB?::?*INSTR`; filter SDG6052X/SDG6000X USB resources by `::0xF4EC::0x1101::`, but always allow manual full VISA resource entry.
- On connect, open the VISA session and query only `*IDN?`. Do not change output, waveform, voltage, load, or trigger state during connection.
- Append `\n` on every VISA write. Trim CR/LF from query responses before showing or parsing them.
- Keep output commands compatible with the known Siglent behavior:
  - `C{ch}:OUTP ON/OFF`
  - optional `C{ch}:OUTP LOAD,HZ/50`
  - optional `C{ch}:OUTP PLRT,NOR/INVT`
- Keep basic-wave commands in this form: `C{ch}:BSWV WVTP,<TYPE>,FRQ,...`; omit empty numeric fields instead of sending blank values.
- Support `SINE`, `SQUARE`, `PULSE`, `RAMP`, `NOISE`, and `DC`; validate channels as only `1` or `2`.
- Keep Raw SCPI as an advanced/debug console. Do not use Raw SCPI as the mechanism for normal UI actions or calibration workflows.

## Qt Design

Prefer one shared SDG VISA worker per host process. If multiple pages need the signal generator, inject or share the same `SdgVisaClient` rather than opening duplicate VISA sessions.

Use queued signal/slot calls from UI pages to the worker:

- UI emits request signals such as `requestApplyBasicWave(...)`.
- Worker emits `busyChanged`, `connected`, `disconnected`, `operationFailed`, and command-specific completion signals.
- UI controls are disabled while the worker is busy or disconnected.
- Long workflows, such as sweeps, should be a timer/state-machine orchestration over the shared worker rather than sleeps in the UI thread.

For calibration or frequency sweeps, use this host-side sequence unless the experiment requires a different acquisition protocol:

1. Validate SDG connected, MAROC/target hardware connected, and all sweep parameters.
2. Optionally send current target configuration once before the sweep.
3. If output should be enabled during the sweep, query current output first; turn it on only if it was off, and turn it back off only if the scan opened it.
4. For each frequency point: set SDG basic wave, wait settle time, send target acquisition start, wait acquire time, send acquisition stop, update UI status/log.
5. On Stop or failure, stop timers, send acquisition stop if currently acquiring, and restore output if the scan enabled it.

## Validation

Before calling the integration done:

- Test SCPI generation for output, waveform, raw normalization, invalid channel, invalid waveform, and invalid numeric fields.
- Test the VISA worker with a fake backend: resource filtering, unique-resource connect, connect-time `*IDN?`, write/query failures, timeout error mapping, and disconnect close.
- Test sweep helpers: frequency-point generation, floating-step tolerance, point-count cap, invalid ranges, and expected command order.
- Build the host target and run the relevant CTest targets.
- Treat hardware smoke as separate evidence: verify refresh, connect/IDN, output readback, waveform readback, and a small low-risk sweep when the instrument is online.

## Detailed Reference

For implementation patterns, CMake snippets, fake backend test structure, and common failure modes, read `references/qt-visa-integration.md` when working on an actual codebase.
