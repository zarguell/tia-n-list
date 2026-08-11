Kaspersky has documented **OkoBot**, a malicious framework delivering more than 20 payloads focused on stealing cryptocurrency wallet seed phrases, credentials, and browser data. The framework reaches victims through ClickFix attacks and malicious GitHub repositories — one impersonating SQL Server Management Studio but dropping a trojanized Audacity installer. OkoBot evolved from the TookPS campaign (running since March 2025) with a completely redesigned infection chain.

Notable modules include: an injector that installs hidden malicious Chrome extensions (Rilide), **SeedHunter** (injects into Trezor Suite/Ledger Wallet to display fake seed recovery screens), **MC Keylogger** (clipboard monitoring, USB detection, screenshots every 5 minutes), and **OkoSpyware** (FFmpeg-based video recording of 100 monitored applications). Geoblocking of payload delivery excludes Russia/CIS. Majority of victims are in Brazil, Vietnam, Canada, Mexico, and Turkey.

**Action:** Audit GitHub repositories before cloning. Monitor for SeedHunter's fake recovery screen behavior in Trezor Suite and Ledger Live. OkoBot's modular architecture and ClickFix delivery vector indicate a maturing operation.

---
