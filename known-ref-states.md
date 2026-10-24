# Known reference states (so audits stop re-raising settled items as rot)

Committed, code-side record of reference conditions the owner has already
decided about. `cronman/lib/ref_liveness.py` is FLAG-ONLY by contract
(removal needs explicit owner sign-off), so a settled state has to be
recorded here or every later audit re-opens it.

## Classification reminder (cronman `ref_liveness.classify`)

| status | meaning | rot? |
| --- | --- | --- |
| `alive` | HTTP < 400 | no |
| `dead` | 404 / 410 — definitive rot | yes (owner triage) |
| `walled` | 401 / 403 / 407 / 429 — bot wall / rate limit (Reuters, BleepingComputer) | no |
| `unreachable` | DNS/timeout/reset/5xx — transient, rechecked daily | no |

`dead` and `unreachable` are deliberately distinct classes: only 404/410 is
ever rot, and only `dead` should ever be proposed for removal.

## Standing disposition: host-wide `unreachable` with no archive snapshot

- **Owner decision** (2026-10-21 audit Issue 6 / Rec 6, batch
  20261024T130156Z decision `a365461eedca`): a **host-wide** `unreachable`
  classification — DNS resolves, TCP connect times out for every URL on the
  host, including the bare site root — with **no Wayback snapshot** is a
  **known state**, not article rot. Later audits must treat it as known and
  must not re-raise it as rot per record, per day.
- Why it is not rot: nothing on the host answers, so no individual reference
  can be judged; the class is transient/rechecked daily
  (`unreachable` TTL = 1 day in `ref_liveness.TTL_DAYS`) and the host did
  answer when the records were authored.
- Re-raise only when the evidence changes: at least one URL on the host
  returns `dead` (404/410) — i.e. the host is answering again and the
  specific reference is gone — or the owner says so. Removal still needs
  explicit owner sign-off.

### Known instance: `cybersecuritynews.com` (2026-10-21)

Observed 2026-10-21: DNS resolved (35.212.63.154), TCP connect timed out at
25s for every path *and* for `https://cybersecuritynews.com/`; cronman's
ref-liveness cache recorded 3 such URLs `unreachable` at 2026-10-21T11:34Z;
no Wayback snapshot for any of them.

Owner decision: **keep the references** — no data change. The four CTI
records that cite the host keep their URLs as written:

- `the-internet-goes-on-high-alert-after-discovery-of-8-compromised` →
  `https://cybersecuritynews.com/emudhra-security-compromise/`
- `north-korea-linked-malware-abuses-ethereum-transactions-as-cover` →
  `https://cybersecuritynews.com/ethereum-secret-messaging-system/`
- `threat-actors-abuse-chatgpt-custom-gpts-to-deliver-rat-payloads` →
  `https://cybersecuritynews.com/chatgpt-custom-gpt-malware/`
- `openai-agents-flood-rubygems-with-2-000-packages-and-exploit-bui` →
  `https://cybersecuritynews.com/`

Rec 6's follow-up ("prefer sources that answer without a bot wall", host
watch) is folded into this disposition, not carded separately: when the host
answers again, `ref_liveness` re-checks the URLs within its TTL and a
genuine 404/410 surfaces as `dead`.
