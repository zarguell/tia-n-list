*Previously covered July 17-21 (SharePoint exploitation cluster, CVE-2026-58644). New: A different SharePoint CVE — CVE-2026-50522 — now being exploited for machine key theft.*

A **critical unauthenticated RCE vulnerability** in Microsoft SharePoint (CVE-2026-50522, deserialization-of-untrusted-data) is under active exploitation. watchTowr confirmed that within **hours** of a public PoC becoming available on July 20, their global honeypot network captured exploitation attempts that successfully **stole machine keys** from vulnerable on-premise SharePoint servers.

Attackers obtaining machine keys can create valid authentication tokens to impersonate any user and access SharePoint sites and documents indefinitely — **even after the server is patched**. Microsoft patched the flaw in the July 2026 Patch Tuesday but did not mark it as actively exploited at the time.

This is separate from the previously tracked CVE-2026-58644 (the deserialization RCE in the earlier exploitation cluster). Together, they represent a **two-front attack** on on-premise SharePoint deployments.

**Action:** Immediately patch CVE-2026-50522. After patching, **rotate machine keys** on any server that was internet-exposed prior to patching. Hunt for unauthorized authentication tokens.

---
