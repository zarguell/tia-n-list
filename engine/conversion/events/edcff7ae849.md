New analysis from InfoStealers reveals the operational mechanics behind the FortiBleed credential theft campaign with striking detail: the attackers bypassed Fortinet's encryption by renting a **36-GPU cluster on Vast.ai** — a decentralized cloud compute marketplace built for the GenAI industry — at **$14.40/hour (~$350/day)** .

The cluster, managed entirely through a Telegram bot, achieved:

- **720 billion hashes/second** against legacy Fortinet salted SHA-256 hashes

- **180–360 million hashes/second** against newer PBKDF2-based hashes (designed to resist GPU cracking)

Beyond raw compute, the operators used **AI-assisted coding tools (Cursor)** to write the Telegram bots and management scripts, and **agentic penetration testing frameworks** to automate Active Directory enumeration after cracking credentials. This creates a fully AI-integrated intrusion pipeline: AI-written management code → rented AI GPUs → AI-driven post-exploitation. Initial access broker **SantaAd** was identified selling bulk Fortinet access on Russian-language forums, confirming the IAB-to-ransomware affiliate pipeline these credentials feed into.

The campaign has now been linked to **theft from 86,000+ Fortinet devices** across 194 countries. Kevin Beaumont's analysis highlights the dark irony: the GenAI industry's GPU infrastructure has commoditized nation-state cryptographic attack capability.

**Context:** *Previously covered June 18–21 (initial disclosure, CISA warning, Unit 42 analysis, IAB attribution). New today: full operational mechanics of password cracking infrastructure at $350/day.*

---
