Microsoft's November 2026 Patch Tuesday fixes 1,094 vulnerabilities (63 critical, 1,029 important, 1 moderate) across 287 products, the second-largest monthly release on record. Elevation of privilege accounts for 48.9% of the fixes and remote code execution 27.1%. The single zero-day is CVE-2026-124194, a moderate (CVSS 6.5) Outlook spoofing flaw that leaks NTLMv2 hashes when a target opens a crafted Office file; it is fixed through Office updates rather than the Windows cumulative update.

The zero-day is actively exploited and Microsoft classifies it as publicly disclosed or actively exploited with no official fix previously available. Office channels should move first. Other heavy counts this month include Microsoft Office Word (65 CVEs), Excel (64), and SQL Server (53).

Some outlets report 1,235 to 1,260 total flaws by including fixes released earlier in the month; the 1,094 figure counts only Patch Tuesday-day releases. Plan Office-first patching and verify NTLMv2 hash exposure for affected users.

