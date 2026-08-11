*Previously covered Jul 24 (Clop exploiting CVE-2026-12569). New today: ReliaQuest and Ransom-ISAC publish detailed campaign analysis with new IoCs.*

A **Cl0p ransomware affiliate** continues exploiting **CVE-2026-12569** (CVSS 9.3) in PTC Windchill and FlexPLM enterprise PLM systems. New campaign intelligence:

- Attack chain: pre-authentication information disclosure in FlexPLM WSDL endpoint chained with server-side flaw in Windchill login servlet to achieve RCE and deploy JSP webshells

- **Campaign active since July 20**, targeting **aerospace, automotive, manufacturing, and retail/apparel** sectors

- Attackers enumerate filesystems, stage data, and exfiltrate for extortion

- Extortion emails sent with subject line **"Windchill PDMLink module serious data leak"** to hundreds of users per victim

- As of July 22, Cl0p has not yet listed victims on its dark web leak site

**Action:** Patch CVE-2026-12569 immediately. Hunt for JSP webshells under `/Windchill/login/`. Block extortion email domains. CISA added this CVE to KEV on June 25 — any internet-exposed, unpatched instance should be treated as potentially compromised.

---
