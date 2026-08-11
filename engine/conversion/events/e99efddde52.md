Microsoft has published a detailed threat report on a surge in **ACR Stealer** (MaaS, believed to be a rebranding of Amatera Stealer) attacks against its enterprise customers between late April and mid-June 2026. Two primary intrusion chains are documented:

**Chain 1 — ClickFix + WebDAV:** A ClickFix social-engineering lure executes a command to run a malicious DLL from a remote WebDAV share via rundll32.exe. Attackers use GUID-based directory structures and filenames mimicking legitimate resources. After C2 contact, a heavily obfuscated PowerShell script establishes persistence via scheduled tasks masked as software updates, clears PowerShell history, and injects the payload into a system process for in-memory execution. Some variants use blockchain services as dead-drop resolvers ("EtherHiding") for updated C2 addresses.

**Chain 2 — ClickFix + MSHTA:** ClickFix launches MSHTA to retrieve malicious content, executing an obfuscated PowerShell downloader that extracts an encrypted payload concealed in a steganographic JPEG image and runs it directly in memory.

Targeted data includes browser passwords, cookies, session tokens (Chrome/Edge via DPAPI decryption), PDFs, Microsoft 365 documents, files from Desktop/Downloads, and enterprise-synced OneDrive/SharePoint directories.

**Action:** Block ClickFix delivery vectors — restrict rundll32.exe, mshta.exe, and PowerShell from launching content from remote/user-writeable paths. Microsoft provides IOCs and detailed mitigations in its report.
