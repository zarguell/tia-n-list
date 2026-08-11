The Bluekit phishing-as-a-service platform has evolved significantly, adding browser-in-the-middle (BitM) capabilities that use the open-source `rrweb` JavaScript library to serialize DOM changes and stream them over WebSocket to the attacker's browser session. Netcraft reports 70+ new hostnames identified over the past week.

Unlike adversary-in-the-middle setups, BitM gives the victim a legitimate login page loaded in the attacker's browser — authentication completes in the attacker's session, granting an active session token. Anti-analysis features: randomized CSS filters (defeats screenshot detection), >1MB frequently changing obfuscated JS bundles, custom CAPTCHA mimicking Cloudflare, browser fingerprinting (RAM, CPU, screen resolution, headless detection), and WebRTC IP mismatch detection.

Bluekit previously offered AI-assisted phishing email drafting via multi-LLM support (Llama, GPT-4.1, Claude, Gemini, DeepSeek) and 40+ templates targeting Outlook, Gmail, iCloud, GitHub, and Ledger. The live monitoring system (5-second update interval) still allows operators to track victims in real time.

**Detection signals:** CSS filter manipulation on top-level HTML elements with randomized values, WebSocket connections sending binary/encrypted data on login pages, and keyboard input/mouse click delays on login forms exceeding normal latency.

---
