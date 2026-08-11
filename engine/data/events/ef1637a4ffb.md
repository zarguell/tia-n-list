Guardio researchers disclosed **CVE-2026-48294** (dubbed **HermeticReader**), a UXSS-class cross-origin data disclosure vulnerability in the **Adobe Acrobat Chrome extension** (329 million installs). The attack chain:

1. A victim visits a malicious webpage

2. The page abuses the extension's internal messaging system — lacking security checks — to activate the **Hermes** integration engine (dormant unless a feature flag is enabled)

3. Once activated, Hermes bridges to **WhatsApp Web** with a predictable Tab ID

4. The attacker silently scrapes private **chats, contacts, and account details** in plain text

No WhatsApp vulnerability, malware, or credential theft is required. Adobe patched the flaw in June after Guardio's disclosure. Despite the massive install base and severe impact, no active exploitation has been publicly confirmed.

**Action:** The Adobe Acrobat Chrome extension auto-updates. Verify your browser has the latest version. Consider disabling the extension if WhatsApp integration is not actively used.

---
