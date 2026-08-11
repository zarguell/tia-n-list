Kaspersky identified an ongoing malware campaign targeting WhatsApp users across **11 countries** — Brazil, India, Mexico, Singapore, the UK, Spain, Taiwan, Australia, Russia, Vietnam, and Malaysia — using compromised accounts to distribute malicious VBScript files disguised as business and financial documents.

The infection chain: compromised WhatsApp account sends messages containing only an obfuscated VBScript file → victim opens the file → VBScript downloads two additional scripts that disable UAC via Registry modification → a ZIP archive containing **ManageEngine Endpoint Central** is silently installed and configured to connect to attacker-controlled management servers → full remote administration access.

Filenames are localized in multiple languages, confirming the campaign's global reach. On WhatsApp Desktop, the VBScript executes directly via `wscript.exe` without requiring a manual download. While not definitively attributed, researchers found Chinese-language indicators and infrastructure overlap with IPs previously tied to **ValleyRAT** and **Gh0st RAT** activity.

---
