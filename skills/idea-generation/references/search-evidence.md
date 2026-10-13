# Optional literature-search helper

## Choose tools first

Use a search/browsing capability actually available in the current session. This script is an optional Semantic Scholar metadata collector when Python and permitted network access are available. It uses only the Python standard library (Python 3.9+); no installation or API key is mandatory. Respect user restrictions on network use. Credentials, when already configured, stay in the environment.

Resolve `scripts/novelty_check.py` from the actual `idea-generation` directory. Example with placeholders replaced by real paths:

```text
<python> <skill-root>/scripts/novelty_check.py --idea "Pound Drever Hall digital servo loop delay" --max-rounds 2 --result-limit 5 --output <task-dir>/search-evidence.json
```

## Compatibility and execution status

Existing arguments remain: `--idea`, `--idea-file`, `--max-rounds`, `--result-limit`, `--output`. Defaults are 5 rounds and 10 results per query. An idea file takes precedence when both idea inputs are supplied; it must be a nonempty JSON object. `Title` and `Experiment`, when present, must be strings. Other nonempty objects retain the legacy serialized-object fallback. Rounds must be positive and the per-query result limit 1–100.

`run_novelty_check(idea, max_rounds=5, result_limit=10)` returns a dictionary. Old fields `idea`, `total_papers_found`, `rounds_used`, `queries_used`, `most_cited_similar` remain. Read the added `search_status`, `query_records`, `errors`, `candidates`, timestamps and limitations before interpreting those old fields.

| search_status | CLI exit | Meaning |
|---|---:|---|
| complete | 0 | Every executed query succeeded; zero matches is a valid successful response. |
| partial | 3 | At least one query succeeded and at least one failed; inspect retained evidence and gaps. |
| failed | 1 | No query succeeded. |
| invalid input | 2 | CLI input or parameters were invalid; no search is claimed. |

An output write failure exits 1, reports the error and emits the result to stdout for recovery. Without `--output`, stdout is JSON; progress goes to stderr. Search failures still produce evidence JSON when output is writable. API retries are bounded to three attempts per query, with a 30-second request timeout and short backoff; no endless retries.

Per-query `success`, `empty` and `failed` are distinct. `result_count=null` on failure is not a count of zero. Invalid JSON/schema, timeouts, network errors and exhausted rate limits are failures. `complete` describes execution, not exhaustive literature coverage. Default query generation is a simple heuristic and needs domain-specific supplementation, especially for multilingual queries.

## What the result does not prove

`candidates` preserves discovery order, available paper IDs/DOIs/URLs, metadata and query provenance. Missing identifiers stay null. Deduplication uses paper ID, otherwise DOI, otherwise normalized title/year; entries whose identifier availability differs may still need manual reconciliation.

`most_cited_similar` is a legacy field containing a citation-count ordering. Its name is not evidence of similarity. The helper does not calculate semantic overlap, inspect full text or decide novelty; its `assessment` remains `insufficient_evidence`. A separate reading/comparison step can establish substantive overlap or a potential difference within a stated scope.

Official API behavior: [Semantic Scholar tutorial](https://webflow.semanticscholar.org/product/api/tutorial) and [Academic Graph API reference](https://api.semanticscholar.org/api-docs/graph). Check current documentation before changing provider request fields or limits.

## Local regression check

With an existing Python 3.9+ runtime, run `python tests/test_novelty_check.py` from this skill directory. Tests use mocked HTTP responses and isolated temporary files; they do not prove live API availability.

Set `NOVELTY_TEST_TMP` to the project's permitted temporary task directory when required (in Laser, a `.codex_work/<date-task>/` directory). Otherwise Python uses the operating system temporary directory. No test should require installing a service or exposing an API key.
