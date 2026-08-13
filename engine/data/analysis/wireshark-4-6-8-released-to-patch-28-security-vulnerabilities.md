Wireshark 4.6.8 patches 28 security issues in the network protocol analyzer. The release fixes problems that can cause crashes, abnormal exits, memory-safety failures, and denial-of-service when the software parses specially crafted traffic or capture files. No CVEs are named in the coverage, so per-issue severity is not yet public.

Wireshark is the default tool for inspecting packet captures, and capture files are attacker-controllable input in any environment that analyzes third-party pcaps. Memory-safety fixes in the dissector stack matter because a malformed capture handed to an analyst is a realistic initial access path.

Upgrade to 4.6.8 and treat unsolicited capture files as untrusted input until the per-issue advisories land. Watch for the upstream Wireshark security announcements that will attach CVE identifiers to the 28 fixed issues.
