# Retention policy — how long a story page stays published

Status: **proposal, report-only**. Nothing is deleted, moved or delisted by
this policy yet. `engine/retention.py --report` prices it against the live
store; the archive sweep is a later, flag-gated step.

This exists because the site is a research archive whose product is *lasting*.
"Delete old pages" is therefore an editorial promise, not a size knob — so the
rules are written down, derived from facts that never decay, and measured
before anything is removed.

## Tiers

| tier | keeps | horizon | membership |
|---|---|---|---|
| **A** | long | 5 years | `peak_score ≥ 7.5` (the `hottest` display band) **or** cited by an immutable published artifact (a CTI case, and the STIX snapshot built from it) |
| **B** | medium | 3 years | digest-cited, or `peak_score ≥ 5.0` (`hot` band) |
| **C** | short | 6 months | everything else |

Peak thresholds are the site's own display bands, so a page's tier is
explainable from its badge: "this story was *hottest* at some point".

## Two invariants, both non-negotiable

**Monotone — a hot story never loses its long TTL by cooling.** Tier
membership is a function of `peak_score` (the high-water mark written by
`score.update_peak`, which never decreases) and of citations (permanent once
published) — never of the current score, which decays with a 36 h half-life. A
story that peaked at 8.0 in March stays tier A in 2031 even though its live
score has been 0.0 since March. `test_retention.py` pins exactly that.

**Fail safe — unknown is not zero.** A missing, unparseable or out-of-range
`peak_score` classifies as *unknown*, which promotes the story to A and is
counted separately in the report. The store once held ~8.2k stories with no
peak field at all (before the 2026-09 backfill), so absence must never be read
as "never mattered".

## What it costs (measured 2026-11-27)

`python3 engine/retention.py --report`, excluding merged shells (they are one
`redirects.json` key, not a page):

```
tier   keep    live   stories/mo   stories at plateau
A       5.0y    1294          326                 19580
B       3.0y     910          183                  6600
C       0.5y    6107         1696                 10178
                                                  36358
```

The arithmetic is deliberately blunt: plateau = (recent 3-month rate) ×
(horizon in months). Two consequences worth stating plainly:

- **The peak threshold is not the lever; the horizon is.** Tier A is 326/month
  of which only ~95/month is `peak ≥ 7.5`; the rest is CTI-cited. Moving the
  peak cut from 7.5 to 8.0 changes ~18 stories a year.
- **Any "forever" class is unbounded by construction.** 3,000 stories/month
  of input means every open-ended tier grows without limit; only horizons make
  a plateau.

Alternatives, same measurement:

| horizons (A/B/C) | stories at plateau |
|---|---|
| 5y / 3y / 6mo (proposed) | 36,358 |
| 3y / 3y / 6mo | 28,526 |
| 3y / 2y / 6mo | 26,326 |

Today the store holds 11,396 stories and the published artifact is **9,960
files / 143.5 MB** (after the redirect-map change). A plateau around 36k
stories is roughly 2.5× today in pages — comfortable on GitHub Pages' 1 GB, and
*incompatible with Cloudflare's 20,000-file free cap* at any horizon.

## Link integrity outranks deletion

A page may be removed only when nothing published still points at its URL:

- **Immutable citations** (CTI case, STIX snapshot) are why A exists; they are
  never archived while the citation is live.
- **Digest citations** are generated pages, so B's expiry rewrites the digest's
  link to the archive host at rebuild time rather than leaving a dead link.
- **Every archived URL stays resolvable** through `redirects.json` + the 404
  resolver (the primitive landed in #233). Archiving therefore costs one map
  key, not a stub page.

## Rollout

1. **Report only** (this change): `--report` and `--horizons` price every
   variant; nothing is touched.
2. **Dry-run sweep**: compute the set that *would* expire per tier, diff it
   against the staged artifact (files + bytes), publish the numbers — still no
   deletion.
3. **Archive sweep** behind a flag, per tier, with `retention_class` /
   `retention_reason` stamped once into the story JSON at the moment a tier is
   assigned (monotone: upgrade-only) so every removal is auditable years
   later.

Step 3 must also land the storage side first: expired story data goes to the
archive repo (source of truth, never published), and any URL that stays
referenced gets its `redirects.json` key.
