# Obsidian Sync Reference

## Vaults

Real vault:

```text
C:\01_obsidian\ustc_hy
```

Sample vault:

```text
C:\01_obsidian\obsidian-diary-os\vault
```

Core real-vault areas:

```text
日记/
  00_日记中心.md
  日记/
  周记/
  月记/
  年记/
  财务分析/
模板/
  日记模板.md
  周记模板.md
  月记模板.md
  年记模板.md
```

Treat the real vault as user data. Do not bulk rewrite notes or config unless the user explicitly requested that operation.

## Ignore Rules

Use the same ignore rules for import preview, full import, sync preview, and indexed-note cleanup.

Ignored areas include at minimum:

- `.diary-os-backups/**`
- `.obsidian/**`
- `模板/**`

Important behavior:

- Backup Markdown must not be indexed as canonical notes.
- Sync preview must not use backup files as source paths.
- `cleanup_ignored_note_index` should remove old indexed rows that now match ignored paths.
- When real and backup notes exist for the same date, only the real vault note should participate in sync.

## Note Index

`note_index` stores source identity:

- source id
- absolute path
- relative path
- note type
- date key or period key
- content hash
- mtime

The index is an implementation detail for mapping Markdown files to local SQLite records. It must be kept clean from ignored paths to avoid duplicated logical days.

## Manual Sync Model

The app uses manual sync:

1. Import reads Obsidian Markdown into SQLite and source tracking fields.
2. Local save updates SQLite and sets `local_modified = 1`.
3. Frontend refreshes `preview_obsidian_sync` so pending status is visible immediately.
4. User enters the Obsidian sync page and chooses sync or conflict resolution.
5. Sync writes managed blocks back to real Markdown files.
6. Successful write updates `source_hash`, `source_mtime`, `source_path`, and clears `local_modified`.

Do not change this into auto-writeback without explicit product approval.

## Save Entrypoints That Refresh Sync Status

After these local saves succeed, refresh the current vault sync preview in the frontend:

- `saveWorkTasks`
- `createOrUpdateDailyEntry`
- `createOrUpdateReviewEntry`

This keeps homepage status, top status text, and the Obsidian linkage page consistent without performing automatic writeback.

## Managed Blocks

Writeback uses block-level patching. Preserve unrelated user Markdown.

Current work-task managed block markers:

```markdown
<!-- WORK_TASKS_START -->
- [ ] #work #P1 任务内容
- [x] #work #P2 已完成任务
<!-- WORK_TASKS_END -->
```

Rules:

- Only modify content between `WORK_TASKS_START` and `WORK_TASKS_END` for work tasks.
- Missing priority defaults to `P2`.
- Use `- [ ]` for pending tasks and `- [x]` for completed tasks.
- Keep `#work` and `#P1`/`#P2`/`#P3` tags in rendered task lines.
- Keep backups before writing.

## Backup Policy

Before writing to Obsidian Markdown, back up original content under:

```text
.diary-os-backups/YYYYMMDD-HHMMSS/
```

Backups are protection artifacts, not source notes. Always keep them ignored for import and sync indexing.

## Conflict Policy

Conflict cases include:

- Local SQLite record is modified and Obsidian source file has changed.
- Obsidian source file is missing while local data exists.
- Source hash or mtime differs from last imported/synced metadata.

Use existing conflict tables and commands:

- `sync_conflicts`
- `list_sync_conflicts`
- `resolve_sync_conflict`

Resolution options should preserve the existing model:

- Choose Obsidian version: re-import the file into local SQLite.
- Choose App version: write local managed data back to Markdown.
- Delete local dirty item only when user explicitly requests deletion through existing UI/commands.

## Environment Configuration

Environment configuration is local-only:

- Do not download plugins.
- Do not write third-party code into `.obsidian/plugins/*`.
- Do write/check local config and sample templates when requested by the environment setup feature.

Required plugins:

- `dataview`
- `quickadd`
- `templater-obsidian`
- `calendar`
- `obsidian-advanced-uri`

Optional plugins currently recognized:

- Manual Sorting
- Recent Files
- Style Settings
- Meta Bind

Environment commands:

- `preview_obsidian_environment`
- `configure_obsidian_environment`
- `open_obsidian_vault`
- `open_obsidian_setup_guide`

## Obsidian Opening

Prefer existing commands for opening vault or source files:

- `open_obsidian_vault`
- `open_source_file`

Do not invent shell-specific direct-opening behavior unless the current commands cannot support the requested action.
