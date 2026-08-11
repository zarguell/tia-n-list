Attackers are actively exploiting **CVE-2026-48558**, a critical authentication bypass in the SimpleHelp remote monitoring and management platform (used primarily by MSPs and IT departments), to deploy **TaskWeaver** (a JavaScript-based malware loader) and **Djinn Stealer**, a previously undocumented cross-platform information stealer targeting Windows, macOS, and Linux.

Horizon3.ai disclosed the flaw earlier this month, noting ~1,000 internet-exposed SimpleHelp servers were running vulnerable configurations using OpenID Connect (OIDC). Blackpoint's MDR team investigated an incident where the attacker established an authenticated technician session on an internet-facing SimpleHelp server before deploying the malware chain.

Djinn Stealer specifically targets:

- **AI development credentials** — MCP configuration files for Claude, Gemini, Codex, Cline, OpenCode, and Kilo

- **Cloud/infrastructure credentials** — AWS, GCP, Azure, Docker, Terraform, Pulumi, HashiCorp Vault

- **Git/package manager credentials** — SSH keys, GitHub CLI tokens, npm/pip/Cargo/Maven credentials

- **Cryptocurrency wallets** — Bitcoin, Ethereum, Monero, Exodus, Atomic Wallet, Electrum

Data is packed into a TAR archive, GZIP-compressed, and AES-256-GCM encrypted with an RSA-2048 key embedded in TaskWeaver before exfiltration.

**Recommended action:** Update SimpleHelp instances immediately. Invalidate all existing technician sessions. Rotate any credentials exposed through compromised servers.

---
