ReliaQuest identified a new data-extortion group called **Helix** targeting SharePoint environments via voice phishing, device-code phishing, and MFA abuse. The group calls employees impersonating managers (caller ID spoofing), tricks targets into device-code authentication, registers a new MFA authenticator for persistence, then bulk-exfiltrates SharePoint data from IP `179.43.185[.]230` using `python-requests/2.28.1`.

ReliaQuest found infrastructure overlaps with the now-defunct **BlackFile** group (same AS51852) and tactical overlaps with **ShinyHunters** (vishing playbook, NICENIC registrar use). Helix emerged shortly after BlackFile ceased operations in April, suggesting operator migration. High-impact mitigation: disable device-code authentication where possible.

---
