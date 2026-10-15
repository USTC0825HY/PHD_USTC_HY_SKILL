"""Version-2 behavior, using synthetic routes/workbooks only."""
import copy
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_routes import audit, decode_adc
from audit_workbook import audit as workbook_audit
from audit_common import address, read_json
from test_audits import graph, make_xlsx, view_manifest


def v2(root):
    m, p = graph(root)
    m['schema_version'] = p['schema_version'] = 2
    m['routes'][0].update(route_id='TM1', chain_id='ADC_A')
    m['evidence']['fit']['scope']['version'] = 'fixture-v1'
    exp = p['expected_routes'].pop('0x00')
    exp.update(chain_id='ADC_A', address='0x00')
    p['expected_routes']['TM1'] = exp
    return m, p


def codes(result):
    return {f['code'] for f in result['findings']}


def test_v2_known_route(tmp_path):
    m,p=v2(tmp_path)
    assert audit(m,p,tmp_path)[0]['status']=='passed'


def test_same_hex_different_chain_allowed(tmp_path):
    m,p=v2(tmp_path)
    second=copy.deepcopy(m['routes'][0]); second.update(route_id='TM2', chain_id='ADC_B')
    m['routes'].append(second)
    p['expected_routes']['TM2']={**p['expected_routes']['TM1'], 'chain_id':'ADC_B'}
    assert audit(m,p,tmp_path)[0]['status']=='passed'
    second['chain_id']='ADC_A'; p['expected_routes']['TM2']['chain_id']='ADC_A'
    assert 'DUPLICATE_CHANNEL_ADDRESS' in codes(audit(m,p,tmp_path)[0])


def test_unknown_address_not_invented(tmp_path):
    m,p=v2(tmp_path)
    m['routes'][0].update(address=None, chain_id=None, input=None, status='partial')
    p['expected_routes']['TM1'].update(address=None, chain_id=None, input=None)
    p['physical_inputs']={}
    result=audit(m,p,tmp_path)[0]
    assert result['status']=='needs_review'
    assert 'ADDRESS_UNCONFIRMED' in codes(result)


def test_duplicate_stable_id(tmp_path):
    m,p=v2(tmp_path); m['routes'].append(copy.deepcopy(m['routes'][0]))
    assert 'DUPLICATE_ROUTE_ID' in codes(audit(m,p,tmp_path)[0])


def test_assembly_override_is_version_and_ref_scoped(tmp_path):
    m,p=v2(tmp_path)
    m['evidence']['fit']['scope']['version']='different-board-revision'
    assert 'TSD_OVERRIDE_MISSING' in codes(audit(m,p,tmp_path)[0])


def test_connector_contact_cannot_mate_to_two_contacts(tmp_path):
    m,p=v2(tmp_path)
    p['connector_pairs'].append({'from':'j','to':'u','evidence':['pair']})
    assert 'CONNECTOR_PAIR_CONFLICT' in codes(audit(m,p,tmp_path)[0])


@pytest.mark.parametrize('wrong_pin',['B7','28'])
def test_section_or_mirrored_contact_requires_explicit_pair(tmp_path,wrong_pin):
    m,p=v2(tmp_path)
    m['nodes']['x']['pin']='A7'
    m['nodes']['wrong']={**m['nodes']['x'],'pin':wrong_pin}
    m['routes'][0]['segments'][3]['to']='wrong'
    m['routes'][0]['segments'][4]['from']='wrong'
    m['routes'][0]['source_interface']='wrong'
    assert 'UNBOUND_MARKED_COMPLETE' in codes(audit(m,p,tmp_path)[0])


def test_equal_net_names_do_not_short_boards(tmp_path):
    m,p=v2(tmp_path)
    m['nodes']['x']['net']=m['nodes']['j']['net']
    m['nodes']['u']['net']=m['nodes']['x']['net']
    m['routes'][0]['segments'][3]['kind']='net'
    assert 'CROSS_BOARD_SHORTCUT' in codes(audit(m,p,tmp_path)[0])


def test_assembly_confirmation_cannot_expand_to_other_ref(tmp_path):
    m,p=v2(tmp_path)
    m['evidence']['fit']['scope']['refs']=['R2']
    assert 'TSD_OVERRIDE_MISSING' in codes(audit(m,p,tmp_path)[0])


def test_internal_address_rejects_display_text():
    for value in ('0x05（IN5）','ADC:0x05','0x-1','0x0_5'):
        with pytest.raises(ValueError): address(value)


def workbook_v2():
    m=view_manifest(); m['schema_version']=2
    m['routes'][0].update(route_id='TM1',chain_id='ADC_A')
    m['routes'][0]['display']['address_text']='0x00（IN0）'
    m['routes'].append({'route_id':'TM2','chain_id':'ADC_B','address':'0x00','display':{}})
    for spec in m['workbook']['sheets']:
        spec.update(route_ids=['TM1'],row_bindings={'5':'TM1'})
    return m


def test_display_address_and_explicit_view_subset(tmp_path):
    source=tmp_path/'source.xlsx'
    def modify(parts):
        for name in ('sheet7','sheet42'):
            key=f'xl/worksheets/{name}.xml'
            parts[key]=parts[key].replace('<t>0x00</t>','<t>0x00（IN0）</t>')
    make_xlsx(source, modify)
    m=workbook_v2()
    result=workbook_audit(source,source,m,{'schema_version':1})
    assert result['status']=='passed', result
    m['workbook']['sheets'][0]['route_ids'].append('TM2')
    assert 'VIEW_COVERAGE' in codes(workbook_audit(source,source,m,{'schema_version':1}))


def test_swapped_binding_detected_by_signal_fields(tmp_path):
    source=tmp_path/'source.xlsx'; make_xlsx(source)
    m=workbook_v2(); m['routes'][0]['display']['address_text']='0x00'
    m['routes'][1]['display']={'address_text':'0x00','board':'WRONG','endpoint':'OTHER'}
    spec=m['workbook']['sheets'][0]; spec.update(route_ids=['TM2'],row_bindings={'5':'TM2'})
    assert 'VIEW_VALUE_MISMATCH' in codes(workbook_audit(source,source,m,{'schema_version':1}))


def test_missing_row_binding_detected(tmp_path):
    source=tmp_path/'source.xlsx'; make_xlsx(source)
    m=workbook_v2(); m['workbook']['sheets'][0]['row_bindings']={}
    assert 'VIEW_BINDING_INVALID' in codes(workbook_audit(source,source,m,{'schema_version':1}))


def test_explicit_blank_address_and_display_are_preserved(tmp_path):
    import re
    source=tmp_path/'source.xlsx'
    def modify(parts):
        for name in ('sheet7','sheet42'):
            key=f'xl/worksheets/{name}.xml'
            parts[key]=re.sub(r'<c r="[AB]5"[^>]*>.*?</c>','',parts[key])
    make_xlsx(source,modify)
    m=workbook_v2()
    m['routes'][0].update(chain_id=None,address=None)
    m['routes'][0]['display'].update(address_text=None,board=None)
    result=workbook_audit(source,source,m,{'schema_version':1})
    assert result['status']=='needs_review', result
    assert not result['errors'], result
    del m['routes'][0]['display']['address_text']
    assert 'VIEW_ADDRESS' in codes(workbook_audit(source,source,m,{'schema_version':1}))


@pytest.mark.parametrize('vref',[5,3.3])
@pytest.mark.parametrize('raw',[0,1,2048,4095])
def test_12bit_reference_and_endpoints(vref,raw):
    decoded, voltage=decode_adc(raw,12,'unipolar_binary',vref)
    assert decoded==raw
    assert voltage==pytest.approx(raw*vref/4096)


def test_template_reports_review_not_pass():
    root=Path(__file__).parents[1]/'assets'
    m=read_json(root/'manifest.v2.template.json'); p=read_json(root/'profile.v2.template.json')
    assert audit(m,p,root)[0]['status']=='needs_review'


def test_published_current_coefficients_and_roundtrip():
    import re
    content=(Path(__file__).parents[1]/'references/ycqd-20261015-case.md').read_text(encoding='utf-8')
    published=[float(x) for x in re.findall(r'\| (\d+\.\d+) \|',content)]
    params=[(.01,499,1),(.005,49.9,51000/51010),(.01,1500,100000/100051),(.01,12,100000/100051)]
    assert len(published)==4
    for shown,(rs,rg,k) in zip(published,params):
        gain=1+49400/rg; coefficient=1/(k*gain*rs)
        assert shown==pytest.approx(coefficient,rel=1e-8)
        current=.1; voltage=current*rs*gain*k
        denominator=32768 if rg in (499,49.9) else 4096
        d=voltage*denominator/5
        assert coefficient*(d*5/denominator)==pytest.approx(current)


@pytest.mark.parametrize('resistance',[0,1000,10000,100000])
def test_tt_thevenin_inverse_and_code(resistance):
    voltage=4*(resistance+10000)/(resistance+30000)
    d=voltage*32768/5
    assert 100000*d/(131072-5*d)-10000==pytest.approx(resistance,abs=1e-8)
    if resistance==10000: assert voltage==2
