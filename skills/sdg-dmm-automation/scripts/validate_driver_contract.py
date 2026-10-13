"""Static, read-only validation for a Python driver module's required methods."""
import argparse
import ast
import pathlib
import sys


SOURCE_METHODS = {
    "connect", "identify", "configure_dc", "apply_voltage", "output_off",
    "set_safe_output", "query_error", "close"
}
METER_METHODS = {
    "connect", "identify", "configure", "measure_voltage", "autozero_once",
    "query_error", "raise_for_error_queue", "close"
}


def classes_from_tree(tree, classes=None):
    classes = {} if classes is None else classes
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            methods = {item.name for item in node.body
                       if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))}
            bases = {base.id for base in node.bases if isinstance(base, ast.Name)}
            classes[node.name] = {"methods": methods, "bases": bases}

    def all_methods(name, visiting=None):
        visiting = set() if visiting is None else visiting
        if name in visiting or name not in classes:
            return set()
        visiting.add(name)
        result = set(classes[name]["methods"])
        for base in classes[name]["bases"]:
            result.update(all_methods(base, visiting))
        return result

    return classes, all_methods


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("driver", type=pathlib.Path)
    parser.add_argument("--base-file", action="append", type=pathlib.Path,
                        help="additional Python file containing inherited base classes")
    parser.add_argument("--kind", choices=("source", "meter", "auto"), default="auto")
    args = parser.parse_args()
    try:
        trees = [ast.parse(args.driver.read_text(encoding="utf-8"), str(args.driver))]
        trees.extend(ast.parse(path.read_text(encoding="utf-8"), str(path))
                     for path in (args.base_file or []))
    except (OSError, SyntaxError, UnicodeError) as exc:
        print("ERROR:", exc)
        return 2
    target_classes = {node.name for node in trees[0].body if isinstance(node, ast.ClassDef)}
    class_table = {}
    for tree in trees:
        current = classes_from_tree(tree)[0]
        duplicate = set(current) & set(class_table)
        if duplicate:
            print('ERROR: ambiguous class names:', ', '.join(sorted(duplicate)))
            return 2
        class_table.update(current)

    def all_methods(name, visiting=None):
        visiting = set() if visiting is None else visiting
        if name in visiting or name not in class_table:
            return set()
        visiting.add(name)
        result = set(class_table[name]["methods"])
        for base in class_table[name]["bases"]:
            result.update(all_methods(base, visiting))
        return result

    classes = [(name, all_methods(name)) for name in sorted(target_classes)]
    contracts = {'source': SOURCE_METHODS, 'meter': METER_METHODS}
    selected = contracts if args.kind == 'auto' else {args.kind: contracts[args.kind]}
    found = False
    for name, methods in classes:
        for kind, required in selected.items():
            missing = sorted(required - methods)
            if not missing:
                print('OK:', name, 'matches', kind, 'contract (static method presence only)')
                found = True
            else:
                print('INFO:', name, kind, 'missing', ', '.join(missing))
    if not found:
        print("ERROR: no class matches the requested contract")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
