# Runtime verification tests

- `test_sanitize.py` — sanitizer regression suite (runs in CI: `python engine/test_sanitize.py`).
- `verify-stories-all.js` — runs the SHIPPED all-stories inline script (extracted from the
  generated page) against a DOM with the real index data, stubbing fetch. Runs in CI
  (site-deploy.yml: setup-node + scratch-dir jsdom, after the build step) and locally:
      cd engine/tests && npm i jsdom 2>/dev/null; node verify-stories-all.js
  Caught 2026-08-12: matches() read `.dataset` off raw index objects, breaking every
  filter (search/year/month threw; initial render passed because empty filters
  short-circuit before the `.dataset` access). Re-run after editing stories-all.html.
- `verify-kev.js` — behavioral XSS + filter/sort/paginate checks for the kev dashboard
  (fetches kev/kev-index.json, asserts hostile rows render as text only — no img/svg
  elements, no handlers fire, no data interpolation in the inline script). Same CI + local
  recipe as verify-stories-all.js. Re-run after editing the kev dashboard template.
