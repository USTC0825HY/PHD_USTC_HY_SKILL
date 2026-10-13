"""Static logical IP and core-container evidence. Never opens or modifies Vivado."""
import hashlib
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile


def inspect_ips(inputs, issues):
    logical, containers, consumed = [], [], set()

    def issue(code, detail, severity='error'):
        issues.append(dict(severity=severity, code=code, detail=str(detail)))

    def identity(data, expected):
        root = ET.fromstring(data)
        names = [e.text for e in root.iter() if any(
            v.endswith('Component_Name') for v in e.attrib.values())]
        if len(names) != 1:
            issue('unresolved_ip_identity', expected, 'needs_review')
        elif names[0] != expected:
            issue('ip_identity_mismatch', f'{expected}: {names}')
        return names[0] if len(names) == 1 else None

    rows = [r for r in inputs if r['active'] and r['role'] == 'ip']
    for row in rows:
        p = Path(row['path']) if row['path'] else None
        if not p or p.suffix.lower() != '.xcix':
            continue
        record = dict(path=str(p), members=[], valid=False)
        containers.append(record)
        try:
            with zipfile.ZipFile(p) as z:
                names = z.namelist()
                if len(names) != len(set(names)) or any(n.startswith('/') or '..' in Path(n).parts for n in names):
                    raise ValueError('ambiguous/unsafe container members')
                bad = z.testzip()
                if bad:
                    raise ValueError('CRC failure: ' + bad)
                members = [n for n in names if n.lower().endswith('.xci')]
                expected = f'{p.stem}/{p.stem}.xci'
                if expected not in members:
                    raise ValueError('missing root member: ' + expected)
                name = identity(z.read(expected), p.stem)
                record['members'] = [dict(name=n, size=z.getinfo(n).file_size,
                    sha256=hashlib.sha256(z.read(n)).hexdigest()) for n in names if not n.endswith('/')]
                record['valid'] = True
                for other in inputs:
                    if not other['path'] or other is row:
                        continue
                    try:
                        member = Path(other['path']).relative_to(p.parent).as_posix()
                    except ValueError:
                        continue
                    if member in names and other['fileset'] == row['fileset']:
                        other.update(container=str(p), container_member=member,
                                     exists=True, sha256=hashlib.sha256(z.read(member)).hexdigest())
                        if other['active'] and member == expected:
                            consumed.add(id(other))
                logical.append(dict(name=name, path=str(p), fileset=row['fileset'], kind='xcix', member=expected))
        except (OSError, ValueError, zipfile.BadZipFile, RuntimeError, ET.ParseError) as exc:
            issue('invalid_ip_container', f'{p}: {exc}')
    for row in rows:
        p = Path(row['path']) if row['path'] else None
        if id(row) in consumed or not p or p.suffix.lower() == '.xcix':
            continue
        if p.suffix.lower() == '.bd':
            issue('bd_ip_association_requires_tool', p, 'needs_review')
            continue
        name = None
        if p.is_file():
            try:
                name = identity(p.read_bytes(), p.stem)
            except (OSError, ET.ParseError) as exc:
                issue('invalid_xci', f'{p}: {exc}')
        logical.append(dict(name=name, path=str(p), fileset=row['fileset'], kind='xci'))
    seen = set()
    for ip in logical:
        key = (ip['name'] or Path(ip['path']).stem).casefold()
        if key in seen:
            issue('duplicate_logical_ip', key)
        seen.add(key)
    return logical, containers
