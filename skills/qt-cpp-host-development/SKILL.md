---
name: qt-cpp-host-development
description: "General Qt/C++ desktop host-application development workflow. Use for Qt Widgets or CMake host apps that control hardware, instruments, USB/VISA/serial/TCP devices, command builders, payload transforms, QThread/QObject workers, signal-slot UI integration, fake backends, CTest targets, and hardware-smoke separation. Does not cover QML/mobile-first apps or project-specific protocol truth such as MAROC 829bit fields."
---

# Qt C++ Host Development

## Workflow

1. Inspect the repository first: top-level `CMakeLists.txt`, Qt version, compiler kit, build presets or build folders, source layout, and current tests.
2. Classify the task as build environment, UI wiring, domain model, command/protocol builder, device backend, worker/threading, automation/state machine, tests, or deployment.
3. Keep the host layers separate: UI/panel, binder/controller, domain model, command builder, payload transform, backend interface, real backend, fake backend, worker object, and tests.
4. Keep blocking IO out of the UI thread. Put long-lived device clients in `QObject` workers on `QThread`, communicate through queued signals/slots, and disable UI actions while workers are busy.
5. Prefer pure model/transform tests and fake backend tests before hardware smoke. Treat live USB/VISA/serial/TCP checks as separate evidence.

## Architecture Rules

- Put command formatting, byte order, payload transforms, and validation in pure or near-pure C++ units that can be tested without widgets or hardware.
- Hide hardware SDKs behind small backend interfaces. Allow dependency injection so tests can use fake backends.
- Keep UI classes from owning protocol truth. UI should collect intent and call a binder/controller, not duplicate command bytes or register meanings.
- Use `QTimer` or an explicit state machine for scans, sweeps, polling, and retry flows. Avoid sleeps in UI code.
- Make CMake options explicit for optional SDKs. A missing SDK should fail only when the real backend is enabled.

## References

Read `references/qt-host-patterns.md` when implementing or reviewing:

- QObject worker plus QThread integration.
- Abstract device clients and fake backend injection.
- Protocol builders and payload transforms.
- CTest target organization.
- Optional hardware SDK discovery.
- Host-side evidence boundaries.

## Boundaries

- Host logs prove host-side intent, command construction, and observed transport responses. They do not prove downstream FPGA, board, or chip behavior unless paired with hardware evidence.
- For project-specific packet formats, register maps, board bring-up, or firmware replay, use the project skill that owns that protocol.
- For MAROC QT_MUON work, use `maroc-qt-host-development`; if exported packets must match RTL fixtures, use `maroc-host-rtl-alignment`.

## Asset Library

- Use `C:/Users/Administrator/.codex/hardware-assets/templates/qt-cpp-host/CMakeLists_skeleton.txt` for new Qt/CMake host-app scaffolds.
- Use `C:/Users/Administrator/.codex/hardware-assets/templates/qt-cpp-host/AbstractDeviceClient.h`, `FakeDeviceClient.h`, and `test_payload_transform_skeleton.cpp` for backend abstraction and test patterns.
- Use `C:/Users/Administrator/.codex/hardware-assets/source-refs/maroc-qt-host-assets.md` only as a project example; do not copy MAROC protocol fields into generic Qt work.
