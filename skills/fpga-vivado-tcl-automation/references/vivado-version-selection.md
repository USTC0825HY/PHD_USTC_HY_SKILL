# Select the actual Vivado target

- Resolve the user's explicit target and nearest AGENTS/MEMORY, then inspect the current XPR product version, part, top, active sources/constraints and run inputs. Treat dated MEMORY entries as historical when current artifacts differ.
- Use the shared Laser profile only as a tool-location fallback. Verify the executable version matches the project; do not upgrade an XPR, replace IP or silently choose another installed Vivado version.
- The installed vivado-* guides contain 2025.2 reference material and a separate 2022.2 compatibility audit. Neither proves support in 2018.3. Select only applicable device-family features and check the selected tool's help before execution.
- For 05_CW_TEST_HY the current project rules/XPR select 2018.3 and a 7-series target. This example is not a default for other projects. Preserve each project's build permissions and frozen-source boundaries.
- A review may use existing matching reports without starting a build. New synthesis, implementation, IP regeneration, BIT/LTX generation or hardware operations require the current task's scope to include that stage. A historical task authorization is not current authorization.
- Preserve prior runs and their identity. A run marked Complete is not proof that it matches changed inputs; compare input provenance and report/build dates before using its results.
