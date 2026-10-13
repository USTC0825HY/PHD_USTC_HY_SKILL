"""Strict, fail-closed checks; acceptance is limited to the declared schema/layers."""
from __future__ import annotations
import csv
import hashlib
import json
import math
import re
from pathlib import Path

STATES = {'满足', '不满足', '暂不能判定', '未测试'}
UNKNOWN = {'', 'unknown', 'none', 'null', 'nan', 'n/a', '待确认', '未知'}

def strict_audit(root: Path, kind: str) -> dict:
    errors, warnings, unverified = [], [], []
    result = dict(result_dir=str(root), kind=kind, errors=errors, warnings=warnings,
                  unverified=unverified, mode='strict', checks=['CSV structure', 'metadata', 'source hashes', 'image decode', 'result readability'])
    def require(ok, message):
        if not ok: errors.append(message)
    def number(value, label, positive=False):
        try:
            x = float(value)
            if not math.isfinite(x) or (positive and x <= 0): raise ValueError()
            return x
        except (ValueError, TypeError):
            errors.append('invalid numeric field: ' + label)
            return None
    tables = {}
    for p in sorted(root.rglob('*.csv')):
        try:
            with p.open(encoding='utf-8-sig', newline='') as stream:
                reader = csv.DictReader(stream)
                require(bool(reader.fieldnames) and len(reader.fieldnames) == len(set(reader.fieldnames)), f'{p.name}: missing/duplicate headers')
                rows = list(reader)
                require(bool(rows), f'{p.name}: empty CSV')
                require(all(None not in row and all(v is not None for v in row.values()) for row in rows), f'{p.name}: ragged CSV')
                tables[p] = (reader.fieldnames or [], rows)
        except (OSError, UnicodeError, csv.Error) as exc: errors.append(f'{p.name}: {exc}')
    metadata = {}
    for p, (headers, rows) in tables.items():
        if headers == ['Parameter', 'Value']:
            for row in rows:
                key = row['Parameter']
                if key in metadata and metadata[key] != row['Value']: errors.append('conflicting parameter: ' + key)
                metadata[key] = row['Value']
    sidecar = root / 'audit_metadata.json'
    try:
        extra = json.loads(sidecar.read_text(encoding='utf-8-sig')) if sidecar.exists() else {}
        if not isinstance(extra, dict): raise ValueError('metadata must be an object')
        for key, value in extra.items():
            if key in metadata and str(metadata[key]) != str(value): errors.append('conflicting sidecar parameter: ' + key)
            metadata[key] = value
    except (ValueError, OSError) as exc: errors.append('metadata: ' + str(exc))
    spectrum = [(p,h,r) for p,(h,r) in tables.items() if 'frequency_hz' in h and any(x in h for x in ('psd_V2_per_Hz','asd_V_per_sqrtHz'))]
    calibration = [(p,h,r) for p,(h,r) in tables.items() if {'code_vpp','output_vpp_v'} <= set(h) or {'CodePp','InputVoltageVpp'} <= set(h)]
    if kind == 'auto':
        kind = 'spectral' if spectrum else ('calibration' if calibration else 'generic')
        result['kind'] = kind
    states = []
    for p,(headers,rows) in tables.items():
        state_columns = [x for x in headers if x in ('formal_conclusion','Conclusion','conclusion')]
        # status often describes fit execution, not the formal conclusion.
        for row in rows:
            for key in state_columns:
                states.append(row[key]); require(row[key] in STATES, f'{p.name}: invalid exact conclusion {row[key]!r}')
            for key in headers:
                if key.lower() in ('source_sha256','input_sha256','sha256'):
                    require(bool(re.fullmatch('[0-9a-fA-F]{64}', row[key] or '')), f'{p.name}: invalid {key}')
    state = metadata.get('formal_conclusion')
    if state is not None:
        states.append(state); require(isinstance(state,str) and state in STATES, 'invalid formal_conclusion')
    require(bool(states), 'missing exact formal conclusion field')
    if any(x in ('暂不能判定','未测试') for x in states): unverified.append('formal conclusion is indeterminate/not tested')
    sources = metadata.get('source_files', [])
    # Existing MATLAB calibration measurement rows provide actual paths/hashes.
    if not sources:
        sources = [dict(path=r['input_path'], sha256=r['source_sha256']) for h,rows in tables.values() for r in rows if 'input_path' in h and 'source_sha256' in h]
    require(isinstance(sources,list) and bool(sources), 'source_files required (path + sha256)')
    if isinstance(sources,list):
        for src in sources:
            if not isinstance(src,dict) or not isinstance(src.get('path'),str) or not re.fullmatch('[a-fA-F0-9]{64}',str(src.get('sha256',''))):
                errors.append('invalid source path/hash record'); continue
            p = Path(src['path']); p = p if p.is_absolute() else root/p
            try: require(hashlib.sha256(p.read_bytes()).hexdigest() == src['sha256'].lower(), 'source hash mismatch: '+str(p))
            except OSError: unverified.append('source inaccessible: '+str(p))
    if kind == 'spectral':
        require(bool(spectrum), 'unsupported spectrum CSV: require frequency_hz and psd_V2_per_Hz / asd_V_per_sqrtHz')
        aliases = [metadata[k] for k in ('sample_rate_hz','sample_rate','FsHz','fs_hz') if k in metadata]
        fs = number(aliases[0] if aliases else None,'sample_rate_hz',True)
        require(all(str(v) == str(aliases[0]) for v in aliases), 'conflicting sample rate aliases')
        lo = number(metadata.get('band_start_hz'),'band_start_hz')
        hi = number(metadata.get('band_end_hz'),'band_end_hz',True)
        require(lo is not None and hi is not None and 0 <= lo < hi, 'invalid analysis band')
        for p,h,rows in spectrum:
            axis = [number(r['frequency_hz'],p.name+':frequency_hz') for r in rows]
            if axis and all(x is not None for x in axis):
                require(axis[0] >= 0 and all(a < b for a,b in zip(axis,axis[1:])), p.name+': frequency axis must increase')
                if fs: require(axis[-1] <= fs/2*(1+1e-9), p.name+': exceeds Nyquist (one-sided schema)')
                if lo is not None and hi is not None: require(axis[0] <= lo < hi <= axis[-1],p.name+': spectrum does not cover band')
            for r in rows:
                vals = {}
                for key in ('psd_V2_per_Hz','asd_V_per_sqrtHz','asd_uV_per_sqrtHz'):
                    if key in h:
                        vals[key] = number(r[key],p.name+':'+key)
                        if vals[key] is not None: require(vals[key] >= 0,p.name+': negative density')
                a,b = vals.get('asd_V_per_sqrtHz'),vals.get('psd_V2_per_Hz')
                if a is not None and b is not None: require(math.isclose(a*a,b,rel_tol=1e-5,abs_tol=1e-30),p.name+': PSD != ASD squared')
                c = vals.get('asd_uV_per_sqrtHz')
                if a is not None and c is not None: require(math.isclose(a*1e6,c,rel_tol=1e-5,abs_tol=1e-24),p.name+': ASD unit conversion mismatch')
    if kind in ('spectral','calibration'):
        cal = metadata.get('calibration',{})
        if not isinstance(cal,dict): cal = {}
        for key in ('direction','input_unit','output_unit','reference_plane','source'):
            require(isinstance(cal.get(key),str) and cal[key].strip().lower() not in UNKNOWN,'calibration.'+key+' required')
        require(cal.get('direction') in ('input_to_output','output_to_input','identity'),'unsupported calibration direction')
        if isinstance(sources,list) and isinstance(cal.get('source'),str):
            def absolute(value):
                p=Path(value); return (p if p.is_absolute() else root/p).resolve()
            require(any(isinstance(src,dict) and isinstance(src.get('path'),str) and absolute(src['path'])==absolute(cal['source']) for src in sources),
                    'calibration.source must identify a hashed source_files record')
        bounds = cal.get('valid_range')
        if not isinstance(bounds,list) or len(bounds)!=2: errors.append('calibration.valid_range must have two numeric bounds')
        else:
            a,b = number(bounds[0],'range min'),number(bounds[1],'range max')
            require(a is not None and b is not None and a < b,'invalid calibration range')
    if kind == 'calibration':
        require(bool(calibration),'unsupported calibration measurement CSV')
        for p,h,rows in calibration:
            keys = ('code_vpp','output_vpp_v') if 'code_vpp' in h else ('CodePp','InputVoltageVpp')
            cal=metadata.get('calibration',{})
            if isinstance(cal,dict):
                require(cal.get('input_unit') in ('code_vpp','CodePp','codepp') and cal.get('output_unit') in ('Vpp','Vpp_v'), 'calibration measurement schema requires code peak-to-peak -> Vpp units')
                require(cal.get('direction')=='input_to_output', 'calibration measurement schema requires input_to_output direction')
            for row in rows:
                for key in keys: number(row[key],p.name+':'+key)
                if isinstance(cal,dict) and isinstance(cal.get('valid_range'),list) and len(cal['valid_range'])==2:
                    try:
                        if str(row.get('included_in_fit','true')).lower() not in ('false','0'):
                            require(float(cal['valid_range'][0]) <= float(row[keys[0]]) <= float(cal['valid_range'][1]),p.name+': fitted input outside calibrated range')
                    except (ValueError,TypeError): pass  # Other numeric checks report invalid fields.
    if kind in ('allan','generic'):
        # No verified schema exists for arbitrary scientific tables. Do not infer meaning.
        unverified.append(kind+' numerical schema unsupported; domain review required')
    images = [p for p in root.rglob('*') if p.suffix.lower() in ('.png','.jpg','.jpeg','.tif','.tiff')]
    require(bool(images),'missing result figure')
    try:
        from PIL import Image
        for p in images:
            try:
                with Image.open(p) as im: im.verify()
                with Image.open(p) as im: im.load()
            except Exception as exc: errors.append(f'image unreadable {p.name}: {exc}')
    except ImportError: unverified.append('Pillow unavailable')
    mats = list(root.rglob('*.mat'))
    require(bool(mats),'missing reproducible MAT result')
    try:
        import scipy.io
        for p in mats:
            try:
                data = scipy.io.loadmat(p)
                require(any(not k.startswith('__') for k in data),p.name+': empty MAT')
            except NotImplementedError: unverified.append(p.name+': v7.3 requires separate HDF5/MATLAB validation')
            except Exception as exc: errors.append(f'MAT unreadable {p.name}: {exc}')
    except ImportError: unverified.append('scipy unavailable; MAT not verified')
    result['status'] = 'ERROR' if errors else ('UNVERIFIED' if unverified else 'PASS')
    result['acceptance'] = 'declared_checks_passed' if result['status']=='PASS' else 'not_accepted'
    result['limitations'] = 'No algorithm, instrument, calibration physics or measurement conclusion certification.'
    return result
