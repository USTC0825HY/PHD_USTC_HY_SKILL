"""Resolve an evidence path list without modifying sources or documents."""
import argparse
import json
from pathlib import Path
from evidence_paths import inside, load_mapping, resolve_path, split_paths, write_csv


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--mapping", type=Path)
    parser.add_argument("--input", required=True, type=Path, help="UTF-8 path lines; Chinese semicolon separates paths")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    if inside(args.out, args.root) or args.out.resolve() == args.input.resolve() or (args.mapping and args.out.resolve() == args.mapping.resolve()):
        parser.error("output must be outside the evidence root and must not overwrite inputs")
    mappings = load_mapping(args.mapping)
    rows = [resolve_path(path, args.root, mappings) for line in args.input.read_text(encoding="utf-8-sig").splitlines() for path in split_paths(line)]
    write_csv(args.out, rows, ["original_path", "resolved_path", "display_path", "status", "location", "reason"])
    print(json.dumps({"paths": len(rows), "unverified": sum(r["status"] != "exists" for r in rows)}, ensure_ascii=False))
    return 1 if any(r["status"] != "exists" for r in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
