"""Draft traceability CSV; explicit evidence wins over path-name heuristics."""
import argparse
import csv
import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "hardware-evidence-report-sync" / "scripts"))
from evidence_paths import inside, load_mapping, probe, resolve_path, split_paths, write_csv

DEVICES = [
    (r"adg526(?:_ad677)?|addr_|yaoce", "ADG526_AD677"),
    (r"ad2208|yb2208", "AD2208"), (r"da9726|9726", "DA9726"),
    (r"ad9245|9245", "AD9245"), (r"da766|ad766|766", "DA766"),
    (r"ad677|677", "AD677"), (r"ad128|adc128", "AD128"),
    (r"tlv2548", "TLV2548"), (r"gth|rf_ref|rf_out|rfout", "GTH_RF4"),
    (r"频率计数器|freq_counter", "FREQ_COUNTER"),
]
INDICATORS = [
    (r"sfdr", "SFDR"), (r"inl", "INL/DNL"), (r"isolation|隔离", "隔离度"),
    (r"phase_noise|相噪", "相位噪声"), (r"phase_bandwidth|bode|传输延迟", "相移带宽"),
    (r"inputpower|inputpowerscale|input_power|power_sweep|power_scale", "动态范围/刻度"),
    (r"frequencyresponse|input_freq|frequency_sweep|bandwidth", "输入频率范围/3dB带宽"),
    (r"telemetry|遥测|addr_", "遥测码值"), (r"pico|250k|1hz", "输入等效噪声(PICO 1Hz)"),
    (r"ila|input_noise", "输入等效噪声(ILA)"), (r"noise|噪声", "输出噪声/噪声"),
    (r"output_voltage|output_amp|outputvolt", "输出电压范围"), (r"scale|kedu", "刻度"),
    (r"时钟|clocksource", "时钟源"), (r"秒稳|stability", "秒稳"), (r"串扰|crosstalk", "通道串扰"),
]
IF_RE = re.compile(r"(ADC\d_JG\d+|DAC\d_JG\d+|JG\d{2}|X11-[1-7]|X77-[78]|X12G|X1[03]|X[1-4]G|X[379]|SIG_IN[1-8]|ADDR_[0-9A-Fa-f]{2}|CH[1-8])(?![0-9A-Za-z])", re.I)
RUN_RE = re.compile(r"run_(20\d{6})_(\d{6})_.+$")
SESSION_RE = re.compile(r"^(20\d{6})_(\d{4})(?:\d{2})?$")
BATCH_RE = re.compile(r"^(20\d{6})_[A-Za-z].*$")

def classify(path, metadata=None, root=None, mappings=()):
    metadata = metadata or {}
    s = str(path)
    parts = re.split(r"[\\/]", s)
    run = next((RUN_RE.fullmatch(part) for part in reversed(parts) if RUN_RE.fullmatch(part)), None)
    capture = next((SESSION_RE.fullmatch(part) for part in reversed(parts) if SESSION_RE.fullmatch(part)), None)
    batch = next((BATCH_RE.fullmatch(part) for part in parts if BATCH_RE.fullmatch(part)), None)
    dev = next((name for pattern, name in DEVICES if re.search(pattern, s, re.I)), "")
    ind = next((name for pattern, name in INDICATORS if re.search(pattern, s, re.I)), "")
    interface = IF_RE.search(s)
    pre = bool(re.search(r"gaihanqian|改焊前", s, re.I))
    post = bool(re.search(r"gaihanhou|改焊后", s, re.I))
    status = ("改焊前" if pre else "改焊后") if pre != post else "待确认"
    status = metadata.get("rework_status", status)
    if status not in ("改焊前", "改焊后", "—", "待确认"):
        raise ValueError("unsupported rework_status")
    source = metadata.get("source_path", "" if run else s)
    result = metadata.get("result_path", s if run else "")
    summary = metadata.get("summary_file", "")
    def verified(candidate):
        state = resolve_path(str(candidate), root, mappings) if root else probe(candidate)
        return state["status"] == "exists"
    results = split_paths(result)
    if len(results) == 1 and not summary:
        candidate = Path(results[0]) / "结果汇总.xlsx"
        if verified(candidate):
            summary = candidate.name
    if summary:
        candidates = split_paths(summary)
        if any(not verified(Path(item) if Path(item).is_absolute() else
                            Path(results[0]) / item if len(results) == 1 else Path(item))
               for item in candidates):
            summary = ""
    # Do not infer a sibling raw folder as the source of a run.
    acquisition = metadata.get("acquisition_date", capture.group(1) if capture else "")
    return {"器件": metadata.get("device", dev), "指标": metadata.get("indicator", ind),
            "接口": metadata.get("interface", interface.group(1).upper() if interface else ""),
            "改焊状态": status, "源数据路径": source, "分析结果路径": result,
            "关键汇总文件": summary, "_类型": "结果" if result else "源", "_日期": acquisition,
            "_采集日期": acquisition, "_处理日期": metadata.get("processing_date", run.group(1) if run else ""),
            "_批次日期": metadata.get("batch_date", batch.group(1) if batch else ""),
            "备注": (metadata.get("notes", "") + "；" if metadata.get("notes") else "") + ("改焊状态待确认；" if status == "待确认" else "") + ("源数据待清单确认；" if not source else "") + ("汇总文件待确认" if result and not summary else ""),
            "_元数据依据": metadata.get("_manifest", "路径候选，须核验")}

def read_metadata(path):
    if not path:
        return {}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = json.load(stream) if path.suffix.lower() == ".json" else list(csv.DictReader(stream))
    result = {}
    for row in rows:
        key = row.get("input_path", "")
        if not key or key in result:
            raise ValueError("manifest requires unique input_path per row")
        result[key] = {**row, "_manifest": str(path)}
    return result

def draft(paths, root=None, mappings=(), metadata=None):
    rows = []
    for line in paths:
        for value in split_paths(line):
            row = classify(Path(value), (metadata or {}).get(value), root, mappings)
            row["旧路径输入"] = value
            checks = []
            for column in ("源数据路径", "分析结果路径"):
                if not row[column]:
                    continue
                values = []
                for path in split_paths(row[column]):
                    checked = resolve_path(path, root, mappings) if root else {"display_path": path, **probe(path), "location": "unchecked_root"}
                    checks.append({"column": column, "original": path, **checked})
                    values.append(checked["display_path"])
                row[column] = "；".join(values)
            row["_路径核验"] = json.dumps(checks, ensure_ascii=False)
            if any(c["status"] != "exists" for c in checks):
                row["备注"] += "；路径未全部核验"
            if any(c["location"] == "outside_library" and c["status"] == "exists" for c in checks):
                row["备注"] += "；不在指定主库（库外路径已核验）"
            rows.append(row)
    return rows

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paths", nargs="*", default=[])
    parser.add_argument("--paths-file", type=Path)
    parser.add_argument("--campaign", choices=("鉴定件", "加强件"))
    parser.add_argument("--root", type=Path, help="library root for relative display")
    parser.add_argument("--mapping", type=Path)
    parser.add_argument("--manifest", type=Path, help="CSV/JSON with input_path and explicitly verified metadata")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    sources = [p for p in (args.paths_file, args.mapping, args.manifest) if p]
    if any(args.out.resolve() == p.resolve() for p in sources) or (args.root and inside(args.out, args.root)):
        parser.error("output must not overwrite inputs or enter the library")
    paths = list(args.paths)
    if args.paths_file:
        paths += args.paths_file.read_text(encoding="utf-8-sig").splitlines()
    metadata = read_metadata(args.manifest)
    protected = [value for line in paths for value in split_paths(line)]
    protected += [value for row in metadata.values() for column in ("source_path", "result_path", "summary_file")
                  for value in split_paths(row.get(column, ""))]
    for value in protected:
        candidate = Path(value)
        if args.root and not candidate.is_absolute():
            candidate = args.root / candidate
        if args.out.resolve() == candidate.resolve() or (candidate.is_dir() and inside(args.out, candidate)):
            parser.error("output must not overwrite an evidence file or enter an evidence directory")
    rows = draft(paths, args.root, load_mapping(args.mapping), metadata)
    if not rows:
        parser.error("no paths")
    write_csv(args.out, rows, list(rows[0]))
    print(f"rows={len(rows)} -> {args.out}; 草稿须核对采集、改焊和源数据记录")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

