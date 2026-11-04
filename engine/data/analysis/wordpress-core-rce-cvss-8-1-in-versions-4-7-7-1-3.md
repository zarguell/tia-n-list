CVE-2026-119977 is a high-severity WordPress Core flaw caused by a TOCTOU race condition in the full-package core upgrade process, reported by Picus Security researcher Umut Bayram. Predictable, web-accessible staging paths during upgrades can let unprivileged remote attackers execute code on the server. CISA added the flaw to its Known Exploited Vulnerabilities Catalog and confirmed active exploitation, ordering federal agencies to patch by Friday under BOD 26-04.

WordPress 7.1.4, released October 28, patches the issue along with 21 other security vulnerabilities. The flaw affects WordPress versions 4.7 through 7.1.3. Site operators should update to 7.1.4 immediately and verify no unauthorized files remain in staging directories.

Because exploitation occurs during the upgrade window, delayed or partial updates leave sites exposed. Defenders should also check for signs of compromise on sites upgraded in the affected period.
