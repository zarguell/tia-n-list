CVE-2026-94096 is a critical command injection vulnerability in Netcore NBR200V2 routers running firmware v1.3.241127.071246. The flaw is in /usr/bin/network_tools and carries a CVSS score of 9.4. It is remotely exploitable without authentication.

The vulnerability exists in the network diagnostic utility bundled with the router firmware. An attacker can inject arbitrary OS commands through crafted input to the network_tools binary. Netcore has not yet released a patched firmware version as of this writing.

NBR200V2 is an enterprise-grade wireless router commonly deployed in SMB and branch-office environments. The combination of no authentication requirement and high CVSS score makes this a high-priority patching candidate. Network administrators should restrict management access to trusted interfaces and monitor for unusual network_tools process execution until a fix is available.
