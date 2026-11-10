A while back, I had released a blog showing that NTLMv1 downgrade attacks still work on Windows Server 2022! While it isn't a default setting, it's still a misconfiguration to potentially look for. If a DC’s LmCompatibilityLevel is set to 0-2, you can coerce authentication, strip Extended Session Security (ESS), and obtain an NTLMv1-SSP hash that’s crackable with a rainbow table. :) Blog: https://hunio.org/security/ntlmv1-ssp-cracking/ submitted by /u/elohhs [link] [comments]

via reddit r/cybersecurity: Cracking Server 2022 NTLMv1-SSP Hashes with Rainbow Tables
