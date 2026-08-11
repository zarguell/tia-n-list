A critical zero-click remote code execution vulnerability in the Windows Netlogon service, tracked as **CVE-2026-41089**, is now being actively exploited in the wild, confirmed by the Center for Cybersecurity Belgium (CCB). Unauthenticated remote attackers can execute arbitrary code with **SYSTEM-level privileges** by sending specially crafted Netlogon network requests — no user interaction, no credentials required.

This zero-click, pre-auth profile makes the flaw exceptionally attractive for automated exploitation, rapid lateral movement, and potential worm-like propagation across poorly segmented environments. Domain controller compromise cascades into full domain takeover: malware deployment via Group Policy, credential manipulation, security control bypass, and lateral movement into connected cloud resources.

**Scope:** All supported Windows Server versions from 2012 onward running as domain controllers. Patched in Microsoft's May 2026 Patch Tuesday (118 CVEs addressed, 16 critical). The CCB recommends prioritizing this as a top-tier emergency remediation item.

**Action:** Patch domain controllers first — particularly those with any internet exposure. Patching alone is insufficient given active exploitation; upscale monitoring for anomalous Netlogon traffic, unusual authentication patterns, sudden privileged group changes, and new admin account creation. Revisit network segmentation around domain controllers and ensure no direct internet exposure.

---
