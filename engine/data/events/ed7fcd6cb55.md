*Initial disclosure, incomplete-first-fix, and Huntress telemetry covered Aug 3. New today: CISA added CVE-2026-18577 to the KEV catalog (Aug 3, first KEV addition since Jul 29), and N-able confirms hotfix 2026.3.1.7 is the only unaffected build.*

CISA formally added **CVE-2026-18577** (N-able N-central authentication bypass using an alternate path/channel) to its Known Exploited Vulnerabilities catalog on **August 3**, binding FCEB agencies under BOD 26-04 to urgent remediation and pre-patch compromise checks — and confirming federal recognition of the in-the-wild exploitation N-able disclosed August 1.

- N-able's Sunday hotfix **2026.3.1.7** addresses the flaw across all N-central versions before 2026.3; **hosted deployments are already updated, on-premises customers must install manually**.

- Recall from Aug 3 coverage: the original advisory (CVE-2026-18556) was an incomplete patch; **CVE-2026-18577** is the bypass of that patch affecting *all* supported versions, giving unauthenticated attackers god-mode RMM console access — with downstream reach into every MSP-managed endpoint (Huntress documented Take Control abuse and Cloudflare-tunnel persistence). Huntress reported 55.6% of reachable cloud N-central servers unpatched as of Aug 3.

- **IOCs:** `87.249.138[.]34`, `37.19.210[.]32`, `37.153.90[.]88`, `92.118.112[.]181`.

**Action:** Apply 2026.3.1.7 immediately (on-prem is manual — verify, don't assume). Audit for suspicious logins, new Take Control sessions, and unexpected Cloudflare tunnel processes; hunt the four IOCs. KEV listing means this should now be at the top of every vulnerability-management queue.
