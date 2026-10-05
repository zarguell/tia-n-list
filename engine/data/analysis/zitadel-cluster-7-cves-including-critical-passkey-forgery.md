The ZITADEL identity platform has a cluster of seven CVEs, with CVE-2026-105209 peaking at CVSS 9.3. The critical flaw allows forging the x-zitadel-orgid header to issue passkey enrollment for any user in any organization. Additional CVEs in the cluster include CVE-2026-105210, CVE-2026-105211, and CVE-2026-105215.

Passkey forgery across organizational boundaries is a severe authentication bypass. If an attacker can enroll a passkey for an arbitrary user, subsequent access does not require the legitimate user's credentials. This undermines ZITADEL's core identity model and affects all organizations relying on it.

Organizations using ZITADEL should upgrade immediately and audit passkey enrollments for unexpected entries. Watch for a vendor advisory that maps each CVE to specific versions and provides mitigation steps. No exploitation reports are cited yet, but the severity warrants emergency patching.
