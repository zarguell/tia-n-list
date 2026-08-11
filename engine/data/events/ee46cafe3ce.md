Attackers are abusing **Windows Winget's Desired State Configuration** feature to execute arbitrary PowerShell code through `ConfigurationRemotingServer.exe` — a trusted system process that EDR tools rarely flag. The attack is combined with a self-referencing LNK shortcut that bypasses the manual confirmation prompt entirely, enabling silent, trusted-process-based code execution.

---
