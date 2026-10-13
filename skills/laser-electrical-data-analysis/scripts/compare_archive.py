"""Compare every archive member with source files by size and SHA-256. Never delete."""
from __future__ import annotations
import argparse
import collections
import json
import locale
import ntpath
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from audit_duplicates import scan
from evidence_paths import inside, long_path, sha256, write_csv

def validate_members(names):
    errors = []
    seen = set()
    for raw in names:
        value = raw.replace("\\", "/")
        parts = value.rstrip("/").split("/")
        key = value.rstrip("/").casefold()
        if not value or value.startswith("/") or ntpath.splitdrive(value)[0] or any(p in ("..", "") for p in parts) or ":" in value:
            errors.append("unsafe archive member: " + raw)
        if key in seen:
            errors.append("duplicate/case-colliding archive member: " + raw)
        seen.add(key)
    return errors

def compare_extracted(root, extracted, expected_files):
    sources, errors = scan(root)
    members, extraction_errors = scan(extracted)
    errors.extend(extraction_errors)
    expected = {n.replace("\\", "/") for n in expected_files}
    actual = {Path(r["path"]).relative_to(extracted).as_posix() for r in members}
    if expected != actual:
        errors.append({"path": str(extracted), "error": "member inventory mismatch", "missing": sorted(expected-actual), "unexpected": sorted(actual-expected)})
    by_size = collections.defaultdict(list)
    for source in sources:
        by_size[source["bytes"]].append(source)
    cache, rows = {}, []
    for member in members:
        row = {"member": Path(member["path"]).relative_to(extracted).as_posix(), "bytes": member["bytes"], "sha256": "", "status": "unique", "matching_paths": "", "reason": ""}
        try:
            row["sha256"] = sha256(member["path"])
            matches = []
            for source in by_size[member["bytes"]]:
                path = source["path"]
                if path not in cache:
                    cache[path] = sha256(path)
                if cache[path] == row["sha256"]:
                    matches.append(path)
            if matches:
                row.update(status="matched", matching_paths="；".join(matches))
        except OSError as exc:
            row.update(status="unreadable", reason=str(exc))
            errors.append({"path": member["path"], "error": str(exc)})
        rows.append(row)
    for name in sorted(expected - actual):
        rows.append({"member": name, "bytes": "", "sha256": "", "status": "unreadable", "matching_paths": "", "reason": "listed member missing after extraction"})
    return rows, errors

def run(root, archive, out, scratch, tar=None, encoding=None):
    root, archive, out, scratch = (Path(p).resolve() for p in (root, archive, out, scratch))
    if inside(out, root) or inside(scratch, root) or inside(archive, out) or inside(archive, scratch):
        raise ValueError("outputs/scratch must be outside source root and cannot contain the archive")
    tar = tar or shutil.which("bsdtar") or shutil.which("tar.exe") or shutil.which("tar")
    if not tar:
        raise RuntimeError("bsdtar/tar unavailable")
    out.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="archive_compare_", dir=scratch))
    rows, errors = [], []
    encoding = encoding or locale.getencoding()
    info = {"archive": str(archive), "extracted_to": str(work), "tar": tar, "tool_output_encoding": encoding}
    try:
        before = sha256(archive)
        info["archive_sha256"] = before
        version = subprocess.run([tar, "--version"], capture_output=True, text=True, timeout=30)
        info["tool_version"] = version.stdout.strip()
        listing = subprocess.run([tar, "-tf", str(archive)], capture_output=True, timeout=120)
        info["list_stderr"] = listing.stderr.decode("utf-8", errors="replace")
        if listing.returncode:
            raise RuntimeError("archive listing failed: " + info["list_stderr"])
        names = listing.stdout.decode(encoding, errors="strict").splitlines()
        info["listed_members"] = names
        problems = validate_members(names)
        if problems:
            raise RuntimeError("; ".join(problems))
        # Check metadata before extraction: links and special nodes are never accepted.
        verbose = subprocess.run([tar, "-tvf", str(archive)], capture_output=True, text=True, encoding=encoding, errors="strict", timeout=120)
        details = [line for line in verbose.stdout.splitlines() if line.strip()]
        if verbose.returncode or len(details) != len(names) or any(line[0] not in "-d" for line in details):
            raise RuntimeError("cannot verify regular-file/directory-only archive inventory")
        info["member_inventory"] = [{"name":name,"type":"file" if detail[0]=="-" else "directory"} for name,detail in zip(names,details)]
        expected = [name for name, detail in zip(names, details) if detail[0] == "-"]
        extracted = subprocess.run([tar, "-xf", str(archive), "-C", str(work)], capture_output=True, timeout=3600)
        info["extract_stderr"] = extracted.stderr.decode("utf-8", errors="replace")
        if extracted.returncode:
            rows = [dict(member=n, bytes="", sha256="", status="unreadable", matching_paths="", reason="archive extraction failed") for n in expected]
            raise RuntimeError("archive extraction failed: " + info["extract_stderr"])
        rows, errors = compare_extracted(root, work, expected)
        if sha256(archive) != before:
            errors.append({"path": str(archive), "error": "archive changed during comparison"})
    except (OSError, ValueError, RuntimeError, UnicodeError, subprocess.SubprocessError) as exc:
        errors.append({"path": str(archive), "error": str(exc)})
    info.update(complete=not errors, all_members_duplicate=bool(rows) and not errors and all(r["status"] == "matched" for r in rows), members=len(rows), unique=sum(r["status"] == "unique" for r in rows), errors=errors)
    write_csv(out/"RAR比对报告.csv", rows, ["member","bytes","sha256","status","matching_paths","reason"])
    (out/"archive_comparison.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    return info

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("root", "archive", "out", "scratch"):
        parser.add_argument("--"+name, required=True, type=Path)
    parser.add_argument("--tar")
    parser.add_argument("--encoding", help="tar listing encoding; default is the OS locale encoding")
    args = parser.parse_args()
    result = run(args.root, args.archive, args.out, args.scratch, args.tar, args.encoding)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["complete"] else 2

if __name__ == "__main__":
    raise SystemExit(main())

