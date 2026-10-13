"""Conservative text-level Verilog port extraction; unsupported forms stay unknown."""
from __future__ import annotations
import re
from pathlib import Path


def read_hdl_text(path):
    raw = Path(path).read_bytes()
    try:
        return raw.decode('utf-8-sig')
    except UnicodeDecodeError:
        # Existing Laser sources include GBK Chinese comments. Never rewrite encoding.
        return raw.decode('gb18030')


def strip_comments(text):
    text = re.sub(r'/\*.*?\*/', lambda m: ''.join('\n' if c == '\n' else ' ' for c in m[0]), text, flags=re.S)
    return re.sub(r'//[^\n]*', '', text)


def balanced(text, start):
    depth = 0
    for index in range(start, len(text)):
        if text[index] == '(':
            depth += 1
        elif text[index] == ')':
            depth -= 1
            if depth == 0:
                return text[start + 1:index], index + 1
    raise ValueError('Unclosed module header')


def module_ports(text, module=None):
    text = strip_comments(text)
    has_preprocessor = bool(re.search(r'`(?:ifdef|ifndef|elsif|else|endif|include|define)\b', text))
    match = re.search(r'\bmodule\s+' + (re.escape(module) + r'\b' if module else r'[A-Za-z_]\w*\b'), text)
    if not match:
        raise ValueError(f'Module not found: {module}')
    pos = match.end()
    while pos < len(text) and text[pos].isspace():
        pos += 1
    if text[pos:pos + 1] == '#':
        pos = text.index('(', pos)
        _, pos = balanced(text, pos)
        while pos < len(text) and text[pos].isspace():
            pos += 1
    if text[pos:pos + 1] != '(':
        raise ValueError('Unsupported portless or malformed module header')
    header, end = balanced(text, pos)
    body = text[end:text.find('endmodule', end)]
    ports, issues = {}, []
    if has_preprocessor:
        issues.append('Preprocessor context requires elaboration')
    if module and len(re.findall(r'\bmodule\s+' + re.escape(module) + r'\b', text)) > 1:
        issues.append('Multiple definitions of selected module')
    ansi = bool(re.search(r'\b(input|output|inout)\b', header))
    declarations = header.split(',') if ansi else re.findall(r'\b(?:input|output|inout)\b[^;]+', body)
    direction = None
    width_expr = None
    for declaration in declarations:
        pieces = [declaration] if ansi else declaration.split(',')
        for piece in pieces:
            dm = re.match(r'\s*(input|output|inout)\b', piece)
            if dm:
                direction = dm[1]
                piece = piece[dm.end():]
                width_expr = None
            wm = re.search(r'\[[^\]]+\]', piece)
            if wm:
                width_expr = wm[0]
                piece = piece[:wm.start()] + piece[wm.end():]
            piece = re.sub(r'\b(?:wire|reg|logic|bit|tri|signed|unsigned|var)\b', '', piece).strip()
            piece = piece.split('=')[0].strip()
            if not direction or not re.fullmatch(r'[A-Za-z_]\w*', piece):
                if piece:
                    issues.append('Unsupported declaration: ' + piece)
                continue
            if not ansi and piece not in {n.strip() for n in header.split(',')}:
                continue
            bounds = re.fullmatch(r'\[\s*(-?\d+)\s*:\s*(-?\d+)\s*\]', width_expr or '')
            indices = None if width_expr and not bounds else list(range(min(int(bounds[1]), int(bounds[2])), max(int(bounds[1]), int(bounds[2])) + 1)) if bounds else [None]
            if width_expr and not bounds:
                issues.append(f'Unknown width: {piece} {width_expr}')
            ports[piece] = dict(direction=direction, width=len(indices) if indices is not None else None,
                                width_expr=width_expr, indices=indices)
    if not ansi:
        for name in header.split(','):
            if name.strip() and name.strip() not in ports:
                issues.append('Unresolved non-ANSI port: ' + name.strip())
    if re.search(r'`(?:ifdef|ifndef|elsif|else|endif|include|define)\b', header + body):
        issues.append('Preprocessor context requires elaboration')
    return ports, issues


def port_bits(ports):
    return [name if bit is None else f'{name}[{bit}]' for name, item in ports.items()
            for bit in item['indices'] or []]
