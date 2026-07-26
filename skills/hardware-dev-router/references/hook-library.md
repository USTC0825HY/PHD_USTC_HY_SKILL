# Hardware Hook Library

Use the central hook layer when a request asks to run, wrap, validate, or discover reusable scripts.

## Entry Points

- Registry: `C:/Users/Administrator/.codex/hardware-assets/hooks/hardware-hook-registry.yaml`
- Runner: `C:/Users/Administrator/.codex/hardware-assets/hooks/invoke_hardware_hook.py`
- Guide: `C:/Users/Administrator/.codex/hardware-assets/hooks/hook-library.md`
- Run logs: `C:/Users/Administrator/.codex/hardware-assets/hook-runs`

## Required Policy

1. Start with `--mode dry-run` unless the hook is an internal read-only validator.
2. Read the source script before running any `generated-output`, `project-write`, `hardware-write`, or `destructive` hook.
3. Never run `hardware-write` or `destructive` hooks automatically.
4. Keep original scripts in their project repositories. Register or reference them; do not copy them into skills.
5. Preserve `hook-run.json`, `stdout.log`, and `stderr.log` as the execution record.

## Useful Commands

```powershell
python C:/Users/Administrator/.codex/hardware-assets/hooks/invoke_hardware_hook.py --list
python C:/Users/Administrator/.codex/hardware-assets/hooks/invoke_hardware_hook.py --validate-registry
python C:/Users/Administrator/.codex/hardware-assets/hooks/invoke_hardware_hook.py --hook-id asset.catalog.validate --mode dry-run
```

For MAROC-specific scenario hooks, load `C:/Users/Administrator/.codex/hardware-assets/hooks/maroc-hook-map.md`.
