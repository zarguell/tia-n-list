#!/usr/bin/env python3
"""digest_candidates freshness contract suite — "what's actually new?" (2026-08-14).

The user's complaint: the daily digest headlined "winsock added to the KEV"
three days after CISA actually listed the CVE — it read like catching up with
old news. The brief treated every article's publish date as a fresh
development, so recap articles about an older KEV add kept a story "EVOLVED"
forever.

This suite pins the contracts that fix that:

  1. a recap article (KEV mention, published >= 2 days after the CVE's
     dateAdded) is NOT a development — it cannot re-evolve a story or extend
     its newest-development date;
  2. a KEV add itself IS a development (a CVE listed today evolves the story
     even when every article is older);
  3. a late article with NO KEV mention on a KEV-anchored story is still a
     genuine development (recap classification requires the KEV signal);
  4. non-KEV stories evolve on any new event (no KEV anchor to collapse to);
  5. day-of/next-day KEV reporting is genuine (RECAP_DAYS floor);
  6. the analysis churn marker alone never evolves a story (it is substance,
     not a development);
  7. stale stories are flagged CATCH-UP (newest development >= 2 days old);
  8. merged-away shells stay excluded; coverage resolves through merged_into.

Run: python3 engine/test_digest_candidates.py   (exit 0 = pass)
Wired into CI (site-deploy.yml) and run_engine.sh.
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import digest_candidates as dc  # noqa: E402

TODAY = "2026-08-14"
KEV_CVE = "CVE-2026-68820"  # Windows AFD for WinSock (the real case)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        json.dump(obj, fh)


class Fixture:
    def __init__(self, kev_added=None):
        self.tmp = tempfile.TemporaryDirectory(prefix="tia-dc-")
        self.stories = os.path.join(self.tmp.name, "stories")
        self.events = os.path.join(self.tmp.name, "events")
        self.digests = os.path.join(self.tmp.name, "digests")
        self.kev = os.path.join(self.tmp.name, "kev")
        if kev_added:
            write_json(os.path.join(self.kev, "index.json"),
                       {"cves": [{"cve_id": KEV_CVE, "kev_date_added": kev_added}]})

    def event(self, eid, published, title, content=""):
        write_json(os.path.join(self.events, eid + ".json"),
                   {"id": eid, "published_at": published, "title": title,
                    "content_md": content, "kind": "update", "source": "example.com"})
        return {"event_id": eid, "label": "update"}

    def story(self, slug, evs, cves=None, score=5.5, analysis_at=None, merged_into=None):
        s = {"id": slug, "title": slug.replace("-", " ").title(), "cves": cves or [],
             "n_sources": 3, "score": score, "events": evs}
        if analysis_at:
            s["analysis"] = {"updated_at": analysis_at, "score": score}
        if merged_into:
            s["merged_into"] = merged_into
        write_json(os.path.join(self.stories, slug + ".json"), s)
        return s

    def digest(self, date, slugs):
        write_json(os.path.join(self.digests, date + ".json"),
                   {"date": date, "stories": slugs})

    def compute(self):
        dates = dc.digest_dates(self.digests)
        last_digest = [d for d in dates if d < TODAY][-1]
        since = dc.parse_utc(last_digest + "T00:00:00Z")
        recent_cutoff = dates[-dc.COVERAGE_WINDOW] if len(dates) >= dc.COVERAGE_WINDOW else dates[0]
        stories = dc.load_stories(self.stories)
        events = dc.load_events(self.events)
        kev_map = dc.kev_date_map(self.kev)

        def canonical(slug, seen=None):
            seen = seen or set()
            if slug in seen or slug not in stories:
                return slug
            seen.add(slug)
            target = stories[slug].get("merged_into")
            return canonical(target, seen) if target else slug

        coverage = dc.load_coverage(stories, canonical, self.digests)
        rows = dc.build_rows(stories, events, kev_map, coverage, canonical,
                             since, recent_cutoff, TODAY, last_digest)
        return {r["slug"]: r for r in rows}, coverage

    def close(self):
        self.tmp.cleanup()


def row(fx, slug):
    rows, _ = fx.compute()
    assert slug in rows, f"{slug} missing from rows: {list(rows)}"
    return rows[slug]


def test_recap_does_not_evolve_or_extend_freshness():
    """The AFD/WinSock regression: KEV added 3 days ago, one recap article
    published yesterday -> story must NOT be evolved and MUST be CATCH-UP."""
    fx = Fixture(kev_added="2026-08-11")
    fx.digest("2026-08-12", ["afd"])
    fx.digest("2026-08-13", ["afd"])  # covered yesterday
    evs = [
        fx.event("e1", "2026-08-11T17:55:59Z", "Job Offer Becomes a Zero-Day Attack"),
        fx.event("e2", "2026-08-12T15:38:08Z", "Lazarus hackers exploited Windows zero-day"),
        fx.event("e3", "2026-08-13T11:08:27Z", "CISA Adds Actively Exploited Windows WinSock Vulnerability to KEV Catalog",
                 content="added to the Known Exploited Vulnerabilities catalog"),
    ]
    fx.story("afd", evs, cves=[KEV_CVE])
    r = row(fx, "afd")
    assert r["evolved"] is False, "recap article must not evolve a story"
    assert r["new_events_since"] == 0, "recap must not count as a new event"
    assert r["newest_development_at"] == "2026-08-12", \
        f"recap must not extend newest development (got {r['newest_development_at']})"
    assert r["stale_days"] == 2
    assert r["catchup"] is True, "3-day-old development must be CATCH-UP"
    assert r["kev_added"] == "2026-08-11"
    assert r["tag"] == "UPDATE"
    fx.close()


def test_kev_add_today_is_a_development():
    """Same story, but CISA lists the CVE today: the add itself evolves it."""
    fx = Fixture(kev_added=TODAY)
    fx.digest("2026-08-12", ["afd"])
    fx.digest("2026-08-13", ["afd"])
    evs = [
        fx.event("e1", "2026-08-11T17:55:59Z", "Job Offer Becomes a Zero-Day Attack"),
        fx.event("e2", "2026-08-12T15:38:08Z", "Lazarus hackers exploited Windows zero-day"),
    ]
    fx.story("afd", evs, cves=[KEV_CVE])
    r = row(fx, "afd")
    assert r["evolved"] is True, "a KEV add since the boundary is a development"
    assert r["new_events_since"] == 1
    assert r["newest_development_at"] == TODAY
    assert r["stale_days"] == 0
    assert r["catchup"] is False
    fx.close()


def test_late_article_without_kev_mention_is_genuine():
    """Recap classification requires the KEV signal: a late non-KEV article on a
    KEV-anchored story is still a development."""
    fx = Fixture(kev_added="2026-08-11")
    fx.digest("2026-08-13", ["afd"])
    evs = [
        fx.event("e1", "2026-08-11T17:55:59Z", "Job Offer Becomes a Zero-Day Attack"),
        fx.event("e2", "2026-08-13T09:00:00Z", "Exploit chain expands to new targets"),
    ]
    fx.story("afd", evs, cves=[KEV_CVE])
    r = row(fx, "afd")
    assert r["evolved"] is True, "late non-KEV article is a genuine development"
    assert r["new_events_since"] == 1
    assert r["newest_development_at"] == "2026-08-13"
    assert r["catchup"] is False
    fx.close()


def test_non_kev_story_evolves_on_any_new_event():
    fx = Fixture()
    fx.digest("2026-08-13", ["breach"])
    evs = [
        fx.event("e1", "2026-08-11T10:00:00Z", "Breach disclosed"),
        fx.event("e2", "2026-08-13T10:00:00Z", "More victims named"),
    ]
    fx.story("breach", evs, cves=["CVE-2026-99999"])
    r = row(fx, "breach")
    assert r["evolved"] is True
    assert r["kev_added"] is None
    assert r["catchup"] is False
    assert r["stale_days"] == 1
    fx.close()


def test_day_of_kev_reporting_is_genuine():
    """An article the same day as the add (RECAP_DAYS floor) is a real report,
    not a recap — even with the KEV mention."""
    fx = Fixture(kev_added="2026-08-11")
    fx.digest("2026-08-10", ["afd"])
    evs = [
        fx.event("e1", "2026-08-11T18:00:00Z", "CISA adds WinSock flaw to KEV Catalog"),
    ]
    fx.story("afd", evs, cves=[KEV_CVE])
    r = row(fx, "afd")
    assert r["evolved"] is True, "day-of KEV reporting is a genuine development"
    assert r["newest_development_at"] == "2026-08-11"
    fx.close()


def test_analysis_churn_does_not_evolve():
    """A fresh analysis marker with no new event is substance, not a delta."""
    fx = Fixture()
    fx.digest("2026-08-13", ["story"])
    evs = [fx.event("e1", "2026-08-11T10:00:00Z", "Original report")]
    fx.story("story", evs, analysis_at="2026-08-14T09:00:00Z")
    r = row(fx, "story")
    assert r["evolved"] is False, "analysis churn alone must not evolve a story"
    assert r["has_analysis"] is True
    assert r["analysis_at"] == TODAY
    fx.close()


def test_eventless_story_is_safe():
    fx = Fixture()
    fx.digest("2026-08-13", [])
    fx.story("quiet", [], cves=[KEV_CVE], score=4.0)
    r = row(fx, "quiet")
    assert r["newest_development_at"] is None
    assert r["stale_days"] is None
    assert r["catchup"] is False
    assert r["evolved"] is False
    fx.close()


def test_merged_shells_excluded_and_coverage_resolves():
    fx = Fixture()
    fx.digest("2026-08-13", ["old-shell"])  # digest linked the pre-merge shell
    fx.story("old-shell", [], merged_into="canonical")
    fx.story("canonical", [fx.event("e1", "2026-08-12T10:00:00Z", "Canonical report")])
    rows, coverage = fx.compute()
    assert "old-shell" not in rows, "redirect shells are never digest candidates"
    assert coverage["canonical"] == "2026-08-13", \
        "coverage of a shell must credit the canonical story"
    fx.close()


def main():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\n{len(tests)} checks passed")


if __name__ == "__main__":
    main()
