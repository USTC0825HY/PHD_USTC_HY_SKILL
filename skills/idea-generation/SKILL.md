---
name: idea-generation
description: Develop research questions, hypotheses and feasible experiment proposals from supplied evidence and constraints. Use for research brainstorming and refinement; distinguish unverified ideas from literature-supported differences, and use novelty-assessment for a focused overlap check when available.
metadata:
  argument-hint: "[research-area]"
---

# Idea Generation

Turn an observed problem into candidate questions, testable hypotheses and a feasible next experiment. Keep the user's scientific domain and available resources central; a generic ML example is not the project specification.

## Workflow

1. Establish the problem, known evidence, current limitations, available data/equipment and intended decision. Use known context before asking for information. Distinguish a supplied observation from a proposed explanation.
2. Produce as many distinct candidates as the task needs. For each, state the question, proposed mechanism, what could disprove it, a comparison/baseline and the smallest useful experiment.
3. Refine candidates using feasibility and evidence gaps. Do not require a fixed reflection count, invent measurements, assume extra compute/equipment, or promise a top-venue outcome.
4. For candidates being recommended for commitment, inspect relevant literature with actually available tools. Search exact methods, synonyms, alternatives and recent work, then verify primary sources. If `novelty-assessment` is available, use it for a focused comparison; do not recursively request another generation cycle unless the user needs alternatives.
5. Recommend the candidate(s) whose next experiment best resolves the user's question. State uncertainty and resource needs. Brainstorming may remain exploratory when search is unavailable; label it as unverified rather than presenting it as established novelty.

## Evidence and optional helper

The standard-library [scripts/novelty_check.py](scripts/novelty_check.py) collects Semantic Scholar candidates. It does **not** decide novelty, read full papers or establish similarity from citations. It is optional; prefer current search tools when they better fit the task.

Before using the helper or consuming its JSON, read [references/search-evidence.md](references/search-evidence.md). Resolve paths from this skill's actual installed directory. No other provider's home directory or absent skill is a dependency. A configured API key may be used but must never be printed or requested in chat. Do not install services simply to satisfy a template.

Read [references/ideation-prompts.md](references/ideation-prompts.md) for comparison prompts or structured proposals. Default to clear prose suitable for the user. If ratings are useful, label them as qualitative judgments with reasons; `Novelty` is `null` when evidence cannot support it. Use evidence states `overlap_found`, `potential_difference` and `insufficient_evidence`, not a mandatory novelty boolean.
