Security researchers at **BlackFog** have analyzed **MedusaHVNC**, a remote access trojan sold as malware-as-a-service (MaaS) via its own website and Telegram channel. The malware uses Windows' legitimate hidden desktop capability to operate completely invisibly to the user.

Infection chain (5 stages):

1. **wscript.exe** executes a JScript launcher (7.5-second delay)

2. Drops files to `%TEMP%\Nx2981Okkr2\` including encrypted payload and `.bat` in Startup folder for persistence

3. **AutoIT** decrypts payload and starts **charmap.exe** (Windows Character Map — LOLBIN)

4. Two-layer decryption: 16-byte repeating XOR on 1M+ bytes, then **ChaCha20** with 32-byte key

5. Final payload communicates with hardcoded C2: **51.89.204.28:4444**

The operator can launch Chrome, Edge, or Firefox within a hidden desktop, invisible to the victim. Uses legitimate Windows functions (BitBlt, SendInput, SetWindowsHookExW, clipboard APIs) for screen capture and interaction.

**Detection:** Since the hidden desktop is a legitimate Windows feature, detection relies on identifying unexpected data exfiltration rather than behavioral monitoring of the desktop itself.
