# Laser profile paths: validate before use

Resolve only the paths needed for the current action. Precedence is explicit task/CLI path, the existing corresponding LASER_TEST_* environment override, then `<CODEX_HOME>/laser-fpga-profile.json`; CODEX_HOME defaults to the user's `.codex` directory. Read current local project rules before choosing a campaign or report.

Run the read-only validator with the available Python interpreter:

```powershell
python <skill-dir>/scripts/validate_profile_paths.py --key test_data_root --key requirement_root
python <skill-dir>/scripts/validate_profile_paths.py --key test_data_root --override test_data_root=F:/explicit/current/data
```

`<skill-dir>` is this hardware-dev-router directory. It prints JSON and exits 2 for a missing/invalid required path or malformed profile; it creates no directories, outputs or device sessions. Explicit overrides can resolve their keys without requiring unrelated missing profile entries. An absent/malformed profile is reported when a selected key needs it. Environment mappings are listed in the script's `ENV_KEYS`.

Check selected files/directories, not just drive availability. Missing required inputs stop dependent analysis/editing; unrelated valid paths remain usable. Do not create an obsolete input directory, substitute a similarly named tree, or choose the newest file as authority. Keep the missing key/path in the report and accept only an evidenced explicit replacement.

2026-09-20 audit: cw513_test_data_root, schematic_pdf_root, test_data_root and requirement_root in the shared profile were absent. Their values are retained as migration clues; do not treat them as working defaults. This dated result must be checked again at use time.

Use `laser-electrical-data-analysis/scripts/inventory_workspace.py --require-root data --data-root <explicit-path>` for a campaign-specific inventory. Unselected missing roots are reported as unavailable, not successful empty inventories. A general inventory requires all selected roots; missing required roots fail before writing a report.

Report destination profiles are distinct: an explicit report directory or LASER_TEST_REPORT_ROOT wins; the formal Word corpus may intentionally live under the Obsidian report branch. Do not silently replace that branch with the historical profile report_root. Source-root validation does not authorize writing the source or overwriting an existing report.
