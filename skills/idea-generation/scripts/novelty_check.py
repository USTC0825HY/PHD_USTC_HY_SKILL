#!/usr/bin/env python3
"""Collect literature evidence, not an automatic novelty verdict.

Adapted from AI-Scientist's check_idea_novelty() in generate_ideas.py.
Local maintenance adds explicit query/error states; standard library only.
"""
import argparse
import datetime as dt
import http.client
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

S2_API_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "")
S2_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
FIELDS = "paperId,externalIds,url,title,authors,venue,year,abstract,citationCount"
EXIT_CODES = {"complete": 0, "partial": 3, "failed": 1}


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


class SearchError(Exception):
    def __init__(self, kind, message, attempts=1, http_status=None):
        super().__init__(message)
        self.kind, self.attempts, self.http_status = kind, attempts, http_status

    def as_dict(self):
        return dict(kind=self.kind, message=str(self), attempts=self.attempts, http_status=self.http_status)


def search_semantic_scholar(query: str, limit: int = 10) -> list[dict]:
    """Return successful papers (possibly []); failures raise SearchError."""
    params = urllib.parse.urlencode(dict(query=query, limit=limit, fields=FIELDS))
    req = urllib.request.Request(f"{S2_SEARCH_URL}?{params}")
    if S2_API_KEY:
        req.add_header("X-API-KEY", S2_API_KEY)
    for attempt in range(1, 4):
        retry = False
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read()
            try:
                data = json.loads(raw.decode("utf-8"))
            except (ValueError, UnicodeError) as exc:
                raise SearchError("invalid_response", "Response is not valid UTF-8 JSON", attempt) from exc
            if not isinstance(data, dict) or not isinstance(data.get("data"), list):
                raise SearchError("invalid_response", "Expected an object with a data array", attempt)
            if not all(isinstance(p, dict) for p in data["data"]):
                raise SearchError("invalid_response", "Paper entries must be objects", attempt)
            for paper in data["data"]:
                for field in ("paperId", "title", "url", "venue", "abstract"):
                    if paper.get(field) is not None and not isinstance(paper[field], str):
                        raise SearchError("invalid_response", f"Invalid paper field: {field}", attempt)
                for field in ("year", "citationCount"):
                    if paper.get(field) is not None and (type(paper[field]) is not int or paper[field] < 0):
                        raise SearchError("invalid_response", f"Invalid paper field: {field}", attempt)
                ids = paper.get("externalIds")
                if ids is not None and (not isinstance(ids, dict) or any(v is not None and not isinstance(v, (str, int)) for v in ids.values())):
                    raise SearchError("invalid_response", "Invalid externalIds", attempt)
                authors = paper.get("authors")
                if authors is not None and (not isinstance(authors, list) or any(not isinstance(a, dict) for a in authors)):
                    raise SearchError("invalid_response", "Invalid authors", attempt)
            return data["data"]
        except urllib.error.HTTPError as exc:
            error = SearchError("rate_limited" if exc.code == 429 else "http_error", f"HTTP {exc.code}", attempt, exc.code)
            retry = exc.code == 429 or 500 <= exc.code < 600
        except (TimeoutError, socket.timeout):
            error = SearchError("timeout", "Request timed out", attempt)
            retry = True
        except http.client.HTTPException:
            error = SearchError("invalid_response", "Incomplete or invalid HTTP response", attempt)
            retry = True
        except urllib.error.URLError as exc:
            kind = "timeout" if isinstance(exc.reason, (TimeoutError, socket.timeout)) else "network_error"
            error = SearchError(kind, "Network request failed", attempt)
            retry = True
        except OSError:
            error = SearchError("network_error", "Network request failed", attempt)
            retry = True
        if not retry or attempt == 3:
            raise error
        time.sleep(2 ** attempt)
    raise SearchError("network_error", "Request attempts exhausted", 3)


def generate_search_queries(idea: str) -> list[str]:
    """Bounded suggestions; cannot establish comprehensive search coverage."""
    queries = [" ".join(idea.lower().split()[:15])]
    chunks, current = [], []
    stop = {"with", "from", "that", "this", "using", "based", "through", "which", "their", "have", "been", "into", "also", "more"}
    for word in idea.split():
        if len(word) > 3 and word.lower() not in stop:
            current.append(word)
        elif current:
            chunks.append(" ".join(current)); current = []
    if current:
        chunks.append(" ".join(current))
    for chunk in sorted(chunks, key=len, reverse=True)[:3]:
        if len(chunk.split()) >= 2:
            queries.append(chunk)
    unique, seen = [], set()
    for q in queries:
        key = q.casefold().strip()
        if key and key not in seen:
            seen.add(key); unique.append(q)
    return unique[:5]


def _count(paper):
    n = paper.get("citationCount")
    return n if isinstance(n, (int, float)) and not isinstance(n, bool) else 0


def _identity(paper):
    ids = paper.get("externalIds") or {}
    if paper.get("paperId"):
        return ("paperId", str(paper["paperId"]))
    if isinstance(ids, dict) and ids.get("DOI"):
        return ("doi", str(ids["DOI"]).casefold())
    title = " ".join(str(paper.get("title") or "").casefold().split())
    return ("title_year", title, paper.get("year")) if title else None


def _candidate(paper, query):
    ids = paper.get("externalIds")
    ids = ids if isinstance(ids, dict) else {}
    return dict(paperId=paper.get("paperId"), doi=ids.get("DOI"), url=paper.get("url"),
                title=paper.get("title", ""), year=paper.get("year"), venue=paper.get("venue", ""),
                citations=_count(paper), abstract=paper.get("abstract") or "", authors=paper.get("authors") or [],
                queries=[query], evidence_level="api_metadata", overlap_assessed=False)


def format_paper(paper: dict) -> str:
    return f"  [{paper.get('year', '?')}] {paper.get('title', 'Unknown')} (citations: {_count(paper)})"


def run_novelty_check(idea: str, max_rounds: int = 5, result_limit: int = 10) -> dict:
    """Return a dictionary on search success, partial success, or failure."""
    result = dict(idea=idea, total_papers_found=0, rounds_used=0, queries_used=[], most_cited_similar=[],
                  search_status="failed", started_at=utc_now(), finished_at=None, source=S2_SEARCH_URL,
                  query_records=[], errors=[], candidates=[], assessment="insufficient_evidence",
                  limitations=["Metadata candidates require reading and overlap assessment.",
                               "Search completion is not proof of coverage or novelty.",
                               "most_cited_similar is a legacy citation-count ordering, not a similarity score."])
    valid = (isinstance(idea, str) and bool(idea.strip()) and type(max_rounds) is int and max_rounds > 0
             and type(result_limit) is int and 1 <= result_limit <= 100)
    if not valid:
        result["errors"].append(dict(kind="invalid_input", message="Nonempty idea, positive rounds and result-limit 1..100 required"))
        result["finished_at"] = utc_now()
        return result
    queue, queried, papers_by_id = generate_search_queries(idea), set(), {}
    for _ in range(max_rounds):
        while queue and queue[0].casefold().strip() in queried:
            queue.pop(0)
        if not queue:
            break
        query = queue.pop(0); queried.add(query.casefold().strip())
        record = dict(query=query, started_at=utc_now(), finished_at=None, status="failed", result_count=None, paper_keys=[], error=None)
        result["queries_used"].append(query)
        print(f"Searching: {query}", file=sys.stderr)
        try:
            papers = search_semantic_scholar(query, result_limit)
            record.update(status="success" if papers else "empty", result_count=len(papers))
            for paper in papers:
                key = _identity(paper)
                if key is None:
                    result["limitations"].append("A metadata entry without usable identity was omitted.")
                    continue
                record["paper_keys"].append(list(key))
                if key not in papers_by_id:
                    papers_by_id[key] = (paper, _candidate(paper, query))
                elif query not in papers_by_id[key][1]["queries"]:
                    papers_by_id[key][1]["queries"].append(query)
            if papers and not queue:
                for paper in papers[:2]:
                    title = str(paper.get("title") or "")[:80]
                    if len(title.split()) >= 3 and title.casefold().strip() not in queried:
                        queue.append(title)
        except SearchError as exc:
            record["error"] = exc.as_dict()
            result["errors"].append(dict(query=query, **exc.as_dict()))
        finally:
            record["finished_at"] = utc_now(); result["query_records"].append(record)
    successes = sum(r["status"] != "failed" for r in result["query_records"])
    failures = len(result["query_records"]) - successes
    result["search_status"] = "partial" if successes and failures else "complete" if successes else "failed"
    result["rounds_used"] = len(result["queries_used"])
    result["candidates"] = [candidate for _, candidate in papers_by_id.values()]
    result["total_papers_found"] = len(result["candidates"])
    ranked = sorted((p for p, _ in papers_by_id.values()), key=_count, reverse=True)
    result["most_cited_similar"] = [dict(title=p.get("title", ""), year=p.get("year"), venue=p.get("venue", ""),
                                           citations=_count(p), abstract=(p.get("abstract") or "")[:200]) for p in ranked[:10]]
    result["finished_at"] = utc_now()
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Collect literature evidence; does not decide novelty")
    parser.add_argument("--idea", type=str, help="Research idea text")
    parser.add_argument("--idea-file", type=str, help="JSON object; takes precedence over --idea")
    parser.add_argument("--max-rounds", type=int, default=5)
    parser.add_argument("--result-limit", type=int, default=10)
    parser.add_argument("--output", type=str, help="Output JSON file")
    args = parser.parse_args(argv)
    if args.max_rounds < 1 or not 1 <= args.result_limit <= 100:
        parser.error("--max-rounds must be positive; --result-limit must be 1..100")
    if args.idea_file:
        try:
            with open(args.idea_file, encoding="utf-8-sig") as f:
                data = json.load(f)
            if not isinstance(data, dict) or not data:
                raise ValueError("idea file must contain a nonempty object")
            if not all(isinstance(data.get(k, ""), str) for k in ("Title", "Experiment")):
                raise ValueError("Title and Experiment must be strings")
            idea = (data.get("Title", "") + ". " + data.get("Experiment", "")).strip(". ")
            if not idea:
                idea = json.dumps(data, ensure_ascii=False)
        except (OSError, ValueError, UnicodeError) as exc:
            parser.error(f"Invalid --idea-file: {exc}")
    else:
        idea = args.idea
    if not idea or not idea.strip():
        parser.error("Either nonempty --idea or --idea-file is required")
    result = run_novelty_check(idea, args.max_rounds, args.result_limit)
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False); f.write("\n")
        except OSError as exc:
            print(f"Output write failed: {exc}", file=sys.stderr)
            print(json.dumps(result, ensure_ascii=False))
            return 1
        print(f"Results saved to {args.output}", file=sys.stderr)
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return EXIT_CODES[result["search_status"]]


if __name__ == "__main__":
    sys.exit(main())
