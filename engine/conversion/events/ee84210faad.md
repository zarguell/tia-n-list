A coordinated cyberattack disrupted water and wastewater systems across more than 30 Minnesota communities on July 26-27, triggering a multi-agency state and federal investigation.

**What happened:**

- Attackers targeted operational technology (OT) systems at water utilities across Minnesota, affecting cities including Maple Plain, Braham, South St. Paul, and Plymouth

- The City of Braham briefly took its water plant offline after "attackers shut down the operating controls, which shut down the well and water treatment plant"

- Plymouth noted impact was "limited to equipment connected via cellular communications within the system"

- All affected cities confirmed drinking water remains safe and services are operational

- In most cases, contingency procedures were activated and operations continued

**Attribution assessment:**

- No formal attribution has been made, but the timing closely aligns with the July 22 update to **CISA Advisory AA26-097A**, which warned about **Iranian-affiliated PLC exploitation activity** targeting Rockwell Automation, Schneider Electric, and Siemens devices

- The advisory was expanded to document **project file exfiltration** for the first time and added detection guidance for manipulation of reusable code modules embedded in PLC programs

- **CVE-2021-22681** (CVSS 9.8) — a critical authentication bypass in Rockwell Automation Logix controllers with **no available vendor patch** — was added to CISA KEV in March 2026 following confirmed Iranian-affiliated exploitation

- Iranian threat groups CyberAv3ngers and Handala fit the targeting profile

- The cellular vector aligns with 2020 Israeli water facility attacks linked to Iranian actors exploiting vulnerable cellular routers

**Defender takeaways:**

- Remote SCADA assets (water towers, lift stations, pump stations) connecting over cellular modems are often overlooked in risk assessments — integrator-built infrastructure increases this blind spot

- Internet-exposed PLCs are being actively probed by Iranian-linked groups; CISA AA26-097A should be mandatory reading for OT security teams

- The same vulnerabilities "almost certainly exist in water infrastructure well beyond Minnesota" according to BreachLock founder Seemant Sehgal
