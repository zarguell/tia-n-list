A researcher publishing as NightmareEclipse (GitHub user MSNightmare) has released BigDiskBuster, a proof-of-concept that blocks Microsoft Defender from completing its platform and security intelligence signature updates by filling disk space. It is described as a Windows Defender update denial of service, and there is no patch available, making this a zero-day.

The practical effect is that Windows endpoints can be left running with stale anti-malware definitions without anything obviously broken. An attacker who can consume disk space on a target, whether locally or through a quirk of a deployed workload, degrades the one defensive agent most organizations assume is current.

This is a published PoC, not observed in-the-wild abuse, so the immediate risk is opportunistic use. Watch whether Microsoft acknowledges the behavior in a Defender platform update, whether it gets a CVE, and whether attackers chain it with techniques that bloat disks on endpoints before planting malware.
