A critical zero-day vulnerability discovered by **Marcus Hutchins** (MalwareTech) in Comodo Internet Security's firewall driver `Inspect.sys` allows remote attackers to crash a target Windows system with a **single IPv6 packet**, bypassing all firewall rules. Dubbed **ComoDoS**, the flaw is an integer underflow in the IPv6 extension header parser that wraps `payload_length` to ~18 quintillion bytes, causing immediate system crash at DISPATCH_LEVEL.

**Key technical details:**

- The crash is triggerable regardless of firewall rules or open/closed ports — the IPv6 parsing occurs *before* enforcement

- A reachable OOB-write primitive via `memcpy` with a 4 GB copy size exists but is too large to survive under realistic network conditions, making RCE unlikely with this bug alone

- Hutchins submitted a full root-cause analysis, patch recommendations, and PoC to Comodo — **received no acknowledgment** despite two follow-ups

- This follows ZDI's nearly two-year failed attempt to get Comodo to patch a separate vulnerability (ZDI-24-953)

- Full PoC published on GitHub via Scapy: `IPv6 + IPv6ExtHdrDestOpt + TCP`

**Verdict:** RCE is unlikely from this specific bug, but the crash (DoS) is trivial to trigger remotely. Organizations using Comodo Internet Security should monitor for a vendor response and consider alternative endpoint protection if none materializes.

---
