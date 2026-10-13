"""Read-only evidence filesystem and path mapping helpers (Python 3.10+)."""
from __future__ import annotations

import csv
import hashlib
import ntpath
import os
import stat
import time
from pathlib import Path


def long_path(path):
    value = os.fspath(path)
    if os.name != "nt" or value.startswith("\\\\?\\"):
        return value
    value = os.path.abspath(value)
    return "\\\\?\\UNC\\" + value[2:] if value.startswith("\\\\") else "\\\\?\\" + value


def display_path(path):
    value = os.fspath(path)
    if value.startswith("\\\\?\\UNC\\"):
        return "\\\\" + value[8:]
    return value[4:] if value.startswith("\\\\?\\") else value


def probe(path, attempts=3, delay=0.2, stat_fn=None, sleep_fn=time.sleep):
    """Distinguish absent child from unavailable drive/share/ancestor; bounded retry."""
    stat_fn = stat_fn or os.stat
    value = display_path(path)
    last = None
    for attempt in range(attempts):
        try:
            info = stat_fn(long_path(value))
            return {"status": "exists", "reason": "", "size": info.st_size,
                    "mtime_ns": info.st_mtime_ns, "is_dir": stat.S_ISDIR(info.st_mode)}
        except OSError as exc:
            last = exc
            if attempt + 1 < attempts:
                sleep_fn(delay * (attempt + 1))
    if isinstance(last, (FileNotFoundError, NotADirectoryError)):
        # A missing ancestor is not evidence that an offline drive is absent.
        parent = Path(value).parent
        while True:
            try:
                stat_fn(long_path(parent))
                return {"status": "missing", "reason": str(last)}
            except (FileNotFoundError, NotADirectoryError):
                if parent == parent.parent:
                    break
                parent = parent.parent
            except OSError as exc:
                return {"status": "inaccessible", "reason": str(exc)}
    return {"status": "inaccessible", "reason": str(last)}


def walk(root, errors, attempts=3):
    """Yield (directory, dirs, files); never follow links/junctions or hide errors."""
    pending = [Path(display_path(root))]
    while pending:
        folder = pending.pop()
        entries = None
        for attempt in range(attempts):
            try:
                with os.scandir(long_path(folder)) as iterator:
                    entries = list(iterator)
                break
            except OSError as exc:
                if attempt + 1 == attempts:
                    errors.append({"path": str(folder), "error": str(exc)})
                else:
                    time.sleep(0.2 * (attempt + 1))
        if entries is None:
            continue
        dirs, files = [], []
        for entry in sorted(entries, key=lambda item: item.name.casefold()):
            path = folder / entry.name
            try:
                info = entry.stat(follow_symlinks=False)
                if entry.is_symlink() or getattr(info, "st_file_attributes", 0) & 0x400:
                    errors.append({"path": str(path), "error": "link/reparse point not followed"})
                elif stat.S_ISDIR(info.st_mode):
                    dirs.append(path)
                elif stat.S_ISREG(info.st_mode):
                    files.append(path)
            except OSError as exc:
                errors.append({"path": str(path), "error": str(exc)})
        yield folder, dirs, files
        pending.extend(reversed(dirs))


def sha256(path):
    before = os.stat(long_path(path))
    digest = hashlib.sha256()
    with open(long_path(path), "rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    after = os.stat(long_path(path))
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise OSError("file changed while hashing: " + str(path))
    return digest.hexdigest()


def inside(path, root):
    """Path containment for native paths; resolves links before output checks."""
    try:
        Path(path).resolve().relative_to(Path(root).resolve())
        return True
    except ValueError:
        return False


def write_csv(path, rows, fields):
    with open(long_path(path), "w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def split_paths(value):
    return [part.strip() for part in value.split("；") if part.strip()]


def canonical(value):
    # Windows datasets remain Windows paths even when unit-tested on another OS.
    return ntpath.normpath(display_path(value).replace("/", "\\"))


def mapping_status(row):
    """Missing status remains a readable draft, never implicit approval."""
    return (row.get("status") or row.get("状态") or "").strip()


def load_mapping(path):
    if not path:
        return []
    rows = []
    with open(long_path(path), encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            old = row.get("old", row.get("原路径", ""))
            new = row.get("new", row.get("新路径/处置", ""))
            state = mapping_status(row)
            if state not in ("OK", "confirmed", "已确认"):
                continue
            if not old or not new:
                raise ValueError("confirmed mapping requires old and new paths")
            # Existing appendix maps describe COMPLETE paths, not prefix rules.
            match = row.get("match", "exact") or "exact"
            if match not in ("exact", "prefix"):
                raise ValueError("mapping match must be exact or prefix")
            rows.append({"old": old, "new": new, "match": match})
    return rows


def mapped_path(value, mappings):
    key = canonical(value)
    candidates = []
    for rule in mappings:
        old = canonical(rule["old"])
        exact = key.casefold() == old.casefold()
        prefix = rule.get("match", "exact") == "prefix" and key.casefold().startswith(old.casefold() + "\\")
        if exact or prefix:
            suffix = key[len(old):].lstrip("\\")
            candidates.append((len(old), ntpath.join(rule["new"], suffix) if suffix else rule["new"]))
    if not candidates:
        return value, False
    longest = max(length for length, _ in candidates)
    targets = {canonical(target) for length, target in candidates if length == longest}
    if len(targets) != 1:
        raise ValueError("ambiguous mapping: " + value)
    return targets.pop(), True


def resolve_path(value, root, mappings=(), probe_fn=probe):
    row = {"original_path": value, "resolved_path": value, "display_path": value,
           "status": "", "location": "", "reason": ""}
    try:
        target, mapped = mapped_path(value, mappings)
        root_abs = os.path.abspath(root)
        # On Windows, reject drive-relative paths such as I:foo.
        if os.name == "nt" and ntpath.splitdrive(target)[0] and not ntpath.isabs(target):
            raise ValueError("drive-relative path is ambiguous")
        physical = Path(target) if Path(target).is_absolute() else Path(root_abs) / target
        physical = Path(os.path.abspath(physical))
        root_state = probe_fn(root_abs)
        state = probe_fn(physical)
        contained = inside(physical, root_abs)
        row.update(resolved_path=str(physical), status=state["status"],
                   location="in_library" if contained else "outside_library", reason=state["reason"])
        if contained and root_state["status"] != "exists":
            row.update(status="inaccessible", reason="library root unavailable: " + root_state["reason"])
        elif contained and state["status"] == "exists":
            row["display_path"] = str(physical.relative_to(Path(root_abs)))
        else:
            # A failed mapping must never turn an external original into a broken relative path.
            row["display_path"] = value if mapped else str(physical)
        if not contained and state["status"] == "exists":
            row["reason"] = "verified outside library"
    except (ValueError, OSError) as exc:
        row.update(status="unresolved", reason=str(exc))
    return row
