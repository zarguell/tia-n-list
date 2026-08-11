The ongoing Shai-Hulud / Mini Shai-Hulud / Miasma supply chain campaign has escalated dramatically, now totaling over **471 malicious artifacts across 106 NPM packages and 37 PyPI packages**, with new waves continuing to hit the ecosystem.

**Three new developments since the June 9 update:**

1. **Typosquat wave (June 7):** GitLab's Vulnerability Research team identified five malicious PyPI packages — `rlask` and `tlask` (Flask typosquats), `rsquests` (Requests typosquat), `nhmpy` (NumPy typosquat), and weaponized `mflux-streamlit` — all deploying the Shai-Hulud worm via a copycat actor using TeamPCP's open-sourced code. These packages execute at install time, no import required.

2. **Second "Hades" wave (June 8):** A new PyPI wave hit 29+ packages targeting bioinformatics, graph ML, and **MCP-themed packages** including `langchain-core-mcp`, `openai-mcp`, `instructor-mcp`, `tiktoken-mcp`, and `ray-mcp-server`. The malware mutated: payload is no longer bundled — instead searches `sys.path` at runtime to split loader from payload, evading static detection.

3. **471 total artifacts:** The campaign now spans 411 npm artifacts (106 packages) + 60 PyPI artifacts (37 packages). High-profile casualties include TanStack (84 malicious versions), UiPath, DraftLab, and `mistralai`/`guardrails-ai` on PyPI.

**Action:** Rotate all CI/CD secrets, npm/PyPi publish tokens, and cloud credentials on any system that may have installed affected packages. Audit for `*-setup.pth` files, unexpected Bun runtime downloads, and GitHub Actions creating unexpected public repos. Lock dependencies and add time delays to package update pipelines.

---
