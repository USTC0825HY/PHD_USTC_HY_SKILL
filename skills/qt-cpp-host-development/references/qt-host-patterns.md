# Qt Host Patterns

Use these patterns for Qt/C++ desktop host applications that control hardware or instruments.

## 1. Repository And Build Inspection

Start by reading:

- Top-level `CMakeLists.txt` and the application subdirectory `CMakeLists.txt`.
- Qt version requirements and `CMAKE_PREFIX_PATH` defaults.
- Options that enable hardware SDKs, such as USB, VISA, serial, or vendor libraries.
- Test registration, `enable_testing()`, `add_test()`, and any CTest helper functions.

Keep optional SDKs behind CMake options. When the option is off, pure model and fake-backend tests should still build.

## 2. Recommended Layering

Use this order when analyzing or adding host features:

1. UI/panel: widgets, buttons, tables, and user feedback.
2. Binder/controller: maps UI intent into domain or device operations.
3. Domain model: typed state, parameter validation, and configuration objects.
4. Command builder: text or binary commands with no widget dependency.
5. Payload transform: byte order, packet framing, checksums, and wire format.
6. Backend interface: small abstraction for USB/VISA/serial/TCP operations.
7. Real backend: vendor SDK calls and hardware-specific error mapping.
8. Fake backend: deterministic tests for connect, write, read, timeout, and failure.
9. Worker object: QObject slots that execute IO away from the UI thread.
10. Automation/state machine: timers, scans, sweeps, retries, and stop handling.

Do not let UI code duplicate command bytes, packet framing, register meanings, or low-level SDK calls.

## 3. Device Backend Pattern

Define a narrow interface around the transport:

- `connect` / `disconnect`
- `isOpen` or `isConnected`
- `write` / `query` or `send` / `receive`
- `lastError` or structured result

For fake backends, record command history and expose deterministic failures. Test resource filtering, connection behavior, write/query order, timeout mapping, and cleanup.

## 4. QObject Worker And QThread

Use a QObject worker for blocking or long-lived device operations:

- Create the worker in the UI owner, then `moveToThread(workerThread)`.
- Start the thread before queued requests.
- Connect `QThread::finished` to `QObject::deleteLater`.
- UI emits request signals; worker emits completion, failure, busy, connected, and log signals.
- UI controls should be disabled while the worker is busy or disconnected.

Avoid direct blocking SDK calls from `MainWindow`, widgets, or button handlers.

## 5. Protocol Builder And Payload Transform

Keep protocol code testable without Qt Widgets or live hardware:

- Put SCPI/text command generation in a small builder class or namespace.
- Put binary packet framing and byte swapping in pure functions.
- Validate channels, ranges, enum values, and optional fields before formatting commands.
- Preserve input buffers unless mutation is intentional and documented.
- Test empty payloads, odd lengths, endianness, invalid values, and known examples.

## 6. Automation And Scans

For scans, calibration loops, and multi-step hardware workflows:

- Use `QTimer` or a state machine instead of sleeps.
- Validate all devices and parameters before start.
- Query current output or device state before changing it when restoration matters.
- On stop or failure, cancel timers, stop acquisition if active, and restore only state that the workflow changed.
- Emit point-level status, elapsed time, log messages, and final success/failure.

## 7. Testing Strategy

Prefer this test ladder:

1. Pure command builder tests.
2. Payload transform and packet framing tests.
3. Domain model and configuration tests.
4. Fake backend worker tests.
5. Automation/state-machine tests.
6. Real hardware smoke tests.

Hardware smoke should not be required to prove pure model/export correctness.

## 8. Evidence Boundaries

- A passing CTest proves the tested host logic under the compiled configuration.
- A fake backend test proves host sequencing and error handling, not real hardware behavior.
- A live hardware smoke proves a tested device state for that setup only.
- A host log proves what the host sent or received; it does not prove downstream FPGA, board, ASIC, or instrument analog behavior without matching hardware evidence.

