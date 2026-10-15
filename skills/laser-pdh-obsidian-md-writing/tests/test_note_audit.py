"""Local-only Markdown fixtures; no vault edits."""
import importlib.util
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

SCRIPTS=Path(__file__).parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
spec=importlib.util.spec_from_file_location('telemetry_note_audit',SCRIPTS/'audit_laser_pdh_md.py')
audit=importlib.util.module_from_spec(spec); spec.loader.exec_module(audit)
HEADER='---\ncssclasses: [laser-pdh-note]\nproject: Laser_PDH_Study\n---\n'


def note(root,text=''):
    p=root/'笔记.md'; p.write_text(HEADER+text,encoding='utf-8'); return p


def test_existing_embedded_image_is_not_note_link(tmp_path):
    (tmp_path/'局部图.png').write_bytes(b'fixture')
    p=note(tmp_path,'![[局部图.png|600]]\n')
    issues={}; audit.audit_file(p,set(),issues,tmp_path); audit.audit_schematic_images(p,issues,tmp_path)
    assert not issues


def test_missing_embedded_image_is_reported(tmp_path):
    p=note(tmp_path,'![[missing.png]]\n'); issues={}
    audit.audit_schematic_images(p,issues,tmp_path)
    assert issues['LOCAL_IMAGE_MISSING']


def test_wikilink_relative_vault_and_basename_resolution(tmp_path):
    sub=tmp_path/'目录'; sub.mkdir(); (sub/'目标.md').write_text('target',encoding='utf-8')
    p=note(tmp_path,'[[目录/目标#标题]] [[目标]]')
    issues={}; audit.audit_file(p,set(),issues,tmp_path)
    assert not issues


def test_real_broken_wikilink_reported(tmp_path):
    p=note(tmp_path,'[[不存在]]'); issues={}; audit.audit_file(p,set(),issues,tmp_path)
    assert issues['BROKEN_WIKILINKS']


@pytest.mark.parametrize('newline',['\n','\r\n'])
def test_nested_fences_not_markdown_or_mermaid(tmp_path,newline):
    body='````text\n# not a heading\n[[missing]]\n```mermaid\nA-->B\n```\n````\n'
    p=note(tmp_path,body.replace('\n',newline)); issues={}
    audit.audit_file(p,set(),issues,tmp_path)
    assert not issues
    assert audit.iter_mermaid_blocks(p.read_text(encoding='utf-8'))==[]


def test_tilde_mermaid_and_unclosed_fence(tmp_path):
    assert audit.iter_mermaid_blocks('~~~mermaid\nflowchart LR\nA-->B\n~~~')==[(1,'flowchart LR\nA-->B')]
    p=note(tmp_path,'```text\nunfinished'); issues={}; audit.audit_file(p,set(),issues,tmp_path)
    assert issues['UNCLOSED_FENCE']


def viewer(root,source='flowchart LR\nA-->B'):
    assets=root/'assets'/'中文路由'; assets.mkdir(parents=True)
    mmd=assets/'one.mmd'; mmd.write_text(source,encoding='utf-8')
    html=assets/'one.html'
    html.write_text('<button>放大</button><button>缩小</button><button>重置</button>'
                    '<a href="one.mmd">源</a><pre id="diagram-source">'+source+'</pre><script>/*fixture*/</script>',encoding='utf-8')
    return mmd,html


def test_single_file_audits_linked_assets_only(tmp_path):
    mmd,html=viewer(tmp_path)
    p=note(tmp_path,'```mermaid\n'+mmd.read_text()+'\n```\n[图源](assets/中文路由/one.mmd) [查看](assets/中文路由/one.html)')
    (tmp_path/'无关坏笔记.md').write_text('[[broken]]',encoding='utf-8')
    legacy=tmp_path/'_mermaid'; legacy.mkdir(); (legacy/'unrelated.mmd').write_text('bad',encoding='utf-8')
    with patch.object(sys,'argv',['audit','--root',str(tmp_path),'--file',str(p)]):
        assert audit.main()==0
    html.write_text(html.read_text().replace('重置','无按钮'),encoding='utf-8')
    with patch.object(sys,'argv',['audit','--root',str(tmp_path),'--file',str(p)]):
        assert audit.main()==1


def test_viewer_source_mismatch(tmp_path):
    mmd,html=viewer(tmp_path); mmd.write_text('flowchart LR\nA-->C',encoding='utf-8')
    issues={}; audit.audit_mermaid_html_viewer(html,issues)
    assert issues['MERMAID_SOURCE_MISMATCH']


def test_inline_source_mismatch(tmp_path):
    viewer(tmp_path)
    p=note(tmp_path,'```mermaid\nflowchart LR\nA-->C\n```\n[源](assets/中文路由/one.mmd)')
    issues={}; audit.audit_markdown_mermaid(p,issues)
    assert issues['MERMAID_SOURCE_MISMATCH']


def test_missing_viewer_dependency(tmp_path):
    mmd,html=viewer(tmp_path); html.write_text(html.read_text()+'<script src="missing.js"></script>',encoding='utf-8')
    issues={}; audit.audit_mermaid_html_viewer(html,issues)
    assert issues['MERMAID_LINK_TARGET']


def test_fenced_example_images_and_links_are_ignored(tmp_path):
    p=note(tmp_path,'```md\n![[absent.png]]\n[x](no.mmd)\n```')
    issues={}; audit.audit_schematic_images(p,issues,tmp_path); audit.audit_markdown_mermaid(p,issues)
    assert not issues


def test_repeat_file_and_legacy_project_entry(tmp_path):
    p=note(tmp_path); q=tmp_path/'second.md'; q.write_text(HEADER,encoding='utf-8')
    with patch.object(sys,'argv',['audit','--root',str(tmp_path),'--file',str(p),'--file',str(q)]):
        assert audit.main()==0
    with patch.object(sys,'argv',['audit','--root',str(tmp_path),'--project','Laser_PDH_Study']):
        assert audit.main()==0
