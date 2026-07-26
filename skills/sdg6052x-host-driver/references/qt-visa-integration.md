# Qt/VISA SDG6052X Integration Reference

## Reusable Module Shape

Use these source-level responsibilities when porting the module into a new C++/Qt host:

- `SdgScpi`: pure functions for validation and command strings. No Qt widgets, no VISA calls, no hardware state.
- `SdgVisaBackend`: interface for resource listing, opening, writing, querying, closing, and `isOpen()`.
- `NativeVisaBackend`: implementation of NI/IVI VISA C API.
- `SdgVisaClient`: QObject worker wrapping the backend, emitting UI-safe signals.
- `SdgControlPanel`: manual page for connection, output, basic wave, readback, advanced Raw SCPI, and log.
- Sweep/calibration controller: a separate state machine that reuses `SdgVisaClient` instead of constructing a second client.

Do not merge SCPI string construction into button handlers. Keep it testable without hardware.

## CMake Pattern

Default to enabling native VISA if the target environment is expected to have the SDK:

```cmake
option(QT_MUON_ENABLE_SDG_VISA "Enable native VISA control for SDG signal generators" ON)

if(QT_MUON_ENABLE_SDG_VISA)
    find_path(SDG_VISA_INCLUDE_DIR
        NAMES visa.h
        HINTS
            "C:/Program Files/IVI Foundation/VISA"
            "C:/Program Files (x86)/IVI Foundation/VISA"
            "$ENV{VISA_ROOT}"
            "$ENV{VXIPNPPATH}"
        PATH_SUFFIXES Include Win64/Include WinNT/Include
    )
    find_library(SDG_VISA_LIBRARY
        NAMES visa64 visa32
        HINTS
            "C:/Program Files/IVI Foundation/VISA"
            "C:/Program Files (x86)/IVI Foundation/VISA"
            "$ENV{VISA_ROOT}"
            "$ENV{VXIPNPPATH}"
        PATH_SUFFIXES Lib_x64/msc Win64/Lib_x64/msc Lib/msc WinNT/Lib/msc
    )
    if(NOT SDG_VISA_INCLUDE_DIR OR NOT SDG_VISA_LIBRARY)
        message(FATAL_ERROR
            "QT_MUON_ENABLE_SDG_VISA=ON requires NI/IVI VISA C headers and library. "
            "Install the VISA SDK or set VISA_ROOT to the IVI Foundation/VISA directory.")
    endif()
endif()
```

For tests that use fake backends only, link Qt Core and avoid linking VISA unless the test instantiates the native backend.

## SCPI Command Rules

Resource discovery:

- Query: `USB?::?*INSTR`
- Default Siglent SDG match: `::0xF4EC::0x1101::`
- Example: `USB0::0xF4EC::0x1101::SDG6XFCC900258::INSTR`

Connection:

- Open VISA resource.
- Configure timeout and `\n` termination.
- Query `*IDN?`.
- Close session on failed IDN query.
- Do not write output/waveform state on connect.

Output:

```text
C1:OUTP ON
C1:OUTP OFF
C1:OUTP LOAD,HZ
C1:OUTP LOAD,50
C1:OUTP PLRT,NOR
C1:OUTP PLRT,INVT
C1:OUTP?
```

Basic wave:

```text
C1:BSWV WVTP,SINE,FRQ,1000,AMP,1,OFST,0
C2:BSWV?
```

Build the comma-separated field list from non-empty values only. Validate numeric fields with C locale and finite double parsing. Format numbers compactly with enough precision, for example `QString::number(value, 'g', 12)` or `QLocale::c().toString(value, 'g', 12)`.

Raw SCPI:

- Normalize by removing leading/trailing CR/LF only.
- Reject empty commands.
- Reject non-ASCII commands.
- Append `\n` in the backend, not in UI text boxes.
- Keep it collapsed or labeled as advanced/debug.

## VISA Backend Practices

The native backend should:

- Own both resource-manager and instrument sessions.
- Close both sessions in destructor/close.
- Re-open by closing any prior instrument session first.
- On query, write the command then read until success, termination character, timeout, or a maximum response cap.
- Return structured result objects: `ok`, `timeout`, `text`, `values`, `error`.
- Convert VISA status codes to readable messages with `viStatusDesc` when possible.

The fake backend should record:

- list queries
- opened resources
- writes
- queries
- closed resources
- configurable open/write/query failures

This enables deterministic unit tests without hardware.

## Qt Worker And UI Practices

Run the VISA client in a dedicated `QThread`:

```cpp
auto *thread = new QThread(parent);
auto *client = new SdgVisaClient();
client->moveToThread(thread);
connect(thread, &QThread::finished, client, &QObject::deleteLater);
thread->start();
```

Use `QMetaObject::invokeMethod(client, "disconnectResource", Qt::BlockingQueuedConnection)` during shutdown before quitting the thread.

For shared use:

- Create the worker once in the application owner, often `MainWindow`.
- Inject the same `SdgVisaClient *` into every page that needs it.
- Connect UI request signals to client slots.
- Connect client status signals back to pages.
- Do not let every page allocate its own worker unless it is truly standalone.

For manual controls:

- Disable connection controls while connected or busy.
- Disable output/wave controls while disconnected or busy.
- Show readback fields as "Device response" or equivalent, not as user input.
- Keep logs timestamped and bounded with `document()->setMaximumBlockCount(...)`.

## Calibration/Frequency Sweep Pattern

Use a state machine with `QTimer`, not blocking sleeps:

```text
Idle
 -> QueryOutput
 -> EnableOutput if needed
 -> SetWave(point N)
 -> Settle timer
 -> ACQ Start
 -> Acquire timer
 -> ACQ Stop
 -> next point or Finish
 -> DisableOutput if scan enabled it
```

Important details:

- Generate and validate all frequency points before touching hardware.
- Use an inclusive increasing sweep with `start <= stop`, `step > 0`, and a point cap such as 1000.
- Use a small floating epsilon so `0.1, 0.2, 0.3` style sweeps include the final point.
- Treat Stop as a request to finish the current safe boundary; if acquiring, send ACQ Stop immediately.
- If another target device is involved, expose tiny host callbacks/signals such as `sendCurrentConfig`, `sendAcqStart`, `sendAcqStop`, and `isConnected` rather than letting the SDG layer know target-device details.

## Test Checklist

SCPI tests:

- `C1:OUTP ON`, `LOAD,HZ`, `PLRT,INVT`
- `C1:OUTP?`
- `C1:BSWV WVTP,SINE,FRQ,1000,AMP,1,OFST,0`
- empty optional fields omitted
- invalid channel
- invalid waveform
- invalid number
- raw command trimming and ASCII rejection
- SDG resource filter

VISA fake tests:

- resource discovery filters only SDG resources
- blank resource connects only when exactly one SDG match exists
- connect sends exactly `*IDN?`
- connect closes on failed IDN query
- output and wave writes match expected SCPI
- raw write-only vs query behavior
- timeout/failure emits operation failure
- disconnect closes session

Sweep tests:

- normal point list
- floating-step tolerance
- reverse range rejection
- step <= 0 rejection
- point cap rejection
- output-state parsing from `C1:OUTP ON,...` and `OFF`
- nominal command order: optional config, output query/on, per-point wave/start/stop, output off if scan enabled it

## Common Failure Modes

- Duplicate VISA sessions: caused by each page owning a client. Fix by sharing one worker.
- UI freeze: caused by VISA calls or sleeps on UI thread. Move calls to worker and use timers.
- Unsafe connect: caused by writing output/wave state during connection. Connect should only IDN-query.
- Broken manual resource entry: caused by filtering too aggressively. Filter discovered resources but allow manual full resource text.
- Unclear readback fields: users confuse readback with input. Label as device response/readback.
- Raw SCPI taking over normal workflows: keep Raw SCPI debug-only and collapsed by default.
- Sweep output restore bug: query output first, then disable at finish only if the scan turned it on.
