#!/usr/bin/env python3
"""Deterministic local flat build. Python 3.9+, no external packages."""
import argparse,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REFERENCES=('editing-modes','patterns','platform-patterns','whitelists','punctuation','syntax','brand-voice','reference-models','examples','sources')
def version():
    text=(ROOT/'SKILL.md').read_text(encoding='utf-8')
    fm=text.split('---',2)[1]
    match=re.search(r'^  version:\s*["\']?([^"\'\s]+)',fm,re.M)
    if not match:raise ValueError('Missing metadata.version')
    return match.group(1)
def render():
    text=(ROOT/'SKILL.md').read_text(encoding='utf-8')
    body=text.split('---',2)[2].strip()
    refs={p.stem for p in (ROOT/'references').glob('*.md')}
    if refs!=set(REFERENCES):raise ValueError(f'Reference manifest mismatch: {refs.symmetric_difference(REFERENCES)}')
    chunks=[body,'# 附录：按任务选择参考']
    for name in REFERENCES:
        # Keep applicability preambles; discarding them could reactivate old blanket rules.
        chunks.append(f'<!-- references/{name}.md -->\n'+(ROOT/f'references/{name}.md').read_text(encoding='utf-8').strip())
    body='\n\n---\n\n'.join(chunks)+'\n'
    return {name:f'# qu-ai-wei · {platform}\n\n> 版本 {version()}。由 scripts/build-flat.sh 生成；本地维护版，来源与许可见 README.md / LICENSE。\n> 仅为不支持按需引用的平台提供完整单文件。以下入口的任务授权与内容保护同样适用于全部附录。\n\n'+body for name,platform in [('.cursorrules','Cursor / Windsurf rules'),('WARP.md','Warp rules')]}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    outputs=render()
    if args.check:
        bad=[n for n,t in outputs.items() if not (ROOT/n).exists() or (ROOT/n).read_bytes()!=t.encode('utf-8')]
        if bad:raise SystemExit('Flat build drift: '+', '.join(bad))
        print('Flat build byte comparison passed')
    else:
        for name,text in outputs.items():(ROOT/name).write_text(text,encoding='utf-8',newline='\n')
        print('Generated .cursorrules and WARP.md; references:',len(REFERENCES))
if __name__=='__main__':main()
