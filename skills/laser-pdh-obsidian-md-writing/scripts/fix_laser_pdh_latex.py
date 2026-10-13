#!/usr/bin/env python3
"""Repair recognized Markdown math; preview by default, scoped writes only."""
from __future__ import annotations
import argparse
import hashlib
import os
import re
import tempfile
from pathlib import Path
from _portable_profile import profile_path

DEFAULT_ROOT = profile_path('obsidian_vault_root', Path.home()/'Obsidian')/'01_科研主系统'
DEFAULT_PROJECT = 'Laser_PDH_Study'
EXCLUDED = {'01_Raw','03_原始摘录','90_历史项目','_archive','.git','.obsidian'}
TOKENS = re.compile(
    r'(?P<protected>(?P<ticks>`+)(?!`).*?(?<!`)(?P=ticks)(?!`)|!?\[[^\]\r\n]*\](?:\([^\r\n]*?\)|\[[^\]\r\n]*\])|\[\[[^\]\r\n]*\]\]|<code\b[^>]*>.*?</code>|<pre\b[^>]*>.*?</pre>)'
    r'|(?P<display>(?<!\\)\$\$(?P<display_body>.*?)(?<!\\)\$\$)'
    r'|(?P<legacy_display>\\\[(?P<legacy_display_body>.*?)\\\])'
    r'|(?P<legacy_inline>\\\((?P<legacy_inline_body>[^\r\n]*?)\\\))'
    r'|(?P<inline>(?<![\\$])\$(?!\$)(?P<inline_body>[^\r\n]*?)(?<![\\$])\$(?!\$))', re.S)
ABS = re.compile(r'\|(?:l_g(?:\(f\))?|D\(f\)|H\(f\)|c_\{gD\}\(f_m\)|\\nu_\\mathrm\{(?:cl|free)\}\(f\)|\\nu_1-\\nu_2|\\Delta\\nu(?:\(t\))?)\|')

def _math(body):
    body=ABS.sub(lambda m:r'\lvert '+m.group()[1:-1]+r'\rvert',body)
    return body.replace(r'\left|',r'\left\lvert ').replace(r'\right|',r'\right\rvert ')

def _prose(text):
    def replace(m):
        if m.group('protected') is not None: return m.group()
        for kind,delimiter in [('display','$$'),('legacy_display','$$'),('legacy_inline','$'),('inline','$')]:
            if m.group(kind) is not None: return delimiter+_math(m.group(kind+'_body'))+delimiter
        return m.group()
    return TOKENS.sub(replace,text)

def fix_text(text: str) -> str:
    result=[];chunk=[];fence=None;front=False
    def flush():
        result.append(_prose(''.join(chunk)));chunk.clear()
    for index,line in enumerate(text.splitlines(keepends=True)):
        if index==0 and line.strip()=='---': front=True;flush();result.append(line);continue
        if front:
            result.append(line)
            if line.strip() in ('---','...'): front=False
            continue
        marker=re.match(r'^(?: {0,3}> ?)* {0,3}(?:(?:[-+*]|[0-9]+[.)]) )?(`{3,}|~{3,})(.*?)(?:\r?\n)?$',line)
        if fence:
            result.append(line)
            if marker and marker[1][0]==fence[0] and len(marker[1])>=fence[1] and not marker[2].strip(): fence=None
        elif marker:
            flush();fence=(marker[1][0],len(marker[1]));result.append(line)
        elif re.match(r'^(?: {4}|\t)',line):
            flush();result.append(line)
        else: chunk.append(line)
    flush()
    return ''.join(result)

def iter_md_files(root: Path, project: str | None = None) -> list[Path]:
    selected=[]
    for p in sorted(root.rglob('*.md')):
        if not p.is_file() or p.is_symlink() or set(p.relative_to(root).parts)&EXCLUDED or p.name.endswith('_旧版.md'): continue
        if not p.resolve().is_relative_to(root.resolve()): continue
        text=p.read_text(encoding='utf-8-sig')
        fm=re.match(r'\A---\r?\n(.*?)\r?\n(?:---|\.\.\.)(?:\r?\n|$)',text,re.S)
        if not project or (fm and re.search(rf'(?m)^project\s*:\s*["\x27]?{re.escape(project)}["\x27]?\s*$',fm[1])): selected.append(p)
    return selected

def write_checked(path, original, replacement):
    digest=hashlib.sha256(original).hexdigest()
    if path.read_bytes()!=original: raise RuntimeError('source changed before write: '+str(path))
    backup=path.with_name(path.name+'.before-latex-'+digest[:16]+'.bak')
    if backup.exists():
        if backup.read_bytes()!=original: raise RuntimeError('backup conflict: '+str(backup))
    else:
        with backup.open('xb') as stream: stream.write(original)
    fd,name=tempfile.mkstemp(prefix=path.name+'.',suffix='.tmp',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as stream: stream.write(replacement);stream.flush();os.fsync(stream.fileno())
        if path.read_bytes()!=original: raise RuntimeError('source changed during write: '+str(path))
        os.replace(name,path)
    finally:
        if os.path.exists(name): os.unlink(name)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=DEFAULT_ROOT)
    parser.add_argument('--project',default=DEFAULT_PROJECT)
    parser.add_argument('--file',type=Path,action='append',help='Explicit Markdown file; repeatable')
    parser.add_argument('--all-project',action='store_true',help='Explicitly select project-wide scope')
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    if args.file and args.all_project: parser.error('--file and --all-project are mutually exclusive')
    if args.write and not (args.file or args.all_project): parser.error('writing requires --file or --all-project')
    if not args.file and not args.root.is_dir(): parser.error('root is not a readable directory')
    files=list(dict.fromkeys(p.resolve() for p in args.file)) if args.file else iter_md_files(args.root,args.project or None)
    changes=[]
    for path in files:
        if path.suffix.lower()!='.md' or not path.is_file(): parser.error('not a Markdown file: '+str(path))
        original=path.read_bytes();bom=original.startswith(b'\xef\xbb\xbf')
        text=original.decode('utf-8-sig');new=fix_text(text)
        replacement=(b'\xef\xbb\xbf' if bom else b'')+new.encode('utf-8')
        if original!=replacement: changes.append((path,original,replacement))
    for path,original,replacement in changes:
        if args.write: write_checked(path,original,replacement)
    print(('WRITE' if args.write else 'DRY_RUN')+'_CHANGED = '+str(len(changes)))
    for path,_,_ in changes: print(path)
    return 0

if __name__=='__main__': raise SystemExit(main())
