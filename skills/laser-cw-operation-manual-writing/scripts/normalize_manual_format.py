#!/usr/bin/env python3
"""Preserve DOCX content/CJK styling; normalize Latin fonts and centered tables.

Usage: normalize_manual_format.py INPUT OUTPUT
       normalize_manual_format.py INPUT --check
Never overwrites an input or existing output. Works directly on the DOCX package.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
NS={'w':W,'a':A}; FONT='Times New Roman'
def w(n): return '{'+W+'}'+n
def child(parent, name, first=False):
    x=parent.find(w(name))
    if x is None:
        x=E.Element(w(name))
        if first: parent.insert(0,x)
        else: parent.append(x)
    return x
def fonts(rpr):
    f=child(rpr,'rFonts',True)
    for k in ('ascii','hAnsi','cs'): f.set(w(k),FONT)
    for k in ('asciiTheme','hAnsiTheme','cstheme','csTheme'):
        f.attrib.pop(w(k),None)
    # Deliberately preserve eastAsia, eastAsiaTheme, hint, lang and all other rPr.
def center(ppr):
    child(ppr,'jc').set(w('val'),'center')
    ind=child(ppr,'ind');ind.attrib.clear()
    for k in ('left','right','firstLine'):ind.set(w(k),'0')
    for tabs in ppr.findall(w('tabs')):ppr.remove(tabs)
def vertical(tcpr): child(tcpr,'vAlign').set(w('val'),'center')
def table_style(s):
    center(child(s,'pPr'));vertical(child(s,'tcPr'))
    for cond in s.findall(w('tblStylePr')):
        center(child(cond,'pPr'));vertical(child(cond,'tcPr'))
def normalize(root):
    # Run/style/default/numbering properties, including headers, textboxes and footnotes.
    for r in root.xpath('//w:r',namespaces=NS): fonts(child(r,'rPr',True))
    for s in root.xpath('//w:style',namespaces=NS): fonts(child(s,'rPr'))
    for rpr in list(root.xpath('//w:rPr',namespaces=NS)): fonts(rpr)
    for f in root.xpath('//w:rFonts',namespaces=NS):fonts(f.getparent())
    if root.tag==w('styles'):
        defaults=child(root,'docDefaults',True)
        fonts(child(child(defaults,'rPrDefault'),'rPr'))
        for s in root.xpath('//w:style[@w:type="table"]',namespaces=NS):table_style(s)
        for s in root.xpath('//w:style[w:name[@w:val="表格正文"]]',namespaces=NS):center(child(s,'pPr'))
    # DrawingML text: Latin only; retain a:ea and all size/emphasis attributes.
    for rpr in root.xpath('//a:rPr | //a:defRPr | //a:endParaRPr',namespaces=NS):
        latin=rpr.find('{'+A+'}latin')
        if latin is None:latin=E.SubElement(rpr,'{'+A+'}latin')
        latin.set('typeface',FONT)
    for tbl in root.xpath('//w:tbl',namespaces=NS):
        child(child(tbl,'tblPr',True),'jc').set(w('val'),'center')
        rows=tbl.findall(w('tr'))
        if rows:child(child(rows[0],'trPr',True),'tblHeader').set(w('val'),'true')
    for tr in root.xpath('//w:tbl/w:tr',namespaces=NS):
        child(child(tr,'trPr',True),'cantSplit').set(w('val'),'true')
    for tc in root.xpath('//w:tc',namespaces=NS):
        vertical(child(tc,'tcPr',True))
        for p in tc.xpath('.//w:p',namespaces=NS):center(child(p,'pPr',True))
        # Replace layout tabs with spaces, not removal that joins words.
        for tab in tc.xpath('.//w:r/w:tab',namespaces=NS):
            t=E.Element(w('t'));t.text=' ';t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
            tab.getparent().replace(tab,t)
    return root

def content(root):
    # Formatting tabs can become spaces; all visible text, fields and breaks remain.
    keep=[]
    for n in root.iter():
        if n.tag in (w('t'),'{'+A+'}t',w('instrText'),w('delText')):keep.append(n.text or '')
        elif n.tag==w('tab') and n.getparent().tag==w('r'):keep.append(' ')
        elif n.tag in (w('br'),w('cr')):keep.append('\n')
    return ''.join(keep)
def cjk_snapshot(root):
    tree=root.getroottree();out={}
    for node in root.xpath('//w:rFonts',namespaces=NS):
        vals={k:v for k,v in node.attrib.items() if E.QName(k).localname not in ('ascii','hAnsi','cs','asciiTheme','hAnsiTheme','cstheme','csTheme')}
        if vals:out[tree.getpath(node)]=vals
    return out
def check_tree(root):
    errors=[]
    for rpr in root.xpath('//w:rPr',namespaces=NS):
        f=rpr.find(w('rFonts'))
        if f is None or any(f.get(w(k))!=FONT for k in ('ascii','hAnsi','cs')):errors.append('Latin font not explicit')
        elif any(f.get(w(k)) is not None for k in ('asciiTheme','hAnsiTheme','cstheme','csTheme')):errors.append('Latin theme fallback')
    for r in root.xpath('//w:r',namespaces=NS):
        if r.find(w('rPr')) is None:errors.append('Run missing font properties')
    for tc in root.xpath('//w:tc',namespaces=NS):
        if tc.find('w:tcPr/w:vAlign',NS) is None or tc.find('w:tcPr/w:vAlign',NS).get(w('val'))!='center':errors.append('Cell not vertically centered')
        for p in tc.xpath('.//w:p',namespaces=NS):
            pr=p.find(w('pPr'));jc=None if pr is None else pr.find(w('jc'))
            if jc is None or jc.get(w('val'))!='center':errors.append('Table paragraph not centered')
            ind=None if pr is None else pr.find(w('ind'))
            if ind is None or any(ind.get(w(k))!='0' for k in ('left','right','firstLine')):errors.append('Table indentation')
        if tc.xpath('.//w:r/w:tab',namespaces=NS):errors.append('Table layout tab')
    return errors
def read_xml(data):return E.fromstring(data,E.XMLParser(remove_blank_text=False,resolve_entities=False))
def eligible(name):return name.startswith('word/') and name.endswith('.xml')
def check(path):
    errors=[];cells=0
    with ZipFile(path) as z:
        if z.testzip():raise ValueError('Invalid package')
        for name in z.namelist():
            if eligible(name):
                root=read_xml(z.read(name));cells+=len(root.xpath('//w:tc',namespaces=NS))
                errors.extend(name+': '+e for e in check_tree(root))
    if errors:raise ValueError('\n'.join(errors[:30]))
    print(f'FORMAT_CHECK_PASS cells={cells} {path.name}')
def repair(source,output):
    if source.resolve()==output.resolve() or output.exists():raise ValueError('Choose a new output path')
    with ZipFile(source) as zin, ZipFile(output,'w') as zout:
        for info in zin.infolist():
            data=zin.read(info.filename)
            if eligible(info.filename):
                root=read_xml(data);oldcontent=content(root);oldcjk=cjk_snapshot(root)
                normalize(root)
                assert content(root)==oldcontent,'Content changed: '+info.filename
                for path,attrs in oldcjk.items():
                    found=root.getroottree().xpath(path,namespaces=root.nsmap)
                    assert found and all(found[0].get(k)==v for k,v in attrs.items()),'CJK font changed: '+path
                data=E.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True)
            zout.writestr(info,data)
    check(output)
def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('input',type=Path);a.add_argument('output',type=Path,nargs='?');a.add_argument('--check',action='store_true');args=a.parse_args()
    if args.check:
        if args.output:a.error('--check takes one input')
        check(args.input)
    elif args.output:repair(args.input,args.output)
    else:a.error('Provide a new output path or --check')
if __name__=='__main__':main()
