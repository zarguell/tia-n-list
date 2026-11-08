SonicWall advisory AV26-1133, dated 2026-11-06, covers CVE-2026-19868 (PSIRT advisory SNWLID-2026-0014), an authentication enforcement flaw in the SonicOS SSLVPN service. A user with valid credentials for an alternate authentication method can bypass SAML controls, including SAML-enforced multi-factor authentication. The CVE record carries CWE-308 with a CVSS 3.1 base score of 7.5.

Affected builds are Gen7 and Gen8 SonicOS 7.3.3-7015 and older, and 8.2.2-8015 and older; the fixed releases are 7.3.4-7013 and 8.2.2-8015. NIST NVD published its entry on 2026-11-06 sourcing SonicWall, and CISA added CVE-2026-19868 to its Known Exploited Vulnerabilities catalog the same day.

Because the flaw sits in SSLVPN authentication and is already in the KEV catalog, exposed SonicOS gateways should be prioritized for patching to 7.3.4-7013 or 8.2.2-8015. MFA bypass means multi-factor authentication alone does not protect vulnerable gateways.
