Six Microsoft 365 Android apps — Word, PowerPoint, Excel, 365 Copilot, Loop, and OneNote — shipped with `set IsDebugMode(true)` in their production builds, disabling the security check that restricts FOCI (Family of Client IDs) account token sharing to trusted Microsoft apps only. Enclave Security discovered that any malicious app on the same device can silently steal Microsoft account access tokens with just 15 lines of code.

**Attack vector:** A supply chain attack via trojanized app updates. An attacker updates a legitimate app (e.g., a game) with malicious code. Auto-update silently installs it, the malicious code requests account tokens from the debug-enabled Microsoft app, and receives them without authorization checks. The stolen FOCI tokens are **reusable and refreshable** over long periods. Impact: full read/write access to emails, files, documents, and calendar — the attacker's access mirrors the victim's within the affected app context.

Microsoft patched the flaw on May 12 (Patch Tuesday) and via Google Play Store. **User action required:** Ensure all Microsoft Android apps are updated to the latest versions. Microsoft Teams was not affected.

---
