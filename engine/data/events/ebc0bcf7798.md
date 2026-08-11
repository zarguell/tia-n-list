Proofpoint documented a sharp escalation from TA4922, a Chinese-speaking financially motivated cybercrime group that has rapidly expanded operations into Europe, hitting Germany, Italy, the UK, and South Africa. The group now conducts **more unique campaigns than any other tracked cybercrime threat actor** in Proofpoint's telemetry, using localized phishing lures crafted for payroll notices, tax audits, VAT filings, and government compliance in each target country.

**Malware arsenal expansion:**

- **Atlas RAT** — New remote access trojan with system recon, targeted file theft, keylogging, screenshot capture, audio/webcam recording, and plugin download. Includes anti-sandbox checks (Microsoft Defender Application Guard, CExecSvc service, OS UUID).

- **RomulusLoader** — Process hollowing + shellcode injection loader deploying AnyDesk and SyncFuture (Chinese RMM tool, specifically used against German targets).

- **SilentRunLoader** — Python-based info stealer targeting Chrome credentials, deployed against UK and Southeast Asian targets.

- **Winos4.0 (ValleyRAT)** — Full remote access framework.

Proofpoint assesses the group uses LLMs to accelerate malware development based on AI-generated code artifacts (placeholder values, structured comments). Since March, activity has increased sharply with "unprecedented operational diversity." While financially motivated, the malware capabilities also support surveillance that could be sold to espionage groups. Contact methods include WhatsApp, LINE messenger, and Microsoft Teams.

---
