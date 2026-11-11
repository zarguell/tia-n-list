Railway disclosed a breach that began October 20, 2026: attackers exploited a previously unknown vulnerability in Railway's build infrastructure to escape filesystem isolation, steal an internal credential, access build histories and a copy of Railway's source code, then abused an improperly configured trust relationship to obtain credentials used to decrypt customer environment variables. Up to 100,000 workspaces (1.85%) were potentially exposed and roughly $740,000 in fraudulent AI usage was generated.

The incident was a roughly 26-hour battle. Railway first warned customers on October 22 to rotate secrets; a new incident report published November 11 confirms the full chain, including the attackers' use of stolen customer secrets (API keys, database passwords, cloud credentials) to fund AI usage.

Customers should rotate all stored secrets and audit usage for anomalies. The case shows how a single sandbox escape can cascade into full credential compromise through source-code analysis and trust misconfiguration.

