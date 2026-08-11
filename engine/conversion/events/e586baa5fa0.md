Trail of Bits researchers demonstrated that all three major AI skill security scanners — ClawHub (OpenClaw), Cisco's skill-scanner, and Vercel's skills.sh (via Gen, Socket, Snyk) — can be reliably bypassed using simple techniques, raising fundamental concerns about agentic AI supply chain defenses.

**Bypass techniques demonstrated:**

- **ClawHub:** Prepend ~100,000 newline characters — OpenClaw truncates oversized content for its guard-model prompt, hiding malicious logic beyond the inspected region. VirusTotal/Gemini 3 Flash also failed.

- **Vercel skills.sh:** Malicious logic hidden in `.docx` ZIP archives (containing XML + embedded shell script) and poisoned `.pyc` bytecode — all three scanning integrations reported the skill as safe.

- **Cisco skill-scanner:** Even backed by Claude Sonnet 4.6, the scanner marked prompt-injection-style skills as low risk, focusing on "internal URL exposure" rather than malicious npm registry control.

The core problem is structural, not a signature gap. Skills can embed malicious behavior in SKILL.md instructions, embedded scripts, binary artifacts, or multimodal content — and scanners are static targets attackers can iteratively probe. Cisco has accepted a PR adding spec validation and broader language support, but this does not address prompt injection or arbitrary binary payloads.

**Recommendation:** Organizations should not outsource trust decisions to automated scanners. Use curated internal skill registries, version pinning, and treat public skills as untrusted code by default.

---
