"""Read XLSX packages without re-saving; check views and authorized differences."""
import argparse
import copy
import difflib
import hashlib
import posixpath
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile, BadZipFile
from audit_common import Audit, address, route_key, channel_key, read_json, sha256, write_report, exit_code

M = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
P = "http://schemas.openxmlformats.org/package/2006/relationships"
ns = {"m": M, "r": R}


def canon(e):
    if e is None:
        return None
    return (e.tag, tuple(sorted(e.attrib.items())), e.text or "", tuple(canon(c) for c in e))


def text(e):
    return "" if e is None else "".join(x.text or "" for x in e.iter(f"{{{M}}}t"))


def target(base, name):
    return name.lstrip("/") if name.startswith("/") else posixpath.normpath(posixpath.join(posixpath.dirname(base), name))


def rels(z, part):
    name = posixpath.join(posixpath.dirname(part), "_rels", posixpath.basename(part) + ".rels")
    if name not in z.namelist():
        return {}
    return {e.get("Id"): target(part, e.get("Target")) for e in ET.fromstring(z.read(name))
            if e.get("TargetMode") != "External"}


def col_number(s):
    v = 0
    for c in s:
        v = v * 26 + ord(c) - 64
    return v


def col_name(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def bounds(ref):
    parts = ref.split(":")
    parsed = []
    for p in (parts[0], parts[-1]):
        m = re.fullmatch(r"\$?([A-Z]+)\$?(\d+)", p)
        if not m:
            raise ValueError(f"Unsupported cell range: {ref}")
        parsed.append((col_number(m[1]), int(m[2])))
    return (*parsed[0], *parsed[1])


def snapshot(path):
    with ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            raise ValueError(f"Invalid ZIP member: {bad}")
        parts = {n: hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()}
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        wr = rels(z, "xl/workbook.xml")
        shared = []
        if "xl/sharedStrings.xml" in parts:
            shared = list(ET.fromstring(z.read("xl/sharedStrings.xml")))
        result = dict(parts=parts, sheets={}, sheet_parts=[], styles=None)
        if "xl/styles.xml" in parts:
            result["styles"] = ET.fromstring(z.read("xl/styles.xml"))
        for se in wb.findall("m:sheets/m:sheet", ns):
            name, part = se.get("name"), wr[se.get(f"{{{R}}}id")]
            result["sheet_parts"].append(part)
            root = ET.fromstring(z.read(part))
            sheet = dict(cells={}, rows={}, meta={}, tables=[])
            for row in root.findall("m:sheetData/m:row", ns):
                sheet["rows"][row.get("r")] = {k: v for k, v in row.attrib.items() if k not in ("r", "spans")}
                for c in row:
                    if c.tag != f"{{{M}}}c":
                        continue
                    t = c.get("t")
                    v = c.find("m:v", ns)
                    inline = c.find("m:is", ns)
                    st = shared[int(v.text)] if t == "s" else inline if t == "inlineStr" else None
                    runs = []
                    if st is not None:
                        value = text(st)
                        for run in st.findall("m:r", ns):
                            runs.append(dict(text=text(run), font=canon(run.find("m:rPr", ns))))
                    else:
                        value = v.text if v is not None else None
                    attrs = {k: val for k, val in c.attrib.items() if k not in ("r", "s", "t")}
                    attrs["type"] = "text" if t in ("s", "inlineStr", "str") else t
                    sheet["cells"][c.get("r")] = dict(value=value, formula=canon(c.find("m:f", ns)),
                                                       style=c.get("s", "0"), runs=runs, attributes=attrs)
            for child in root:
                k = child.tag.split("}")[-1]
                if k != "sheetData":
                    sheet["meta"].setdefault(k, []).append(canon(child))
            sr = rels(z, part)
            for tp in root.findall("m:tableParts/m:tablePart", ns):
                path_t = sr[tp.get(f"{{{R}}}id")]
                table = ET.fromstring(z.read(path_t))
                sheet["tables"].append(dict(part=path_t, xml=table))
            result["sheets"][name] = sheet
        return result


def get_value(sheet, addr):
    return sheet["cells"].get(addr, {}).get("value")


def character_fonts(cell):
    if cell.get("runs"):
        return [r["font"] for r in cell["runs"] for _ in r["text"]]
    return [None] * len(str(cell.get("value") or ""))


def audit(before, after, manifest, changes):
    a = Audit("workbook_preservation_and_views")
    version = manifest.get("schema_version")
    if version not in (1, 2) or changes.get("schema_version") != 1:
        raise ValueError("manifest schema_version must be 1/2; changes remains 1")
    b, c = snapshot(before), snapshot(after)
    a.stats.update(sheets=len(c["sheets"]), images=sum(n.startswith("xl/media/") for n in c["parts"]),
                   visual_check="not_run", formula_recalculation="not_run")
    if list(b["sheets"]) != list(c["sheets"]):
        a.add("SHEET_SET_OR_ORDER", "Sheet names/order changed outside this checker scope")
    fields = ("value", "formula", "style", "runs", "attributes")
    for name in set(b["sheets"]) & set(c["sheets"]):
        old, new = b["sheets"][name], c["sheets"][name]
        moves = changes.get("moves", {}).get(name, {})
        remapped = {}
        for k, v in old["cells"].items():
            key = moves.get(k, k)
            if key in remapped:
                a.add("MOVE_COLLISION", key, location=name)
            remapped[key] = v
        for addr in set(remapped) | set(new["cells"]):
            allowed = set(changes.get("cells", {}).get(name, {}).get(addr, []))
            x, y = remapped.get(addr, {}), new["cells"].get(addr, {})
            for field in fields:
                if x.get(field) != y.get(field) and field not in allowed:
                    a.add("UNAUTHORIZED_CELL_CHANGE", field, location=f"{name}!{addr}")
            # A text change may alter run boundaries, but is not permission to restyle retained text.
            if x and y and "runs" in allowed and "typography" not in allowed:
                xf, yf = character_fonts(x), character_fonts(y)
                xs, ys = str(x.get("value") or ""), str(y.get("value") or "")
                for tag, i, j, k, l in difflib.SequenceMatcher(None, xs, ys, autojunk=False).get_opcodes():
                    if tag == "equal" and xf[i:j] != yf[k:l]:
                        a.add("UNAUTHORIZED_RICH_STYLE", "Font/bold changed on retained text", location=f"{name}!{addr}")
                        break
        for key in set(old["meta"]) | set(new["meta"]):
            if old["meta"].get(key) != new["meta"].get(key) and key not in changes.get("meta", {}).get(name, []):
                a.add("UNAUTHORIZED_SHEET_META", key, location=name)
        for row in set(old["rows"]) | set(new["rows"]):
            if old["rows"].get(row) != new["rows"].get(row) and row not in changes.get("rows", {}).get(name, []):
                a.add("UNAUTHORIZED_ROW", row, location=name)
    semantic = set(b["sheet_parts"] + c["sheet_parts"] + ["xl/sharedStrings.xml"])
    for part in set(b["parts"]) | set(c["parts"]):
        if part in semantic:
            continue
        if b["parts"].get(part) != c["parts"].get(part) and part not in changes.get("parts", []):
            a.add("UNAUTHORIZED_PACKAGE_PART", part)
    for name, sheet in c["sheets"].items():
        for cell_addr, cell in sheet["cells"].items():
            if cell.get("attributes", {}).get("type") == "e":
                a.add("FORMULA_ERROR", str(cell.get("value")), location=f"{name}!{cell_addr}")
        for table_data in sheet["tables"]:
            t = table_data["xml"]
            ref = t.get("ref")
            x1, y1, x2, y2 = bounds(ref)
            columns = t.findall("m:tableColumns/m:tableColumn", ns)
            columns_element = t.find("m:tableColumns", ns)
            if len(columns) != x2 - x1 + 1 or int(columns_element.get("count", "0")) != len(columns):
                a.add("TABLE_WIDTH", ref, location=name)
            if t.get("headerRowCount", "1") != "0":
                for i, column in enumerate(columns):
                    addr = f"{col_name(x1+i)}{y1}"
                    value = get_value(sheet, addr)
                    if not value:
                        a.add("HEADER_EMPTY", addr, location=name)
                    if value != column.get("name"):
                        a.add("HEADER_TABLE_MISMATCH", f"{addr}: {value!r} != {column.get('name')!r}", location=name)
            for merge_block in sheet["meta"].get("mergeCells", []):
                for merged in merge_block[3]:
                    mx1, my1, mx2, my2 = bounds(dict(merged[1])["ref"])
                    if max(mx1, x1) <= min(mx2, x2) and max(my1, y1) <= min(my2, y2):
                        a.add("MERGED_TABLE_CELL", dict(merged[1])["ref"], location=name)
            af = t.find("m:autoFilter", ns)
            if af is not None:
                ax1, ay1, ax2, ay2 = bounds(af.get("ref"))
                if (ax1, ay1, ax2) != (x1, y1, x2) or ay2 != y2 - int(t.get("totalsRowCount", "0")):
                    a.add("TABLE_FILTER_RANGE", str(af.get("ref")), location=name)
    records = {}
    channels = set()
    for r in manifest.get("routes", []):
        key = route_key(r, version)
        if key in records:
            a.add("MANIFEST_DUPLICATE_ADDRESS", str(key))
        if version == 2:
            channel = channel_key(r)
            if channel is None:
                a.add("ADDRESS_UNCONFIRMED", str(key), "review")
            elif channel in channels:
                a.add("DUPLICATE_CHANNEL_ADDRESS", str(channel))
            else:
                channels.add(channel)
        records[key] = r
    layout = manifest.get("workbook", {})
    layouts = layout.get("sheets", [])
    if not layouts or not records:
        a.add("VIEW_COVERAGE_MISSING", "No workbook view bindings or route records", "review")
    for spec in layouts:
        name = spec["name"]
        if name not in c["sheets"]:
            a.add("VIEW_SHEET_MISSING", name)
            continue
        sheet = c["sheets"][name]
        for col, value in spec.get("headers", {}).items():
            at = f"{col}{spec['header_row']}"
            if get_value(sheet, at) != value:
                a.add("EXPECTED_HEADER", f"Expected {value!r}", location=f"{name}!{at}")
        seen = set()
        expected_ids = set(records)
        if version == 2:
            ids = spec.get("route_ids", [])
            expected_ids = set(ids)
            if not ids or len(ids) != len(expected_ids) or not expected_ids <= set(records):
                a.add("VIEW_BINDING_INVALID", "route_ids must be a nonempty unique subset of manifest routes", location=name)
            expected_rows = {str(row) for row in range(spec["first_data_row"], spec["last_data_row"] + 1)}
            if set(spec.get("row_bindings", {})) != expected_rows:
                a.add("VIEW_BINDING_INVALID", "row_bindings must cover exactly the declared data rows", location=name)
        for row in range(spec["first_data_row"], spec["last_data_row"] + 1):
            at = f"{spec['address_column']}{row}"
            val = get_value(sheet, at)
            try:
                key = spec.get("row_bindings", {}).get(str(row)) if version == 2 else address(val)
                if key is None:
                    raise ValueError("Missing row binding")
            except (ValueError, TypeError):
                a.add("VIEW_ADDRESS", str(val), location=f"{name}!{at}")
                continue
            if key in seen:
                a.add("VIEW_DUPLICATE", str(val), location=name)
            seen.add(key)
            route = records.get(key)
            if route is None:
                a.add("VIEW_UNKNOWN_ADDRESS", str(val), location=name)
                continue
            if version == 2:
                display = route.get("display", {})
                expected_address = display.get("address_text")
                if "address_text" not in display or val != expected_address:
                    a.add("VIEW_ADDRESS", "Display address differs from explicit record binding", location=f"{name}!{at}")
                if not spec.get("fields"):
                    a.add("VIEW_IDENTITY_UNCHECKED", "Bind signal/board display fields as well as address", "review", name)
            for col, field in spec.get("fields", {}).items():
                cell = f"{col}{row}"
                display = route.get("display", {})
                expected = display.get(field)
                if field not in display or (version == 1 and expected is None):
                    a.add("DISPLAY_EXPECTATION_MISSING", field, "review", f"{name}!{cell}")
                elif get_value(sheet, cell) != (None if expected is None else str(expected)):
                    a.add("VIEW_VALUE_MISMATCH", f"{val} field {field}", location=f"{name}!{cell}")
            for col in spec.get("route_columns", []):
                v = get_value(sheet, f"{col}{row}") or ""
                if re.search(r"\|\||[∥‖→⇢⇒➜➝]|(?<![A-Za-z0-9])N\d{5,}", v):
                    a.add("DISPLAY_NOTATION", "Internal net number or unsupported route symbol", location=f"{name}!{col}{row}")
        if seen != expected_ids:
            a.add("VIEW_COVERAGE", f"Missing {sorted(expected_ids-seen)}, extra {sorted(seen-expected_ids)}", location=name)
    for req in layout.get("required_bold", []):
        cell = c["sheets"].get(req["sheet"], {}).get("cells", {}).get(req["cell"], {})
        bold = "".join(run["text"] for run in cell.get("runs", []) if has_bold(run["font"]))
        if req["text"] not in bold:
            a.add("BOLD_NOT_VERIFIED", req["text"], "review", f"{req['sheet']}!{req['cell']}")
    for req in layout.get("numeric_checks", []):
        sheet = c["sheets"].get(req["sheet"], {})
        value = get_value(sheet, req["cell"]) if sheet else None
        try:
            if abs(float(value) - req["expected"]) > req.get("tolerance", 1e-12):
                a.add("NUMERIC_CHECK", str(value), location=f"{req['sheet']}!{req['cell']}")
        except (ValueError, TypeError):
            a.add("NUMERIC_CACHE_MISSING", "No numeric saved value; recalculate in intended engine", "review", req["cell"])
    a.stats["native_tables"] = sum(len(s["tables"]) for s in c["sheets"].values())
    return a.result()


def has_bold(node):
    if not node:
        return False
    tag, attrs, _, children = node
    if tag == f"{{{M}}}b":
        return dict(attrs).get("val", "1") not in ("0", "false")
    return any(has_bold(c) for c in children)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for key in ("before", "after", "manifest", "changes", "report"):
        p.add_argument("--" + key, required=True)
    args = p.parse_args()
    protected = [args.before, args.after, args.manifest, args.changes]
    try:
        result = audit(args.before, args.after, read_json(args.manifest), read_json(args.changes))
        result["inputs"] = {str(Path(x).resolve()): sha256(x) for x in protected}
    except (ValueError, TypeError, KeyError, OSError, BadZipFile, ET.ParseError, AttributeError, IndexError) as e:
        result = dict(status="input_error", error=str(e))
    try:
        write_report(args.report, result, protected)
    except (ValueError, OSError) as e:
        print(f"Report not written: {e}")
        return 3
    print(result["status"])
    return exit_code(result)


if __name__ == "__main__":
    raise SystemExit(main())
