"""Two supported 513 layouts; a layout is never a permission to migrate."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "hardware-evidence-report-sync" / "scripts"))
from evidence_paths import probe, walk

SNAPSHOT_CAMPAIGNS = {"鉴定件": "513_CW_DATA_jianding", "加强件": "513_CW_jiaqiang"}
LAYOUTS = ("auto", "snapshot-v2", "session-v1")
SNAPSHOT_INDICATORS = {
    "AD2208": ("01_SFDR", "02_FrequencyResponse", "03_InputPowerScale", "04_Isolation", "05_INL_DNL", "06_Noise", "07_ClockSource", "08_PhaseBandwidth"),
    "AD9245": ("01_noise", "02_FrequencyResponse", "03_InputPowerScale", "04_Isolation", "05_INL_DNL", "06_SFDR"),
    "DA766": ("01_UpdateRate", "02_PhaseNoise", "03_DCNoise", "04_OutputVoltage", "05_Isolation", "06_scale"),
    "DA9726": ("01_Linearity", "02_PhaseNoise", "03_Noise", "04_OutputVoltage", "05_Isolation", "06_scale"),
    "AD677": ("01_noise", "02_FrequencyResponse"),
}

def detect_layout(root, requested="auto"):
    state = probe(root)
    if state["status"] != "exists" or not state.get("is_dir"):
        raise ValueError("数据根不可用，待确认: " + state["status"] + " " + state["reason"])
    if requested != "auto":
        return requested
    errors = []
    first = next(walk(root, errors), None)
    if errors or first is None:
        raise ValueError("目录无法读取，待确认: " + str(errors))
    names = {p.name for p in first[1]}
    snapshot = root.name in SNAPSHOT_CAMPAIGNS.values() or bool(names & set(SNAPSHOT_CAMPAIGNS.values()))
    session = root.name in SNAPSHOT_CAMPAIGNS or bool(names & set(SNAPSHOT_CAMPAIGNS))
    if snapshot == session:
        raise ValueError("布局未知或两种布局共存，待确认；请显式指定 --layout")
    return "snapshot-v2" if snapshot else "session-v1"

def campaign_roots(root, layout, campaign=None):
    mapping = SNAPSHOT_CAMPAIGNS if layout == "snapshot-v2" else {key: key for key in SNAPSHOT_CAMPAIGNS}
    if root.name in mapping.values():
        if campaign and root.name != mapping[campaign]:
            raise ValueError("所选数据根与 --campaign 不一致")
        return [root]
    return [root / mapping[key] for key in ([campaign] if campaign else mapping)]

