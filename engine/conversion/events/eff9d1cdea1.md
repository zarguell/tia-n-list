The **Clop/Cl0p** ransomware gang is actively exploiting **CVE-2026-12569**, a critical improper input validation vulnerability (CVSS 9.3) in **PTC Windchill** and **FlexPLM** enterprise systems, in a data-theft extortion campaign documented by ReliaQuest and Ransom-ISAC.

Key details:

- Exploitation enables **unauthenticated remote code execution**

- Clop operators deploy **JSP webshells** to exfiltrate sensitive product data

- Extortion emails sent from `support@cryptohox.com` (multiple variants)

- Targets **Internet-exposed Windchill and FlexPLM instances**

- Attribution to Cl0p based on tradecraft overlap with prior enterprise-targeting campaigns

- CVE-2026-12569 already on **CISA KEV** since June 25

**Action:** Immediately identify and patch all Internet-exposed PTC Windchill and FlexPLM instances. Hunt for JSP webshells under `/Windchill/login/`. Block email domains associated with extortion outreach.

---
