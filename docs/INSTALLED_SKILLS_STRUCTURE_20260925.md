# 当前已安装个人技能库结构（2026-09-25）

来源：`C:/Users/86183/.codex/skills/` 的顶层技能目录；不计 `.system` 和插件缓存。
共 100 个顶层技能。通常每个技能以 `SKILL.md` 为入口，可有 `references/`、`scripts/`、`assets/`、`agents/openai.yaml` 等子目录。

本次将仓库原本缺少的 35 个顶层技能复制到 `skills/`，并登记在 `registry/skills.json`、`registry/skills.csv` 与 `profiles/all.json`、`profiles/codex.json`。三个 CW／仪器技能取工程维护源码，其余取当前已安装目录；缓存和字节码未纳入。原本已存在的技能目录保留，尚未逐个同步其较新本机版本。

云端总体仓库当前为 Public。其 `SECURITY.md` 与 `docs/GITHUB_UPLOAD_CHECKLIST.md` 要求未完成许可证与项目内容审查前保持 Private，因此这次只完成本地检出复制和校验，未推送到公开远端。

## Laser 专用（8）

- `laser-cw-operation-manual-writing`
- `laser-cw-qualification-test-development`
- `laser-electrical-data-analysis`
- `laser-electrical-test-report-standard`
- `laser-indicator-visio-style`
- `laser-pdh-obsidian-md-writing`
- `laser-schematic-screenshot-repair`
- `laser-test-report-writing`

## FPGA／硬件／测试上位机（26）

- `cw-dac-host-development`
- `fpga-board-signal-chain-closure`
- `fpga-cdc-reset-timing`
- `fpga-ila-debug`
- `fpga-orcad-xdc-pipeline`
- `fpga-register-command-parser`
- `fpga-rtl-code-review`
- `fpga-substitute-board-workflow-validation`
- `fpga-testbench-simulation`
- `fpga-vivado-tcl-automation`
- `gf-architect`
- `gf-plan`
- `gf-viz`
- `hardware-datasheet-to-schematic`
- `hardware-dev-router`
- `hardware-evidence-report-sync`
- `hardware-pcb-bringup-debug`
- `hardware-schematic-review`
- `host-rtl-alignment`
- `qt-cpp-host-development`
- `rtl-schematic-xdc-alignment`
- `sdg-dmm-automation`
- `vivado-analysis`
- `vivado-constraints`
- `vivado-impl`
- `vivado-synth`

## MAROC 项目适配（15）

- `maroc-evidence-ppt-sync`
- `maroc-fpga-cdc-reset-timing`
- `maroc-fpga-ila-debug`
- `maroc-fpga-register-command-parser`
- `maroc-fpga-rtl-code-review`
- `maroc-fpga-testbench-simulation`
- `maroc-fpga-vivado-tcl-automation`
- `maroc-hardware-dev-router`
- `maroc-host-rtl-alignment`
- `maroc-obsidian-md-writing`
- `maroc-ppt-debug-report`
- `maroc-ppt-group-meeting`
- `maroc-ppt-progress-summary`
- `maroc-qt-host-development`
- `maroc-rtl-schematic-xdc-alignment`

## MATLAB（6）

- `matlab-clean-code`
- `matlab-modernize-code`
- `matlab-review-code`
- `matlab-testing`
- `matlab-validate-function-arguments`
- `matlab-write-help`

## 研究与学术写作（14）

- `academic-paper-analysis-ppt`
- `benchmark-paper-template`
- `figure-designer`
- `hypothesis-generation`
- `idea-evaluator`
- `idea-generation`
- `intro-drafter`
- `novelty-assessment`
- `pre-submission-reviewer`
- `research-defense-ppt`
- `research-ideation`
- `scientific-brainstorming`
- `tech-paper-template`
- `vibe-research-workflow`

## 软件开发／云端／安全（13）

- `aspnet-core`
- `chatgpt-apps`
- `cloudflare-deploy`
- `develop-web-game`
- `gh-address-comments`
- `gh-fix-ci`
- `netlify-deploy`
- `playwright-interactive`
- `render-deploy`
- `security-best-practices`
- `security-ownership-map`
- `security-threat-model`
- `winui-app`

## 其他工具与文档（18）

- `audit-optimize-windows-performance`
- `business-trip-reimbursement-organizer`
- `codex-log-guard`
- `codex-reset-credits`
- `figma`
- `figma-implement-design`
- `imagegen`
- `jupyter-notebook`
- `linear`
- `pdf`
- `photo-person-filter`
- `qu-ai-wei`
- `screenshot`
- `speech`
- `systematic-literature-review`
- `transcribe`
- `yeet`
- `zz-academic-paper-ppt`

## 覆盖关系

| 项目 | 数量 |
|---|---:|
| 本机个人技能目录 | 100 |
| 同步前总体仓库顶层技能目录 | 88 |
| 本次新增 | 35 |
| 同步后总体仓库顶层技能目录 | 123 |
| 同步后注册表逻辑技能 | 130（含原有嵌套技能） |
