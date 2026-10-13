#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描旧数据根，生成 旧路径→新规范位置 的映射候选 CSV（草稿，须人工确认）。
只读：绝不写入旧根。用法：
  make_legacy_map.py --old-root I:\\CW_Data\\513_CW_jiaqiang --campaign 加强件 --out map_jiaqiang.csv
"""
import argparse
import csv
import re
from pathlib import Path

from taxonomy import DEVICES, GROUPS, INDICATORS, INTERFACES
from layouts import LAYOUTS, detect_layout, probe, walk
from evidence_paths import inside, mapped_path, write_csv, mapping_status

DEV_KEYS = [
    ("ADG526_AD677", ("adg526", "addr_", "yaoce")),
    ("AD2208", ("ad2208", "yb2208", "2208")),
    ("DA9726", ("da9726", "9726")),
    ("AD9245", ("ad9245", "9245")),
    ("DA766", ("da766", "766")),
    ("AD677", ("ad677", "677")),
    ("AD128", ("ad128", "adc128")),
    ("TLV2548", ("tlv2548",)),
    ("GTH_RF4", ("gth", "5ghz_linerate", "rf_ref", "rf_out", "rfout")),
    ("FREQ_COUNTER", ("频率计数器", "counter")),
    ("ADG526_AD677", ("addr_", "遥测", "adg526", "yaoce")),
]

IND_KEYS = [
    (re.compile(r"sfdr", re.I), "Sfdr"),
    (re.compile(r"inl", re.I), "InlDnl"),
    (re.compile(r"isolation|隔离", re.I), "Isolation"),
    (re.compile(r"phase_noise|相噪|_pn-|pn-500", re.I), "PhaseNoise"),
    (re.compile(r"phase_bandwidth|bode|传输延迟|delay", re.I), "PhaseBandwidth"),
    (re.compile(r"inputpower|input_power|power_sweep|power_scale", re.I), "DynamicRange"),
    (re.compile(r"frequencyresponse|input_frequency|input_freq|_freq|frequency_sweep", re.I), "FreqBandwidth"),
    (re.compile(r"scale|kedu", re.I), "Scale"),
    (re.compile(r"noise|噪声", re.I), "Noise"),
    (re.compile(r"output_voltage|output_amp|outputvolt", re.I), "OutputVoltage"),
    (re.compile(r"时钟|clocksource|clk_test", re.I), "ClockSource"),
    (re.compile(r"秒稳|稳定度", re.I), "FreqStability"),
    (re.compile(r"串扰|crosstalk", re.I), "ChannelCrosstalk"),
    (re.compile(r"telemetry|遥测|码值", re.I), "TelemetryCodes"),
]

IF_RES = [
    re.compile(r"(ADC\d+)_JG(\d+)", re.I),
    re.compile(r"(?:adc|ch)\d?_?(jg\d+)", re.I),
    re.compile(r"\b(JG\d{2})\b"),
    re.compile(r"\b(X11-\d|X77-\d|X1[0-3]G?|X[79]G?|X10|X1G|X2G|X3G|X4G|X3|X13)\b"),
    re.compile(r"\b(CH[1-8])\b", re.I),
    re.compile(r"\b(SIG_IN[1-8])\b", re.I),
    re.compile(r"\b(ADDR_[0-9A-Fa-f]{2})\b"),
]
DATE_RE = re.compile(r"(20\d{6})(?:_)?(\d{4,6})?")
SHORTDATE_RE = re.compile(r"gaihan(?:qian|hou)_(20\d{6})|(?:^|_)(0[19]\d{2})(?:_|$)")


def norm_if(dev: str, raw: str | None) -> str | None:
    if not raw:
        return None
    s = raw.upper().replace('-', '_')
    valid = INTERFACES[dev]
    exact = [v for v in valid if v.upper().replace('-', '_') == s]
    if len(exact)==1: return exact[0]
    # A full conflicting label must not collapse to its ADC prefix.
    if re.fullmatch(r'ADC\d+_JG\d+', s): return None
    candidates = [v for v in valid if s in v.upper().replace('-', '_').split('_')]
    return candidates[0] if len(candidates)==1 else None


def classify(rel: Path):
    pstr = str(rel).replace("\\", "/")
    low = pstr.lower()
    dev = None
    for d, keys in DEV_KEYS:
        if any(k in low for k in keys):
            dev = d
            break
    ind_hint = None
    for rx, name in IND_KEYS:
        if rx.search(pstr):
            ind_hint = name
            break
    ifc = None
    for rx in IF_RES:
        m = rx.search(pstr)
        if m:
            ifc = m.group(0) if rx is IF_RES[0] else (m.group(1) if m.lastindex else m.group(0))
            break
    # Resolve separated labels without discarding contradictory channel information.
    adcs = set(re.findall(r'ADC\d+', pstr, re.I))
    jgs = set(re.findall(r'JG\d+', pstr, re.I))
    if adcs and jgs:
        ifc = '_'.join((next(iter(adcs)), next(iter(jgs)))) if len(adcs)==len(jgs)==1 else '|'.join(sorted(adcs | jgs))
    device_hits = {d for d,keys in DEV_KEYS if any(k in low for k in keys)}
    if 'ADG526_AD677' in device_hits: device_hits.discard('AD677')
    if len(device_hits)>1: dev = None
    date = None
    m = next((DATE_RE.fullmatch(part) for part in reversed(pstr.split("/")) if re.fullmatch(r"20\d{6}_\d{4}(?:\d{2})?", part)), None)
    if m:
        date = m.group(1) + ("_" + m.group(2)[:4] if m.group(2) else "")
    else:
        m2 = SHORTDATE_RE.search(pstr)
        if m2:
            date = (m2.group(1) or ("2026" + m2.group(2))) + "_0000"
    return dev, ind_hint, ifc, date



def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--old-root", required=True, type=Path)
    ap.add_argument("--campaign", required=True, choices=("鉴定件", "加强件"))
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--max-depth", type=int, default=8)
    ap.add_argument("--layout", choices=LAYOUTS, default="auto")
    ap.add_argument("--mapping", type=Path, help="approved directory CSV; v2 uses no guessed targets")
    args = ap.parse_args()
    old = args.old_root.resolve()
    if inside(args.out, old) or (args.mapping and args.out.resolve() == args.mapping.resolve()):
        ap.error("output cannot enter source root or overwrite mapping")
    try:
        layout = detect_layout(old, args.layout)
    except ValueError as exc:
        ap.error(str(exc))
    rules = []
    mapping_notes = []
    if args.mapping:
        with args.mapping.open(encoding="utf-8-sig", newline="") as stream:
            for row in csv.DictReader(stream):
                if row.get("库") and row["库"] != ("JD" if args.campaign == "鉴定件" else "JQ"):
                    continue
                source = row.get("现路径", row.get("old", ""))
                target = row.get("目标路径", row.get("new", ""))
                state = mapping_status(row)
                if state not in ('OK','confirmed','已确认'):
                    mapping_notes.append({'old':source,'status':state or '未声明','reason':'未确认映射，不生成批准目标'})
                    continue
                if not source or not target: ap.error('confirmed mapping requires source and target')
                match = row.get('match', 'exact') or 'exact'
                if match not in ('exact','prefix'): ap.error('mapping match must be exact or prefix')
                rules.append({'old':source, 'new':target, 'match':match})
    errors, rows = [], []
    group_of = {d:g for g in GROUPS for d in DEVICES[g]}
    for folder, dirs, files in walk(old, errors):
        rel=folder.relative_to(old)
        if len(rel.parts)>args.max_depth or not files:
            continue
        dev,hint,ifc,date=classify(rel)
        interface = norm_if(dev,ifc) if dev else None
        target, matched = mapped_path(str(rel), rules)
        note="已确认映射；执行前仍须核对冲突、范围和日志" if matched else "未提供已确认映射；保留现位置"
        if ifc and not interface: note += '；接口冲突或不明确，禁止按前缀替换：'+ifc
        suggestion=str(old/target) if matched else ""
        if layout=="session-v1" and not matched and dev and hint:
            indicator=next((i for i in INDICATORS[dev] if i.endswith("_"+hint)), "")
            if indicator and interface and date:
                suggestion=str(Path(args.campaign)/group_of[dev]/dev/indicator/interface/date)
                note="候选分类；不得作为已确认移动指令"
        rows.append({"旧路径":str(folder),"器件":dev or "","指标提示":hint or "","接口":ifc or "","会话日期":date or "","置信度":"EXPLICIT_MAP" if matched else "ADVISORY","建议新路径":suggestion,"备注":note,"布局":layout,"源核验":probe(folder)["status"],"目标核验":probe(suggestion)["status"] if matched else "未核验"})
    for issue in errors:
        rows.append({"旧路径":issue["path"],"备注":issue["error"],"源核验":"inaccessible","布局":layout})
    fields=["旧路径","器件","指标提示","接口","会话日期","置信度","建议新路径","备注","布局","源核验","目标核验"]
    write_csv(args.out, rows, fields)
    print(f"rows={len(rows)} errors={len(errors)} unconfirmed_mappings={len(mapping_notes)} layout={layout}; dry-run only")
    for item in mapping_notes: print(item)
    return 2 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
