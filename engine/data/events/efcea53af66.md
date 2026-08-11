7-Zip version 26.02 patches a remote code execution vulnerability in its processing of XZ-compressed data. Disclosed by Lunbun researcher Landon Peng and documented by Zero Day Initiative (ZDI-26-444), specially crafted XZ data triggers a heap-based buffer overflow that can allow attackers to execute arbitrary code as the user. The patch adds output buffer boundary checks to prevent the decoder from writing beyond available space.

Exploitation requires user interaction — opening a malicious archive or visiting a page that triggers archive extraction. 7-Zip has no automatic update mechanism; users must manually download version 26.02 from 7-zip.org.

While no active exploitation has been reported at this time, 7-Zip archive vulnerabilities have been weaponized before — in early 2025, a separate 7-Zip flaw was exploited as a zero-day by Russian hackers, and a WinRAR vulnerability (CVE-2025-8088) was used in phishing attacks to deliver RomCom malware.

**Action:** Update to 7-Zip 26.02 manually — the lack of auto-update means vulnerable versions will persist on endpoints indefinitely without proactive IT intervention.

---
