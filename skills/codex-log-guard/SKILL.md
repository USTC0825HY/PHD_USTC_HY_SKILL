---
name: codex-log-guard
description: Audit and mitigate excessive SQLite log writes from Codex Desktop or Codex CLI. Use when users report high SSD writes, rapid logs_2.sqlite or WAL churn, disk stalls, large Codex log databases, or ask to apply, verify, or remove selective low-value log filtering on Windows, macOS, or Linux.
---

# Codex Log Guard

Audit Codex SQLite logging and apply a reversible selective filter that drops noisy `TRACE`/`DEBUG` and duplicate OTel mirror events while preserving `INFO`/`WARN`/`ERROR`.

## Safety Rules

- Run `status` or `measure` freely; they are read-only.
- Before `apply` or `remove`, tell the user to fully exit Codex, including tray/background processes.
- Because Codex must be stopped, do not try to run `apply` or `remove` inside the active Codex session. Give the user the command to run from an external terminal after exiting.
- Never delete conversations, state databases, skills, plugins, or project files.
- Prefer selective filtering over blocking all inserts.
- Explain that this is a community mitigation, not an official OpenAI fix.
- Preserve a timestamped database backup before modifying triggers.
- Warn that repeated apply/remove operations create full-size backups that may accumulate.
- Do not use `VACUUM`, delete WAL files, or replace the database while Codex is running.

Read [references/safety-and-impact.md](references/safety-and-impact.md) before recommending or applying mitigation.
Use [references/public-evidence.md](references/public-evidence.md) when the user asks whether the issue is publicly documented.

## Script

Use `scripts/codex_log_guard.py`.

### Inspect

```bash
python scripts/codex_log_guard.py status
```

Report:

- database and WAL size
- whether the selective trigger is installed
- retained rows and estimated bytes by level
- top log targets

### Measure Churn

Run while Codex is active:

```bash
python scripts/codex_log_guard.py measure --seconds 30
```

Interpret rapid `MAX(id)` growth with little retained-row growth as insert/delete or rotation churn. State clearly that this measures SQLite activity, not total physical SSD writes.

### Apply Selective Filtering

Only after Codex is fully exited:

```bash
python scripts/codex_log_guard.py apply
```

The script:

1. Refuses to continue if a Codex process is detected.
2. Creates a timestamped backup beside the database.
3. Installs `codex_drop_noisy_logs`.
4. Verifies the trigger definition.

The filter drops:

```text
TRACE
DEBUG
codex_otel.log_only
codex_otel.trace_safe
```

The two OTel targets are filtered only at `INFO` level. All `WARN` and `ERROR` rows are preserved.

### Remove Filtering

Only after Codex is fully exited:

```bash
python scripts/codex_log_guard.py remove
```

### Force Override

Do not use `--force` by default. It exists only for environments where process detection is wrong and the user has independently confirmed Codex is stopped.

## Validation

After applying:

1. Restart Codex.
2. Confirm chat, tool execution, and file editing work.
3. Run `measure --seconds 30`.
4. Compare churn and OS-level process write rate with the baseline.
5. Run `status` to confirm `INFO/WARN/ERROR` remain available.

If behavior changes unexpectedly, fully exit Codex and run `remove`.

## Publishing and Installation

The skill folder is self-contained. For standard installation, publish it as a `codex-log-guard/` subdirectory in the repository and install that path. If the skill is the repository root, the installer must be given `--path . --name codex-log-guard`. Restart Codex after installation.
