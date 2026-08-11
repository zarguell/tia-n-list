Proofpoint threat researchers published analysis of an ongoing espionage campaign targeting physics and engineering departments at US and Canadian universities. The threat cluster, tracked as UNK_MassTraction, exploited a two-CVE chain in the Roundcube open-source email client:

- **CVE-2024-42009** — Remote code execution via XSS in Roundcube (requires victim to open a crafted email)

- **CVE-2025-49113** — Post-authentication RCE to gain persistent foothold on the mailserver

Proofpoint identified fewer than 10 confirmed university victims but estimates "a few dozen" may be impacted, noting "there is a high likelihood that many victims have not been made aware of this activity yet." The campaign, first observed in May 2026, targets administrators and professors with national security links or research in astrophysics and particle physics. Attackers deployed webshells and backdoors for persistent access and data exfiltration. The campaign is ongoing.

**Recommended action:** Verify Roundcube versions against CVE-2024-42009 and CVE-2025-49113 patches. Monitor for anomalous webshell activity on university mailservers. Alert institutional security teams at physics/engineering research departments.

---
