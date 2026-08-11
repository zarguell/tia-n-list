ASEC's Q2 2026 Attack Techniques Trend Report documents a notable shift in the threat landscape: CISA KEV listings reached 75 in Q2 2026, a 27% increase over Q2 2025, with the percentage of listings associated with ransomware rising from 8.5% to 16.0%. Primary targets included web and server applications, endpoints, network perimeter devices, and remote management tools, with growing attention to AI and supply chain vulnerabilities.

Key findings from the report:

- **Threat actors** frequently used T1190 (Exploit Public-Facing Application) to bypass authentication, targeting SimpleHelp, Check Point, Ivanti Sentry, Oracle PeopleSoft, Cisco, and Splunk

- **Identity attacks** included OAuth device code phishing, AiTM (man-in-the-middle) attacks, and stolen token/session exploitation targeting Microsoft Entra ID

- **AI-related exploits** expanded: SearchLeak (CVE-2026-42824) targets M365 Copilot Enterprise for data exfiltration; CVE-2026-26030 and CVE-2026-25592 in Microsoft Semantic Kernel enable prompt injection leading to RCE; CVE-2026-42271 in LiteLLM listed in KEV

- **Three Microsoft Defender zero-days** were listed in the KEV, with threat actors blocking legitimate processes and telemetry to evade detection

- **Malicious skill supply chain attacks** (OpenClaw, ClawHub) continued against AI agent platforms

The report recommends shifting from signature-based to behavior-based detection, focusing on memory injection, sensor telemetry disconnection, abnormal authentication sessions, and abnormal token issuance.

---
