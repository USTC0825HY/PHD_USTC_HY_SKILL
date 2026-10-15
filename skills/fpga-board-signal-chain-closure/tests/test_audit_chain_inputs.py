from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "audit_chain_inputs.py"
SKILL_ROOT = Path(__file__).parents[1]


def write_pst(directory: Path) -> None:
    directory.mkdir()
    (directory / "pstxnet.dat").write_text(
        "PSTWRITER test\nNET_NAME\n'NET_A';\n'root';\nNODE_NAME D1 A1\n'BALL';\nNODE_NAME X1 1\n'CONTACT';\n",
        encoding="utf-8",
    )
    (directory / "pstxprt.dat").write_text("D1 'FPGA';\nX1 'CONN';\n", encoding="utf-8")
    (directory / "pstchip.dat").write_text("primitive 'FPGA'\nVALUE='xc7';\n", encoding="utf-8")


def run_tool(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, check=False)


def test_legacy_three_board_call_still_works(tmp_path: Path) -> None:
    boards = []
    for name in ("szsd", "backplane", "child"):
        board = tmp_path / name
        write_pst(board)
        boards.append(board)
    xpr = tmp_path / "demo.xpr"
    xpr.write_text(
        """<Project><Configuration><Option Name='Part' Val='xc7demo'/></Configuration>
        <FileSets><FileSet Name='sources_1' Type='DesignSrcs'><Config><Option Name='TopModule' Val='top'/></Config></FileSet>
        <FileSet Name='constrs_1' Type='Constrs'><File Path='$PSRCDIR/constrs_1/top.xdc'><FileInfo><Attr Name='UsedIn' Val='synthesis'/></FileInfo></File></FileSet></FileSets></Project>""",
        encoding="utf-8",
    )
    xdc = tmp_path / "top.xdc"
    xdc.write_text("set_property PACKAGE_PIN A1 [get_ports sig]\nset_property IOSTANDARD LVCMOS18 [get_ports sig]\n", encoding="utf-8")
    output = tmp_path / "out.json"
    result = run_tool(
        "--szsd-pst-dir", str(boards[0]), "--backplane-pst-dir", str(boards[1]),
        "--child-pst-dir", str(boards[2]), "--xpr", str(xpr), "--xdc", str(xdc),
        "--query-net", "NET_A", "--output", str(output),
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["schema"].endswith("preflight-v2")
    assert data["fpga_implementation"]["xpr"]["top"] == "top"
    assert data["fpga_implementation"]["xpr"]["part"] == "xc7demo"
    assert data["fpga_implementation"]["xdc"]["package_pin_count"] == 1
    assert [board["label"] for board in data["boards"]] == ["SZSD", "backplane", "child"]
    assert all(board["queries"][0]["status"] == "found" for board in data["boards"])
    assert "no cross-board continuity" in data["boundary"].lower()


def test_v2_registry_keeps_versions_separate_and_models_power(tmp_path: Path) -> None:
    complete = tmp_path / "complete"
    write_pst(complete)
    pdf = tmp_path / "pz.pdf"
    pdf.write_text("pin evidence only", encoding="utf-8")
    dsn = tmp_path / "error.dsn"
    dsn.write_text("dsn only", encoding="utf-8")
    registry = {
        "schema": "fpga-board-signal-chain-closure/board-registry-v2",
        "boards": [
            {"id": "SZSD", "role": "controller", "selected_evidence_set": "szsd-public"},
            {"id": "BASE", "role": "interconnect", "selected_evidence_set": "base-public"},
            {"id": "POWER", "role": "power_source", "selected_evidence_set": "power-public"},
            {"id": "YCQD", "role": "function", "selected_evidence_set": "ycqd-public"},
            {"id": "PZ", "role": "frequency_synthesis", "selected_evidence_set": "pz-pdf"},
            {"id": "LOCK_DRIVE", "role": "lock_drive"},
            {"id": "ERROR_DETECT", "role": "error_detection", "selected_evidence_set": "error-dsn"},
        ],
        "evidence_sets": [
            {"id": "szsd-public", "board_id": "SZSD", "pst_dir": str(complete), "selected": True},
            {"id": "szsd-alternate", "board_id": "SZSD", "pst_dir": str(tmp_path / "unused"), "selected": False},
            {"id": "base-public", "board_id": "BASE", "pst_dir": str(complete), "selected": True},
            {"id": "power-public", "board_id": "POWER", "pst_dir": str(complete), "selected": True},
            {"id": "ycqd-public", "board_id": "YCQD", "pst_dir": str(complete), "selected": True},
            {"id": "ycqd-internal", "board_id": "YCQD", "pst_dir": str(tmp_path / "unused2"), "selected": False},
            {"id": "pz-pdf", "board_id": "PZ", "pdf": str(pdf), "selected": True},
            {"id": "error-dsn", "board_id": "ERROR_DETECT", "dsn": str(dsn), "selected": True},
        ],
        "edges": [{"id": "POWER_BASE", "from": "POWER", "to": "BASE", "type": "power_rail", "connector_mapping_evidence": []}],
        "chains": [
            {"id": "SZSD_BASE_POWER", "kind": "fpga_control", "path": ["SZSD", "BASE", "POWER"]},
            {"id": "SZSD_BASE_YCQD", "kind": "fpga_control", "path": ["SZSD", "BASE", "YCQD"]},
            {"id": "SZSD_BASE_PZ", "kind": "fpga_control", "path": ["SZSD", "BASE", "PZ"]},
            {"id": "YCQD_BASE_PZ", "kind": "board_signal", "path": ["YCQD", "BASE", "PZ"]},
            {"id": "POWER_BASE_ERROR", "kind": "power_rail", "path": ["POWER", "BASE", "ERROR_DETECT"]},
        ],
    }
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    output = tmp_path / "out.json"
    result = run_tool("--boards-file", str(registry_path), "--output", str(output))
    assert result.returncode == 0, result.stderr
    data = json.loads(output.read_text(encoding="utf-8"))
    board = {item["id"]: item for item in data["boards"]}
    chain = {item["id"]: item for item in data["chains"]}
    assert board["PZ"]["role"] == "frequency_synthesis"
    assert board["LOCK_DRIVE"]["role"] == "lock_drive"
    assert board["PZ"]["status"].startswith("E0")
    assert board["PZ"]["source_availability"] == "schematic_available_unreviewed"
    assert board["ERROR_DETECT"]["source_availability"] == "native_source_available_unreviewed"
    assert "人工核图" in chain["SZSD_BASE_PZ"]["preflight_status"]
    assert board["ERROR_DETECT"]["status"].startswith("E0")
    assert [item["id"] for item in board["SZSD"]["evidence_sets"] if item["selected"]] == ["szsd-public"]
    assert [item["id"] for item in board["YCQD"]["evidence_sets"] if item["selected"]] == ["ycqd-public"]
    assert chain["POWER_BASE_ERROR"]["rtl_xdc_requirement"] == "not_applicable"
    assert chain["SZSD_BASE_POWER"]["rtl_xdc_requirement"] == "required"
    assert "ERROR_DETECT" in chain["POWER_BASE_ERROR"]["path"]
    assert [segment["board_id"] for segment in chain["POWER_BASE_ERROR"]["segments"]] == ["POWER", "BASE", "ERROR_DETECT"]
    assert all(segment["generated_placeholder"] for segment in chain["POWER_BASE_ERROR"]["segments"])
    assert any(point.get("board_id") == "PZ" for point in data["unclosed_points"])
    assert any(point.get("edge_id") == "POWER_BASE" for point in data["unclosed_points"])


def test_conflicting_evidence_selection_is_rejected(tmp_path: Path) -> None:
    registry = {
        "schema": "fpga-board-signal-chain-closure/board-registry-v2",
        "boards": [{"id": "SZSD", "selected_evidence_set": "a"}],
        "evidence_sets": [
            {"id": "a", "board_id": "SZSD", "selected": True},
            {"id": "b", "board_id": "SZSD", "selected": True},
        ],
        "edges": [],
        "chains": [],
    }
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    result = run_tool("--boards-file", str(registry_path), "--output", str(tmp_path / "out.json"))
    assert result.returncode == 2
    assert "多个selected证据集" in result.stderr


def test_skill_assets_cover_disabled_conflict_and_reporting_contract() -> None:
    skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    topology = (SKILL_ROOT / "references" / "multi-board-topology.md").read_text(encoding="utf-8")
    report = (SKILL_ROOT / "assets" / "signal_chain_report.table.md").read_text(encoding="utf-8")
    combined = skill + topology + report
    for token in ("D120", "OE", "DIR", "TSD*", "DNP", "NC", "方向冲突", "跨板待确认"):
        assert token in combined
    for classification in ("必需控制", "硬件默认", "可选功能", "状态输出"):
        assert classification in combined
    for section in ("## Conflicts", "## Unclosed points", "## Physical checks"):
        assert section in report
