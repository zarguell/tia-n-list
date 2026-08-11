Microsoft Threat Intelligence discovered that Anthropic's Claude Code GitHub Action could expose CI/CD workflow secrets when AI agents process untrusted GitHub content. While the Bash tool was sandboxed via Bubblewrap with environment scrubbing enabled for non-write-user-triggered workflows, the **Read tool was not subject to the same isolation** — it operated as direct in-process calls, bypassing the sandbox entirely and accessing `/proc/self/environ` to read `ANTHROPIC_API_KEY` and other credentials.

**Bypass chain:** The researchers embedded a prompt injection in an issue body framing credential access as a "compliance review" and instructed the model to strip the first 7 characters of any discovered API key (`sk-ant-...` → laundered to `...`). This defeated both Claude's safety filters (no visible API key prefix to trigger refusal) and GitHub's secret scanner (no known credential pattern remaining in stdout). The laundered key could then be exfiltrated via WebFetch, Bash, GitHub MCP to issue comments, or workflow logs.

Anthropic mitigated in **Claude Code v2.1.128** (May 5) by blocking access to sensitive `/proc/` files in the Read tool.

**Broader rule:** Microsoft recommends the "Agents Rule of Two" — an AI-powered workflow should never hold all three capabilities simultaneously: (1) processing untrusted input, (2) access to secrets, and (3) ability to change state or communicate externally.

---
