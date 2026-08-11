Veeam released security updates for **CVE-2026-44963**, a critical RCE vulnerability in Backup & Replication 12.3.2.4465 and earlier (fixed in 12.3.2.4854). Any authenticated domain user can exploit the flaw — notably, many organizations join Veeam servers to Windows domains despite Veeam's long-standing best practices. Version 13.x builds are unaffected due to architectural changes.

**Ransomware context:** Veeam backup servers are prime targets — ransomware gangs have explicitly told BleepingComputer they target VBR to block restoration. CISA has flagged four prior Veeam flaws as actively exploited, including CVE-2024-40711 (abused by Akira, Fog, Frag, FIN7). While no active exploitation of CVE-2026-44963 has been reported yet, the disclosure of a patch is the starting gun for exploit development. Apply immediately.

---
