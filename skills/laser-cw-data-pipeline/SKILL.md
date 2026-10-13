---
name: laser-cw-data-pipeline
description: Organize and audit 513/CW qualification and strengthened-board data, recognizing the v2 snapshot library and v1 acquisition sessions. Use for directory inventories, coverage, naming, legacy path maps, or dry-run migration planning; route numerical analysis and report editing to their dedicated skills.
---

# Laser CW Data Pipeline

Select the existing layout before applying naming rules. The 513 report baseline is the v2 snapshot library; existing v1 acquisition trees remain valid. Explicit task paths win over examples and old profile defaults.

运行脚本前按 [运行时验证](../hardware-dev-router/references/runtime-validation.md) 探测实际 Python 版本和所需导入；优先复用可执行专用环境。

旧路径分类保留完整 ADCn_JGn 标识；与器件允许接口冲突时输出待确认，不按 ADC 前缀改接口。显式映射仅 status=OK/confirmed/已确认参与批准映射，草稿/拒绝/缺状态保持读取兼容但不批准；match 默认 exact。生成器始终只读建议，不执行移动。

## Directory work

Read [layout rules](references/data-organization-spec.md). Use scripts/audit_tree.py --root <dir> --layout auto --json; --layout snapshot-v2|session-v1 resolves ambiguity, and --campaign 鉴定件|加强件 limits the campaign. A root may be a library parent or one campaign. Missing/offline roots are unresolved, never invitations to scaffold.

- v2: preserve current device/batch/indicator trees and nearby results, including results inside raw, singular result and legacy isolation trees. Report compatibility and historical anomalies separately.
- v1: scripts/scaffold_tree.py --root <explicit-new-parent> --dry-run previews the acquisition skeleton. Creation requires a task requesting new directories. It refuses parents containing snapshot/legacy campaign roots.
- scripts/make_legacy_map.py --old-root <dir> --campaign <campaign> --out <csv> --layout <layout> [--mapping <csv>] only drafts mappings. v2 targets require an explicit mapping; v1 heuristic classifications remain advisory. Read [mapping and journal discipline](references/legacy-mapping.md) before moves.
- Audit returns coverage by present indicator, failed-run markers, empty directories, stray files and large-file candidates. File presence is not measurement completeness. Use requirements and report evidence to build the full expected coverage matrix.
- Raw names are evidence. Directory typo corrections are explicit per-path decisions; never apply global device/indicator substitutions to raw filenames.

## Other work

- Calculations and duplicate-content audit: [processing handoff](references/processing-mode.md), then laser-electrical-data-analysis.
- Evidence-to-report paths: hardware-evidence-report-sync, including its optional 513 reference.
- DOCX content/layout: [report handoff](references/report-format.md), then laser-test-report-writing.
- Acceptance and four-state conclusions: [verification](references/verification.md).

## Safety and runtime

Organization is zero-delete. An authorized move requires dry-run, confirmed mapping, journal written before each operation, conflict checks, accounting, resumable state and reverse journal rollback. Duplicate deletion is a separate explicitly scoped task; a past cleanup never authorizes a new deletion.

Python 3.10+ tools share read-only filesystem helpers from sibling hardware-evidence-report-sync/scripts/evidence_paths.py; install these skills together. Long/UNC paths use extended paths; bounded retries distinguish missing from inaccessible. Unreadable files make the audit incomplete.

Probe the runtime before use; the historical laser-fpga-runtime venv may be broken. Use an available Python with the required dependencies; do not rebuild environments or change global settings merely to read data.
