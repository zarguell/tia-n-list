FreeRDP 3.32.0 addresses multiple vulnerabilities, including CVE-2026-111380 (CVSS 8.8) with an integer overflow in the audin buffer calculation leading to a heap out-of-bounds write on macOS and iOS. The advisory also references CVE-2026-111375 and CVE-2026-91962, and notes the fix bypasses an earlier issue tracked as CVE-2026-91962.

Why it matters: FreeRDP is widely deployed in remote desktop, thin-client, and virtualization environments. A heap corruption vulnerability in the audio pipeline allows remote attackers to target clients during session setup. Patching is strongly recommended given the active vulnerability disclosure and specific CVSS rating.

What to watch: whether in-the-wild exploitation is reported, whether vendors integrating FreeRDP (virtual desktop infrastructure providers, embedded devices) release updated builds, and whether CISA includes any of these CVEs in the Known Exploited Vulnerabilities catalog.
