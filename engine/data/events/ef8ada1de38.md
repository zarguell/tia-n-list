A newly identified Lazarus subgroup has been targeting financial institutions and cryptocurrency organizations with a sophisticated malware framework operating almost entirely in memory, according to researchers at Fox-IT (Cognyte). The three-component toolset — **DPAPILoader**, **RemotePELoader**, and **RemotePE** — uses Windows Data Protection API (DPAPI) for environmental keying that binds malware execution to a specific victim environment, making traditional hash-based detection ineffective.

The infection chain: DPAPILoader decrypts and launches the next stage using DPAPI → RemotePELoader retrieves the final payload from attacker-controlled infrastructure entirely in memory → RemotePE RAT provides command execution, file manipulation, process management, and data access. Environmental keying means each deployment generates a unique encrypted payload — a deliberate shift toward stealth-first tradecraft that reduces forensic visibility and enables long-term access.

**Recommended action:** Monitor for suspicious DPAPI function calls (`CryptProtectData`/`CryptUnprotectData`) from unusual processes. Deploy behavioral detection for memory-only execution patterns.

---
