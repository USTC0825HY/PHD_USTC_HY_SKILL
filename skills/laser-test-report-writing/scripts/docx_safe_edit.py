"""Small OOXML operations and checks; no automatic whole-document normalization."""
from __future__ import annotations
import copy
import hashlib
import json
import zipfile
from pathlib import Path
from lxml import etree
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}

def reference_checks(doc):
    """Check visible figure references even when no manifest is supplied."""
    import re
    from audit_figure_mapping import image_caption_pairs, FIGURE_REFERENCE_RE
    styles = {s.style_id for s in doc.styles if s.name in ('Caption','题注','图表题注')}
    # python-docx overrides xpath without the namespaces keyword; use plain lxml.
    root = etree.fromstring(etree.tostring(doc._element))
    _, captions, _ = image_caption_pairs(root, styles)
    numbers = {int(c['number']) for c in captions}
    result=[]
    for i,p in enumerate(root.xpath('.//w:p',namespaces=NS),1):
        text=''.join(p.xpath('.//w:t/text()',namespaces=NS))
        for m in FIGURE_REFERENCE_RE.finditer(text):
            first,last=int(m[1]),int(m[2] or m[1])
            if first<1 or last<first or last-first>len(numbers) or any(n not in numbers for n in range(first,last+1)):
                result.append(dict(location=f'paragraph {i}',issue='figure reference has no matching caption',text=m[0]))
    return result

def set_cell_text(tc, text, color="000000"):
    """Rewrite plain text only; preserve tcPr/pPr/rPr and set explicit readable color."""
    if hasattr(tc, "_tc"):
        tc = tc._tc
    allowed = {"p", "pPr", "r", "rPr", "t", "br", "tab"}
    for child in tc:
        if child.tag == qn("w:tcPr"):
            continue
        for node in child.iter():
            local = etree.QName(node).localname
            if any(a.tag in (qn("w:pPr"), qn("w:rPr")) for a in node.iterancestors()):
                continue
            if local not in allowed or etree.QName(node).namespace != W:
                raise ValueError("non-text cell requires a dedicated edit: " + local)
    paragraphs = tc.findall(qn("w:p"))
    ppr = copy.deepcopy(paragraphs[0].find(qn("w:pPr"))) if paragraphs and paragraphs[0].find(qn("w:pPr")) is not None else None
    rpr = next((copy.deepcopy(n) for n in tc.iter(qn("w:rPr"))), None)
    for child in list(tc):
        if child.tag != qn("w:tcPr"):
            tc.remove(child)
    paragraph = OxmlElement("w:p")
    if ppr is not None:
        paragraph.append(ppr)
    run = OxmlElement("w:r")
    rpr = rpr if rpr is not None else OxmlElement("w:rPr")
    font_color = rpr.find(qn("w:color"))
    if font_color is None:
        font_color = OxmlElement("w:color")
        rpr.append(font_color)
    font_color.attrib.clear()
    font_color.set(qn("w:val"), color)
    run.append(rpr)
    for index, line in enumerate(text.split("\n")):
        if index:
            run.append(OxmlElement("w:br"))
        node = OxmlElement("w:t")
        node.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        node.text = line
        run.append(node)
    paragraph.append(run)
    tc.append(paragraph)

def _text(node):
    return "".join(n.text or "" for n in node.iter(qn("w:t"))) if node is not None else ""

def _val(node, tag, attribute="w:val", default=""):
    found = node.find(qn(tag)) if node is not None else None
    return found.get(qn(attribute), default) if found is not None else default

def table_checks(doc, profiles=None):
    findings = []
    def add(code, table, row, message):
        findings.append(dict(code=code, table=table, row=row, cell=current_cell, message=message))
    current_cell = 0
    for ti, table in enumerate(doc.tables, 1):
        current_cell = 0
        grid = table._tbl.tblGrid.gridCol_lst
        grid_count = len(grid)
        grid_width = sum(int(c.get(qn("w:w"), "0")) for c in grid)
        table_width = table._tbl.tblPr.find(qn("w:tblW"))
        if table_width is not None:
            kind, value = table_width.get(qn("w:type")), table_width.get(qn("w:w"), "")
            if value.lstrip("-").isdigit():
                value = int(value)
                if kind == "pct" and not 0 < value <= 5000:
                    add("TABLE.WIDTH", ti, 0, "pct table width must be in (0,5000]")
                if kind == "dxa" and value > 0 and abs(value-grid_width) > 40:
                    add("TABLE.WIDTH_GRID", ti, 0, "dxa table width differs from tblGrid")
        previous = None
        for ri, tr in enumerate(table._tbl.tr_lst, 1):
            current_cell = 0
            tcs = tr.tc_lst
            spans = [int(_val(tc.tcPr, "w:gridSpan", default="1")) for tc in tcs]
            before = int(_val(tr.trPr, "w:gridBefore", default="0"))
            after = int(_val(tr.trPr, "w:gridAfter", default="0"))
            if sum(spans)+before+after != grid_count:
                add("TABLE.GRID", ti, ri, "cell spans do not cover tblGrid")
            texts = [_text(tc) for tc in tcs]
            status = next((x for x in texts if x in ("改焊前", "改焊后")), "")
            header = tr.trPr is not None and tr.trPr.find(qn("w:tblHeader")) is not None
            if ri == 2 and previous is not None:
                first_has_merge = any(_val(tc.tcPr, "w:vMerge") == "restart" for tc in previous.tc_lst)
                second_continues = any(tc.tcPr is not None and tc.tcPr.find(qn("w:vMerge")) is not None and _val(tc.tcPr, "w:vMerge") in ("", "continue") for tc in tcs)
                first_header = previous.trPr is not None and previous.trPr.find(qn("w:tblHeader")) is not None
                if first_header and first_has_merge and second_continues and not header:
                    add("TABLE.SECOND_HEADER", ti, ri, "second header row must also repeat")
            if status == "改焊前" and previous is not None and any(_text(tc) == "改焊后" for tc in previous.tc_lst):
                for tc in previous.tc_lst:
                    for para in tc.findall(qn("w:p")):
                        if para.find("w:pPr/w:keepNext", NS) is None:
                            add("REWORK.KEEP_PAIR", ti, ri-1, "post/pre comparison pair may break across pages")
                            break
            column = before
            for current_cell, (tc, span) in enumerate(zip(tcs, spans), 1):
                fill = _val(tc.tcPr, "w:shd", "w:fill", "FFFFFF").upper()
                width = tc.tcPr.find(qn("w:tcW")) if tc.tcPr is not None else None
                if width is not None:
                    kind, val = width.get(qn("w:type")), width.get(qn("w:w"), "")
                    if val.lstrip("-").isdigit():
                        if kind == "pct" and not 0 <= int(val) <= 5000:
                            add("TABLE.CELL_WIDTH", ti, ri, "invalid pct cell width")
                        if kind == "dxa" and int(val) > 0:
                            expected = sum(int(c.get(qn("w:w"), "0")) for c in grid[column:column+span])
                            if abs(int(val)-expected) > 40:
                                add("TABLE.CELL_GRID", ti, ri, "cell dxa width differs from its grid span")
                column += span
                for paragraph in tc.findall(qn("w:p")):
                    pstyle = _val(paragraph.find(qn("w:pPr")), "w:pStyle")
                    for run in paragraph.findall(qn("w:r")):
                        if not run.findall(qn("w:t")):
                            continue
                        color = _val(run.find(qn("w:rPr")), "w:color")
                        if not color and pstyle:
                            styles = doc.styles.element.xpath(f"./w:style[@w:styleId='{pstyle}']")
                            if styles:
                                color = _val(styles[0].find(qn("w:rPr")), "w:color")
                        if fill in ("FFFFFF","B8CCE4","E5B8B7","AUTO") and color.upper() == "FFFFFF":
                            add("TABLE.LIGHT_WHITE_TEXT", ti, ri, "white text on a light cell")
                        if header and fill == "1F4E79" and color.upper() != "FFFFFF":
                            add("TABLE.HEADER_COLOR", ti, ri, "dark-blue header needs explicit white text")
            previous = tr
        current_cell = 0
        profile = (profiles or {}).get(str(ti), {})
        headers = " ".join(_text(tr) for tr in table._tbl.tr_lst[:2])
        for required in profile.get("required_columns", []):
            if required not in headers:
                add("TABLE.PROFILE_COLUMN", ti, 0, "required column missing: " + required)
    return findings

def surgical_diff(before, after, scope):
    """Scope JSON: before_body/after_body 1-based node indices, allowed_parts exact names."""
    def package(path):
        with zipfile.ZipFile(path) as archive:
            return {n: archive.read(n) for n in archive.namelist()}
    left, right = package(before), package(after)
    findings = []
    allowed = set(scope.get("allowed_parts", []))
    if "word/document.xml" in allowed:
        raise ValueError("document.xml needs body-node scope, not a whole-part exemption")
    for part in set(left) | set(right):
        if part != "word/document.xml" and part not in allowed and left.get(part) != right.get(part):
            findings.append("unauthorized package part changed: " + part)
    untouched = []
    for data, key in ((left, "before_body"), (right, "after_body")):
        root = etree.fromstring(data["word/document.xml"])
        body = root.find(qn("w:body"))
        excluded = set(scope.get(key, []))
        # Each cell scope binds exact body table + physical OOXML row/tc, not visual columns.
        seen = set()
        for spec in scope.get("cells", []):
            indices = spec[key]
            if not isinstance(indices,list) or len(indices)!=3 or any(type(i) is not int or i < 1 for i in indices):
                raise ValueError("cell scope requires [body_node, row, physical_cell] (1-based)")
            bi,ri,ci = indices
            if bi in excluded: raise ValueError("cell-scoped table cannot also have a whole-body exemption")
            if tuple(indices) in seen: raise ValueError("duplicate cell scope")
            seen.add(tuple(indices))
            try:
                tbl=body[bi-1]
                if tbl.tag != qn("w:tbl"): raise ValueError("cell scope body is not a table")
                tc=tbl.findall(qn("w:tr"))[ri-1].findall(qn("w:tc"))[ci-1]
            except IndexError: raise ValueError("cell scope index out of range")
            # Keep a positional placeholder: surrounding row/table geometry remains compared.
            tc.clear()

        if any(not isinstance(i,int) or i < 1 or i > len(body) for i in excluded):
            raise ValueError("scope body index out of range")
        untouched.append([etree.tostring(node, method="c14n") for i,node in enumerate(body,1) if i not in excluded])
    if untouched[0] != untouched[1]:
        findings.append("unauthorized body content/format/order changed")
    return findings

def snapshot(path):
    path = Path(path)
    lock = path.with_name("~$"+path.name)
    if lock.exists():
        raise RuntimeError("Word owner lock exists: " + str(lock))
    # Windows sharing check: do not treat every WINWORD process as this file's owner.
    if __import__("os").name == "nt":
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.CreateFileW.argtypes = [wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,wintypes.LPVOID,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE]
        kernel.CreateFileW.restype = wintypes.HANDLE
        handle = kernel.CreateFileW(str(path.resolve()), 0x80000000, 0, None, 3, 0, None)
        if handle == wintypes.HANDLE(-1).value:
            raise OSError(ctypes.get_last_error(), "target unavailable or open")
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel.CloseHandle(handle)
    stat = path.stat()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    current = path.stat()
    if (stat.st_size,stat.st_mtime_ns) != (current.st_size,current.st_mtime_ns):
        raise RuntimeError("target changed during snapshot")
    return {"path":str(path.resolve()),"size":stat.st_size,"mtime_ns":stat.st_mtime_ns,"sha256":digest}

