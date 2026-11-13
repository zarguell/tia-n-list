Microsoft's November 2026 Patch Tuesday addressed 1093 CVEs across 287 products and components: 63 critical, 1029 important, and one moderate. Elevation-of-privilege flaws accounted for 48.9% of the fixes and remote code execution for 27.1%. Microsoft Office Word (65), Excel (64), and SQL Server (53) carried the highest CVE counts this month.

Among the specifics, CVE-2026-124194 is a moderate Outlook spoofing vulnerability (CVSS 6.5) in which a crafted Office file can capture a target's NTLMv2 hash for use in follow-on impersonation. The November updates also caused a known printing regression for documents containing zero-width or zero-height images, affecting Word output via GDI on Windows 10 and later and Server 2016 and later.

Administrators should prioritize the 63 critical fixes and validate printing workflows before broad deployment. The volume of EoP and RCE fixes this month, combined with the printing regression, makes staged rollout and rollback planning advisable.
