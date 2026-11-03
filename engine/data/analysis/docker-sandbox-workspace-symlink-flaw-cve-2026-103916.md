CVE-2026-103916 affects Docker Sandboxes and allows a malicious sandbox to use workspace symlinks so that a user-initiated copy reads or writes host files. The CVE record confirms the vulnerability involves host filesystem access via symlink manipulation in workspace contexts.

This is a sandbox escape with potential host-level impact for Docker-based development and CI environments. The concrete artifact is CVE-2026-103916 and the symlink-based workspace escape vector. There is no CVSS score mentioned in the event content, but the flaw allows reading or writing host files, which implies high severity for multi-tenant or shared-host Docker deployments.

Watch for Docker's security advisory and patch timeline, and verify whether workspace symlink restrictions can be applied as a temporary mitigation in environments running vulnerable Docker Sandbox versions.
