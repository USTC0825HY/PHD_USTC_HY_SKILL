import importlib.util
from pathlib import Path
import pytest

spec=importlib.util.spec_from_file_location('closure_dimensions',Path(__file__).parents[1]/'scripts/audit_chain_inputs.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)


def test_missing_sources_distinct_from_pdf(tmp_path):
    board={'id':'SRC'}
    sources=[{'id':'v1','board_id':'SRC','pdf':str(tmp_path/'missing.pdf')}]
    result=mod.summarize_board(board,sources,'v1',[])
    assert result['source_availability']=='missing_sources'
    (tmp_path/'missing.pdf').write_bytes(b'%PDF-1.4 fixture, not reviewed')
    result=mod.summarize_board(board,sources,'v1',[])
    assert result['source_availability']=='schematic_available_unreviewed'
    assert result['status'].startswith('E0')
    assert not result.get('net_count')


@pytest.mark.parametrize('kind',['board_signal','clock_reference','power_rail','ground_return'])
def test_non_fpga_chain_does_not_require_port(tmp_path,kind):
    registry={'edges':[], 'chains':[{'id':'C1','kind':kind,'path':['A','B'],
        'trace_direction':'sink_to_source','signal_direction':'A_to_B',
        'verification':{'continuity':{'status':'pending'}},
        'segments':[{'board_id':'A','status':'硬件禁用','assembly':{'marker':'TSD','state':'unknown'},'translator':{'OE':'disabled','DIR':'B_to_A'}}]}]}
    _,chains=mod.annotate_topology(registry,[{'id':'A','status':'E1'},{'id':'B','status':'E1'}])
    c=chains[0]
    assert c['rtl_xdc_requirement']=='not_applicable'
    assert c['signal_direction']=='A_to_B'
    assert c['segments'][0]['status']=='硬件禁用'
    assert c['verification']['continuity']['status']=='pending'
    assert c['preflight_status']=='跨板待确认'


@pytest.mark.parametrize('kind',['fpga_control','status_return'])
def test_fpga_control_and_return_keep_digital_requirement(kind):
    _,chains=mod.annotate_topology({'edges':[],'chains':[{'id':'C','kind':kind,'path':['A']}]},[{'id':'A','status':'E1'}])
    assert chains[0]['rtl_xdc_requirement']=='required'


def test_closed_edge_without_mapping_is_rejected():
    registry=mod.empty_registry()
    registry['boards']=[{'id':'A'},{'id':'B'}]
    registry['edges']=[{'id':'E','from':'A','to':'B','type':'board_signal','status':'已闭环'}]
    with pytest.raises(ValueError,match='connector_mapping_evidence'):
        mod.validate_registry(registry)


@pytest.mark.parametrize('status',['NC','硬件禁用','方向冲突'])
def test_unavailable_branch_is_not_promoted_by_preflight(status):
    registry={'edges':[], 'chains':[{'id':'C','kind':'board_signal','path':['A'],
        'segments':[{'board_id':'A','status':status,'verification':{'assembly':{'status':'pending'}}}]}]}
    _,chains=mod.annotate_topology(registry,[{'id':'A','status':'E1'}])
    assert chains[0]['segments']==registry['chains'][0]['segments']
    assert chains[0]['preflight_status']!='已闭环'


def test_report_does_not_overwrite_registry(tmp_path,monkeypatch):
    import json, sys
    registry=mod.empty_registry(); registry['boards']=[{'id':'A'}]
    p=tmp_path/'registry.json'; p.write_text(json.dumps(registry),encoding='utf-8'); before=p.read_bytes()
    monkeypatch.setattr(sys,'argv',['audit','--boards-file',str(p),'--output',str(p)])
    assert mod.main()==2
    assert p.read_bytes()==before
