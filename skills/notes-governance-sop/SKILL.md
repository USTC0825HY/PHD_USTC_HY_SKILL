---
name: notes-governance-sop
description: Organize Obsidian note folders into stable multi-level taxonomy with deduplication, frontmatter normalization, and Base/SQLite indexing. Use when a folder is messy, has repeated notes, weak categorization, or needs reusable governance assets (manifest, db, .base, report).
---

# Notes Governance SOP

1. Define target root and run baseline scan.
- Count files, markdown notes, directory distribution.
- Detect exact duplicates by hash and title collisions.

2. Build target taxonomy first.
- Create standard top-level buckets (management + business buckets).
- Create second-level standard subcategories per domain.
- Migrate files with deterministic path/name rules.
- Write migration manifest CSV.

2.5 Extract reusable notes from project folders (copy mode).
- Select reusable technical notes from project-specific directories.
- Copy (do not move) into target skill-knowledge folders with source-trace subfolder (for example `μ子成像提炼`).
- Deduplicate by body hash before copying.
- Write extraction manifest CSV.

3. Repair links after renames.
- Rebuild `rename_manifest.csv` if needed (for reruns).
- Update wikilinks/markdown links that still reference old names.
- Prefer path-aware replacements; avoid ambiguous global basename replacement.

4. Deduplicate with traceability.
- Prefer canonical file by stable path rule.
- Move duplicates to recycle/archive folder (or delete by policy).
- Write duplicate manifest CSV.

5. Normalize note metadata.
- Ensure frontmatter keys: title, category, subcategory, template, status, created, updated, tags.
- Backfill missing values from path rules.
- Keep body content unchanged.

6. Build governance assets.
- SQLite index table for notes and metadata.
- CSV export from SQLite.
- Obsidian `.base` file with views:
  - all notes
  - by category
  - by subcategory
  - recycle/duplicate review
- missing metadata review
- Generate a markdown report.

7. Final polish.
- Manually refine high-risk misclassified notes.
- Log manual moves in final polish manifest.
- Rebuild DB/CSV/Base and re-check constraints.

8. Acceptance checks.
- Duplicate groups in main scope = 0.
- Missing subcategory in main scope = 0.
- Base view opens without YAML errors.
- Renamed-link stale references = 0 (for known rename patterns).
- Manifests exist and are non-empty when changes happened.

## Output Contract

Always produce these artifacts under `<root>/00_知识管理`:
- `*_manifest.csv` files (migration/dedupe/final-polish)
- extraction manifest (for cross-project copy operations)
- `rename_manifest.csv` (and keep it consistent with current files)
- `*_notes.db`
- `*_notes_index.csv`
- `*.base`
- `00_整理报告.md`
- `*全流程*.md` implementation summary

## Practical Notes

- Do not rewrite note bodies unless explicitly requested.
- Prefer deterministic rules; avoid heuristic changes without manifest.
- If terminal encoding looks garbled, validate via file path checks and DB counts instead of console rendering.
