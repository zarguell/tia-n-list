Seqrite's Threat Research Unit documented an active malware campaign targeting **Thailand's healthcare ecosystem**, including Ministry of Health personnel, hospital administration, and clinical departments. Active since at least April 7, 2026, the campaign uses healthcare-themed spear-phishing lures (medical equipment approvals, patient admission requests, CT scan results) delivered through malicious RAR archives. The infection chain follows a consistent pattern:

**RAR → Obfuscated BAT → Rouki-Obfuscated Payload Loader → Startup Persistence (WindowSecuryt.bat) → Python Infostealer (sim.py) → Telegram Exfiltration**

Key technical details: GitHub-hosted payload delivery (masqueraded as `.png` files), PowerShell-based decoding routines, auto-cleanup of temporary artifacts, and a Python-based information stealer that exfiltrates data via Telegram. The targeting specificity — tailored lure filenames for radiology, procurement, and clinical staff — suggests either prior reconnaissance of healthcare organizations or sector-informed targeting from knowledge of operational workflows. All observed samples were uploaded from Thailand IPs, suggesting in-country staging infrastructure.

**IOCs:** GitHub repos `ud-7-te/ud-vtn`, `d7-te/vtn`; persistence path `%STARTUP%\WindowSecuryt.bat`; C2 staging via raw.githubusercontent.com.

---
