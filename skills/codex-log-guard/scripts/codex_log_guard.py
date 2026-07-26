#!/usr/bin/env python3
"""Audit and selectively mitigate Codex SQLite feedback-log writes."""

import argparse
import os
import shutil
import sqlite3
import stat
import subprocess
import sys
import time
from contextlib import closing
from datetime import datetime
from pathlib import Path


CODEX_HOME = os.environ.get("CODEX_HOME") or str(Path.home() / ".codex")
DB = Path(CODEX_HOME).expanduser() / "logs_2.sqlite"
TRIGGER = "codex_drop_noisy_logs"
CREATE_TRIGGER = f"""
CREATE TRIGGER IF NOT EXISTS {TRIGGER}
BEFORE INSERT ON logs
WHEN NEW.level IN ('TRACE', 'DEBUG')
  OR (
    NEW.level = 'INFO'
    AND NEW.target IN ('codex_otel.log_only', 'codex_otel.trace_safe')
  )
BEGIN
  SELECT RAISE(IGNORE);
END;
"""
DROP_TRIGGER = f"DROP TRIGGER IF EXISTS {TRIGGER};"
REQUIRED_COLUMNS = {"level", "target"}


def fail(message):
    raise SystemExit(message)


def connect(read_only=False):
    if not DB.exists():
        fail(f"Codex log database not found: {DB}")
    if read_only:
        uri = DB.resolve().as_uri() + "?mode=ro"
        return sqlite3.connect(uri, uri=True, timeout=10)
    return sqlite3.connect(DB, timeout=10)


def validate_schema(con):
    table = con.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='logs'"
    ).fetchone()
    if not table:
        fail("Unsupported database schema: table 'logs' was not found.")
    columns = {row[1] for row in con.execute("PRAGMA table_info(logs)")}
    missing = REQUIRED_COLUMNS - columns
    if missing:
        fail(
            "Unsupported database schema: missing logs columns: "
            + ", ".join(sorted(missing))
        )
    return columns


def codex_processes():
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                ["tasklist", "/FO", "CSV", "/NH"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                return None
            names = {
                line.split('","', 1)[0].strip('"').lower()
                for line in result.stdout.splitlines()
                if line.strip()
            }
            return sorted(
                name
                for name in names
                if name in {"codex.exe", "codex desktop.exe", "codex-app-server.exe"}
            )
        result = subprocess.run(
            ["ps", "-A", "-o", "comm="],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return None
        matches = []
        for line in result.stdout.splitlines():
            name = Path(line.strip()).name.lower()
            if (
                name in {"codex", "codex desktop"}
                or name.startswith("codex-app-ser")
            ):
                matches.append(name)
        return sorted(set(matches))
    except OSError:
        return None


def file_size(path):
    return path.stat().st_size if path.exists() else 0


def human_size(size):
    units = ["B", "KB", "MB", "GB", "TB"]
    sign = "-" if size < 0 else ""
    value = float(size)
    value = abs(value)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{sign}{value:.2f} {unit}"
        value /= 1024


def trigger_sql(con):
    row = con.execute(
        "SELECT sql FROM sqlite_master WHERE type='trigger' AND name=?",
        (TRIGGER,),
    ).fetchone()
    return row[0] if row else None


def normalize_sql(value):
    return " ".join((value or "").lower().replace(";", " ").split())


def canonical_trigger_sql(value):
    return normalize_sql(value).replace(
        "create trigger if not exists ", "create trigger ", 1
    )


def expected_trigger(sql):
    return canonical_trigger_sql(sql) == canonical_trigger_sql(CREATE_TRIGGER)


def backup_files():
    return sorted(
        path
        for path in DB.parent.glob(f"{DB.name}.backup-*")
        if not path.name.endswith(("-wal", "-shm", ".partial"))
    )


def status(_args):
    with closing(connect(read_only=True)) as con:
        columns = validate_schema(con)
        installed = trigger_sql(con)
        print(f"Database: {DB}")
        print(f"Database size: {human_size(file_size(DB))}")
        print(f"WAL size: {human_size(file_size(Path(str(DB) + '-wal')))}")
        if installed:
            state = "enabled" if expected_trigger(installed) else "conflicting"
        else:
            state = "disabled"
        print(f"Selective filter: {state}")
        backups = backup_files()
        print(
            f"Backups: {len(backups)} files, "
            f"{human_size(sum(file_size(path) for path in backups))}"
        )
        print("\nRows by level:")
        size_expression = (
            "COALESCE(SUM(estimated_bytes), 0)"
            if "estimated_bytes" in columns
            else "0"
        )
        query = (
            "SELECT level, COUNT(*), "
            + size_expression
            + " FROM logs GROUP BY level ORDER BY COUNT(*) DESC"
        )
        for level, count, size in con.execute(query):
            print(f"  {level:8} {count:10}  {human_size(size)}")
        print("\nTop targets:")
        for target, count in con.execute(
            """
            SELECT target, COUNT(*) FROM logs
            GROUP BY target ORDER BY COUNT(*) DESC LIMIT 10
            """
        ):
            print(f"  {count:10}  {target}")


def snapshot():
    with closing(connect(read_only=True)) as con:
        columns = validate_schema(con)
        if "id" not in columns:
            fail("Unsupported database schema: logs.id was not found.")
        count, max_id = con.execute(
            "SELECT COUNT(*), COALESCE(MAX(id), 0) FROM logs"
        ).fetchone()
    return {
        "count": count,
        "max_id": max_id,
        "db": file_size(DB),
        "wal": file_size(Path(str(DB) + "-wal")),
    }


def measure(args):
    before = snapshot()
    print(f"Measuring SQLite churn for {args.seconds} seconds...")
    time.sleep(args.seconds)
    after = snapshot()
    elapsed = float(args.seconds)
    print(f"ID advance: {after['max_id'] - before['max_id']}")
    print(f"Retained row delta: {after['count'] - before['count']}")
    print(f"ID advances/sec: {(after['max_id'] - before['max_id']) / elapsed:.2f}")
    print(f"Database size delta: {human_size(after['db'] - before['db'])}")
    print(f"WAL size delta: {human_size(after['wal'] - before['wal'])}")
    print("Note: this measures SQLite churn, not total physical SSD writes.")


def require_stopped(force):
    processes = codex_processes()
    if processes is None and not force:
        fail(
            "Could not determine whether Codex is running. Refusing to modify "
            "the database. Confirm Codex is stopped, then retry with --force."
        )
    if processes and not force:
        fail(
            "Codex appears to be running ("
            + ", ".join(processes)
            + "). Fully exit Codex, including tray and background processes, "
            "then retry. Use --force only after confirming detection is wrong."
        )


def verify_integrity(con, label):
    row = con.execute("PRAGMA quick_check").fetchone()
    if not row or row[0] != "ok":
        fail(f"{label} failed SQLite quick_check: {row[0] if row else 'no result'}")


def backup_database():
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup = DB.with_name(f"{DB.name}.backup-{stamp}")
    partial = backup.with_name(backup.name + ".partial")
    free_bytes = shutil.disk_usage(DB.parent).free
    required_bytes = file_size(DB) + 16 * 1024 * 1024
    if free_bytes < required_bytes:
        fail(
            "Insufficient free space for a safe database backup. "
            f"Need at least {human_size(required_bytes)}, "
            f"available {human_size(free_bytes)}."
        )
    try:
        with closing(connect(read_only=True)) as source:
            verify_integrity(source, "Source database")
            with closing(sqlite3.connect(partial)) as target:
                source.backup(target)
                verify_integrity(target, "Backup database")
        os.replace(partial, backup)
    except BaseException:
        try:
            if partial.exists():
                partial.unlink()
        except OSError:
            pass
        raise
    try:
        os.chmod(backup, stat.S_IMODE(DB.stat().st_mode))
    except OSError:
        pass
    return backup


def apply_filter(args):
    require_stopped(args.force)
    with closing(connect(read_only=True)) as con:
        validate_schema(con)
        verify_integrity(con, "Source database")
        existing = trigger_sql(con)
        if existing and not expected_trigger(existing):
            fail(
                f"A different trigger named {TRIGGER} already exists. "
                "Refusing to overwrite it."
            )
        if existing:
            print(f"Trigger already installed: {TRIGGER}")
            return
    backup = backup_database()
    require_stopped(args.force)
    with closing(connect()) as con:
        con.execute(CREATE_TRIGGER)
        installed = trigger_sql(con)
        if not installed or not expected_trigger(installed):
            con.rollback()
            fail("Trigger verification failed; database change was rolled back.")
        con.commit()
    print(f"Backup: {backup}")
    print(f"Installed trigger: {TRIGGER}")


def remove_filter(args):
    require_stopped(args.force)
    with closing(connect(read_only=True)) as con:
        validate_schema(con)
        verify_integrity(con, "Source database")
        existing = trigger_sql(con)
        if not existing:
            print(f"Trigger not installed: {TRIGGER}")
            return
        if not expected_trigger(existing):
            fail(
                f"A different trigger named {TRIGGER} exists. "
                "Refusing to remove an unrecognized trigger."
            )
    backup = backup_database()
    require_stopped(args.force)
    with closing(connect()) as con:
        con.execute(DROP_TRIGGER)
        remaining = trigger_sql(con)
        if remaining:
            con.rollback()
            fail("Trigger removal verification failed; database change was rolled back.")
        con.commit()
    print(f"Backup: {backup}")
    print(f"Removed trigger: {TRIGGER}")


def main():
    parser = argparse.ArgumentParser(
        description="Audit and mitigate excessive Codex SQLite log writes."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status").set_defaults(func=status)
    measure_parser = sub.add_parser("measure")
    measure_parser.add_argument("--seconds", type=int, default=30)
    measure_parser.set_defaults(func=measure)
    for name, function in (("apply", apply_filter), ("remove", remove_filter)):
        command = sub.add_parser(name)
        command.add_argument("--force", action="store_true")
        command.set_defaults(func=function)
    args = parser.parse_args()
    if getattr(args, "seconds", 1) < 1:
        fail("--seconds must be positive.")
    args.func(args)


if __name__ == "__main__":
    main()
