Researcher acid.vegas placed an IRC network on TCP port 0, a port nobody is supposed to use, then scanned all of IPv4 and found listeners that exist there. The findings were posted to r/cybersecurity by /u/acidvegas and linked from acid.vegas/blog/the-port-that-does-not-exist/.

It matters because port 0 is widely assumed to be unused, so firewalls and monitoring often ignore it. Finding neighbors on port 0 that really should not be there suggests an unmonitored channel that could be abused for command and control or data exfiltration.

Watch for what the other port-0 services turn out to be, whether attackers adopt port 0 for covert traffic, and whether defenders begin logging or blocking port 0.
