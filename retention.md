# Retention policy — how long a story page stays published

Status: **decided 2026-11-27 (owner): A 3y / B 3y / C 6mo**, report-only.
Nothing is deleted, moved or delisted. `engine/retention.py --report` prices
the policy and `--expiring` is the dry-run sweep; the real sweep is a later,
flag-gated step.

This exists because the site is a research archive whose product is *lasting*.
"Delete old pages" is therefore an editorial promise, not a size knob — so the
rules are written down, derived from facts that never decay, and measured
before anything is removed.

## Tiers

| tier | keeps | horizon | membership |
|---|---|---|---|
| **A** | long | 3 years | `peak_score ≥ 7.5` (the `hottest` display band) **or** cited by an immutable published artifact (a CTI case, and the STIX snapshot built from it) |
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
A       3.0y    1294          326                 11736
B       3.0y     910          183                  6588
C       0.5y    6107         1696                 10178
                                                  28526
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
| 5y / 3y / 6mo | 36,358 |
| **3y / 3y / 6mo (chosen)** | **28,526** |
| 3y / 2y / 6mo | 26,326 |

Today the store holds 11,396 stories and the published artifact is **9,960
files / 143.5 MB** (after the redirect-map change). A plateau of ~28.5k stories
is roughly 2× today in pages — comfortable on GitHub Pages' 1 GB, and
*incompatible with Cloudflare's 20,000-file free cap* at any horizon.

## Dry-run sweep (step 2, running)

`python3 engine/retention.py --expiring` (read-only, nothing deleted):

```
expirable        212     horizon elapsed, no live citation at all
needs-digest       0     expired but a digest page links it — rewrite first
immutable       1294     tier A: never expires
inside          6805     horizon not elapsed
unknown-date       0     unparseable last_seen: never expires (fail safe)
merged          3085     redirect map key, not a page
```

`expires_at()` measures from **last_seen, not first_seen** — a story that keeps
receiving events is live coverage and must not expire on its birthday. Only 212
stories are expirable today because the site is 13 months old; the number grows
to the C-tier plateau (~10k) over the next two years.

## Link integrity outranks deletion

A page may be removed only when nothing published still points at its URL:

- **Immutable citations** (CTI case, STIX snapshot) are why A exists; they are
  never archived while the citation is live.
- **Digest citations** are generated pages, so B's expiry rewrites the digest's
  link to the archive host at rebuild time rather than leaving a dead link.
- **Every archived URL stays resolvable** through `redirects.json` + the 404
  resolver (the primitive landed in #233). Archiving therefore costs one map
  key, not a stub page.

## Archive repo (step 3 scaffolding)

`engine/archive.py` is the only code allowed to move story data out of the hot
store. Layout — data only, private, never published:

```
manifest.jsonl          one appended line per archived story (id, tier, sha256s)
stories/<id>.json       the story record as it left the store
events/<event-id>.{json,md}   only events no live story references
analysis/<id>.md        only when the story brought one (blocked today)
```

```bash
python3 engine/archive.py                          # dry run, report only
python3 engine/archive.py --json                   # machine-readable plan
python3 engine/archive.py --archive-root DIR --apply
python3 engine/archive.py --archive-root DIR --verify
```

It blocks rather than guesses: redirect targets (their URL is a `redirects.json`
key), digest-cited stories (the link rewrite is step 3 proper), stories with an
analysis file, and stories sharing an event with a story that stays. `--apply`
copies every file, appends the manifest line, and only then unlinks the
originals, so an interrupted run leaves a complete archive and an untouched
store; a second run is a no-op.

One-time setup (owner):

```bash
gh repo create zarguell/tia-n-list-archive --private \
  --description "Cold store for aged-out Tia N. List stories (never published)"
git clone git@github.com:zarguell/tia-n-list-archive.git ~/repos/tia-n-list-archive
export TIA_ARCHIVE_ROOT=~/repos/tia-n-list-archive   # in the cron env
```

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
