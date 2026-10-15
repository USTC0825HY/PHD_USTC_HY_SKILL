"""Read-only audit helpers; no workbook/netlist writer."""
import hashlib
import json
import re
from pathlib import Path


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def address(value):
    if not isinstance(value, str) or not re.fullmatch(r"0[xX][0-9a-fA-F]+", value):
        raise ValueError(f"Address must be HEX text: {value!r}")
    n = int(value, 16)
    if n < 0:
        raise ValueError("Negative address")
    return n


def route_key(route, version):
    if version == 1:
        return address(route.get("address"))
    key = route.get("route_id")
    if not isinstance(key, str) or not key.strip():
        raise ValueError("schema 2 requires a non-empty route_id")
    return key


def channel_key(route):
    """Only canonical fields, never guess an ADC from human display text."""
    value = route.get("address")
    chain = route.get("chain_id")
    if chain is not None and (not isinstance(chain, str) or not chain.strip()):
        raise ValueError("chain_id must be a non-empty string or null")
    if value is None:
        return None
    if not isinstance(chain, str) or not chain.strip():
        raise ValueError("Known address requires chain_id")
    return chain, address(value)


class Audit:
    def __init__(self, kind):
        self.kind = kind
        self.findings = []
        self.stats = {}

    def add(self, code, message, level="error", location=""):
        self.findings.append(dict(code=code, level=level, location=location, message=message))

    def result(self):
        errors = sum(f["level"] == "error" for f in self.findings)
        reviews = sum(f["level"] == "review" for f in self.findings)
        status = "failed" if errors else "needs_review" if reviews else "passed"
        return dict(audit=self.kind, status=status, errors=errors, needs_review=reviews,
                    statistics=self.stats, findings=self.findings,
                    boundary="Record/file checks only; not proof of physical continuity, measurements, or visual layout.")


def write_report(report, result, protected):
    dest = Path(report).resolve()
    for p in protected:
        source = Path(p).resolve()
        if dest == source or (dest.exists() and source.exists() and dest.samefile(source)):
            raise ValueError("Report path aliases an input")
    # Exclusive creation avoids overwrite and preserves existing evidence.
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("x", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")


def exit_code(result):
    return {"passed": 0, "failed": 1, "needs_review": 2, "input_error": 3}[result["status"]]
