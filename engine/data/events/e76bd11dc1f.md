The U.S. Cybersecurity and Infrastructure Security Agency (CISA), Australian Signals Directorate's ACSC, the FBI, and international partners released new guidance titled **"CI Fortify – Advice for isolating vital systems"** urging critical infrastructure organizations to prepare to disconnect operational technology systems during cyberattacks.

**Key recommendations:**

- Identify the **minimum systems and networks** required to continue delivering a critical service

- **Document every connection** between vital systems and corporate networks, remote access, cloud, vendors, and other CI operators

- Establish predetermined **isolation points** where connectivity can be physically or administratively disconnected

- Implement **graduated isolation** — first block remote workers and vendors, then corporate networks, then all external connections

- Use **data diodes** (one-way data flow devices) where appropriate

- **Test complete isolation** regularly — partial tests may miss shared infrastructure and hidden dependencies

- Keep an **offline or printed copy** of the isolation plan

**Risks of isolation:** Systems fall behind on security updates, monitoring is reduced, and removable media use increases. Organizations must prepare to operate, monitor, and update systems manually during isolation periods.

The guidance specifically references **Volt Typhoon** (Chinese state-sponsored, undetected in CI networks for 5 years), **Salt Typhoon** (telecom breaches), and water infrastructure attacks as motivating scenarios. The timing — two days after the Minnesota water attacks — is notable.

**Action:** OT security teams should review CI Fortify against existing isolation plans. Cellular-connected SCADA assets (the likely vector in Minnesota) should be specifically evaluated.
