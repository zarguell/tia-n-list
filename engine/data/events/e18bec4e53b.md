Volexity documented a long-running campaign by **VerdantBamboo** (aka WARP PANDA / UNC5221) that compromised network edge appliances to infiltrate enterprise networks and access Microsoft 365 environments. Discovered during an incident response engagement in September 2025, the operation achieved at least **18 months of persistent access**.

**Tradecraft highlights:**

- Initial compromise of an **Egnyte Storage Sync VM** used as proxy to blend traffic and bypass Conditional Access policies

- Compromised the victim's **MSP via pfSense firewall** — established a beachhead that persisted even after primary remediation

- Deployed **BRICKSTORM** malware in Linux and FreeBSD variants, with separate C2 domains for fallback implants (opsec: if primary is blocked, secondary backdoors remain hidden)

- Exploited a sudo misconfiguration on Egnyte for local privilege escalation; used obfuscated BRICKSTORM variant for FreeBSD/pfSense

- When Egnyte was isolated, pivoted to **Synology NAS** using stolen admin credentials (no MFA) and deployed **PLENET** backdoor

- C2 infrastructure consistently used **Cloudflare IP addresses** with distinct TLS certificates

**Recommendation:** Audit network edge appliances (Egnyte, pfSense, Synology NAS) for unauthorized SSH, cron entries, or unexpected outbound connections. Enforce MFA on all administrative accounts — including MSP-managed devices.

---
