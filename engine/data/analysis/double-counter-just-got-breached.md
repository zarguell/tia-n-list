Double Counter, a Discord moderation bot used by thousands of servers, was breached on October 4. The attacker accessed cloud credentials, hijacked the bot, copied roughly 12 GB of database contents, and misused a separate payment account according to operator Tellter SAS. Reports cite about 275,000 exposed email addresses and Discord usernames, with some references to millions of linked accounts.

This matters because the bot is embedded in server-level security: a compromised moderation bot can become a pivot into server management channels. The incident also highlights cloud-credential hygiene at a widely deployed open-source project.

Watch for the full incident report from Tellter SAS, confirmation of whether the attacker maintained persistence after the initial breach, and any evidence of secondary misuse of server-level permissions. The 12 GB database copy suggests a significant data exfiltration that may extend beyond the initially reported email and username set.
