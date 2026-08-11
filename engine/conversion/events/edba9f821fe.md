Sophos documented a threat actor using an AI-assisted ransomware development framework that deployed **Cursor and Claude Opus agents** to automate EDR bypass research, payload generation, and testing against CrowdStrike, Sophos, and Microsoft Defender. The toolkit generated ~80 Windows payload modules across 70+ evasion techniques, with C2 routed through Telegram Bot API and Cloudflare Workers as redirectors.

**Key finding:** Agents extracted bypass techniques from published research by Kaspersky, Palo Alto Networks, Bishop Fox, and SpecterOps, then autonomously generated, tested, and iterated evasion modules in virtualized EDR test environments. While AI was not embedded in deployed malware, the technology compressed the timeline from "research published" to "weaponized payload in the wild" from months to days.

---
