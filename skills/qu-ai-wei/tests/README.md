# 当前验证规范 · 0.8.2-local.1

现行行为判据见 `eval-manifest.txt`。请用真实模型执行请求，保存请求、读取文件、执行者/模型（不可得则注明）、真实输出及独立判定依据。普通终稿无需门检、作者身份判断或报告。

- `fixtures/`、`baseline/`、`after/` 为历史样本，字节保留。文件名中的 human-stop 不代表当前任务策略。
- `history/` 保存旧测试规范和检查器，仅供追溯；旧脚本路径假设也属历史，不作为现行命令执行。
- `runs/` 保存本地版真实运行和人工复核。旧输出与新结果分开存放，不覆盖历史快照。
- `historical-hashes.json` 保护历史样本；`check-snapshot-smoke.sh` 只检查这些文件是否被改动。
- `check-runs.sh <captured-run.json>` 只检查捕获材料完整性，不能代替语义复核。
- `check-triggers.sh` 只检查描述锚点，不能证明自动发现行为。

构建和检查使用已发现的 Python 3.9+，不自动安装：

```bash
python scripts/build_flat.py
python scripts/build_flat.py --check
python tests/check_structure.py version
python tests/check_structure.py history
python tests/check_structure.py triggers
python tests/check_behavior.py tests/runs/0.8.2-local.1/captured.json
```

原 shell 入口保留，可用 `QU_AI_WEI_PYTHON` 指定解释器。`check-skills-cli-discovery.sh` 是原有外部工具检查，会调用 npx；仅在明确需要和具备环境时另行执行，本次未运行，也不将其列为语义验证。
