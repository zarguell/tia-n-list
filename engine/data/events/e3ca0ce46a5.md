Qualys has published a detailed technical analysis of the "FortiBleed" campaign — large-scale credential exposure and abuse targeting internet-reachable FortiGate management and SSL-VPN gateways. The analysis maps eight relevant Fortinet CVEs (including CVE-2026-24858, CVE-2025-59718, and CVE-2025-59719) to Qualys QIDs and provides QQL queries for VMDR, ETM, and CSAM to identify and prioritize exposed assets.

Key finding: a patched device can remain compromised if credentials or configuration material were stolen before remediation, particularly where PBKDF2 migration and legacy-hash cleanup are incomplete. The post provides detection and threat-hunting guidance across four areas: authentication anomalies, configuration and account changes, downstream identity activity, and exposure and integrity validation.

**Recommended action:** Treat Qualys QID matches as investigation seeds, not confirmed compromise. Revoke sessions, rotate credentials, enforce MFA, and validate PBKDF2 migration and configuration integrity on all FortiGate devices — even those already patched.

---
