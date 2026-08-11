SOCRadar published new operational details on the large-scale FortiBleed credential theft campaign, revealing the attackers deployed a **Go-based tool called "FortigateSniffer"** on compromised FortiGate devices after gaining administrative access via credential stuffing and brute-force attacks.

The tool abuses FortiOS's built-in `diagnose sniffer packet` command to monitor traffic for authentication protocols across **24 protocols** including RADIUS, NTLM, Kerberos, LDAP, SMB, RDP, and database services. Captured PCAP data is processed through a "PCAP Deep Analysis Toolkit" that extracts cleartext credentials, password hashes, and Kerberos tickets, then generates Hashcat-ready files for offline cracking on a distributed GPU cluster.

The campaign has been active since at least **February 2026**, targeting more than **430,000 FortiGate firewalls** worldwide. The operator functions as an initial access broker (IAB), selling harvested network access to ransomware affiliates.

**Context:** *Previously covered June 18–22 (initial disclosure, CISA warning, Unit 42 analysis, IAB attribution, GPU cluster mechanics). New today: SOCRadar's FortigateSniffer analysis showing on-device traffic interception as the primary credential harvesting vector.*

---
