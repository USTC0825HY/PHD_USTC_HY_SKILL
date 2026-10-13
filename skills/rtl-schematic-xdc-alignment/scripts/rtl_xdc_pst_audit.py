#!/usr/bin/env python3
"""Conservative static RTL/XDC/PST audit. Never evaluates Tcl or claims applied constraints."""
from __future__ import annotations
import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'fpga-vivado-tcl-automation' / 'scripts'))
from project_inputs import inspect_project, sha256
from rtl_ports import module_ports, port_bits, read_hdl_text, strip_comments as strip_verilog_comments


def parse_rtl_ports(path, module):
    ports, _ = module_ports(read_hdl_text(path), module)
    if not ports: raise ValueError(f'未能解析顶层端口: {path}')
    return ports


def active_xdc_lines(path):
    """Split commands without evaluation. Tcl # starts a command comment."""
    text = read_hdl_text(path)
    commands, buf = [], []
    braces = brackets = 0
    quoted = False
    line = start = 1
    pos = 0
    while pos < len(text):
        c = text[pos]
        if c == '\\' and pos + 1 < len(text) and text[pos + 1] == '\n':
            buf.append(' '); line += 1; pos += 2; continue
        if c == '#' and not ''.join(buf).strip() and not braces and not brackets and not quoted:
            stop = text.find('\n', pos)
            if stop < 0: break
            pos = stop; continue
        if not ''.join(buf).strip(): start = line
        if c == '"' and not braces: quoted = not quoted
        if not quoted:
            if c == '{': braces += 1
            elif c == '}': braces -= 1
        if not braces:
            if c == '[': brackets += 1
            elif c == ']': brackets -= 1
        if c in ';\n' and not braces and not brackets and not quoted:
            if ''.join(buf).strip(): commands.append((start, ''.join(buf).strip()))
            buf = []
        else: buf.append(c)
        if c == '\n': line += 1
        pos += 1
    if ''.join(buf).strip(): commands.append((start, ''.join(buf).strip()))
    if braces or brackets or quoted: raise ValueError(f'Unbalanced Tcl command in {path}')
    return commands


def words(command):
    result, buf = [], []
    braces = brackets = 0
    quoted = False
    for c in command:
        if c.isspace() and not braces and not brackets and not quoted:
            if buf: result.append(''.join(buf)); buf = []
            continue
        if c == '"' and not braces: quoted = not quoted
        if not quoted:
            if c == '{': braces += 1
            elif c == '}': braces -= 1
        if not braces:
            if c == '[': brackets += 1
            elif c == ']': brackets -= 1
        buf.append(c)
    if braces or brackets or quoted: raise ValueError('Unbalanced Tcl words')
    if buf: result.append(''.join(buf))
    return result


def literal(word):
    braced = word.startswith('{') and word.endswith('}')
    quoted = word.startswith('"') and word.endswith('"')
    value = word[1:-1] if braced or quoted else word
    if '\\' in value or (not braced and any(c in value for c in '$[]')):
        raise ValueError('Dynamic/escaped Tcl word: ' + word)
    return value


def expand_ports(expression, rtl_ports):
    expanded = []
    for token in words(literal(expression)):
        if token.startswith(('{', '"')): token = literal(token)
        if token.endswith('[*]'):
            base = token[:-3]
            item = rtl_ports.get(base, {})
            indices = item.get('indices')
            if indices is None and item.get('width') and not item.get('width_expr'):
                indices = list(range(item['width']))
            if indices is None: raise ValueError('Unknown bus width: ' + base)
            expanded += [f'{base}[{i}]' for i in indices if i is not None]
        elif '*' in token or '?' in token:
            matched = [name for name in port_bits(rtl_ports) if fnmatch.fnmatchcase(name, token)]
            if not matched: raise ValueError('Empty port pattern: ' + token)
            expanded += matched
        else: expanded.append(token)
    return expanded


def get_port_expression(word):
    if not word.startswith('[') or not word.endswith(']'): raise ValueError('Expected literal get_ports')
    parts = words(word[1:-1])
    if not parts or parts.pop(0) != 'get_ports': raise ValueError('Not get_ports')
    if parts and parts[0] == '-quiet': parts.pop(0)
    if len(parts) != 1 or parts[0].startswith('-'): raise ValueError('Unsupported get_ports options')
    return parts[0]


def parse_xdc_full(paths, rtl_ports):
    records, errors, unresolved, ignored = {}, [], [], []
    for path in paths:
        for number, line in active_xdc_lines(path):
            source = f'{path}:{number}'
            try:
                tokens = words(line)
                if not tokens: continue
                if re.search(r'\[\s*(?:exec|eval|source|set|set_property|reset_property)\b', line):
                    raise ValueError('Side-effectful command substitution requires tool review')
                if tokens[0] in {'create_clock', 'create_generated_clock', 'set_clock_groups', 'set_false_path',
                                 'set_multicycle_path', 'set_max_delay', 'set_min_delay', 'set_input_delay', 'set_output_delay'}:
                    ignored.append(dict(source=source, reason='timing command; not a pin audit')); continue
                if tokens[0] != 'set_property': raise ValueError('Unsupported command: ' + tokens[0])
                if len(tokens) != 4: raise ValueError('Unsupported set_property syntax')
                if tokens[1] == '-dict':
                    values = words(literal(tokens[2]))
                    if len(values) % 2: raise ValueError('Odd property dictionary')
                    pairs = [(literal(values[i]).upper(), literal(values[i+1])) for i in range(0, len(values), 2)]
                else: pairs = [(literal(tokens[1]).upper(), literal(tokens[2]))]
                if any(not re.fullmatch(r'[A-Z_][A-Z0-9_.]*', p) for p, _ in pairs):
                    raise ValueError('Unsupported property name/list')
                pin_pairs = [(p, v) for p, v in pairs if p in {'PACKAGE_PIN', 'IOSTANDARD'}]
                if not pin_pairs:
                    ignored.append(dict(source=source, reason='non-pin property')); continue
                ports = expand_ports(get_port_expression(tokens[3]), rtl_ports)
                if not ports: raise ValueError('Empty get_ports result')
                for port in ports:
                    record = records.setdefault(port, dict(port=port, package_pin=None, iostandard=None, xdc_sources=[]))
                    for prop, value in pin_pairs:
                        key = prop.lower()
                        if record[key] is not None: errors.append(f'端口{port}存在重复有效{prop}: {record[key]} / {value}')
                        record[key] = value
                    record['xdc_sources'].append(source)
            except ValueError as exc:
                unresolved.append(dict(source=source, command=line, reason=str(exc)))
    return list(records.values()), errors, unresolved, ignored


def parse_xdc(path, rtl_ports):
    records, errors, unresolved, _ = parse_xdc_full([path], rtl_ports)
    return records, errors + [u['reason'] for u in unresolved]


def parse_pst_fpga(path, refdes):
    current_net = None
    result, expect_name = {}, False
    for index, line in enumerate(Path(path).read_text(encoding='utf-8', errors='replace').splitlines(), 1):
        if line.strip().upper() == 'NET_NAME': expect_name = True; continue
        if expect_name:
            match = re.match(r"^\s*'([^']*)'", line)
            if match: current_net = match[1]; expect_name = False
            continue
        node = re.match(r'^NODE_NAME\s+([^\s]+)\s+([^\s]+)', line, re.I)
        if node and node[1].upper() == refdes.upper():
            result.setdefault(node[2].upper(), []).append(dict(network=current_net, source=f'{path}:{index}'))
    if not result: raise ValueError(f'PST中未找到FPGA位号{refdes}: {path}')
    return result


def base_port(port):
    return re.sub(r'\[-?\d+\]$', '', port)


def load_exemptions(path, part):
    if not path: return {}
    evidence = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    source = Path(evidence['evidence_file'])
    if not source.is_absolute(): source = Path(path).resolve().parent / source
    if not part or evidence.get('part') != part or sha256(source) != evidence.get('evidence_sha256'):
        raise ValueError('Dedicated pin evidence part/hash mismatch')
    pins = evidence.get('pins', {})
    if not pins or any(not re.fullmatch(r'MGT(?:(?:H|P|X)(?:TX|RX)|REFCLK)[A-Za-z0-9_]*', function, re.I)
                       for function in pins.values()):
        raise ValueError('Dedicated pin evidence must contain actual MGT package-pin functions')
    return {pin.upper(): function for pin, function in pins.items()}


def audit(args):
    manifest = inspect_project(args.project, 'implementation', args.top) if getattr(args, 'project', None) else None
    top = manifest['top'] if manifest else args.top
    errors, review = [], []
    if manifest:
        for issue in manifest['issues']:
            (errors if issue['severity'] == 'error' else review).append(str(issue))
        active = [i for i in manifest['inputs'] if i['active']]
        matches = []
        for item in active:
            if item['exists'] and item['role'] == 'rtl' and Path(item['path']).suffix.lower() in {'.v', '.sv'}:
                if re.search(r'\bmodule\s+' + re.escape(top) + r'\b', strip_verilog_comments(read_hdl_text(item['path']))):
                    matches.append(Path(item['path']))
        if len(matches) != 1: raise ValueError(f'Top requires one active RTL definition: {top}: {matches}')
        rtl = matches[0]
        selected = [i for i in active if i['role'] == 'constraint']
        rank = {'EARLY': 0, 'NORMAL': 1, 'LATE': 2}
        selected.sort(key=lambda i: (rank.get(i['processing_order'].upper(), 1), i['order']))
        xdcs = [Path(i['path']) for i in selected if i['exists']]
        if any(i['scoped_to_ref'] or i['scoped_to_cells'] for i in selected):
            review.append('Scoped XDC requires Vivado object resolution; not a flat top-port audit')
        if getattr(args, 'rtl', None) and args.rtl.resolve() != rtl: errors.append('Explicit RTL disagrees with active XPR top')
        explicit_xdc = getattr(args, 'xdc', None)
        if explicit_xdc and [p.resolve() for p in explicit_xdc] != xdcs: errors.append('Explicit XDC list disagrees with XPR implementation constraints')
        part = manifest['part']
    else:
        rtl = args.rtl.resolve()
        xdcs = args.xdc if isinstance(args.xdc, list) else [args.xdc]
        part = getattr(args, 'part', None)
    ports, port_issues = module_ports(read_hdl_text(rtl), top)
    review += port_issues
    if not ports: errors.append('No RTL ports parsed')
    records, xerrors, unknown, ignored = parse_xdc_full(xdcs, ports)
    errors += xerrors
    review += [u['reason'] for u in unknown]
    if not records: errors.append('No pin constraints parsed; coverage is zero')
    pst = parse_pst_fpga(args.pstxnet, args.fpga_refdes)
    exemptions = load_exemptions(getattr(args, 'dedicated_pins', None), part)
    all_bits = set(port_bits(ports))
    expected = all_bits.copy()
    selection = getattr(args, 'ports', None)
    if selection:
        chosen = set()
        for expression in selection: chosen.update(expand_ports('{' + expression + '}', ports))
        for port in chosen - expected: errors.append('Requested port absent or unresolved: ' + port)
        expected &= chosen
    else: chosen = None
    seen, pins, rows = set(), {}, []
    for record in records:
        pin = str(record['package_pin'] or '').upper()
        if pin and pin in pins and pins[pin] != record['port']: errors.append(f'封装管脚{pin}同时绑定{pins[pin]}和{record["port"]}')
        pins[pin] = record['port']
        port = record['port']
        if chosen is not None and port not in chosen: continue
        seen.add(port)
        rtl_port = ports.get(base_port(port))
        if port not in all_bits: errors.append(f'XDC端口{port}在RTL顶层中不存在或下标越界/无法确认')
        if not pin: errors.append(f'端口{port}缺少PACKAGE_PIN')
        if not record['iostandard'] and pin not in exemptions: errors.append(f'端口{port}缺少IOSTANDARD')
        if pin in exemptions and record['iostandard']: errors.append(f'Dedicated pad {port}/{pin} has a fabric IOSTANDARD')
        mappings = pst.get(pin, [])
        if pin and not mappings: errors.append(f'XDC封装管脚{pin}未在PST {args.fpga_refdes}节点中找到')
        if any(not row['network'] for row in mappings): review.append(f'Unresolved PST net for {pin}')
        rows.append(dict(record, rtl_base_port=base_port(port), rtl_direction=(rtl_port or {}).get('direction'),
                         rtl_width=(rtl_port or {}).get('width'), fpga_refdes=args.fpga_refdes,
                         pst_networks=mappings, dedicated_pin_function=exemptions.get(pin),
                         evidence_level='Static candidate; effective Vivado application unverified'))
    for missing in sorted(expected - seen): errors.append('Missing pin constraint: ' + missing)
    errors, review = sorted(set(errors)), sorted(set(review))
    inputs = [rtl, *xdcs, args.pstxnet]
    if getattr(args, 'dedicated_pins', None): inputs.append(args.dedicated_pins)
    return dict(schema_version=2, top=top, part=part, rtl=str(rtl), xdc=str(xdcs[0]) if len(xdcs) == 1 else [str(p) for p in xdcs], xdc_files=[str(p) for p in xdcs],
                pstxnet=str(args.pstxnet), fpga_refdes=args.fpga_refdes, rows=rows, errors=errors,
                needs_review=review, unparsed=unknown, ignored_non_pin=ignored,
                coverage=dict(scope='selected_ports' if selection else 'whole_top', expected=len(expected),
                              constrained=len(expected & seen), missing=sorted(expected - seen),
                              unknown_widths=[n for n, p in ports.items() if p['indices'] is None]),
                input_sha256={str(p): sha256(p) for p in inputs}, project_manifest=manifest,
                status='fail' if errors else 'needs_review' if review else 'pass',
                vivado_status='RTL/XDC静态核查完成，Vivado应用状态未复核')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path)
    parser.add_argument('--rtl', type=Path)
    parser.add_argument('--top')
    parser.add_argument('--part')
    parser.add_argument('--xdc', type=Path, action='append', help='Repeat in processing order; or derive from --project')
    parser.add_argument('--ports', nargs='+', help='Exact port bits or literal patterns; default whole top')
    parser.add_argument('--pstxnet', required=True, type=Path)
    parser.add_argument('--fpga-refdes', default='D1')
    parser.add_argument('--dedicated-pins', type=Path, help='Hash-bound reviewed package-pin evidence JSON')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if not args.project and not all([args.rtl, args.top, args.xdc]): parser.error('Provide --project or --rtl, --top and --xdc')
    try: result = audit(args)
    except (ValueError, OSError, KeyError) as exc: result = dict(status='fail', errors=[str(exc)])
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8')
    else: print(text, end='')
    return 0 if result['status'] == 'pass' else 2


if __name__ == '__main__': raise SystemExit(main())
