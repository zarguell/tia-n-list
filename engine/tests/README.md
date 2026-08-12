# Runtime verification tests

- `test_sanitize.py` — sanitizer regression suite (runs in CI: `python engine/test_sanitize.py`).
- `verify-stories-all.js` — runs the SHIPPED all-stories inline script (extracted from the
  generated page) against a DOM with the real index data, stubbing fetch. Not in CI (needs
  node + jsdom); run locally after any stories-all.html change:
      cd engine/tests && npm i jsdom 2>/dev/null; node verify-stories-all.js
  Caught 2026-08-12: matches() read `.dataset` off raw index objects, breaking every
  filter (search/year/month threw; initial render passed because empty filters
  short-circuit before the `.dataset` access). Re-run after editing stories-all.html.
