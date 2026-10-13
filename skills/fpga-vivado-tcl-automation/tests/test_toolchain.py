"""Behavior regressions for shared project, RTL and XDC helpers. Synthetic inputs only."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SKILLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILLS / 'fpga-vivado-tcl-automation/scripts'))
from project_inputs import inspect_project, sha256
from rtl_ports import module_ports
from audit_native_layout import audit as layout


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, SKILLS / path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


pin = load('pin_test_module', 'rtl-schematic-xdc-alignment/scripts/rtl_xdc_pst_audit.py')
arch = load('arch_test_module', 'gf-architect/scripts/rtl_hierarchy_scan.py')


class ToolchainTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='rtl-skill-test-', dir=os.environ.get('RTL_TEST_ROOT'))
        self.root = Path(self.temp.name)
        self.rtl = self.put('top.v', 'module top(input wire clk, output wire [7:4] data); endmodule\n')
        self.pst = self.put('pst.dat', ''.join(f"NET_NAME\n'N_{i}'\nNODE_NAME D1 A{i}\n" for i in range(1, 10)))
        self.xdc = self.put('pins.xdc', self.constraints())

    def tearDown(self):
        self.temp.cleanup()

    def put(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def constraints(self):
        names = ['clk', 'data[4]', 'data[5]', 'data[6]', 'data[7]']
        return '\n'.join(f'set_property -dict {{PACKAGE_PIN A{i} IOSTANDARD LVCMOS18}} [get_ports {{{name}}}]' for i, name in enumerate(names, 1))

    def audit(self, **kwargs):
        args = dict(rtl=self.rtl, top='top', xdc=[self.xdc], pstxnet=self.pst, fpga_refdes='D1')
        args.update(kwargs)
        return pin.audit(argparse.Namespace(**args))

    def xpr(self, extra='', top='top'):
        return self.put('design.xpr', f'''<Project Version="7"><Configuration><Option Name="Part" Val="testpart"/></Configuration>
<FileSets><FileSet Name="sources_1"><File Path="$PPRDIR/top.v"><FileInfo><Attr Name="UsedIn" Val="synthesis"/><Attr Name="UsedIn" Val="implementation"/></FileInfo></File>{extra}<Config><Option Name="TopModule" Val="{top}"/></Config></FileSet>
<FileSet Name="constrs_1"><File Path="$PPRDIR/pins.xdc"/></FileSet><FileSet Name="sim_1"><File Path="$PPRDIR/nonexistent_tb.v"/></FileSet></FileSets></Project>''')

    def test_dict_and_nonzero_bus(self):
        result = self.audit()
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['coverage']['expected'], 5)
        self.assertEqual([r['port'] for r in result['rows']], ['clk', 'data[4]', 'data[5]', 'data[6]', 'data[7]'])

    def test_separate_multiline_and_comments(self):
        self.xdc.write_text('# set_property PACKAGE_PIN Z9 [get_ports wrong]\n' +
                            '\n'.join(f'set_property PACKAGE_PIN A{i} [get_ports {{{n}}}]' for i,n in enumerate(['clk','data[4]','data[5]','data[6]','data[7]'],1)) +
                            '\nset_property IOSTANDARD LVCMOS18 [get_ports {\n clk {data[*]}\n}]\n', encoding='utf-8')
        self.assertEqual(self.audit()['status'], 'pass')

    def test_empty_and_unsupported_never_pass(self):
        for text in ['', '# only comment', 'source other.xdc', 'foreach p $ports {set_property PACKAGE_PIN A1 $p}']:
            with self.subTest(text=text):
                self.xdc.write_text(text, encoding='utf-8')
                self.assertNotEqual(self.audit()['status'], 'pass')

    def test_dynamic_with_other_valid_lines_needs_review(self):
        self.xdc.write_text(self.constraints() + '\nset_property PACKAGE_PIN $pin [get_ports clk]', encoding='utf-8')
        self.assertEqual(self.audit()['status'], 'needs_review')

    def test_missing_and_selected_scope(self):
        self.xdc.write_text(self.constraints().splitlines()[0], encoding='utf-8')
        self.assertEqual(self.audit()['status'], 'fail')
        result = self.audit(ports=['clk'])
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['coverage']['scope'], 'selected_ports')

    def test_multifile_conflict(self):
        extra = self.put('override.xdc', 'set_property PACKAGE_PIN A9 [get_ports clk]')
        self.assertEqual(self.audit(xdc=[self.xdc,extra])['status'], 'fail')

    def test_duplicate_pin(self):
        self.xdc.write_text(self.constraints().replace('PACKAGE_PIN A2', 'PACKAGE_PIN A1'), encoding='utf-8')
        self.assertTrue(any('同时绑定' in e for e in self.audit()['errors']))

    def test_out_of_range(self):
        self.xdc.write_text(self.constraints().replace('data[7]', 'data[8]'), encoding='utf-8')
        self.assertEqual(self.audit()['status'], 'fail')

    def test_symbolic_width_not_scalar(self):
        self.rtl.write_text('module top #(parameter W=4)(input clk, output [W-1:0] data); endmodule', encoding='utf-8')
        ports, issues = module_ports(self.rtl.read_text(), 'top')
        self.assertIsNone(ports['data']['width'])
        self.assertTrue(issues)
        self.assertNotEqual(self.audit()['status'], 'pass')

    def test_ascending_negative_bus(self):
        ports, _ = module_ports('module top(input [-2:1] bus); endmodule')
        self.assertEqual(pin.expand_ports('{bus[*]}', ports), ['bus[-2]', 'bus[-1]', 'bus[0]', 'bus[1]'])

    def test_dedicated_pads_need_hash_bound_evidence(self):
        self.rtl.write_text('module top(output tx); endmodule', encoding='utf-8')
        self.xdc.write_text('set_property PACKAGE_PIN A1 [get_ports tx]', encoding='utf-8')
        self.assertEqual(self.audit()['status'], 'fail')
        evidence = self.put('package.tsv', 'A1\tMGTH_TXP0\n')
        exemption = self.put('dedicated.json', json.dumps(dict(part='testpart', evidence_file=str(evidence), evidence_sha256=sha256(evidence), pins={'A1':'MGTHTXP0_100'})))
        self.assertEqual(self.audit(part='testpart', dedicated_pins=exemption)['status'], 'pass')
        content=json.loads(exemption.read_text())
        content['pins']={'A1':'MGTREFCLK1P_119'}
        exemption.write_text(json.dumps(content),encoding='utf-8')
        self.assertEqual(self.audit(part='testpart', dedicated_pins=exemption)['status'], 'pass')
        with self.assertRaises(ValueError): self.audit(part='wrongpart', dedicated_pins=exemption)
        evidence.write_text('changed', encoding='utf-8')
        with self.assertRaises(ValueError): self.audit(part='testpart', dedicated_pins=exemption)

    def test_ansi_and_nonansi(self):
        for code in ['module top(input wire clk, output wire [7:0] data); endmodule',
                     'module top(clk,data); input clk; output [7:0] data; endmodule']:
            ports = arch.parse_ports(code, 1)
            self.assertEqual(ports[1]['direction'], 'output')
            self.assertEqual(ports[1]['resolved_width'], 8)

    def test_disabled_sim_and_generated_sources(self):
        xpr = self.xpr('<File Path="$PPRDIR/old.v"><FileInfo><Attr Name="AutoDisabled" Val="1"/></FileInfo></File>')
        result = inspect_project(xpr)
        self.assertEqual(result['status'], 'pass')
        self.assertFalse(next(i for i in result['inputs'] if i['raw_path'].endswith('old.v'))['active'])
        self.assertEqual(inspect_project(xpr,'simulation')['status'], 'fail')
        xpr = self.xpr('<File Path="$PPRDIR/gen.v"><FileInfo><Attr Name="IsGenerated" Val="1"/></FileInfo></File>')
        self.assertEqual(inspect_project(xpr)['status'], 'needs_review')

    def test_missing_and_wrong_top_fail_even_legacy(self):
        xpr = self.xpr('<File Path="$PPRDIR/missing.v"/>')
        self.assertEqual(inspect_project(xpr)['status'], 'fail')
        self.assertFalse(layout(xpr,legacy=True)['passed'])
        self.assertEqual(inspect_project(self.xpr(),top='wrong')['status'], 'fail')

    def test_unresolved_variable_not_success(self):
        self.assertEqual(inspect_project(self.xpr('<File Path="$UNKNOWN/foo.v"/>'))['status'], 'needs_review')

    def test_duplicate_definition_not_resolved(self):
        a = self.put('a.v', 'module child(input a); endmodule\n')
        b = self.put('b.v', 'module child(input b); endmodule\n')
        self.rtl.write_text('module top(input a);\n child u_child(.a(a));\nendmodule\n', encoding='utf-8')
        modules = sum([arch.parse_modules(p,self.root) for p in [self.rtl,a,b]], [])
        data = arch.build_map(self.root,modules,[self.rtl,a,b],[],top='top')
        self.assertIn('child',data['duplicates'])
        self.assertEqual(data['edges'],[])
        self.assertEqual(data['unresolved'][0]['reason'],'duplicate_definition')

    def test_macros_generate_candidates(self):
        self.rtl.write_text('module top(input a);\n`ifdef TEST\n generate if (1) begin\n child u(.a(a));\n end endgenerate\n`endif\nendmodule', encoding='utf-8')
        self.assertTrue(arch.parse_modules(self.rtl,self.root)[0]['needs_review'])

    def test_keywords_not_split_into_fake_instances(self):
        code='module top(input a);\n always @(posedge a) begin\n if (a) begin\n end\n case (a)\n endcase\n end\n child u_real(.a(a));\nendmodule'
        self.assertEqual([i['module'] for i in arch.parse_instances(code,1)],['child'])

    def test_arch_cli_xpr_ignores_history_no_writes(self):
        self.put('historical.v', 'module top(input wrong); endmodule')
        xpr = self.xpr()
        before = {str(p):sha256(p) for p in self.root.iterdir() if p.is_file()}
        cmd = [sys.executable,'-B',str(SKILLS/'gf-architect/scripts/rtl_hierarchy_scan.py'),str(self.root),'--project',str(xpr)]
        run = subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(run.returncode,0,run.stderr)
        data = json.loads(run.stdout)
        self.assertEqual(len(data['modules']),1)
        self.assertEqual(data['configured_top'],'top')
        self.assertFalse((self.root/'.fpga-map').exists())
        self.assertEqual(before,{str(p):sha256(p) for p in self.root.iterdir() if p.is_file()})

    def test_project_pin_audit_and_scoped_uncertainty(self):
        xpr = self.xpr()
        self.assertEqual(self.audit(project=xpr,xdc=None,rtl=None)['status'],'pass')
        xpr.write_text(xpr.read_text().replace('<File Path="$PPRDIR/pins.xdc"/>','<File Path="$PPRDIR/pins.xdc"><FileInfo><Attr Name="ScopedToRef" Val="sub"/></FileInfo></File>'),encoding='utf-8')
        self.assertEqual(self.audit(project=xpr,xdc=None,rtl=None)['status'],'needs_review')

    def test_gbk_comments_and_actual_current_run_schema(self):
        self.rtl.write_bytes('// 中文历史源码\nmodule top(input clk); endmodule'.encode('gbk'))
        xpr=self.xpr()
        content=xpr.read_text().replace('Name="sources_1"','Name="custom_sources"').replace('</Project>',
          '<Runs><Run Id="synth_custom" Type="Ft3:Synth" State="current" SrcSet="custom_sources" ConstrsSet="constrs_1"/>'
          '<Run Id="impl_custom" Type="Ft2:EntireDesign" State="current" SynthRun="synth_custom" ConstrsSet="constrs_1"/></Runs></Project>')
        xpr.write_text(content,encoding='utf-8')
        result=inspect_project(xpr)
        self.assertEqual(result['status'],'pass')
        self.assertEqual(result['source_set'],'custom_sources')

    def test_unsupported_property_list_and_side_effect(self):
        for extra in ['set_property {PACKAGE_PIN IOSTANDARD} {A9 LVCMOS18} [get_ports clk]',
                      'create_clock -period 10 [set_property PACKAGE_PIN A9 [get_ports clk]]']:
            self.xdc.write_text(self.constraints()+'\n'+extra,encoding='utf-8')
            self.assertEqual(self.audit()['status'],'needs_review')


if __name__ == '__main__': unittest.main(verbosity=2)
