# Research proposal prompts

## Source and local adaptation

Originally extracted from AI-Scientist, AI-Scientist-v2 and AI-Researcher. The local version keeps hypothesis generation, reflection and experiment planning; it removes assumptions about API access, ML-only resources and compulsory binary novelty decisions. Retain this attribution when adapting the prompts.

## Generate and refine

Use the supplied observations and constraints to propose a concrete question. Identify the mechanism or explanation being tested, plausible alternatives, the available observations that support it, and evidence that would refute it. Define a baseline and the smallest discriminating experiment. Include units and measurement conditions when relevant; unknown values remain unknown.

For refinement, ask whether the experiment distinguishes rival explanations, whether a simpler test exists and whether required data or equipment are actually available. Preserve the useful idea while changing unsupported assumptions. Stop at the depth requested rather than filling a fixed number of ideas or iterations.

## Literature check

Discover the current session's search tools before planning calls. Use exact terms, synonyms, competing methods and task-relevant dates. Open primary sources and record what was actually read. Compare the claim and experiment, not just paper titles or citation counts. If access fails or only local sources are available, record `insufficient_evidence` and what needs checking.

Do not assert an API was accessed, a paper was read or an idea is new when the execution record does not establish it. Summarize checkable reasons and sources; do not require a hidden-reasoning transcript.

## Optional structured proposal

```json
{
  "Name": "candidate_identifier",
  "Title": "Concrete research question",
  "Hypothesis": "Testable explanation, explicitly provisional",
  "Experiment": "Available inputs, baseline, measurement and refutation criterion",
  "Interestingness": null,
  "Feasibility": null,
  "Novelty": null,
  "assessment": "insufficient_evidence",
  "brief_basis": "Literature overlap has not yet been checked",
  "most_similar_papers": [],
  "constraints": [],
  "next_step": "Smallest useful check"
}
```

Scores, when requested and supported, remain subjective 1–10 judgments, not measured probabilities. Keep a separate explanation of the evidence. `assessment` can become `overlap_found` or `potential_difference` after a literature comparison. The legacy `novel` boolean is retained only as historical format information, not a default output requirement. Never map successful zero search results automatically to novelty.
