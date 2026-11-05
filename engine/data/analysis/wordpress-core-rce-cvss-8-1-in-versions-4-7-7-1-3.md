WordPress Core contains CVE-2026-119977, an unauthenticated time-of-check time-of-use race condition that becomes a remote code execution during core updates. Versions prior to 7.1.4 are affected, and WordPress released 7.1.4 on October 28, 2026 along with fixes for 22 security vulnerabilities. The Hacker News first disclosed the flaw on October 29. The flaw carries CVSS 8.1.

Exploitation is live. Wordfence reported 58,693 blocked attacks in 24 hours - nearly 60,000 attempts rather than confirmed successful compromises - and The Hacker News described nearly 63,000 attempts around the October 29 disclosure. CISA added CVE-2026-119977 to the KEV catalog on November 3, 2026.

The flaw sits in the full-package core upgrade path, where the installer unpacks into a predictable location and gives attackers a brief window during an update. Watch for confirmed compromises beyond blocked attempts and for any active exploitation kits.
