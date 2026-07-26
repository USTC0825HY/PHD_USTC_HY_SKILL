# Safety and Impact

## Scope

The mitigation modifies only a trigger in:

```text
$CODEX_HOME/logs_2.sqlite
```

It does not modify session JSONL files, project files, authentication, skills, plugins, `state_*.sqlite`, `goals_*.sqlite`, or memories.

## Preserved Behavior

Normal chat, model calls, tool execution, file editing, conversation history, project state, and updates do not depend on retaining every row in the diagnostic `logs` table.

## Reduced Diagnostics

The trigger discards:

- `TRACE`
- `DEBUG`
- `codex_otel.log_only` at `INFO` level
- `codex_otel.trace_safe` at `INFO` level

It retains other `INFO` plus all `WARN` and `ERROR` rows. Low-level streaming and transport diagnostics will be less complete. Remove the trigger before reproducing a problem when full diagnostic logs are required.

## Limitations

- SQLite still evaluates attempted inserts before the trigger ignores them.
- The mitigation reduces persistence and write amplification but does not stop event generation at the source.
- It does not mitigate writes to other Codex databases.
- Codex updates may replace the database or remove the trigger.
- A future database migration that changes or removes `logs.level` or `logs.target`
  could conflict with the trigger. Remove the trigger before a manual Codex
  upgrade when practical, then run `status` after upgrading.
- Database file size may remain large because filtering does not compact existing free pages.

## Recovery

The script creates a timestamped backup before `apply` and `remove`.
Each backup is a full SQLite database copy and may be large. `status` reports
the number and total size of backups. Review and delete obsolete backups
manually only after confirming the current database works.
Backups may contain diagnostic text, local paths, and other sensitive context.
Do not upload or share them.
The script refuses to start a backup when free disk space is less than the
current database size plus a small safety margin.

To restore normal logging, fully exit Codex and run:

```bash
python scripts/codex_log_guard.py remove
```

If the database is replaced during an update, run `status` and re-evaluate rather than applying blindly.
