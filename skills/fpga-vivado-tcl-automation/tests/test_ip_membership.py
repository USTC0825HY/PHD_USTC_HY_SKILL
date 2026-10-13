"""Read-only IP/container regressions using temporary synthetic XPRs."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from project_inputs import inspect_project
from audit_native_layout import audit


class IPTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=os.environ.get('RTL_TEST_ROOT'))
        self.root = Path(self.tmp.name)
        self.xpr = self.root / 'demo.xpr'
        self.put('demo.srcs/sources_1/new/system/top.v', 'module top; endmodule')

    def tearDown(self):
        self.tmp.cleanup()

    def put(self, path, text):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return p

    def xci(self, name='core'):
        return f'<design><configurableElementValue referenceId="PARAM_VALUE.Component_Name">{name}</configurableElementValue></design>'

    def project(self, block='', runs=True, extra=''):
        self.xpr.write_text(f'''<Project><Configuration><Option Name="Part" Val="test"/></Configuration><FileSets>
<FileSet Name="sources_1"><File Path="$PSRCDIR/sources_1/new/system/top.v"/>{extra}<Config><Option Name="TopModule" Val="top"/></Config></FileSet>
<FileSet Name="core" Type="BlockSrcs">{block}<Config><Option Name="TopModule" Val="core"/></Config></FileSet>
</FileSets><Runs>{'<Run Id="core_synth_1" SrcSet="core"/>' if runs else ''}</Runs></Project>''')
        return inspect_project(self.xpr)

    def container(self, content=None):
        p = self.root / 'demo.srcs/sources_1/ip/core.xcix'
        p.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(p, 'w') as z:
            z.writestr('core/core.xci', self.xci() if content is None else content)
            z.writestr('core/core.v', 'module core; endmodule')
        return p

    def files(self):
        return '<File Path="$PSRCDIR/sources_1/ip/core.xcix"/><File Path="$PSRCDIR/sources_1/ip/core/core.xci"/>'

    def test_container_pair_and_native_role(self):
        self.container()
        r = self.project(self.files())
        self.assertEqual(r['status'], 'pass')
        self.assertEqual(r['active_ip_count'], 1)
        self.assertTrue(r['inputs'][-1]['exists'])
        self.assertEqual(len(r['containers'][0]['members']), 2)
        self.assertTrue(audit(self.xpr)['passed'])

    def test_standalone_xci(self):
        self.put('demo.srcs/sources_1/ip/core/core.xci', self.xci())
        r = self.project('<File Path="$PSRCDIR/sources_1/ip/core/core.xci"/>')
        self.assertEqual((r['status'], r['active_ip_count']), ('pass', 1))

    def test_missing_container(self):
        self.assertEqual(self.project(self.files())['status'], 'fail')

    def test_broken_zip(self):
        self.put('demo.srcs/sources_1/ip/core.xcix', 'broken')
        self.assertEqual(self.project(self.files())['status'], 'fail')

    def test_broken_member(self):
        self.container('<broken')
        self.assertEqual(self.project(self.files())['status'], 'fail')

    def test_missing_root_member(self):
        p = self.container()
        with zipfile.ZipFile(p, 'w') as z:
            z.writestr('elsewhere.xci', self.xci())
        self.assertEqual(self.project(self.files())['status'], 'fail')

    def test_identity_mismatch(self):
        self.container(self.xci('other'))
        self.assertEqual(self.project(self.files())['status'], 'fail')

    def test_duplicate_registration(self):
        self.container()
        self.assertEqual(self.project(self.files() * 2)['status'], 'fail')

    def test_unknown_association(self):
        self.container()
        self.assertEqual(self.project(self.files(), runs=False)['status'], 'needs_review')

    def test_disabled_ip(self):
        block = '<File Path="$PSRCDIR/sources_1/ip/absent.xci"><FileInfo><Attr Name="IsEnabled" Val="0"/></FileInfo></File>'
        r = self.project(block)
        self.assertEqual((r['status'], r['active_ip_count']), ('pass', 0))

    def test_container_inherits_disabled_root(self):
        self.container()
        files = self.files().replace('core/core.xci"/>', 'core/core.xci"><FileInfo><Attr Name="AutoDisabled" Val="1"/></FileInfo></File>')
        r = self.project(files)
        self.assertEqual((r['status'], r['active_ip_count']), ('pass', 0))

    def test_history_not_dependency(self):
        self.container()
        files = self.files().replace('core.xcix"/>', 'core.xcix"><FileInfo><Attr Name="ImportPath" Val="$PPRDIR/build/old.xcix"/></FileInfo></File>')
        self.assertEqual(self.project(files)['status'], 'pass')

    def test_temp_and_reference_dependency(self):
        for path in ['build/old.v', 'demo.srcs/reference/old.v']:
            self.put(path, 'module old; endmodule')
            self.assertEqual(self.project(extra=f'<File Path="$PPRDIR/{path}"/>')['status'], 'fail')

    def test_simulation_lists_isolate_same_model(self):
        a = self.put('demo.srcs/sim_1/new/a/model.v', 'module model; endmodule')
        b = self.put('demo.srcs/sim_1/new/b/model.v', 'module model; endmodule')
        self.put('demo.srcs/sim_1/new/a/tb.v', 'module tb; endmodule')
        self.project()
        s = self.xpr.read_text().replace('</FileSets>', '''<FileSet Name="sim_1"><File Path="$PSRCDIR/sim_1/new/a/model.v"/><File Path="$PSRCDIR/sim_1/new/a/tb.v"/><Config><Option Name="TopModule" Val="tb"/></Config></FileSet><FileSet Name="case_b"><File Path="$PSRCDIR/sim_1/new/b/model.v"/></FileSet></FileSets>''')
        self.xpr.write_text(s)
        self.assertEqual(inspect_project(self.xpr, 'simulation')['status'], 'pass')
        self.xpr.write_text(s.replace('<Config><Option Name="TopModule" Val="top"/>', f'<File Path="{a.as_posix()}"/><File Path="{b.as_posix()}"/><Config><Option Name="TopModule" Val="top"/>'))
        self.assertNotEqual(inspect_project(self.xpr)['status'], 'pass')


if __name__ == '__main__':
    unittest.main()
