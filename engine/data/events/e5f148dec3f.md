Citrix disclosed **six vulnerabilities** in NetScaler ADC and NetScaler Gateway appliances (CVSS 6.9–8.8), including a high-severity memory disclosure flaw discovered by watchTowr that shares a **root cause with the 2023 CitrixBleed** vulnerability — out-of-bounds memory reads triggered by malformed SAML requests.

CVE-2026-8451 affects NetScaler appliances configured as SAML identity providers for single sign-on. The bulletin also includes: two memory overflow DoS conditions, an unauthenticated arbitrary file read vulnerability (management interface exposed), a TCP timestamp memory overread, and an HTTP/2 DoS requiring manual configuration. NetScaler has amassed **20+ KEV entries** in three years. No active exploitation confirmed at disclosure time.

**Recommended action:** Patch to latest NetScaler builds. For the HTTP/2 DoS, manually configure the timeout parameter per Citrix guidance even after patching.

---
