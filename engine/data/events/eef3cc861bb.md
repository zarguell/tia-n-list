Just one day after Ivanti released patches for a maximum-severity OS command injection in Sentry secure mobile gateways, the Shadowserver Foundation reported that attackers had already backdoored virtually every reachable exposed instance. CVE-2026-10520 allows unauthenticated remote code execution as root via a crafted request. Shadowserver identified 19 vulnerable instances in its scans, with at least 2 confirmed backdoored, and noted "if you have not patched now you are most likely compromised" — Ivanti's own advisory still states "no evidence of exploitation at time of disclosure" as of this writing.

**Prior context (June 10):** Ivanti patched CVE-2026-10520 on Tuesday alongside an auth bypass (CVE-2026-10523, CVSS 9.9). CISA has flagged 34 Ivanti CVEs as actively exploited. Every exposed Sentry instance should be treated as compromised — rebuild from known-good firmware.

---
