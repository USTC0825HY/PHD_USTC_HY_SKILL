#!/usr/bin/env python3
"""Structural checks only: no claims of semantic or automatic-trigger success."""
import hashlib,importlib.util,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('flat',ROOT/'scripts/build_flat.py');flat=importlib.util.module_from_spec(spec);spec.loader.exec_module(flat)
mode=sys.argv[1]
if mode=='version':
    v=flat.version()
    for name in ('README.md','CHANGELOG.md','.cursorrules','WARP.md'):
        assert v in '\n'.join((ROOT/name).read_text(encoding='utf-8').splitlines()[:8]),name
    print('Version strings agree:',v)
elif mode=='triggers':
    text=(ROOT/'SKILL.md').read_text(encoding='utf-8').split('---',2)[1]
    for word in ('去 AI 味','去ai味','改得说人话','改自然点','读着别扭','太生硬了','humanize'):
        assert word in text,word
    print('Description anchors present; automatic selection NOT tested')
elif mode=='history':
    manifest=json.loads((ROOT/'tests/historical-hashes.json').read_text(encoding='utf-8'))
    for name,sha in manifest.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
    print('Historical fixtures and snapshots byte-preserved:',len(manifest))
else:raise SystemExit('Unknown mode')
