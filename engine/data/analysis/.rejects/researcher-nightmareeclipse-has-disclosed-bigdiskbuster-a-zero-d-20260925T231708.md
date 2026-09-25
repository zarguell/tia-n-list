A researcher publishing as NightmareEclipse, GitHub user MSNightmare, disclosed BigDiskBuster, a proof-of-concept that prevents Microsoft Defender from completing its platform and security intelligence signature updates by filling disk space. Coverage by GBHackers and others describes it as a Windows Defender update denial-of-service technique that leaves endpoints stuck on stale antimalware definitions.

The risk is quieter than typical malware: systems stay online and appear healthy while their protection ages out. An attacker who can fill the disk, whether through a separate foothold or a low-privilege quota trick, degrades endpoint detection before doing anything noisy. No patch or vendor mitigation is available as of disclosure, and Microsoft has not issued a CVE.

What to watch: a Microsoft response or fix, whether the technique is folded into real attack tooling, and defensive checks on disk space monitoring and Defender definition freshness alerting.
