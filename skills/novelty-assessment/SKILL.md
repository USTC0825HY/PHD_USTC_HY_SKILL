---
name: novelty-assessment
description: Assess a research idea against traceable literature evidence, identify substantive overlap and possible differences, and report coverage limits. Use for novelty checks before selecting or developing a research direction; this is not a patentability opinion or automatic novelty verdict.
metadata:
  argument-hint: "[idea]"
---

# Novelty Assessment

Establish what the available literature supports about the proposed contribution. Separate similarity in topic from overlap in the actual claim, method, assumptions and evaluation.

## Workflow

1. State the proposed claim and its scope; separate supplied facts, assumptions and the change being proposed. Respect the user's research area, resources and requested depth.
2. Discover search/browsing tools actually available in this session. Search the specific method, synonyms, alternative solutions to the same problem and relevant recent work. Use the requested date range; a date filter cannot replace foundational work. Iterate to resolve material gaps, not to reach a fixed round or paper count.
3. Open primary papers or official publication pages. Record whether evidence comes from metadata, an abstract or the relevant full-text sections. Do not present snippets as full-paper review. Verify titles, dates and identifiers from the source.
4. Compare the nearest relevant works claim by claim: what overlaps, what differs, and what evidence would test the difference. Citation counts are not relevance scores. Prioritize papers by the contribution under examination.
5. Report one of the evidence states below, with brief reasons, supporting sources, limitations and a next verification step. Keep factual overlap separate from contribution value or publication prospects.

| assessment | Meaning |
|---|---|
| overlap_found | Read evidence shows substantive overlap with the claimed contribution; identify the overlap and any residual difference. |
| potential_difference | A specific difference appears plausible within the searched/read scope; it still needs verification. |
| insufficient_evidence | Search or reading is missing, failed, too limited or inconclusive. |

No matching result does not prove novelty. Do not infer a publishable contribution from a score or assume a result is new because it combines familiar components.

## Evidence and tools

- Keep a compact query/source/time record, stable paper identifiers or URLs, reading depth, comparison and unsearched areas. Add more detail when the decision depends on it; no fixed output template is required.
- If an API helper is useful, locate the **actual available** `idea-generation` skill and its `scripts/novelty_check.py`; read its `references/search-evidence.md` before use. Do not guess another installation root or require that skill to exist.
- The helper only collects candidates. Inspect `search_status`, per-query failures and coverage limitations before using its output. Its `assessment` stays `insufficient_evidence` until a separate evidence-based review is performed.
- If online tools are unavailable or prohibited, work only from supplied/local documents and label the scope and missing verification. Do not claim a live search, install a search service or demand an API key as a prerequisite to useful work.

Read [references/assessment-prompts.md](references/assessment-prompts.md) for a detailed comparison or structured output. Use `idea-generation` only when new or revised ideas are requested and the skill is available; do not recursively bounce between the two skills.
