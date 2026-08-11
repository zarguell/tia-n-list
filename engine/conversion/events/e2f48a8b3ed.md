Microsoft patched three Edge browser vulnerabilities discovered at the Pwn2Own competition by researcher **Orange Tsai** (DEVCORE Research Team), disclosed June 4.

| CVE | Score | Type | Impact |

|-----|-------|------|--------|

| CVE-2026-45492 | 4.3 | Origin Validation Error | Chained to RCE in current user context |

| CVE-2026-45494 | 5.0 | UXSS | Script execution across any target domain |

| CVE-2026-45495 | **7.5** | **Directory Traversal → RCE** | Full RCE via feedback log file path handling |

CVE-2026-45495 is the most severe — a directory traversal in Edge's feedback log handling that, combined with the other flaws, enables full arbitrary code execution. Patches available via MSRC. **Action:** Update Edge via `edge://settings/help` immediately on all managed endpoints.

---
