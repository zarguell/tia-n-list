The disgruntled security researcher known as Nightmare Eclipse (aka Chaotic Eclipse) has released another unpatched Windows zero-day, timed to coincide with the July 2026 Patch Tuesday. **LegacyHive** is a local privilege escalation vulnerability in the Windows User Profile Service that allows an attacker to mount another user's NT registry hive — including administrator hives — into the current user's classes root. The PoC requires another standard user's credentials and a target username (e.g., an admin), and works on systems running Microsoft's July 2026 patches.

Unlike previous drops (BlueHammer, RedSun, UnDefend, GreatXML), LegacyHive was released with a stripped PoC to slow weaponization. The researcher states the exploit originally required no credentials and could load any hive — capabilities that are still possible with additional work. Microsoft has not acknowledged the vulnerability.

This is the eighth+ zero-day Nightmare Eclipse has released targeting Microsoft products, with previous exploits confirmed used in real attacks.

**Action:** Monitor for exploitation of User Profile Service manipulation. The strip-down of the PoC slows but does not prevent weaponization by determined actors.

---
