Intigriti researchers Ayoub and Inti De Ceukelaire documented a class of vulnerabilities in AI-powered customer service agents that go beyond prompt injection. The agents read support inboxes, access knowledge bases, invoke backend tools, and perform account actions, and each integration point is an attack surface.

In one scenario, a chatbot identified customers by the visible email From header. An attacker could spoof that header and issue a malicious instruction, causing the bot to send phishing messages from the legitimate support address. In other cases, SPF/DKIM validated one sender identity while the AI agent parsed a different header to determine which customer account to access, allowing data retrieval tied to a victim and exfiltration to an attacker-controlled address.

The researchers also demonstrated MFA bypass and OTP extraction through agent tool access, producing over $50,000 in bug bounties over several weekends without using vulnerability scanners. The core risk is that AI agents bridge authentication systems with external-facing channels, and the trust boundaries between them are poorly defined.

Organizations deploying AI customer service should audit which tools agents can invoke, how identity is resolved from inbound channels, and whether agents can trigger outbound communications without human approval.
