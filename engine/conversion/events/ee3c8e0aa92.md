Threat actors are actively exploiting a chained vulnerability in LiteLLM, the popular open-source AI gateway proxy, combining two flaws for a **CVSS 10.0 unauthenticated remote code execution** attack path requiring zero credentials. Horizon3.ai researchers confirmed the chain works end-to-end.

**How it works:** CVE-2026-42271 is a command injection flaw in LiteLLM's Model Context Protocol (MCP) server test endpoints — endpoints like `POST /mcp-rest/test/connection` and `POST /mcp-rest/test/tools/list` accept full server configurations (commands, args, environment variables) and spawn the supplied input as a subprocess on the host. When initially disclosed on April 20, the flaw was considered limited because exploitation required a valid proxy API key. That assumption fell when Horizon3.ai chained it with **CVE-2026-48710**, a Starlette "BadHost" Host Header validation bypass (Starlette ≤ 1.0.0). By manipulating the HTTP Host header, attackers sidestep LiteLLM's API key requirement entirely.

**Impact:** Once code execution is achieved, attackers can execute arbitrary OS commands on the LiteLLM host, steal API keys and model provider credentials stored by the proxy, access secrets and environment variables, and move laterally into connected AI infrastructure and downstream systems. The LiteLLM proxy sits at the gateway layer between organizations and LLM providers — compromising it means the attacker controls the choke point for all AI API traffic.

**Affected:** LiteLLM 1.74.2 through 1.83.6 with Starlette ≤ 1.0.0.

**Action:** Upgrade LiteLLM to 1.83.7+ and Starlette to 1.0.1+ as emergency priority. Block external access to MCP test endpoints. Rotate all credentials and API keys stored by the proxy. Monitor for requests targeting `/mcp-rest/test/connection` or `/mcp-rest/test/tools/list` with anomalous Host header values.

---
