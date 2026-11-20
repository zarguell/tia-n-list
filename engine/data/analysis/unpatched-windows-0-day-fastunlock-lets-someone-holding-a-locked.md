FastUnlock is an unpatched Windows technique that lets someone with physical access to a locked PC start programs without signing in. The researcher posting as MSNightmare, also using Nightmare Eclipse, published the method, and endpoint-security firm ThreatLocker confirmed the behaviour in coverage by The Hacker News. The session is limited: it is not administrator control of the machine.

The practical impact is narrower than a remote exploit but still concrete for laptops and kiosks left unattended. An attacker who reaches the lock screen can launch tools in a limited user context; the write-up gives no CVE, patch or affected Windows build, and no vendor fix is listed.

Watch for Microsoft's response and for details on which builds and lock-screen configurations are affected. Until then the observable defensive signal is local activity from a locked session, not a network indicator.
