A **malvertising campaign** on Bing search is pushing a fake Claude desktop app installer hosted on a **legitimate Claude.ai domain** to deliver the **SectopRAT** remote access trojan. Dubbed **FakeAgent**, the campaign compromised **at least 29 organizations** between July 21–22.

Attack flow:

1. Malicious **Claude Artifact** hosted on claude.ai (downloaded **7,100 times** before Anthropic removed it)

2. Directs victims to fake installer page serving `ClaudeDesktop.exe`

3. The executable is a legitimate JetBrains Chromium component that **DLL-side-loads** `libcef.dll` (SectopRAT)

4. Persistence via `DockerDesktop.exe` installing a scheduled task

5. Anti-analysis: **VMProtect packing**, shellcode injection, string obfuscation

This follows earlier patterns of Claude Artifact abuse used to push macOS malware via ClickFix lures earlier this year.

**Action:** Block untrusted Claude Artifact URLs. Hunt for IOCs provided by Huntress. Restrict DLL sideloading paths in enterprise environments.

---
