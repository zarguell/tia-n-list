Microsoft has remediated the **AutoJack** vulnerability chain in AutoGen Studio, three weeks after the initial disclosure. The fix, committed to the GitHub main branch, addresses three weaknesses: (1) MCP WebSocket trusted localhost origin without authentication, (2) authentication middleware excluded `/api/mcp/*` routes, and (3) base64-encoded `server_params` from the URL were passed verbatim to process-launching code.

Microsoft emphasizes that the vulnerable code **never shipped in a public PyPI release** — only developers building from the GitHub main branch between the MCP plugin landing and the hardening commit were exposed. The latest PyPI package (autogenstudio 0.4.2.2) is clean. Microsoft recommends running AutoGen Studio in isolated, sandboxed environments.

**Context:** *Previously covered June 19 (initial disclosure of AutoJack chain by Microsoft Defender Security Research). New today: fix deployed, PyPI unaffected, containment guidance confirmed.*

---
