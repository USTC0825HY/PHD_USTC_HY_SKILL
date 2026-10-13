"""Read-only XPR membership manifest, not elaboration or a build acceptance gate."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def properties(element, tag):
    result = {}
    if element is None:
        return result
    for item in element.findall('.//' + tag):
        result.setdefault(item.get('Name', '').lower(), []).append(item.get('Val', ''))
    return result


def last(props, key, default=''):
    return props.get(key.lower(), [default])[-1]


def truth(value):
    return str(value).lower() in {'1', 'true', 'yes'}


def inspect_project(xpr, stage='synthesis', top=None):
    xpr = Path(xpr).resolve(strict=True)
    tree = ET.parse(xpr).getroot()
    config = properties(tree.find('Configuration'), 'Option')
    sets = {e.get('Name'): e for e in tree.findall('./FileSets/FileSet')}
    run_list = []
    for run in tree.findall('./Runs/Run'):
        run_list.append(dict(run.attrib, properties=properties(run, 'Option')))
    active_run = next((r for r in run_list if 'Synth' in r.get('Type', '') and
                       (r.get('State') == 'current' or truth(r.get('Current', '')))), None)
    source_set = (active_run or {}).get('SrcSet', 'sources_1')
    active_impl = next((r for r in run_list if r.get('SynthRun') and
                       (r.get('State') == 'current' or truth(r.get('Current', '')))), None)
    constraint_set = (active_impl or active_run or {}).get('ConstrsSet', 'constrs_1')
    top_set = 'sim_1' if stage == 'simulation' else source_set
    source_opts = properties(sets.get(top_set, ET.Element('empty')).find('Config'), 'Option')
    configured_top = last(source_opts, 'TopModule')
    issues = []
    if not last(config, 'Part'):
        issues.append({'severity': 'error', 'code': 'missing_part', 'detail': str(xpr)})
    if not configured_top:
        issues.append({'severity': 'error', 'code': 'missing_top', 'detail': top_set})
    if top and top != configured_top:
        issues.append({'severity': 'error', 'code': 'top_mismatch', 'detail': f'{top} != {configured_top}'})
    if source_set not in sets:
        issues.append({'severity': 'error', 'code': 'missing_sourceset', 'detail': source_set})
    inputs, seen = [], set()
    selected_sets = {source_set, constraint_set} if stage != 'simulation' else {source_set, 'sim_1'}
    # BlockSrcs are registered independent of the main fileset. OOC runs
    # establish ownership; ambiguous orphan blocks must not silently disappear.
    for fsname, fs in sets.items():
        if fs.get('Type') == 'BlockSrcs':
            opts = properties(fs.find('Config'), 'Option')
            if last(opts, 'IsEnabled', '1').lower() not in {'0', 'false', 'no'}:
                selected_sets.add(fsname)
                linked = any(r.get('SrcSet') == fsname for r in run_list)
                if not linked:
                    issues.append(dict(severity='needs_review', code='unresolved_ip_association', detail=fsname))
    for fsname, fs in sets.items():
        for order, element in enumerate(fs.findall('File')):
            raw = element.get('Path', '')
            attrs = properties(element, 'Attr')
            uses = [v.lower() for v in attrs.get('usedin', [])]
            disabled = truth(last(attrs, 'AutoDisabled')) or last(attrs, 'IsEnabled', '1').lower() in {'0', 'false', 'no'}
            stage_flag = last(attrs, 'UsedIn' + stage, 'true')
            active = fsname in selected_sets and not disabled and (not uses or stage in uses) and truth(stage_flag)
            resolved = raw.replace('$PPRDIR', str(xpr.parent)).replace('$PSRCDIR', str(xpr.parent / (xpr.stem + '.srcs')))
            path = None
            if '$' not in resolved and resolved:
                path = Path(resolved)
                path = (xpr.parent / path).resolve() if not path.is_absolute() else path.resolve()
            exists = bool(path and path.is_file())
            generated = truth(last(attrs, 'IsGenerated')) or bool(last(attrs, 'ParentCompositeFile'))
            role = ('ip' if raw.lower().endswith(('.xci', '.bd', '.xcix')) else
                    'generated' if generated else 'constraint' if raw.lower().endswith('.xdc') else
                    'simulation' if fsname.startswith('sim_') else 'rtl' if raw.lower().endswith(('.v', '.sv', '.vhd', '.vhdl')) else 'data_or_header')
            row = dict(fileset=fsname, order=order, raw_path=raw, path=str(path) if path else None,
                       active=active, disabled=disabled, used_in=uses, role=role, generated=generated,
                       exists=exists, sha256=sha256(path) if exists else None, attributes=attrs,
                       processing_order=last(attrs, 'ProcessingOrder', 'NORMAL'),
                       scoped_to_ref=last(attrs, 'ScopedToRef'), scoped_to_cells=last(attrs, 'ScopedToCells'))
            inputs.append(row)
    from ip_membership import inspect_ips
    # Container wrappers may omit AutoDisabled while their root XCI carries it.
    for row in inputs:
        if row['path'] and row['path'].lower().endswith('.xcix'):
            p = Path(row['path'])
            virtual = str(p.parent / p.stem / (p.stem + '.xci')).casefold()
            roots = [r for r in inputs if r['fileset'] == row['fileset'] and r['path'] and r['path'].casefold() == virtual]
            if len(roots) == 1 and not roots[0]['active']:
                row['active'] = False
                row['disabled'] = roots[0]['disabled']
    logical_ips, containers = inspect_ips(inputs, issues)
    for row in inputs:
        if not row['active']:
            continue
        path, raw = row['path'], row['raw_path']
        key = path.casefold() if path else raw
        if key in seen:
            issues.append(dict(severity='error', code='duplicate_membership', detail=key))
        seen.add(key)
        if path is None:
            issues.append(dict(severity='needs_review', code='unresolved_path', detail=raw))
        elif not row['exists']:
            issues.append(dict(severity='needs_review' if row['generated'] else 'error',
                code='missing_generated_input' if row['generated'] else 'missing_input', detail=path))
        if path:
            parts = Path(path).parts
            native = xpr.parent / (xpr.stem + '.srcs') / 'reference'
            if Path(path).is_relative_to(native) and row['fileset'] != 'sim_1':
                issues.append(dict(severity='error', code='active_reference_input', detail=path))
            try:
                relevant = Path(path).relative_to(xpr.parent).parts
            except ValueError:
                relevant = parts
            if any(v.lower() in {'build', 'tmp', 'temp', '.codex_work'} for v in relevant):
                issues.append(dict(severity='error', code='temporary_input_dependency', detail=path))
    from rtl_ports import strip_comments, read_hdl_text
    top_candidates = []
    module_sources = {}
    for item in inputs:
        if item['active'] and item['exists'] and item['role'] in {'rtl', 'simulation'} and Path(item['path']).suffix.lower() in {'.v', '.sv'}:
            text = strip_comments(read_hdl_text(item['path']))
            for module in re.findall(r'\bmodule\s+(?:automatic\s+)?([A-Za-z_][\w$]*)', text):
                module_sources.setdefault(module, []).append(item['path'])
            matches = re.findall(r'\bmodule\s+' + re.escape(configured_top) + r'\b', text) if configured_top else []
            top_candidates.extend([item['path']] * len(matches))
    for module, paths in module_sources.items():
        if len(paths) > 1:
            issues.append(dict(severity='needs_review', code='duplicate_module_candidates',
                               detail=f'{module}: {paths}; inspect preprocessor/compile-order evidence'))
    if len(top_candidates) != 1:
        issues.append(dict(severity='error' if len(top_candidates) > 1 else 'needs_review',
                           code='ambiguous_top_definition' if top_candidates else 'unresolved_top_definition',
                           detail=f'{configured_top}: {top_candidates}; VHDL/IP/BD/generated tops need tool evidence'))
    version = re.search(r'Product Version:\s*Vivado\s+v([0-9.]+)', xpr.read_text(encoding='utf-8-sig'))
    return dict(schema_version=1, project=str(xpr), project_sha256=sha256(xpr),
                top_sources=top_candidates,
                xpr_schema_version=tree.get('Version'), tool_version=version[1] if version else None, part=last(config, 'Part'), top=configured_top,
                stage=stage, source_set=source_set, top_fileset=top_set, constraint_set=constraint_set,
                inputs=inputs, runs=run_list, issues=issues,
                logical_ips=logical_ips, active_ip_count=len(logical_ips), containers=containers,
                status='fail' if any(i['severity'] == 'error' for i in issues) else 'needs_review' if issues else 'pass',
                boundary='Static XPR membership only; IP dependencies, effective Tcl/compile order and elaboration are not proven.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xpr', type=Path)
    parser.add_argument('--stage', choices=['synthesis', 'implementation', 'simulation'], default='synthesis')
    parser.add_argument('--top', help='Expected top; does not override the XPR')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        result = inspect_project(args.xpr, args.stage, args.top)
    except (OSError, ValueError, ET.ParseError) as exc:
        result = dict(status='fail', error=str(exc))
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8')
    else:
        print(text, end='')
    return 0 if result['status'] == 'pass' else 2


if __name__ == '__main__':
    raise SystemExit(main())
