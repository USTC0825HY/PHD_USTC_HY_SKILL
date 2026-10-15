"""Validate a declared telemetry graph, not a replacement for PST tracing."""
import argparse
import math
from pathlib import Path
from audit_common import Audit, address, route_key, channel_key, read_json, sha256, write_report, exit_code


def decode_adc(raw, bits, coding, vref):
    if not isinstance(bits, int) or not 1 <= bits <= 32:
        raise ValueError("bits must be 1..32")
    if not isinstance(raw, int) or isinstance(raw, bool) or not 0 <= raw < 2 ** bits:
        raise ValueError("raw out of range")
    if not isinstance(vref, (int, float)) or not math.isfinite(vref) or vref <= 0:
        raise ValueError("invalid reference")
    if coding == "twos_complement":
        n = raw if raw < 2 ** (bits - 1) else raw - 2 ** bits
        return n, n * vref / 2 ** (bits - 1)
    if coding == "offset_binary":
        n = raw - 2 ** (bits - 1)
        return n, n * vref / 2 ** (bits - 1)
    if coding == "unipolar_binary":
        return raw, raw * vref / 2 ** bits
    raise ValueError("Unsupported coding; use a reviewed custom conversion outside this helper")


def audit(manifest, profile, base):
    a = Audit("declared_route_consistency")
    version = manifest.get("schema_version")
    if version not in (1, 2) or profile.get("schema_version") != version:
        raise ValueError("manifest/profile schema_version must match (1 or 2)")
    boards = manifest.get("boards", {})
    nodes = manifest.get("nodes", {})
    evidence = manifest.get("evidence", {})
    routes = manifest.get("routes", [])
    a.stats.update(routes=len(routes), nodes=len(nodes), boards=len(boards), mode=profile.get("mode"))
    if not routes:
        a.add("NO_ROUTES", "No routes declared", "review")
    for board, data in boards.items():
        if not data.get("version") or not data.get("evidence_set"):
            a.add("BOARD_IDENTITY", "Missing board version or selected evidence set", "review", board)
    protected = []
    for key, ev in evidence.items():
        if not ev.get("kind") or not ev.get("locator"):
            a.add("EVIDENCE_DESCRIPTION", "Missing evidence kind or locator", "review", key)
        if ev.get("path"):
            path = (base / ev["path"]).resolve()
            protected.append(path)
            if not path.is_file():
                a.add("SOURCE_MISSING", str(path), "review", key)
            elif not ev.get("sha256"):
                a.add("HASH_MISSING", str(path), "review", key)
            elif sha256(path).lower() != ev["sha256"].lower():
                a.add("SOURCE_CHANGED", str(path), location=key)
        elif ev.get("kind") not in ("interface_confirmation", "assembly_confirmation"):
            a.add("SOURCE_UNAVAILABLE", "No retrievable source file", "review", key)

    def refs(ids, location):
        if not ids:
            a.add("EVIDENCE_MISSING", "No evidence reference", "review", location)
        for key in ids:
            if key not in evidence:
                a.add("EVIDENCE_UNKNOWN", str(key), location=location)

    for key, n in nodes.items():
        if n.get("board") not in boards:
            a.add("NODE_BOARD", "Node board not registered", location=key)
        if not n.get("ref") or not n.get("pin") or not n.get("net"):
            a.add("NODE_INCOMPLETE", "Missing ref, pin or exact net", "review", key)
    physical = {}
    for key, n in nodes.items():
        identity = (n.get("board"), n.get("ref"), n.get("pin"))
        if identity in physical and nodes[physical[identity]].get("net") != n.get("net"):
            a.add("NODE_NET_CONFLICT", str(identity), location=key)
        physical[identity] = key

    pairs = {}
    contacts = {}
    for pair in profile.get("connector_pairs", []):
        k = (pair["from"], pair["to"])
        if k in pairs:
            a.add("DUPLICATE_PAIR", str(k))
        pairs[k] = pair
        for x, y in (k, k[::-1]):
            if x in contacts and contacts[x] != y:
                a.add("CONNECTOR_PAIR_CONFLICT", f"{x} paired with both {contacts[x]} and {y}")
            contacts[x] = y
        refs(pair.get("evidence", []), str(k))
        if not any(evidence.get(e, {}).get("kind") in ("interface_confirmation", "schematic", "continuity") for e in pair.get("evidence", [])):
            a.add("PAIR_BASIS", "Pair lacks interface/schematic/continuity evidence", "review", str(k))
        if pair.get("from") not in nodes or pair.get("to") not in nodes:
            a.add("PAIR_NODE", str(k))

    inputs = profile.get("physical_inputs", {})
    cascade = set(profile.get("cascade_inputs", []))
    expected = {(address(k) if version == 1 else k): v for k, v in profile.get("expected_routes", {}).items()}
    if not inputs or not expected:
        a.add("COVERAGE_UNDEFINED", "Physical inputs or expected address map missing", "review")
    if not cascade <= set(inputs):
        a.add("CASCADE_UNKNOWN", "Cascade input not declared")
    used = set()
    seen = set()
    channels = set()
    for route in routes:
        loc = str(route.get("route_id") if version == 2 else route.get("address", "(missing address)"))
        try:
            addr = route_key(route, version)
            channel = channel_key(route) if version == 2 else addr
        except (TypeError, ValueError) as e:
            a.add("ADDRESS_FORMAT", str(e), location=loc)
            continue
        if addr in seen:
            a.add("DUPLICATE_ROUTE_ID" if version == 2 else "DUPLICATE_ADDRESS", loc, location=loc)
        seen.add(addr)
        if channel is None:
            a.add("ADDRESS_UNCONFIRMED", "Canonical address/chain remains unconfirmed", "review", loc)
        else:
            if version == 2 and channel in channels:
                a.add("DUPLICATE_CHANNEL_ADDRESS", str(channel), location=loc)
            channels.add(channel)
        if route.get("status") not in ("complete", "partial", "unavailable"):
            a.add("ROUTE_STATUS", "status must be complete/partial/unavailable", location=loc)
        if route.get("status") != "complete":
            a.add("ROUTE_OPEN", "Route is not complete", "review", loc)
        if route.get("mode") != profile.get("mode"):
            a.add("MODE_MISMATCH", "Route mode differs from selected profile", location=loc)
        inp = route.get("input")
        if inp is not None:
            used.add(inp)
        if inp not in inputs:
            a.add("INPUT_UNKNOWN", str(inp), "review" if version == 2 and inp is None else "error", loc)
        if inp in cascade:
            a.add("CASCADE_AS_MEASUREMENT", str(inp), location=loc)
        exp = expected.get(addr)
        if exp is None:
            a.add("UNEXPECTED_ADDRESS", loc, location=loc)
        else:
            if version == 2:
                if "address" not in exp or "chain_id" not in exp:
                    a.add("EXPECTED_CHANNEL_UNDEFINED", "Expected record needs chain_id and address (nullable)", "review", loc)
                elif channel_key(exp) != channel or exp.get("chain_id") != route.get("chain_id"):
                    a.add("MAPPING_MISMATCH", "chain/address differs from expected record", location=loc)
            for field in ("input", "mux", "source_board", "endpoint"):
                if field in exp and route.get(field) != exp[field]:
                    a.add("MAPPING_MISMATCH", f"{field}: expected {exp[field]!r}, got {route.get(field)!r}", location=loc)
        segs = route.get("segments", [])
        if not segs:
            a.add("NO_SEGMENTS", "No traced segments", "review", loc)
        previous = inputs.get(inp, {}).get("node")
        component_refs = set()
        for i, seg in enumerate(segs):
            sloc = f"{loc}/segment[{i}]"
            x, y = seg.get("from"), seg.get("to")
            if x not in nodes or y not in nodes:
                a.add("SEGMENT_NODE", "Missing node", location=sloc)
                previous = y
                continue
            if previous is not None and x != previous:
                a.add("BROKEN_ADJACENCY", f"Expected start {previous}, found {x}", location=sloc)
            previous = y
            refs(seg.get("evidence", []), sloc)
            xn, yn = nodes[x], nodes[y]
            kind = seg.get("kind")
            if kind == "gap":
                a.add("UNCONFIRMED_GAP", seg.get("note", "Crossing not confirmed"), "review", sloc)
                if route.get("status") == "complete":
                    a.add("GAP_MARKED_COMPLETE", "Complete route contains gap", location=sloc)
            elif kind == "connector":
                pair = pairs.get((x, y)) or pairs.get((y, x))
                if pair is None:
                    a.add("CONNECTOR_UNBOUND", f"{x} -> {y}", "review", sloc)
                    if route.get("status") == "complete":
                        a.add("UNBOUND_MARKED_COMPLETE", "No connector definition", location=sloc)
                if xn["board"] == yn["board"]:
                    a.add("CONNECTOR_SAME_BOARD", "Use net/component for same-board segment", location=sloc)
            elif kind in ("net", "component"):
                if xn["board"] != yn["board"]:
                    a.add("CROSS_BOARD_SHORTCUT", "Cross-board edge must be connector or gap", location=sloc)
                if kind == "net" and xn.get("net") != yn.get("net"):
                    a.add("NET_JUMP", "Same-board net segment changes net", location=sloc)
                if kind == "component":
                    c = seg.get("component", {})
                    component_refs.add(c.get("ref"))
                    if not c.get("ref") or xn.get("ref") != c.get("ref") or yn.get("ref") != c.get("ref") or xn.get("pin") == yn.get("pin"):
                        a.add("COMPONENT_PINS", "Component must cross distinct pins of its refdes", location=sloc)
                    if not c.get("value"):
                        a.add("COMPONENT_VALUE", "Component value/type missing", "review", sloc)
                    state = c.get("state")
                    if state == "unfitted" and route.get("status") == "complete":
                        a.add("UNFITTED_ACTIVE", "Active route traverses unfitted component", location=sloc)
                    elif state != "fitted":
                        a.add("ASSEMBLY_UNCONFIRMED", str(state), "review", sloc)
                    refs(c.get("assembly_evidence", []), sloc + "/assembly")
                    if any(v in c.get("marker", "").upper() for v in ("TSD", "DNP")) and state == "fitted":
                        if not any(evidence.get(e, {}).get("kind") == "assembly_confirmation" and
                                   evidence[e].get("scope", {}).get("board") == xn["board"] and
                                   (version == 1 or evidence[e].get("scope", {}).get("version") == boards[xn["board"]].get("version")) and
                                   c.get("ref") in evidence[e].get("scope", {}).get("refs", [])
                                   for e in c.get("assembly_evidence", [])):
                            a.add("TSD_OVERRIDE_MISSING", "Fitted override lacks scoped assembly confirmation", location=sloc)
            else:
                a.add("SEGMENT_KIND", str(kind), location=sloc)
        if exp:
            for ref in exp.get("required_components", []):
                if ref not in component_refs:
                    a.add("REQUIRED_BRANCH_MISSING", ref, location=loc)
            for ref in exp.get("forbidden_components", []):
                if ref in component_refs:
                    a.add("WRONG_BRANCH", ref, location=loc)
        endpoint = route.get("endpoint")
        if endpoint not in nodes:
            a.add("ENDPOINT_UNKNOWN", str(endpoint), "review", loc)
        elif segs and previous != endpoint:
            a.add("ENDPOINT_MISMATCH", "Last segment does not end at declared source point", location=loc)
        if endpoint in nodes and route.get("source_board") != nodes[endpoint].get("board"):
            a.add("SOURCE_BOARD_MISMATCH", "Source board differs from endpoint owner", location=loc)
        if not route.get("source_interface"):
            a.add("SOURCE_INTERFACE_MISSING", "Use a node, or local for a local reference", "review", loc)
        elif route["source_interface"] != "local" and route["source_interface"] not in nodes:
            a.add("SOURCE_INTERFACE_UNKNOWN", route["source_interface"], location=loc)
        elif route["source_interface"] != "local":
            if route["source_interface"] not in {s.get(f) for s in segs for f in ("from", "to")}:
                a.add("SOURCE_INTERFACE_SKIPPED", "Declared source interface is absent from the route", location=loc)
            if nodes[route["source_interface"]].get("board") != route.get("source_board"):
                a.add("INTERFACE_BOARD_MISMATCH", "Source interface belongs to another board", location=loc)
        for f in ("summary_endpoint", "detail_endpoint"):
            if f in route and route[f] != endpoint:
                a.add("VIEW_ENDPOINT_MISMATCH", f, location=loc)
        conversion = route.get("conversion", {})
        if conversion.get("output_kind") == "physical_quantity":
            if conversion.get("source_parameters_confirmed") is not True or not conversion.get("source_formula") or not conversion.get("source_unit"):
                a.add("UNSUPPORTED_PHYSICAL_VALUE", "Missing confirmed source conversion parameters", location=loc)
        if conversion:
            if not conversion.get("vref_basis"):
                a.add("REFERENCE_BASIS", "Nominal/adopted/measured basis missing", "review", loc)
            try:
                decode_adc(0, conversion.get("bits"), conversion.get("coding"), conversion.get("vref"))
            except (ValueError, TypeError) as e:
                a.add("CONVERSION_MODEL", str(e), "review", loc)
    if expected and set(expected) != seen:
        a.add("ADDRESS_COVERAGE", f"Missing: {sorted(set(expected)-seen)}; unexpected: {sorted(seen-set(expected))}")
    missing = set(inputs) - cascade - used
    if missing:
        a.add("INPUT_COVERAGE", f"Physical input not represented: {sorted(missing)}")
    a.stats.update(physical_inputs=len(inputs), cascade_inputs=len(cascade), represented_inputs=len(used),
                   unique_addresses=len(channels), unique_routes=len(seen), ground_routes=sum(r.get("kind") == "ground" for r in routes),
                   measurement_routes=sum(r.get("kind") == "measurement" for r in routes))
    return a.result(), protected


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for key in ("manifest", "profile", "report"):
        p.add_argument("--" + key, required=True)
    args = p.parse_args()
    protected = [args.manifest, args.profile]
    try:
        m, profile = read_json(args.manifest), read_json(args.profile)
        for ev in m.get("evidence", {}).values():
            if ev.get("path"):
                protected.append((Path(args.manifest).resolve().parent / ev["path"]).resolve())
        result, sources = audit(m, profile, Path(args.manifest).resolve().parent)
        protected.extend(sources)
        result["inputs"] = {str(Path(x).resolve()): sha256(x) for x in protected if Path(x).is_file()}
    except (ValueError, TypeError, KeyError, OSError, AttributeError, IndexError) as e:
        result = dict(status="input_error", error=str(e))
    try:
        write_report(args.report, result, protected)
    except (ValueError, OSError) as e:
        print(f"Report not written: {e}")
        return 3
    print(result["status"])
    return exit_code(result)


if __name__ == "__main__":
    raise SystemExit(main())
