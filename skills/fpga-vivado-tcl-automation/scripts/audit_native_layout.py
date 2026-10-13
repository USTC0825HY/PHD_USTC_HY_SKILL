"""Read-only XPR/layout audit. No Vivado launch, rewrites, moves or deletion."""
import argparse
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from project_inputs import inspect_project


def audit(xpr, legacy=False):
    xpr = Path(xpr).resolve()
    root, name = xpr.parent, xpr.stem
    issues, inputs, seen = [], [], set()

    def issue(code, path, detail, warning=False):
        issues.append(dict(code=code, path=str(path), detail=detail,
                           severity="warning" if warning or (legacy and code not in {'missing_input', 'duplicate_membership', 'missing_top', 'missing_part', 'top_mismatch', 'missing_sourceset', 'ambiguous_top_definition'}) else "error"))

    native = {name + suffix for suffix in
              (".srcs", ".runs", ".cache", ".sim", ".hw", ".ip_user_files", ".gen")}
    allowed = native | {".Xil", ".git", "scripts", "docs", "release"}
    files = {xpr.name, "AGENTS.md", "MEMORY.md", "README.md", ".gitignore", ".gitattributes"}
    for entry in root.iterdir():
        if entry.is_dir() and entry.name not in allowed:
            issue("extra_root_directory", entry, "Inspect ownership; do not delete automatically")
        elif entry.is_file() and entry.name not in files:
            if entry.suffix.lower() in {".log", ".jou", ".str", ".zip"} and entry.name.startswith("vivado"):
                issue("gui_log", entry, "Allowed tool evidence; automation should redirect new logs", True)
            else:
                issue("extra_root_file", entry, "Place new reports/scripts in their owned folder")
    manifest = inspect_project(xpr)
    for problem in manifest['issues']:
        issues.append(dict(problem, path=problem['detail']))
    for entry in manifest['inputs']:
            if not entry['active'] or not entry['path']:
                continue
            fsname = entry['fileset']
            path = Path(entry['path'])
            key = (fsname, str(path).casefold())
            if key in seen:
                issue("duplicate_membership", path, fsname)
            seen.add(key)
            inputs.append(dict(fileset=fsname, path=str(path)))
            expected = root / (name + ".srcs") / ("sources_1" if entry["role"] == "ip" or entry.get("container") else fsname)
            try:
                rel = path.relative_to(expected)
            except ValueError:
                issue("external_input", path, "Needs documented external-library exception; never temporary dependency")
                continue
            if fsname in {"sources_1", "sim_1"} and rel.parts and rel.parts[0] == "new" and len(rel.parts) < 3:
                issue("missing_function_folder", path, "Use new/<function>/<module>")
            if fsname == "sources_1" and (path.name.startswith("tb_") or "sim_1" in path.parts):
                issue("possible_tb_in_design", path, "Inspect source role; filename is a heuristic", True)
    ignore = root / ".gitignore"
    if ignore.exists():
        for line in ignore.read_text(encoding="utf-8-sig").splitlines():
            if re.fullmatch(r"/?(?:\*|[^/]+)\.srcs/?", line.strip()):
                issue("ignored_source_tree", ignore, line)
    return dict(xpr=str(xpr), mode="legacy-read-only" if legacy else "new-project",
                inputs=inputs, issues=issues,
                passed=manifest['status'] == 'pass' and not any(i["severity"] == "error" for i in issues),
                project_manifest_status=manifest['status'],
                boundary="Static layout only; no HDL/compile-order/IP/GUI/timing/board acceptance")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xpr")
    parser.add_argument("--legacy", action="store_true", help="Report findings without applying new-layout failure policy")
    args = parser.parse_args()
    result = audit(args.xpr, args.legacy)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
