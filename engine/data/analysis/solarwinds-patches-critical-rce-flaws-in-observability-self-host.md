SolarWinds released patches for two severe remote code execution vulnerabilities in Observability Self-Hosted: CVE-2026-28324 (CVSS 9.8, insufficient integrity check) and CVE-2026-28325 (CVSS 8.8, deserialization of untrusted data). Both can be exploited by remote attackers without authentication and affect all versions up to 2026.2.2; the fix is version 2026.2.3. SolarWinds credited Kai Huang from Armadin for reporting both.

The event also references last week's separate patch for CVE-2026-28326 (CVSS 8.8) in SolarWinds Access Rights Manager, an unauthenticated RCE caused by a hardcoded static key in versions up to 2026.2. SolarWinds makes no mention of any of these three defects being actively exploited in the wild.

What to watch: whether threat actors begin exploiting these unpatched or recently patched SolarWinds flaws and whether CISA or other agencies add any of the three CVEs to known-exploited catalogs.
