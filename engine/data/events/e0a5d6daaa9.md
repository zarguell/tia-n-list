LayerX researchers devised a prompt injection attack dubbed **BioShocking** that tricks AI-powered browsers into treating sensitive real-world actions as part of a fictional game scenario, causing them to bypass safety guardrails. Tested against **six agentic browser products** (ChatGPT Atlas, Comet, Fellou, Genspark, Sigma Browser, Claude Chrome plugin), **all six were compromised** — only OpenAI has implemented an effective fix.

The PoC presents a BioShock-themed puzzle where wrong answers are rewarded, teaching the AI agent that normal rules do not apply. In the final step, the agent is instructed to visit a GitHub repo and exfiltrate credentials — all six agents complied.

---
