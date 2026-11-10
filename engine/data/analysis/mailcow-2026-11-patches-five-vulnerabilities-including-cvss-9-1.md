Mailcow's 2026-11 release fixes five vulnerabilities, and proof-of-concept details for all five are already public. The most severe is a cross-tenant remote code execution flaw rated CVSS 9.1. Mailcow is a dockerized mail server suite, and a cross-tenant RCE means one tenant could break out of its own environment and run code elsewhere on the host or in other tenants.

Public proof-of-concept steps lower the bar for attackers and make unpatched instances easy targets. The fixed version is 2026-11, and the advisory urges administrators to update as soon as possible. Instances that expose the mailcow web interface or API to untrusted networks face the highest risk.

The five flaws were not individually identified in the posting, so administrators should treat the update as a bundle and review the release notes when the vendor publishes per-issue detail. Watch for scans targeting mailcow installations and for the vendor to link each CVE to its fixed component.
