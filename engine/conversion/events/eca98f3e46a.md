JetBrains warned of a **critical authentication bypass in TeamCity On-Premises** that can be exploited to achieve remote code execution. **CVE-2026-63077** lets an attacker with HTTPS access to a TeamCity server **bypass authentication via the agent polling protocol** and execute arbitrary OS commands with the privileges of the server process — exposing data, configurations, stored credentials, build artifacts, and CI/CD pipelines.

- **All versions of TeamCity On-Premises affected**; TeamCity Cloud already fixed

- Reported privately July 10; fixed in **2025.11.7 and 2026.1.3**, with a patch plugin for 2017.1+ (2024.03+ auto-downloads it)

- No evidence of active exploitation yet, but **TeamCity flaws have been extensively leveraged by ransomware gangs and state-backed actors** in the past

- JetBrains advises VPN-only exposure — even the login page and REST API are entry points

**Action:** Upgrade immediately or install the patch plugin; audit internet-exposed TeamCity instances and treat unpatched ones as compromised candidates.
