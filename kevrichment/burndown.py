#!/usr/bin/env python3
"""KEV backlog burn-down: the exact, quantified list of bad records.

Classification (deterministic, per record):

  research   - thin record: summary <80 chars, <4 sources, no vendor
               advisory, or no hypothesis. Needs full agent re-research.
  hypothesis - PoC is public but the hunting hypothesis lacks concrete
               observables (header/path/payload shapes), or the hypothesis
               is outside 130-240 chars. Agent reads the exploit + rewrites.
  stamp      - substance present, hypothesis NOT deterministic-frame, but
               provenance stamps missing. Fixed deterministically here:
               a non-frame hypothesis cannot come from generate_hunting_
               hypothesis(), so it is agent-authored evidence.
  noise      - deterministic-frame hypothesis AND no public PoC: generic
               phrasing is the published standard when nothing technical is
               public. Accepted; never queued.
  ok         - stamped and compliant.

Deterministic fixes applied by `fix`: duplicate-CWE dedupe,
last_researched := research_meta.timestamp, evidence-based stamping, and an
index rebuild. `fix` also (re)writes data/burndown.json — the source of
truth for the hourly burndown cron. `take N` prints the next batch
(research first, then hypothesis; records with >=2 attempts are `stuck`
and excluded).

Usage:
  burndown.py fix          # apply deterministic fixes + rebuild the list
  burndown.py take [N]     # print next batch as JSON (default 5)
  burndown.py report       # print counts only, change nothing
"""
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone

KEV = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(KEV, "data")
CVES = os.path.join(DATA, "cves")
LIST_PATH = os.path.join(DATA, "burndown.json")
MAX_ATTEMPTS = 3
BATCH_DEFAULT = 5

# generate_hunting_hypothesis() composition frame (deterministic pipeline)
FRAME_RE = re.compile(
    r"^Monitor for (?:unauthenticated network-based|network-based|"
    r"local|physically-proximate )?attempts to")
# keep in sync with cronman/bin/kev-verify.py CONCRETE_OBSERVABLE_RE
CONCRETE_RE = re.compile(
    r"(?:`[^`]+`"
    r"|\b[Xx]-[A-Za-z][A-Za-z-]*\b"
    r"|\bwl-[A-Za-z-]+\b"
    r"|/\w"
    r"|\$\{"
    r"|%2"
    r"|\b(?:GET|POST|PUT|HEAD|OPTIONS)\b"
    r"|[A-Za-z0-9+/]{6,}={1,2}\b)")


def classify(rec):
    r = rec.get("kevrichment_research", {})
    m = rec.get("research_meta", {})
    hyp = r.get("hunting_hypothesis") or ""
    summ = r.get("kevrichment_summary") or ""
    srcs = m.get("sources_consulted", [])
    adv = r.get("vendor_advisory_url") or ""
    frame = bool(FRAME_RE.match(hyp))
    if not summ or len(summ) < 80 or len(srcs) < 4 or not adv or not hyp:
        return "research"
    if r.get("public_poc_exists") == "yes" and not CONCRETE_RE.search(hyp):
        return "hypothesis"
    if not (130 <= len(hyp) <= 240):
        return "hypothesis"
    if (r.get("hunting_hypothesis_source") == "agent"
            and r.get("preconditions_source") == "agent"):
        return "ok"
    if frame and r.get("public_poc_exists") != "yes":
        return "noise"
    if len(r.get("preconditions_for_exploit") or "") < 80:
        return "research"      # stamps can't be earned; preconditions too thin
    if not frame:
        return "stamp"
    return "noise"


def load_all():
    out = {}
    for p in sorted(glob.glob(os.path.join(CVES, "CVE-*.json"))):
        try:
            d = json.load(open(p))
            out[d["cve_id"]] = (d, p)
        except Exception:
            pass
    return out


def _prio_entry(cid, cls, attempts, d):
    """Priority tuple for worst-first ordering: freshest KEV add first
    (defenders are patching those today), then CVSS severity, then
    hypothesis-class (public exploit = live detection gap) before research."""
    added = d.get("kev_date_added") or ""
    cvss = d.get("cvss_v3_base_score") or 0.0
    cls_rank = 0 if cls == "hypothesis" else 1
    return {"cve": cid, "class": cls, "attempts": attempts,
            "kev_added": added, "cvss": cvss,
            "_key": (added, cvss, -cls_rank)}


def rebuild(attempts):
    """Classify every record; returns (queue_by_class, totals)."""
    all_recs = load_all()
    queue = {"research": [], "hypothesis": [], "stamp": []}
    merged = []
    totals = {"ok": 0, "noise": 0, "stuck": 0}
    for cid, (d, _) in all_recs.items():
        c = classify(d)
        if c in ("ok", "noise"):
            totals[c] += 1
            continue
        a = attempts.get(cid, 0)
        if a >= MAX_ATTEMPTS:
            totals["stuck"] += 1
            continue
        e = _prio_entry(cid, c, a, d)
        queue[c].append({k: v for k, v in e.items() if not k.startswith("_")})
        merged.append(e)
    for c in queue:
        queue[c].sort(key=lambda e: e["cve"])
    merged.sort(key=lambda e: e["_key"], reverse=True)
    for e in merged:
        del e["_key"]
    queue["next"] = merged          # worst-first merged order; `take` reads this
    return queue, totals, all_recs


def write_list(queue, totals, fixed):
    doc = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "queued": {c: len(v) for c, v in queue.items() if c != "next"},
        "totals": totals,
        "deterministic_fixes_this_run": fixed,
        "queue": queue,
    }
    json.dump(doc, open(LIST_PATH, "w"), indent=1)
    return doc


def rebuild_index():
    sys.path.insert(0, KEV)
    from schema import build_index_entry
    entries, skipped = [], []
    for cid, (d, _) in load_all().items():
        try:
            entries.append(build_index_entry(d))
        except KeyError as e:
            skipped.append(f"{cid}: {e}")
    entries.sort(key=lambda e: e.get("kev_date_added", "") or "", reverse=True)
    prev = {}
    ip = os.path.join(DATA, "index.json")
    if os.path.exists(ip):
        try:
            prev = json.load(open(ip))
        except Exception:
            pass
    json.dump({"last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "kev_source_date": prev.get("kev_source_date", ""),
               "total_cves_processed": len(entries),
               "cves": entries}, open(ip, "w"), indent=2)
    return len(entries), skipped


def cmd_fix():
    attempts = {}
    prev_batch = []
    if os.path.exists(LIST_PATH):
        try:
            prev = json.load(open(LIST_PATH))
            attempts = {e["cve"]: e["attempts"]
                        for c in prev.get("queue", {}).values() for e in c}
            prev_batch = prev.get("current_batch", [])
        except Exception:
            pass
    def _entries(q):
        return [e for c in ("research", "hypothesis", "stamp") for e in q[c]]

    fixed = {"dup_cwe": 0, "ts_sync": 0, "stamped": 0}
    for cid, (d, p) in load_all().items():
        r = d.get("kevrichment_research", {})
        m = d.get("research_meta", {})
        cwes = d.get("cwe", [])
        changed = False
        if len(cwes) != len(set(cwes)):
            d["cwe"] = list(dict.fromkeys(cwes)); fixed["dup_cwe"] += 1; changed = True
        if d.get("last_researched") != m.get("timestamp") and m.get("timestamp"):
            d["last_researched"] = m["timestamp"]; fixed["ts_sync"] += 1; changed = True
        # evidence-based provenance stamps: a non-frame hypothesis cannot be
        # machine-composed, and preconditions must carry real substance
        if classify(d) == "stamp":
            m2 = dict(m)
            if r.get("hunting_hypothesis_source") != "agent":
                r["hunting_hypothesis_source"] = "agent"; changed = True
            if (r.get("preconditions_source") != "agent"
                    and len(r.get("preconditions_for_exploit") or "") >= 80):
                r["preconditions_source"] = "agent"; changed = True
            m2["hunting_hypothesis_source"] = "agent"
            if len(r.get("preconditions_for_exploit") or "") >= 80:
                m2["preconditions_source"] = "agent"
            if m2 != m:
                d["research_meta"] = m2
            fixed["stamped"] += 1
        if changed:
            d["kevrichment_research"] = r
            json.dump(d, open(p, "w"), indent=2)
    # attempts: records from the previous batch still failing -> +1
    n, skipped = rebuild_index()
    queue, totals, _ = rebuild(attempts)
    still = {e["cve"] for e in _entries(queue)}
    for e in prev_batch:
        if e["cve"] in still:
            attempts[e["cve"]] = attempts.get(e["cve"], 0) + 1
    queue, totals, _ = rebuild(attempts)   # re-apply attempt bumps
    doc = write_list(queue, totals, fixed)
    print(f"burndown: research={len(queue['research'])} hypothesis={len(queue['hypothesis'])} "
          f"stamp={len(queue['stamp'])} ok={totals['ok']} noise={totals['noise']} "
          f"stuck={totals['stuck']} | deterministic: {fixed} | index {n}"
          + (f" (skipped {len(skipped)})" if skipped else ""))
    actionable = len(queue["research"]) + len(queue["hypothesis"])
    print(f"actionable remaining: {actionable}")
    return 0 if actionable == 0 else 2


def cmd_take(n):
    if not os.path.exists(LIST_PATH):
        print("no burndown.json — run fix first"); return 1
    doc = json.load(open(LIST_PATH))
    batch = doc["queue"]["next"][:n]     # worst-first (freshest KEV, severity, PoC gap)
    doc["current_batch"] = batch
    json.dump(doc, open(LIST_PATH, "w"), indent=1)
    print(json.dumps(batch, indent=1))
    return 0


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "report"
    if mode == "fix":
        sys.exit(cmd_fix())
    if mode == "take":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else BATCH_DEFAULT
        sys.exit(cmd_take(n))
    if mode == "report":
        if os.path.exists(LIST_PATH):
            d = json.load(open(LIST_PATH))
            print(json.dumps({"queued": d["queued"], "totals": d["totals"],
                              "updated_at": d["updated_at"]}, indent=1))
        else:
            print("no list yet — run fix")
        return
    print(__doc__)
    sys.exit(1)


if __name__ == "__main__":
    main()
