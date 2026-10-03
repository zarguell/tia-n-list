Cisco Talos has detailed Antino, a previously undocumented Windows backdoor used by a China-nexus actor against government and policy organizations in Taiwan, India, and the Philippines. The campaign is espionage-focused and deliberately hides inside Microsoft's legitimate cloud services.

Antino uses Microsoft Graph, Outlook mail, and OneDrive files as its command-and-control channels, so operator commands and stolen data move through traffic that looks like ordinary Microsoft cloud API use. Reporting on the campaign also points to DMARC spoofing in the delivery chain used to lend the operation's email legitimacy.

Watch for additional victims across Asia-Pacific government and policy sectors, follow-up Talos reporting with indicators, and detections keyed on anomalous Graph API and mailbox access patterns rather than raw network indicators, which this backdoor is built to defeat.
