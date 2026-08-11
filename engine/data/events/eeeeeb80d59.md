ReliaQuest identified a previously undocumented China-linked espionage cluster, tracked as **OP-512**, deploying a purpose-built web shell framework targeting Internet Information Services (IIS) servers. The compromised server ran Windows Server 2016 with end-of-life .NET Framework 4.0 — EDR telemetry had flagged anomalous DNS queries 75 days before the main intrusion.

**Tradecraft highlights:**

- **Self-reporting web shell:** An `.aspx` file manager encodes its own URL into hex-segmented DNS queries on access — fire-and-forget deployment that automatically reports its location to operator infrastructure

- **Dual-channel crypto:** Two `.ashx` command handlers, each with a **unique RSA public key** (separate private keys required per implant). Command pipeline: Base64 → RC4 decrypt → RSA signature verification → execution

- **Timestomping:** All three shells scan surrounding files, calculate a median last-modified timestamp, and backdate themselves — a web shell dropped in 2026 reads forensically as if placed in 2022

- **In-memory privilege escalation:** Loaded Potato Suite (BadPotato, SweetPotato, EfsPotato) via reflective .NET assembly loading — nothing written to disk

OP-512 is at least the **fourth China-linked cluster** targeting IIS servers in under a year, joining CL-STA-0048, GhostRedirector, and DragonRank. Base64-encoded `whoami` commands matched character-for-character with ReliaQuest's documented Flax Typhoon ArcGIS compromise, suggesting shared playbooks across the ecosystem.

**Detection:** Signature-based detection is ineffective by design. Focus on outbound DNS from `w3wp.exe` with long hex-segmented subdomains; reflective .NET assembly loading in IIS worker processes; and new DLL generation in ASP.NET temporary compilation directories outside deployment windows.

---
