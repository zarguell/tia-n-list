**ActiveState's** Shane Warden synthesizes three independently named attacks into a single observation: **AI coding agents hallucinate package names, repositories, and domains that sound real but do not exist**, and attackers can predict and pre-register those names to deliver malware.

Key findings from researchers at **Tel Aviv University, Technion, and Intuit** (published July 8, 2026, led by Aya Spira / Ben Nassi):

- Multiple AI coding agents (Cursor, Windsurf, GitHub Copilot, Cline, Gemini CLI, OpenClaw) hallucinated **identical names up to 85% of the time** for repository requests

- For skill installs, hallucination consistency reached **100%**

- The attack requires no phishing, no stolen credentials, no human clicking a link — just an automated process given permission to fetch

The attacks converge on "**Slopsquatting**" (fake package names), "**Phantom Domains**" (fake domain names), and "**HalluSquatting**" (fake repos/skills). Warden notes the ultimate payoff in one observed case was botnet enrollment via a hallucinated package.

**Action:** Pin dependency versions and hashes in CI/CD. Implement approval gates for packages fetched by AI coding assistants. Treat AI-generated dependency names as unverified until resolved against package registries. Train developers that compiler/CI passing is insufficient validation for AI-suggested dependencies.

---
