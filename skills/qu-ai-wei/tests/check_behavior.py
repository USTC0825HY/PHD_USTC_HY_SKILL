#!/usr/bin/env python3
"""Validate captured-run completeness, not language quality. Review output separately."""
import json,sys
from pathlib import Path
if len(sys.argv)!=2:raise SystemExit('Usage: check_behavior.py <captured-run.json>')
data=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8-sig'))
assert data.get('agent') and data.get('model'),'Record executor; use unknown if model is not exposed'
assert len(data.get('cases',[]))>=6,'Missing required scenarios'
for case in data['cases']:
    assert case.get('request') and case.get('output') and case.get('loaded_files'),'Missing actual input/output/context'
print('Captured-run fields complete. Semantic verdict must come from output review.')
