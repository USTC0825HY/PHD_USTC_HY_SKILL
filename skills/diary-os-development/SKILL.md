---
name: diary-os-development
description: Use for development, review, documentation, and release work on the Obsidian Diary OS standalone offline app in C:\01_obsidian\obsidian-diary-os\standalone, including Rust/Tauri commands, React/TypeScript UI, SQLite schema, Obsidian vault import/sync/writeback, Windows packaging, local-first product architecture, and the app's established visual/style conventions.
---

# Diary OS Development

## Purpose

Use this skill when working on the Obsidian Diary OS standalone app or its related project documentation. The app is a local-first Windows desktop workbench built with Tauri, React, TypeScript, Rust, and SQLite, synchronized manually with an Obsidian vault through indexed Markdown files and managed writeback blocks.

## Project Anchors

- Workspace: `C:\01_obsidian`
- Main repo: `C:\01_obsidian\obsidian-diary-os`
- Standalone app: `C:\01_obsidian\obsidian-diary-os\standalone`
- Backend: `C:\01_obsidian\obsidian-diary-os\standalone\src-tauri\src\lib.rs`
- Tauri entry: `C:\01_obsidian\obsidian-diary-os\standalone\src-tauri\src\main.rs`
- Frontend: `C:\01_obsidian\obsidian-diary-os\standalone\src\App.tsx`
- API bridge: `C:\01_obsidian\obsidian-diary-os\standalone\src\api.ts`
- Shared types: `C:\01_obsidian\obsidian-diary-os\standalone\src\types.ts`
- Styles: `C:\01_obsidian\obsidian-diary-os\standalone\src\styles.css`
- Real vault: `C:\01_obsidian\ustc_hy`
- Sample vault: `C:\01_obsidian\obsidian-diary-os\vault`
- Canonical stage docs: `C:\01_obsidian\obsidian-diary-os\docs`

Do not reset or overwrite the real vault. Treat changes in `C:\01_obsidian\ustc_hy` as user data unless the user explicitly asks to edit a specific vault document.

## Reference Map

Load only the reference needed for the task:

- For backend, SQLite, commands, and module architecture, read `references/architecture-and-data.md`.
- For Obsidian import, index, sync, managed block writeback, conflicts, and environment setup, read `references/obsidian-sync.md`.
- For homepage, navigation, CSS tokens, layout, component style, and UX conventions, read `references/frontend-style.md`.
- For tests, Windows packaging, release exe behavior, and git hygiene, read `references/release-validation.md`.

## Working Rules

1. Inspect current files before editing; this repo may already contain user or prior-agent changes.
2. Keep changes scoped to the standalone app or the requested docs unless the user explicitly expands scope.
3. Preserve the manual sync model: saving locally marks data dirty and refreshes sync preview; it does not auto-write to Obsidian.
4. Use SQLite as the offline source of structured truth; use Obsidian Markdown as readable, editable, synced representation.
5. Use managed block patching for Markdown writeback. Do not overwrite whole notes when a block-level patch exists.
6. Keep Tauri command signatures stable unless the user asks for an API change.
7. Add focused tests when touching parsing, sync, schema migration, conflict logic, or shared UI state.
8. On Windows, add `C:\Users\Administrator\.cargo\bin` to `PATH` before Cargo/Tauri commands if Cargo is missing.

## Implementation Workflow

1. Check `git status --short` from `C:\01_obsidian` and identify unrelated dirty files.
2. Read the relevant local source and, when useful, the canonical docs in `C:\01_obsidian\obsidian-diary-os\docs`.
3. For backend work, update Rust structs, migrations, helpers, commands, and tests in one coherent pass.
4. For frontend work, update `types.ts`, `api.ts`, `App.tsx`, and `styles.css` together so UI state, command payloads, and styling remain aligned.
5. For sync-affecting saves, refresh the current vault sync preview after successful local persistence.
6. Run the smallest meaningful verification first, then the full regression set when behavior or packaging changes.
7. If creating stage documentation, put canonical docs in the repo and mirror reading copies into the vault only when requested.

## Product Direction

Preserve the current product boundary:

- Standalone app: structured local input, validation, analytics, module dashboards, sync control.
- Obsidian vault: long-term Markdown reading, knowledge links, Dataview views, templates, manual editing.
- Daily page: today's aggregate and light capture, not a permanent home for every future module.
- Future modules: work plan, work time/projects, exercise, nutrition, expense/finance, life expansion, reading, writing, reviews, sync center, settings/data.

Prefer modular pages and tables over adding more unrelated fields to the daily page.
