# Release And Validation Reference

## Cargo PATH

On this machine, Cargo may not be in `PATH`. Before Rust/Tauri commands, run:

```powershell
$env:PATH='C:\Users\Administrator\.cargo\bin;' + $env:PATH
```

Run commands from:

```text
C:\01_obsidian\obsidian-diary-os\standalone
```

## Validation Commands

Regression set:

```powershell
npm test -- --run
npm run build
$env:PATH='C:\Users\Administrator\.cargo\bin;' + $env:PATH
cargo test
npm run tauri:build
```

Use a smaller subset while iterating:

- Frontend-only logic: `npm test -- --run`
- Type/build issues: `npm run build`
- Rust parser/sync/schema changes: `cargo test`
- Packaging or Windows subsystem changes: `npm run tauri:build`

Last known verified stage:

- `cargo test`: 23 passed.
- `npm test -- --run`: 8 passed.
- `npm run build`: passed.
- `npm run tauri:build`: passed.

## Windows Console Window

Release builds should not open a black console window. Keep this at the top of `standalone/src-tauri/src/main.rs`:

```rust
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
```

This applies only to non-debug Windows builds, preserving development diagnostics.

## Installer Paths

NSIS installer output:

```text
C:\01_obsidian\obsidian-diary-os\standalone\src-tauri\target\release\bundle\nsis\Obsidian Diary OS Standalone_0.1.0_x64-setup.exe
```

Release exe output:

```text
C:\01_obsidian\obsidian-diary-os\standalone\src-tauri\target\release\obsidian-diary-os-standalone.exe
```

Installed exe path commonly checked by the user:

```text
C:\Program Files\Obsidian Diary OS Standalone\obsidian-diary-os-standalone.exe
```

If the user says the exe did not update, verify the installer was rebuilt and installed, then check the installed exe timestamp. Building the installer alone does not replace the installed Program Files exe until installation is run.

## Git Hygiene

The working tree may include unrelated changes:

- Standalone source modifications from the current development stage.
- Real vault `.obsidian` config changes.
- Real vault note changes.
- Backup folders under `ustc_hy/.diary-os-backups`.
- Submodule or sibling project changes.

Rules:

- Do not run `git reset --hard`.
- Do not run `git checkout --` unless explicitly requested.
- Do not stage real-vault changes when preparing standalone commits unless the user explicitly asks.
- If committing standalone work, stage only relevant files under `obsidian-diary-os/standalone` and any requested repo docs under `obsidian-diary-os/docs`.
- Do not stage `C:\01_obsidian\ustc_hy` unless the task is explicitly about committing vault docs.

## Manual Acceptance Checks

For UI/sync work, confirm:

- Installed release exe opens without the black console in non-debug builds.
- Sidebar remains fixed while main content scrolls.
- Sidebar footer refresh/status stays visible within the sidebar.
- Updating work tasks in `今日日记` marks sync pending without page switching.
- `Obsidian 联动` shows the correct pending items.
- Manual sync updates the real daily file under `C:\01_obsidian\ustc_hy\日记\日记\YYYY-MM-DD.md`.
- `WORK_TASKS_START/END` block updates without disturbing unrelated Markdown.
- Backup files are created but ignored by import and sync preview.

## Documentation Closeout

For stage closeout docs:

- Put canonical docs in `C:\01_obsidian\obsidian-diary-os\docs`.
- Put Obsidian reading mirrors in `C:\01_obsidian\ustc_hy\日记\日记系统开发文档` only when requested.
- Keep filenames date-stamped when documenting stage baselines.
