Chinese hackers of the **Velvet Ant** cluster breached an isolated critical infrastructure network and maintained undetected access for a decade (2016–2026) by hijacking the organization's entire authentication infrastructure. Dubbed **"Operation Highland"** by Sygnia researchers, the intrusion represents one of the longest known persistent compromises of a truly air-gapped environment.

The attack chain began with the compromise of internet-facing servers, deploying a modified **GS-Netcat reverse shell** disguised as a legitimate system component, with persistence via malicious `systemd` services or startup scripts. A custom **SOCKS5 proxy** masquerading as `smbd -D` turned compromised servers into internal pivot points.

The most sophisticated element: Velvet Ant modified a compromised internet-facing **Nginx server** to proxy specially crafted HTTP POST requests through a **FastCGI wrapper (fcgiwrap)** into the isolated network — establishing a remote-execution bridge with no direct connection to the critical infrastructure environment. Inside, they:

- **Replaced `pam_unix.so` with 9 distinct backdoored variants** — each compiled in a separate build environment, indicating a well-resourced operation — accepting hardcoded passwords and harvesting user credentials

- **Trojanized OpenSSH components** (ssh, sshd, scp) to capture credentials and log SSH session commands

- Achieved persistence immune to password changes and session terminations, with full visibility into every administrative login and command

**Cleanup complexity:** Remediation required building a dedicated testing lab to validate binary replacement — removing tampered authentication components risked locking legitimate administrators out entirely.

**Recommendation:** Treat PAM, OpenSSH, and LSASS as critical security assets. Deploy file integrity monitoring, hardened privileged access, and offline recovery procedures with immutable backup snapshots.

---
