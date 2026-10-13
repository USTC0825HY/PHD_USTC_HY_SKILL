import contextlib,importlib.util,io,json,os,pathlib,tempfile,unittest,urllib.error
from unittest.mock import patch
ROOT=pathlib.Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('novelty',ROOT/'scripts/novelty_check.py')
m=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(m)

class Response:
    def __init__(self,data):self.data=data
    def __enter__(self):return self
    def __exit__(self,*a):pass
    def read(self):return self.data

class SearchContract(unittest.TestCase):
    def run_search(self,side,queries=('q1',),rounds=None):
        with patch.object(m,'generate_search_queries',return_value=list(queries)),patch.object(m,'search_semantic_scholar',side_effect=side),contextlib.redirect_stderr(io.StringIO()):
            return m.run_novelty_check('中文 PDH 延迟',rounds or len(queries),2)
    def cli(self,result,args):
        with patch.object(m,'run_novelty_check',return_value=result),contextlib.redirect_stdout(io.StringIO()) as out,contextlib.redirect_stderr(io.StringIO()):
            code=m.main(args)
        return code,out.getvalue()
    def test_empty_success_not_failed_or_novel(self):
        r=self.run_search([[]]);self.assertEqual(r['search_status'],'complete');self.assertEqual(r['query_records'][0]['status'],'empty');self.assertEqual(r['assessment'],'insufficient_evidence');self.assertEqual(r['query_records'][0]['result_count'],0)
    def test_failure_not_zero_result(self):
        r=self.run_search([m.SearchError('timeout','timeout',3)]);self.assertEqual(r['search_status'],'failed');self.assertIsNone(r['query_records'][0]['result_count']);self.assertTrue(r['errors'])
    def test_partial_retains_evidence(self):
        r=self.run_search([[dict(paperId='p1',title='Paper',citationCount=1)],m.SearchError('http_error','HTTP 403',1,403)],('q1','q2'))
        self.assertEqual(r['search_status'],'partial');self.assertEqual(r['total_papers_found'],1);self.assertEqual(len(r['query_records']),2)
    def test_empty_then_failure_is_partial(self):
        self.assertEqual(self.run_search([[],m.SearchError('timeout','timeout')],('q1','q2'))['search_status'],'partial')
    def test_discovery_order_not_citation_similarity(self):
        r=self.run_search([[dict(paperId='a',title='First',citationCount=1),dict(paperId='b',title='Second',citationCount=99)]])
        self.assertEqual([p['paperId'] for p in r['candidates']],['a','b']);self.assertEqual(r['most_cited_similar'][0]['title'],'Second');self.assertFalse(r['candidates'][0]['overlap_assessed'])
    def test_duplicate_identity_and_provenance(self):
        p=dict(paperId='same',title='Paper',externalIds={'DOI':'10.example/mock'},url='https://example.invalid/p')
        r=self.run_search([[p],[p]],('q1','q2'));self.assertEqual(r['total_papers_found'],1);self.assertEqual(r['candidates'][0]['queries'],['q1','q2']);self.assertEqual(r['candidates'][0]['doi'],'10.example/mock')
    def test_duplicate_query_not_repeated(self):
        r=self.run_search([[]],('Query','query'),2);self.assertEqual(r['rounds_used'],1)
    def test_missing_identifiers_not_invented(self):
        r=self.run_search([[dict(title='Paper')]]);self.assertIsNone(r['candidates'][0]['doi']);self.assertIsNone(r['candidates'][0]['url'])
    def test_unicode_query_survives(self):
        with patch.object(m.urllib.request,'urlopen',return_value=Response(b'{"data":[]}')) as call:
            self.assertEqual(m.search_semantic_scholar('数字锁相',1),[])
        self.assertIn('%E6%95%B0',call.call_args.args[0].full_url)
    def test_rate_limit_exhaustion_raises(self):
        error=urllib.error.HTTPError('https://example.invalid',429,'limited',{},None)
        with patch.object(m.urllib.request,'urlopen',side_effect=error) as call,patch.object(m.time,'sleep'):
            with self.assertRaises(m.SearchError) as cm:m.search_semantic_scholar('pdh')
        self.assertEqual(call.call_count,3);self.assertEqual(cm.exception.kind,'rate_limited')
    def test_timeout_exhaustion_raises(self):
        with patch.object(m.urllib.request,'urlopen',side_effect=TimeoutError()),patch.object(m.time,'sleep'):
            with self.assertRaises(m.SearchError) as cm:m.search_semantic_scholar('pdh')
        self.assertEqual(cm.exception.kind,'timeout')
    def test_network_failure_raises(self):
        with patch.object(m.urllib.request,'urlopen',side_effect=urllib.error.URLError('offline')),patch.object(m.time,'sleep'):
            with self.assertRaises(m.SearchError) as cm:m.search_semantic_scholar('pdh')
        self.assertEqual(cm.exception.kind,'network_error')
    def test_http_403_not_retried(self):
        with patch.object(m.urllib.request,'urlopen',side_effect=urllib.error.HTTPError('x',403,'denied',{},None)) as call:
            with self.assertRaises(m.SearchError):m.search_semantic_scholar('pdh')
        self.assertEqual(call.call_count,1)
    def test_invalid_json(self):
        with patch.object(m.urllib.request,'urlopen',return_value=Response(b'<html>')):
            with self.assertRaises(m.SearchError) as cm:m.search_semantic_scholar('pdh')
        self.assertEqual(cm.exception.kind,'invalid_response')
    def test_invalid_data_shape(self):
        for body in [b'{}',b'{"data":null}',b'{"data":[4]}']:
            with self.subTest(body=body),patch.object(m.urllib.request,'urlopen',return_value=Response(body)):
                with self.assertRaises(m.SearchError):m.search_semantic_scholar('pdh')
    def test_retry_recovery(self):
        with patch.object(m.urllib.request,'urlopen',side_effect=[TimeoutError(),Response(b'{"data":[]}')]),patch.object(m.time,'sleep'):
            self.assertEqual(m.search_semantic_scholar('pdh'),[])
    def test_truncated_http_retains_previous_success(self):
        responses=[Response(b'{"data":[{"paperId":"p1","title":"PDH"}]}')]+[m.http.client.IncompleteRead(b'partial')]*3
        with patch.object(m,'generate_search_queries',return_value=['q1','q2']),patch.object(m.urllib.request,'urlopen',side_effect=responses),patch.object(m.time,'sleep'),contextlib.redirect_stderr(io.StringIO()):
            r=m.run_novelty_check('pdh',2)
        self.assertEqual(r['search_status'],'partial');self.assertEqual(r['total_papers_found'],1);self.assertEqual(r['errors'][0]['kind'],'invalid_response')
    def test_invalid_paper_fields_return_failed_dictionary(self):
        for field,value in [('title',3),('year',[]),('abstract',5),('citationCount',float('nan')),('externalIds',[]),('authors','invalid')]:
            body=json.dumps({'data':[{'paperId':'x',field:value}]}).encode()
            with self.subTest(field=field),patch.object(m.urllib.request,'urlopen',return_value=Response(body)),contextlib.redirect_stderr(io.StringIO()):
                result=m.run_novelty_check('pdh',1)
                self.assertEqual(result['search_status'],'failed');self.assertEqual(result['errors'][0]['kind'],'invalid_response');self.assertIsNone(result['query_records'][0]['result_count'])
    def test_success_fields_remain(self):
        r=self.run_search([[]]);self.assertTrue({'idea','total_papers_found','rounds_used','queries_used','most_cited_similar'}<=r.keys())
    def test_cli_exit_states_and_json(self):
        for state,code in [('complete',0),('partial',3),('failed',1)]:
            with self.subTest(state=state):
                c,s=self.cli(dict(search_status=state),['--idea','公开问题']);self.assertEqual(c,code);self.assertEqual(json.loads(s)['search_status'],state)
    def test_invalid_cli_input_exit_two(self):
        for args in [[],['--idea',' '],['--idea','x','--max-rounds','0'],['--idea','x','--result-limit','101']]:
            with self.subTest(args=args),contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as cm:m.main(args)
                self.assertEqual(cm.exception.code,2)
    def test_invalid_python_input_returns_dictionary(self):
        self.assertEqual(m.run_novelty_check('',0)['search_status'],'failed')
    def test_output_failed_and_partial_are_saved(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('NOVELTY_TEST_TMP')) as td:
            p=pathlib.Path(td)/'out.json'
            code,_=self.cli(dict(search_status='partial',errors=['fixture']),['--idea','x','--output',str(p)])
            self.assertEqual(code,3);self.assertEqual(json.loads(p.read_text(encoding='utf-8'))['errors'],['fixture'])
    def test_output_write_error_nonzero(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('NOVELTY_TEST_TMP')) as td:
            code,text=self.cli(dict(search_status='complete'),['--idea','x','--output',td])
            self.assertEqual(code,1);self.assertEqual(json.loads(text)['search_status'],'complete')
    def test_file_precedence_bom_and_chinese(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('NOVELTY_TEST_TMP')) as td:
            p=pathlib.Path(td)/'idea.json';p.write_text(json.dumps({'Title':'数字锁相','Experiment':'延迟比较'},ensure_ascii=False),encoding='utf-8-sig')
            with patch.object(m,'run_novelty_check',return_value=dict(search_status='complete')) as fn,contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(m.main(['--idea','ignored','--idea-file',str(p)]),0)
            self.assertEqual(fn.call_args.args[0],'数字锁相. 延迟比较')
    def test_bad_idea_file_exit_two(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('NOVELTY_TEST_TMP')) as td:
            for body in ['{','[]','{}','{"Title":5}']:
                p=pathlib.Path(td)/'idea.json';p.write_text(body,encoding='utf-8')
                with self.subTest(body=body),contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as cm:m.main(['--idea-file',str(p)])
                    self.assertEqual(cm.exception.code,2)

if __name__=='__main__':
    unittest.main(verbosity=2)
