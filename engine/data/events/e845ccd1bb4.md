SOCRadar's Threat Research Unit documented **DOUBLECUP**, a Russian **loader-as-a-service** active since early June 2026 that delivers malware through ClickFix prompts while hiding the payload **inside PNG images preloaded into the victim's browser cache** (steganographic delivery).

- **Attack flow:** victim lands on a fake login page impersonating **NetSuite, Odoo, HubSpot, or Salesforce** (malicious code loaded via embedded iframe) → fake CAPTCHA instructions convince them to paste-and-run a command that `findstr`/`certutil` extracts the hidden payload from a cached PNG (located by exact file size) → fileless second-stage dropper derives a decryption key from the victim's public IP and executes the final payload in memory after a hardcoded SHA-256 check.

- **Payloads:** an updated **CountLoader** (Windows + macOS/Intel/Apple Silicon builds; info-harvesting, crypto-wallet/browser-extension checks, Signal Desktop detection, scheduled-task persistence) and **DeviceManager**, a previously undocumented modular Python-based Windows RAT.

- **Business model:** customers buy licenses and a Go-based Windows campaign builder; DOUBLECUP handles stego image hosting, session/signal endpoints, encryption keys, and payload rebuilding. Operators run their own ClickFix sites. Licensing panel identified at `213[.]139.77[.]109:9090`. Per-browser commands generated for Chrome, Edge, Firefox, Brave, Opera.

**Action:** This is ClickFix with a stealth delivery twist — cache-resident payloads bypass download-based detections. Block clipboard-paste execution prompts in policy where feasible, filter `findstr`/`certutil` command-line abuse, and treat fake-CAPTCHA "fix your browser" prompts as the phishing tell they are.
