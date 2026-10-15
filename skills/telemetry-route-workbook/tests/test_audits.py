"""Isolated positive/negative tests; generates synthetic files only."""
import argparse
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
from audit_common import sha256, write_report
from audit_routes import audit as route_audit, decode_adc
from audit_workbook import audit as workbook_audit

WORK = None


def graph(root):
    evidence_file = root / "synthetic-net-evidence.txt"
    evidence_file.write_text("Synthetic fixture only, not hardware evidence.\n", encoding="utf-8")
    nodes = {
        "a": dict(board="ACQ", ref="U1", pin="19", net="N1"),
        "r2": dict(board="ACQ", ref="R1", pin="2", net="N1"),
        "r1": dict(board="ACQ", ref="R1", pin="1", net="TM"),
        "j": dict(board="ACQ", ref="J1", pin="A1", net="TM"),
        "x": dict(board="SRC", ref="X1", pin="7", net="MON"),
        "u": dict(board="SRC", ref="U2", pin="6", net="MON"),
    }
    ev = dict(pst=dict(kind="netlist", locator="synthetic line 1", path=str(evidence_file), sha256=sha256(evidence_file)),
              pair=dict(kind="interface_confirmation", locator="fixture explicit pairing"),
              fit=dict(kind="assembly_confirmation", locator="fixture R1 fitted", scope=dict(board="ACQ", refs=["R1"])))
    m = dict(schema_version=1, boards={k:dict(label=k, version="fixture-v1", evidence_set="synthetic") for k in ("ACQ", "SRC")},
             evidence=ev, nodes=nodes, routes=[dict(address="0x00", kind="measurement", mode="CW", status="complete", input="U1.S1", mux={"U1":"S1"},
             segments=[dict(kind="net", **{"from":"a", "to":"r2"}, evidence=["pst"]),
                       dict(kind="component", **{"from":"r2", "to":"r1"}, evidence=["pst"], component=dict(ref="R1", value="5.1k", marker="TSD*", state="fitted", assembly_evidence=["fit"])),
                       dict(kind="net", **{"from":"r1", "to":"j"}, evidence=["pst"]),
                       dict(kind="connector", **{"from":"j", "to":"x"}, evidence=["pair"]),
                       dict(kind="net", **{"from":"x", "to":"u"}, evidence=["pst"])],
             source_board="SRC", source_interface="x", endpoint="u", conversion=dict(bits=16,coding="twos_complement",vref=5,vref_basis="adopted",output_kind="adc_voltage"))])
    p = dict(schema_version=1, mode="CW", physical_inputs={"U1.S1":{"node":"a"}}, cascade_inputs=[],
             expected_routes={"0x00":{"input":"U1.S1","mux":{"U1":"S1"}, "required_components":["R1"],"forbidden_components":["RGS"]}},
             connector_pairs=[dict(**{"from":"j","to":"x"},evidence=["pair"])])
    return m, p


def make_xlsx(path, replace=None):
    """Minimal synthetic native Tables, rich text, non-sequential sheet XML names."""
    mns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    rns = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    pns = 'http://schemas.openxmlformats.org/package/2006/relationships'
    def cell(ref, value, bold=False):
        content = f'<r><rPr><b/><rFont val="微软雅黑"/><sz val="14"/></rPr><t>{value}</t></r>' if bold else f'<t>{value}</t>'
        return f'<c r="{ref}" t="inlineStr" s="0"><is>{content}</is></c>'
    sheets = {}
    for num, ref, title in ((7, "C5", "原始源网名／测点"), (42, "C5", "完整信号链")):
        ctext = "U2.6" if num == 7 else "SRC X1.7 -&gt; U2.6"
        sheets[f'xl/worksheets/sheet{num}.xml'] = f'<worksheet xmlns="{mns}" xmlns:r="{rns}"><sheetViews><sheetView workbookViewId="0"><pane ySplit="4" topLeftCell="A5" state="frozen"/></sheetView></sheetViews><sheetData><row r="4">{cell("A4","地址HEX")}{cell("B4","来源板卡")}{cell("C4",title)}</row><row r="5" ht="70" customHeight="1">{cell("A5","0x00")}{cell("B5","SRC")}{cell(ref,ctext,True)}</row></sheetData><tableParts count="1"><tablePart r:id="table"/></tableParts></worksheet>'
        sheets[f'xl/worksheets/_rels/sheet{num}.xml.rels'] = f'<Relationships xmlns="{pns}"><Relationship Id="table" Type="{rns}/table" Target="../tables/table{num}.xml"/></Relationships>'
        sheets[f'xl/tables/table{num}.xml'] = f'<table xmlns="{mns}" id="{num}" name="T{num}" displayName="T{num}" ref="A4:C5"><autoFilter ref="A4:C5"/><tableColumns count="3"><tableColumn id="1" name="地址HEX"/><tableColumn id="2" name="来源板卡"/><tableColumn id="3" name="{title}"/></tableColumns></table>'
    parts = {
        'xl/workbook.xml': f'<workbook xmlns="{mns}" xmlns:r="{rns}"><sheets><sheet name="遥测简表" sheetId="1" r:id="r1"/><sheet name="地址与物理意义" sheetId="2" r:id="r2"/></sheets></workbook>',
        'xl/_rels/workbook.xml.rels': f'<Relationships xmlns="{pns}"><Relationship Id="r1" Type="{rns}/worksheet" Target="worksheets/sheet7.xml"/><Relationship Id="r2" Type="{rns}/worksheet" Target="worksheets/sheet42.xml"/></Relationships>',
        'xl/styles.xml': f'<styleSheet xmlns="{mns}"><fonts count="1"><font><sz val="14"/><name val="微软雅黑"/></font></fonts><cellXfs count="1"><xf fontId="0"/></cellXfs></styleSheet>',
        'xl/media/image1.png': b'synthetic-image-bytes',
        'xl/drawings/drawing1.xml': '<drawing><anchor row="7"/></drawing>',
        **sheets,
    }
    if replace:
        replace(parts)
    with ZipFile(path, 'w') as z:
        for k, v in parts.items(): z.writestr(k, v)


def view_manifest():
    return dict(schema_version=1, routes=[dict(address="0x00", display=dict(board="SRC",endpoint="U2.6",route="SRC X1.7 -> U2.6"))], workbook=dict(sheets=[
        dict(name="遥测简表",header_row=4,first_data_row=5,last_data_row=5,address_column="A",headers={"A":"地址HEX"},fields={"B":"board","C":"endpoint"},route_columns=["C"]),
        dict(name="地址与物理意义",header_row=4,first_data_row=5,last_data_row=5,address_column="A",headers={"A":"地址HEX"},fields={"B":"board","C":"route"},route_columns=["C"])
    ], required_bold=[dict(sheet="遥测简表",cell="C5",text="U2.6")]))


class Audits(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=WORK, prefix="case-")
        self.root = Path(self.temp.name)
        self.m, self.p = graph(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def route(self, code=None):
        r, _ = route_audit(self.m, self.p, self.root)
        if code:
            self.assertIn(code, [f['code'] for f in r['findings']], r)
            self.assertNotEqual(r['status'], 'passed')
        return r

    def test_valid_route(self): self.assertEqual(self.route()['status'], 'passed')
    def test_duplicate_address(self):
        self.m['routes'].append(copy.deepcopy(self.m['routes'][0])); self.route('DUPLICATE_ADDRESS')
    def test_missing_address(self):
        self.m['routes']=[]; self.route('ADDRESS_COVERAGE')
    def test_wrong_mode(self):
        self.m['routes'][0]['mode']='GS'; self.route('MODE_MISMATCH')
    def test_wrong_mux(self):
        self.m['routes'][0]['mux']={'U1':'S2'}; self.route('MAPPING_MISMATCH')
    def test_unfitted(self):
        self.m['routes'][0]['segments'][1]['component']['state']='unfitted'; self.route('UNFITTED_ACTIVE')
    def test_unscoped_tsd(self):
        self.m['evidence']['fit']['scope']['refs']=['R2']; self.route('TSD_OVERRIDE_MISSING')
    def test_wrong_connector(self):
        self.p['connector_pairs'][0]['to']='u'; self.route('CONNECTOR_UNBOUND')
    def test_broken_adjacency(self):
        self.m['routes'][0]['segments'][2]['from']='a'; self.route('BROKEN_ADJACENCY')
    def test_net_jump(self):
        self.m['nodes']['u']['net']='OTHER'; self.route('NET_JUMP')
    def test_wrong_board(self):
        self.m['routes'][0]['source_board']='ACQ'; self.route('SOURCE_BOARD_MISMATCH')
    def test_missing_physical_parameters(self):
        self.m['routes'][0]['conversion']['output_kind']='physical_quantity'; self.route('UNSUPPORTED_PHYSICAL_VALUE')
    def test_missing_evidence(self):
        self.m['routes'][0]['segments'][0]['evidence']=[]
        self.assertEqual(self.route('EVIDENCE_MISSING')['status'],'needs_review')
    def test_source_changed(self):
        Path(self.m['evidence']['pst']['path']).write_text('changed',encoding='utf-8'); self.route('SOURCE_CHANGED')
    def test_skipped_source_interface(self):
        self.m['nodes']['other']=dict(board='SRC',ref='X2',pin='2',net='MON')
        self.m['routes'][0]['source_interface']='other'; self.route('SOURCE_INTERFACE_SKIPPED')
    def test_unknown_endpoint(self):
        self.m['routes'][0]['endpoint']='missing'; self.route('ENDPOINT_UNKNOWN')
    def test_cascade(self):
        self.p['physical_inputs']['U1.S2']={'node':'a'}; self.p['cascade_inputs']=['U1.S2']
        self.assertEqual(self.route()['status'],'passed')
        self.p['cascade_inputs']=[]; self.route('INPUT_COVERAGE')
    def test_conversion_boundaries(self):
        for raw, expected in [(0,0),(1,5/32768),(0x4000,2.5),(0x7fff,5-5/32768),(0x8000,-5),(0xc000,-2.5),(0xffff,-5/32768)]:
            self.assertAlmostEqual(decode_adc(raw,16,'twos_complement',5)[1],expected)
        with self.assertRaises(ValueError): decode_adc(65536,16,'twos_complement',5)

    def wb(self, modifier=None, changes=None, manifest=None):
        before=self.root/'before.xlsx'; after=self.root/'after.xlsx'
        make_xlsx(before); make_xlsx(after,modifier)
        h=sha256(before)
        result=workbook_audit(before,after,manifest or view_manifest(),changes or {'schema_version':1})
        self.assertEqual(sha256(before),h)
        return result

    def has(self, result, code): self.assertIn(code,[f['code'] for f in result['findings']], result)
    def test_workbook_relationship_lookup(self): self.assertEqual(self.wb()['status'],'passed')
    def test_blank_header(self):
        def change(p): p['xl/worksheets/sheet7.xml']=p['xl/worksheets/sheet7.xml'].replace('<t>来源板卡</t>','<t/>')
        self.has(self.wb(change),'HEADER_EMPTY')
    def test_table_name_mismatch(self):
        def change(p): p['xl/tables/table7.xml']=p['xl/tables/table7.xml'].replace('name="来源板卡"','name="wrong"')
        self.has(self.wb(change),'HEADER_TABLE_MISMATCH')
    def test_wrong_filter(self):
        def change(p): p['xl/tables/table7.xml']=p['xl/tables/table7.xml'].replace('<autoFilter ref="A4:C5"','<autoFilter ref="A4:B5"')
        self.has(self.wb(change),'TABLE_FILTER_RANGE')
    def test_changed_font(self):
        def change(p): p['xl/styles.xml']=p['xl/styles.xml'].replace('val="14"','val="9"')
        self.has(self.wb(change),'UNAUTHORIZED_PACKAGE_PART')
    def test_image_changed(self):
        def change(p): p['xl/media/image1.png']=b'changed'
        self.has(self.wb(change),'UNAUTHORIZED_PACKAGE_PART')
    def test_anchor_changed(self):
        def change(p): p['xl/drawings/drawing1.xml']=p['xl/drawings/drawing1.xml'].replace('row="7"','row="9"')
        self.has(self.wb(change),'UNAUTHORIZED_PACKAGE_PART')
    def test_rich_bold_removed(self):
        def change(p): p['xl/worksheets/sheet7.xml']=p['xl/worksheets/sheet7.xml'].replace('<b/>','')
        self.has(self.wb(change),'BOLD_NOT_VERIFIED')
    def test_bad_notation(self):
        def change(p): p['xl/worksheets/sheet7.xml']=p['xl/worksheets/sheet7.xml'].replace('U2.6','N123456 || R1')
        self.has(self.wb(change),'DISPLAY_NOTATION')
    def test_different_source(self):
        def change(p): p['xl/worksheets/sheet42.xml']=p['xl/worksheets/sheet42.xml'].replace('<t>SRC</t>','<t>WRONG</t>')
        self.has(self.wb(change),'VIEW_VALUE_MISMATCH')
    def test_authorized_text(self):
        def change(p): p['xl/worksheets/sheet7.xml']=p['xl/worksheets/sheet7.xml'].replace('U2.6','U2.7')
        m=view_manifest(); m['routes'][0]['display']['endpoint']='U2.7'; m['workbook']['required_bold'][0]['text']='U2.7'
        r=self.wb(change,{'schema_version':1,'cells':{'遥测简表':{'C5':['value','runs']}}},m)
        self.assertEqual(r['status'],'passed',r)
    def test_no_binding_not_pass(self):
        r=self.wb(manifest={'schema_version':1}); self.assertEqual(r['status'],'needs_review')
    def test_text_permission_does_not_allow_font_change(self):
        def change(p): p['xl/worksheets/sheet7.xml']=p['xl/worksheets/sheet7.xml'].replace('val="14"','val="9"')
        r=self.wb(change,{'schema_version':1,'cells':{'遥测简表':{'C5':['value','runs']}}})
        self.has(r,'UNAUTHORIZED_RICH_STYLE')
    def test_formula_error(self):
        def change(p): p['xl/worksheets/sheet7.xml']=p['xl/worksheets/sheet7.xml'].replace('</row></sheetData>','<c r="D5" t="e"><f>1/0</f><v>#DIV/0!</v></c></row></sheetData>')
        self.has(self.wb(change),'FORMULA_ERROR')
    def test_frozen_pane_changed(self):
        def change(p): p['xl/worksheets/sheet7.xml']=p['xl/worksheets/sheet7.xml'].replace('ySplit="4"','ySplit="0"')
        self.has(self.wb(change),'UNAUTHORIZED_SHEET_META')
    def test_row_height_changed(self):
        def change(p): p['xl/worksheets/sheet7.xml']=p['xl/worksheets/sheet7.xml'].replace('ht="70"','ht="15"')
        self.has(self.wb(change),'UNAUTHORIZED_ROW')
    def test_report_cannot_overwrite_input(self):
        path=self.root/'manifest.json'; path.write_text('{}',encoding='utf-8')
        with self.assertRaises(ValueError): write_report(path,{},[path])
        self.assertEqual(path.read_text(),'{}')
    def test_report_cannot_overwrite_old_report(self):
        path=self.root/'report.json'; path.write_text('old',encoding='utf-8')
        with self.assertRaises(FileExistsError): write_report(path,{},[])
        self.assertEqual(path.read_text(),'old')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',required=True); parser.add_argument('--report',required=True)
    args=parser.parse_args(); WORK=Path(args.work).resolve(); WORK.mkdir(parents=True,exist_ok=True)
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Audits)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    write_report(args.report,dict(tests=result.testsRun,failures=[(str(t),err) for t,err in result.failures],
        errors=[(str(t),err) for t,err in result.errors],status='passed' if result.wasSuccessful() else 'failed'),[])
    raise SystemExit(0 if result.wasSuccessful() else 1)
