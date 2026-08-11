Xint.io (Theori's AI-driven pentest platform) analyzed AI-generated applications and found **434 exploitable security issues** across three test applications. Key findings:

**Most common flaws:**

1. **Rate limiting / DOS** — 93 flaws (most common). Missing controls lead to runaway server costs or trivial service takedown.

2. **Authorization/IDOR** — 88 flaws. Users accessing data beyond permissions scope.

3. **Access boundary / traversal / SSRF** — 54 flaws.

**Critical-severity flaws (23 found):**

- **Hardcoded secrets** most common at 11 findings

- **Debug-mode RCE** — 6 findings

**Positive trend:** Injection flaws (SQLi, XSS) barely showed up, suggesting AI models have genuinely improved in foundational security code generation. However, **fine-grained authorization breaks as apps grow** — IDOR went from 11% in small apps to 28% in a larger brownfield app.

**Action:** Do not skip security review for AI-generated code. Specifically audit for hardcoded secrets, rate limiting, and authorization boundaries. Use automated scanning tools targeting AI-specific weakness patterns.

---
