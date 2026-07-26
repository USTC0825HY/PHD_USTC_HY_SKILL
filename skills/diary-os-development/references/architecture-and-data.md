# Architecture And Data Reference

## System Position

Obsidian Diary OS Standalone is a local-first Windows desktop app. It complements, rather than replaces, the Obsidian vault.

- The app handles structured capture, validation, statistics, dashboards, local SQLite persistence, and controlled sync.
- Obsidian handles long-term Markdown reading, free-form editing, links, Dataview, templates, and human review.
- Manual sync remains intentional: local saves mark dirty state; the user decides when to write back to Obsidian.

## Technology Stack

- Frontend: React + TypeScript + Vite.
- Desktop shell: Tauri.
- Backend: Rust Tauri commands.
- Database: SQLite.
- Packaging: Tauri NSIS for Windows.
- Obsidian integration: file-system scanning, Markdown parsing, managed block patching, `obsidian://` URI opening, and local config helpers.

## Main Source Files

- `standalone/src-tauri/src/lib.rs`: Rust backend, commands, schema, parsers, sync, tests.
- `standalone/src-tauri/src/main.rs`: Tauri entry point and Windows subsystem attribute.
- `standalone/src/App.tsx`: primary frontend app and panels.
- `standalone/src/api.ts`: Tauri invoke wrappers.
- `standalone/src/types.ts`: shared frontend types.
- `standalone/src/styles.css`: global visual system.

## SQLite Tables

Core tables already in use:

- `daily_entries`: daily note record and source tracking.
- `work_segments`: work time segments.
- `work_tasks`: daily work-plan tasks.
- `health_logs`: exercise records.
- `meal_logs`: food records.
- `finance_ledger`: finance ledger and review state.
- `review_entries`: weekly, monthly, yearly reviews.
- `vault_sources`: registered Obsidian vault sources.
- `note_index`: imported Markdown source index.
- `import_runs` / `import_conflicts`: import history and conflicts.
- `sync_runs` / `sync_conflicts`: sync history and conflict handling.

Source-tracking fields for synced records:

- `source_path`
- `source_hash`
- `source_mtime`
- `local_modified`

Use these fields to distinguish local edits, external Obsidian edits, missing source files, and conflict cases.

## Existing Commands

Daily and structured app data:

- `get_dashboard`
- `list_daily_entries`
- `get_daily_entry`
- `create_or_update_daily_entry`
- `delete_daily_entry`
- `get_weekly_work`
- `get_monthly_work`
- `get_work_plan`
- `save_work_tasks`
- `get_work_week_preview`
- `get_work_backlog`
- review and finance commands present in `lib.rs`

Obsidian import/sync:

- `preview_obsidian_import`
- `import_obsidian_vault`
- `list_vault_sources`
- `list_import_conflicts`
- `resolve_import_conflict`
- `preview_obsidian_sync`
- `sync_to_obsidian`
- `list_sync_conflicts`
- `resolve_sync_conflict`
- `delete_sync_item`
- `open_source_file`

Obsidian environment:

- `preview_obsidian_environment`
- `configure_obsidian_environment`
- `open_obsidian_vault`
- `open_obsidian_setup_guide`

Do not rename or remove commands casually; update `api.ts`, `types.ts`, frontend call sites, and tests together if a signature changes.

## Work Plan Model

Current table: `work_tasks`

Fields:

- `id`
- `date`
- `priority`
- `title`
- `completed`
- `order_index`
- `source_text`
- `created_at`
- `updated_at`

Rust structs/functions:

- `WorkTask`
- `WorkPlan`
- `WorkWeekPreview`
- `WorkWeekDayPreview`
- `WorkBacklogItem`
- `WorkPriorityStat`
- `parse_work_tasks`
- `render_work_tasks_block`
- `build_work_plan`
- `build_work_week_preview`
- `load_work_backlog`
- `load_unfinished_work_between`
- `normalize_work_tasks`
- `normalize_task_priority`

Priority normalization:

- Accept `P1`, `P2`, `P3`.
- Missing or unknown priority defaults to `P2`.
- Preserve task order through `order_index`.

Known Rust lifetime pattern:

- Do not return `stmt.query_map(...).collect(...)` as the tail expression when the statement must outlive mapped rows.
- Assign rows to a local variable first, then return `Ok(rows)`.

## Exercise And Food Notes

Exercise data currently includes sanitization and source priority logic:

- Use `sanitize_exercise_type`.
- Clean dirty exercise fields before persistence.
- Prefer manual/watch `运动消耗_kcal` over auto-calculated `运动消耗_kcal_自动`.
- Write `运动消耗_kcal_来源:: 手动优先` when manual value is authoritative.

Food and exercise are currently inside the daily page. Future work should split them into independent modules with daily aggregation back into the journal.

## Module Architecture Direction

Avoid expanding the daily page into a monolith. Move toward:

- Independent module pages.
- Independent SQLite tables per module.
- Shared dimensions: date, week, month, year, project, tag, source.
- Daily page as aggregate entry and review surface.
- Homepage as "today command center" rather than full analytics dashboard.

Recommended future top-level modules:

- Today command center.
- Work plan.
- Work time and projects.
- Exercise training.
- Nutrition.
- Expense and finance.
- Life expansion.
- Reading.
- Writing.
- Weekly/monthly/yearly review.
- Obsidian sync.
- Settings and data.

## Documentation Baseline

Canonical repo docs created for the 2026-04-27 stage:

- `docs/STANDALONE_DEV_PROGRESS_2026-04-27.md`
- `docs/DIARY_OS_SYSTEM_OVERVIEW_2026-04-27.md`
- `docs/DIARY_OS_ROADMAP_2026-04-27.md`

Use these docs for product facts before making broad architectural changes.
