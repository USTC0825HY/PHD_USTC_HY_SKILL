#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在 --root 下创建 鉴定件/加强件 两大骨架（板组→器件→指标空夹 + 各级 INDEX.md）。
幂等：已存在的目录/文件跳过；绝不删除任何内容；只在本脚本创建的两大根内操作。
"""
import argparse
from pathlib import Path

from taxonomy import CAMPAIGNS, DEVICES, GROUPS, INDICATORS, INTERFACES, INDICATOR_REMARKS, REWORK_BOUNDARY

from layouts import detect_layout, probe


def campaign_index(campaign: str) -> str:
    legacy = {
        "加强件": "I:\\CW_Data\\513_CW_jiaqiang",
        "鉴定件": "I:\\CW_Data\\513_CW_DATA_jianding",
    }[campaign]
    rework = ("\n- 改焊分界 **%s**：仅为历史批次参考；实际改焊状态填写于 _session.md，不由日期自动推断。\n" % REWORK_BOUNDARY
              if campaign == "加强件" else "\n- 鉴定件是否改焊以本板记录为准。\n")
    return f"""# {campaign} 数据根 INDEX

目录规范：laser-cw-data-pipeline/references/data-organization-spec.md（v1.0，2026-09-28）。
数据链：`<板组>\\<器件>\\<NN_指标>\\<接口>\\<YYYYMMDD_HHMM>\\{{raw\\, results\\, _session.md}}`；raw 只读；results 只收 `run_*` 分析目录。
- 本根只收新采集/新分析；**存量数据仍在旧根原地不动**：`{legacy}\\`（映射见 legacy-mapping.md 与本根器件 INDEX 的存量索引节）。
{rework.strip()}
## 板组

| 板组 | 器件 |
|---|---|
| SZSD | {", ".join(DEVICES["SZSD"])} |
| YCQD | {", ".join(DEVICES["YCQD"])} |

新增指标/接口必须先扩展规范枚举（taxonomy.py / data-organization-spec.md）再建目录；落盘新会话后建议运行 `audit_tree.py`。
"""


def device_index(campaign: str, group: str, device: str) -> str:
    inds = INDICATORS[device]
    rows = "\n".join(
        "| %s | %s |" % (i, INDICATOR_REMARKS.get(i, "")) for i in inds)
    ifs = "、".join(INTERFACES[device])
    return f"""# {device} 数据 INDEX（{campaign}/{group}）

## 指标

| 指标夹 | 说明 |
|---|---|
{rows}

## 合法接口名（闭集）

{ifs}

## 会话规范

新测试：在本页指标夹下建 `<接口>\\<YYYYMMDD_HHMM>\\raw\\`，复制规范附录 B 的 `_session.md` 模板填写；分析输出去同级 `results\\`。
隔离度等多口联测以驱动口建接口目录，`_session.md` 记录观测口。

## 存量数据索引（旧根映射，人工确认后填写）

_（待 legacy-mapping CSV 确认后并入：旧路径 → 本器件指标/接口/会话日期）_
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", required=True, type=Path, help="I:\\CW_Data 之类的父目录")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    root: Path = args.root.resolve()
    if probe(root)["status"] == "exists":
        snapshot_roots = ("513_CW_DATA_jianding", "513_CW_jiaqiang")
        if root.name in snapshot_roots or any((root / name).exists() for name in snapshot_roots):
            ap.error("contains snapshot/legacy campaign roots; choose a separate explicit session-v1 root")
    created_dirs = created_files = 0
    for campaign in CAMPAIGNS:
        croot = root / campaign
        for group in GROUPS:
            for device in DEVICES[group]:
                for ind in INDICATORS[device]:
                    d = croot / group / device / ind
                    if not d.exists():
                        created_dirs += 1
                        if not args.dry_run:
                            d.mkdir(parents=True, exist_ok=True)
        for group in GROUPS:
            f = croot / group / "INDEX.md"
            if not f.exists():
                created_files += 1
                if not args.dry_run:
                    f.parent.mkdir(parents=True, exist_ok=True)
                    f.write_text(f"# {group} 板组\n\n器件：{', '.join(DEVICES[group])}。\n", encoding="utf-8")
        for group in GROUPS:
            for device in DEVICES[group]:
                f = croot / group / device / "INDEX.md"
                if not f.exists():
                    created_files += 1
                    if not args.dry_run:
                        f.write_text(device_index(campaign, group, device), encoding="utf-8")
        f = croot / "INDEX.md"
        if not f.exists():
            created_files += 1
            if not args.dry_run:
                f.write_text(campaign_index(campaign), encoding="utf-8")
    verb = "DRY-RUN would create" if args.dry_run else "created"
    print(f"{verb}: {created_dirs} dirs, {created_files} INDEX files under {root}")


if __name__ == "__main__":
    main()
