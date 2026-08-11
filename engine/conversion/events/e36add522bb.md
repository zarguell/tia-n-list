The US government has updated its April advisory on Iran-linked attacks against critical infrastructure, revealing that Iranian APT groups have expanded targeting to include **Siemens S7-1200**, **Schneider Electric Modicon M340 (BMX P34)**, and **Rockwell Automation CompactLogix/Micro850** programmable logic controllers (PLCs).

Key findings from the updated advisory (published July 22):

- Hackers used vendor configuration software (**Rockwell Studio 5000**, **Schneider EcoStruxure Control Expert**, **Siemens TIA Portal**) to download malicious project files to PLCs

- Attackers **extracted and exfiltrated PLC project files**, then **modified and deleted logic**

- PLC modifications **disabled critical shutdown and alarm logic**, allowing systems to enter unsafe conditions without operator notification

- Some attacks used **malicious ladder logic** that overrode safe operating parameters

- Connections made via leased third-party-hosted infrastructure to ports 44818, 2222, 102, 502, and 22

The advisory names groups **CyberAv3ngers** (previously linked to many ICS attacks) and **Handala** (which hit Stryker in 2025 and claimed access to California Water Service last month) as active in these campaigns.

Updated IOCs and detection guidance are available in the advisory.

**Action:** Review internet-exposed PLCs. Audit for unauthorized configuration software access. Verify safety shutdown/alarm logic integrity on Siemens, Schneider, and Rockwell PLCs. Restrict access to ports 44818, 2222, 102, 502, 22 from untrusted networks.

---
