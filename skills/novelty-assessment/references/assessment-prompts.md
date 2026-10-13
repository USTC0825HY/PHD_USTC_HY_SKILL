# Evidence-based novelty assessment

## Source and local adaptation

Originally extracted from AI-Scientist (`check_idea_novelty`), data-to-paper and SciMON. This local adaptation preserves the literature-comparison purpose while replacing assumed API access, fixed search years and binary novelty verdicts. These are working prompts, not claims that the cited systems have been run.

## Search and comparison prompts

- What precise claim is being assessed? Which parts already follow from established work?
- Which query would resolve the largest remaining uncertainty: exact technique, alternative terminology, the same problem with a different method, or recent competing work?
- What does the actual paper establish? Record the relevant abstract or section and avoid inferring unread experiments.
- Compare problem, assumptions, mechanism, resources and evaluation. Distinguish same topic, similar approach and substantive overlap; explain the basis instead of treating a keyword match as rejection.
- What new observation or experiment could distinguish the proposal from the nearest work?

Stop when the requested decision can be supported within an explicit scope, when further searches repeat known evidence, or when tool/time limits prevent progress. State unfinished areas. Foundational work and current developments can both matter; choose dates from the task, not this template.

## Evidence record

For each useful query: query text, source/tool, UTC or local timestamp with timezone, success/zero results/failure, useful paper identifiers and reading depth. For each compared paper: title, verified year, DOI/arXiv/publisher URL when available, the claim actually read, overlap and difference. Missing identifiers stay missing; do not construct a DOI.

## Output when structured data is requested

```json
{
  "assessment": "insufficient_evidence",
  "confidence": "low",
  "brief_basis": "Only supplied abstracts were reviewed; current literature search was unavailable.",
  "closest_papers": [],
  "possible_difference": null,
  "uncovered": ["Recent work and relevant full-text methods"],
  "next_check": "Read the nearest methods sections and search competing terminology"
}
```

Allowed states: `overlap_found`, `potential_difference`, `insufficient_evidence`. Confidence describes the evidence for this bounded assessment, not the probability of publication. Legacy `novel`/`not_novel` formats are historical; do not emit a definitive novelty boolean by default. Even `potential_difference` is not a proof that no prior work exists.

## Contribution versus novelty

A result may contribute a method, measurement, dataset, theory or useful validation. Assess its value separately from overlap. Do not impose machine-learning datasets, top-conference criteria or unavailable resources on other disciplines. Return concise, publicly checkable reasons and evidence, not a transcript of internal deliberation.
