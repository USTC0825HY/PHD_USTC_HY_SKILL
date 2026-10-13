# Hardware Hook Library

Use the central hook layer only when a request asks to run, wrap, validate, or discover reusable scripts.

## Resolution

Resolve `<CODEX_HOME>` from the environment, falling back to the current user's `.codex` directory.

- Registry: `<CODEX_HOME>/hardware-assets/hooks/hardware-hook-registry.yaml`
- Runner: `<CODEX_HOME>/hardware-assets/hooks/invoke_hardware_hook.py`
- Guide: `<CODEX_HOME>/hardware-assets/hooks/hook-library.md`
- Run logs: `<CODEX_HOME>/hardware-assets/hook-runs`

If the registry or runner is absent, do not invent a hook command. Read and run the owning project script directly after identifying its write boundary, or report the missing dependency.

## Required Policy

1. Start with `--mode dry-run` unless the hook is an internal read-only validator.
2. Read the source script before running any `generated-output`, `project-write`, `hardware-write`, or `destructive` hook.
3. Never run `hardware-write` or `destructive` hooks automatically.
4. Keep original scripts in their project repositories. Register or reference them; do not copy them into skills.
5. Preserve the hook id, mode, run directory, stdout, stderr, and machine-readable run record as provenance.

For MAROC scenarios, prefer `maroc-hardware-dev-router/references/maroc-hook-map.md`. It is a routing map, not proof that the referenced executable registry exists.
