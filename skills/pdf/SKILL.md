---
name: "pdf"
description: "Apply local workspace paths and runtime discovery to PDF tasks, delegating general PDF operations to the available PDF plugin. Use this personal adapter for project-specific output rules or a basic standalone fallback when the plugin is absent; distinguish it from the same-named plugin skill."
---

# PDF workspace adapter

This personal `pdf` entry provides workspace integration, not a second copy of the plugin manual. Preserve the user's source PDFs, requested edit scope and output format.

## Resolve the workspace and execution path

1. Read the applicable project instructions and relevant memory. Follow the user's target and existing project asset locations. Temporary files belong in the project's designated task directory.
2. In `F:\01_Laser`, use `.codex_work/<date-task>/` for temporary PDFs, images and scripts. Place final files in the user-specified or existing authoritative report/research directory. If the final location cannot be inferred, label the file as a draft in the task directory rather than inventing a root-level `tmp/` or `output/`. These Laser paths do not become defaults in other projects.
3. Identify the **plugin-provided** PDF entry from the current session's discovered skills, recording its actual source/path. Read that entry completely. Do not hardcode a cache version, load an unadvertised stale cache or route back to this personal file. If the plugin is absent or not enabled in this environment, use the standalone fallback below.
4. Discovery does not prove executability. For the plugin path, locate its current runtime and required authoring hooks, including any operation-start marker. Read-only work follows the plugin's read-only rules. Once the plugin workflow is selected, a mandatory hook failure stops the affected create/edit step; do not silently bypass it through fallback and claim plugin success. Report the unavailable step and preserve the source.

## Runtime, evidence and output

- Prefer the environment's dependency-discovery capability and existing installed runtimes. Check the actual Python imports and rendering commands needed for the task; file existence alone does not prove execution.
- When the plugin is available, it owns general PDF processing, form checks and its mandatory execution/delivery contract. Project paths and preservation of valid Unicode take priority over generic plugin directory and ASCII-style defaults; this does not relax required authoring hooks or validation.
- If the plugin is absent, read [references/standalone-fallback.md](references/standalone-fallback.md) for basic extraction, creation and rendering. Do not install packages or services just to satisfy an example; report missing capabilities and use a supported narrower operation when useful.
- Keep Unicode punctuation, math symbols and Chinese characters when the font supports them. Do not replace correct characters merely to enforce ASCII. Check rendered glyphs and extractability for the requested output.
- Text extraction supports content checks, not a claim of visual correctness. When rendering is unavailable, state that layout verification was not performed. Never claim an interactive form is correctly filled solely because a page looks correct.
- Preserve source files and use a separate destination unless the user authorized overwriting. Cleanup follows project rules; do not automatically delete originals, unique intermediate evidence or recovery files.
