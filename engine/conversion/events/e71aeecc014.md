The DFIR Report published a comprehensive incident analysis of a July 2025 intrusion where a user searching Bing for "ManageEngine OpManager" was lured to a lookalike domain, ultimately delivering Bumblebee malware via trojanized MSI, followed by AdaptixC2 C2, full domain compromise, 77GB of exfiltration, and Akira ransomware deployment.

Key findings from the full writeup:

- **Initial access:** SEO poisoning via Bing — the threat actor used a two-tier delivery infrastructure with cloned download pages (opmanager[.]pro) and shared delivery gateways (download-center[.]online) on Hostinger (AS47583), signed with a certificate issued to "LLC Vector"

- **C2 stack:** BumbleBee (DGA domains) → AdaptixC2 beacon (172.96.137[.]160) → reverse SSH tunnel → RustDesk for persistent access

- **Credential harvesting:** NTDS.dit extraction via wbadmin.exe, Veeam credential decryption via DPAPI, LSASS dumping via lsassy, systematic credential store enumeration (password managers, browser data, cloud platform credentials, development directories)

- **Exfiltration:** ~77GB over two SFTP sessions via FileZilla to a server in Ukraine (185.174.100[.]203)

- **Ransomware:** Akira deployed as `locker.exe` targeting specific drive paths with partial encryption (`-n=15`) to accelerate the process; Shadow Copies deleted via WMI PowerShell commands

- **Swisscom parallel:** A second intrusion with near-identical TTPs — service termination via WMIC targeting SQL/IIS, staged `win.exe` payload with `netonly` flag

**Detection opportunities:** Monitor Bing/organic search traffic to enterprise software download pages, particularly SEO-ranked lookalike domains. Event ID 5145 for systematic credential store scanning patterns. DGA DNS queries from non-browser processes. FileZilla installation via RDP clipboard in enterprise environments.

---
