Ubiquiti patched three critical vulnerabilities in UniFi OS Server that chain together to deliver **unauthenticated remote code execution with root privileges**. Bishop Fox confirmed the full exploit chain end-to-end on version 5.0.6 — a single crafted HTTP request yields a root shell, no credentials, no user interaction.

**The chain:**

1. **CVE-2026-34908 / CVE-2026-34909 (CVSS 10.0 each)** — Authentication gateway bypass via URI normalization mismatch. Nginx reads the raw `$request_uri` for auth decisions but passes the normalized `$uri` (where `%2f` decodes to `/`) to upstream backends. Attackers craft a request whose raw form starts with the auth-exempt `/api/auth/validate-sso/` prefix passing the gate, while its normalized form hits authenticated proxy routes.

2. **CVE-2026-34910 (CVSS 10.0)** — Command injection in the package-update service. The handler shells out the attacker-controlled package name via `fmt.Sprintf` into `sh -c`. No validation on the package name means shell metacharacters are interpreted directly. The `ucs-update` account holds passwordless sudo rights over `dpkg`, `chmod`, `systemctl`, and `uos` — enabling installation of a crafted `.deb` whose post-install script runs as root.

**Worse than a single patch:** Root on a UniFi OS Server means full management-plane compromise: the JWT signing key can be read and forged admin sessions minted offline. Bishop Fox confirmed that a forged owner-scope JWT token authenticated successfully against both vulnerable 5.0.6 and **fully patched 5.0.8** consoles. Any signing key stolen before patching continues to generate valid admin sessions indefinitely. In deployments with UniFi Access and UniFi Protect, the same position unlocks physical doors, clones NFC/face credentials, views live camera feeds, and deletes recorded surveillance footage.

**Action:** Patch to UniFi OS Server 5.0.8 or hardware-equivalent fixed version. Restrict TCP 11443 to a dedicated management VLAN. **Treat any instance exposed before patching as fully compromised** — rotate JWT signing key (`/data/unifi-core/config/jwt.yaml`), TLS keys, cloud tokens, and database credentials. Rebuild from known-good image. Biometric and NFC data cannot be rotated — treat as permanently disclosed.

---
