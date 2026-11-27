#!/usr/bin/env python3
"""Retention policy contract suite.

The tiers decide which story pages stay published for years, so the properties
that matter are the ones a decaying score can break:

  1. tiers read the PEAK, never the current score — a story that was hottest
     once stays tier A after it cools (the owner's requirement verbatim);
  2. an immutable citation (a CTI case and the STIX snapshot built from it)
     outranks a digest citation and always lands in A;
  3. FAIL SAFE: a missing, unparseable or out-of-range peak is "unknown", not
     zero — unknown promotes to A and is reported, because the store once held
     ~8.2k stories with no peak at all;
  4. merged shells are never classified (they are one map key, not a page);
  5. the report's steady-state arithmetic follows the horizons it is given.

Run: python3 engine/test_retention.py   (exit 0 = pass)
Wired into CI (site-deploy.yml) and run_engine.sh.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import retention  # noqa: E402


def story(peak=None, score=0.0):
    s = {"id": "s", "first_seen": "2026-11-01T00:00:00Z", "score": score}
    if peak is not None:
        s["peak_score"] = peak
    return s


def check(name, got, expect):
    ok = got == expect
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {expect!r}")
    return ok


def main():
    ok = True

    # 1. the high-water mark decides, not the decayed score
    ok &= check("hottest peak -> A", retention.classify(story(peak=8.0))[0], "A")
    ok &= check("hot peak -> B", retention.classify(story(peak=5.5))[0], "B")
    ok &= check("cold peak -> C", retention.classify(story(peak=1.0))[0], "C")
    ok &= check("cooled story keeps A via its peak (score 0)",
                retention.classify(story(peak=8.0, score=0.0))[0], "A")

    # 2. immutable citation outranks digest citation
    ok &= check("cti-cited, cold peak -> A",
                retention.classify(story(peak=1.0), immutable_cited=True)[0], "A")
    ok &= check("cti + digest cited -> A (immutable wins)",
                retention.classify(story(peak=1.0), immutable_cited=True,
                                   digest_cited=True)[0], "A")
    ok &= check("digest-cited only -> B",
                retention.classify(story(peak=1.0), digest_cited=True)[0], "B")

    # 3. fail safe on unknown peaks
    tier, reason = retention.classify(story())          # no peak_score at all
    ok &= check("missing peak -> A (fail-safe)", tier, "A")
    ok &= check("missing peak says why", "unknown" in reason, True)
    ok &= check("unparseable peak -> A", retention.classify(story(peak="n/a"))[0], "A")
    ok &= check("out-of-range peak -> A", retention.classify(story(peak=11.0))[0], "A")
    ok &= check("real zero peak is NOT unknown", retention.peak_of(story(peak=0.0)),
                (0.0, True))

    # 4. merged shells are not classifications
    stories = {"live": story(peak=8.0), "shell": {"id": "shell", "merged_into": "live"}}
    ok &= check("merged shell excluded", sorted(retention.classify_all(stories, set(), set())),
                ["live"])

    # 5. report arithmetic follows the horizons
    stories = {"a": story(peak=8.0), "b": story(peak=5.5), "c": story(peak=1.0)}
    for peak in ("a", "b", "c"):
        stories[peak]["first_seen"] = "2026-11-02T00:00:00Z"
    saved = dict(retention.TIER_YEARS)
    try:
        retention.TIER_YEARS.update({"A": 5, "B": 3, "C": 0.5})
        rep = retention.report(stories)
        ok &= check("one story per tier", rep["tiers"], {"A": 1, "B": 1, "C": 1})
        ok &= check("steady state = rate x months",
                    [round(rep["steady_state_stories"][t]) for t in "ABC"],
                    [60, 36, 6])
        retention.TIER_YEARS.update({"A": 1, "B": 1, "C": 0.5})
        rep = retention.report(stories)
        ok &= check("horizons are honoured",
                    [round(rep["steady_state_stories"][t]) for t in "ABC"],
                    [12, 12, 6])
    finally:
        retention.TIER_YEARS.update(saved)

    print("ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
