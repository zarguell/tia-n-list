WAVLINK WL-WN530BE1-A firmware V251117 is impacted by CVE-2026-120198, a critical unauthenticated remote command injection in /protocol.csp with a CVSS score of 10. The flaw requires no authentication and allows remote attackers to execute operating system commands against the router. Public exploitation is expected given the severity and the exposed endpoint.

Concrete artifacts include CVE-2026-120198, firmware V251117, the /protocol.csp injection point, and CVSS 10. There is no patch mentioned in the initial disclosure from radar.offseq.com. Network administrators should treat any exposed instance of this model as compromised and isolate it from untrusted traffic immediately.

Watch for a WAVLINK firmware update that patches /protocol.csp, and for exploitation campaigns targeting the unauthenticated command injection. Monitor router logs for unexpected requests to the affected endpoint and prepare replacement or isolation plans for devices that remain unpatched.
