Attackers are actively exploiting CVE-2026-5027 (high-severity), a path traversal vulnerability in Langflow's file upload endpoint (`POST /api/v2/files`). The filename parameter is unsanitized, allowing `../` sequences to write arbitrary files. Langflow enables unauthenticated auto-login by default — a single request yields a valid session token, no credentials required.

Discovered by Tenable (reported January 2026, publicly disclosed March 27 after no vendor response). Fixed in langflow-base 0.8.3 and Langflow 1.9.0. VulnCheck honeypots confirmed active exploitation dropping test files. Censys scans identified ~7,000 publicly exposed instances (historical, 12-month window). Recommended version: 1.10.0. Previous Langflow flaws (CVE-2026-0770, CVE-2026-21445, CVE-2026-33017) have also been exploited, including by MuddyWater (Iranian APT).

---
