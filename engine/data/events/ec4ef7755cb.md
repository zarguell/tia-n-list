Qualys Threat Research Unit, in collaboration with Anthropic (using Claude Mythos Preview during manual audit workflow), discovered **CVE-2026-64600** — a race condition in the Linux kernel's XFS filesystem copy-on-write path. An unprivileged local user can exploit this flaw to **overwrite any readable file on an XFS volume at the block layer**, achieving host root privileges — even on systems running **SELinux in Enforcing mode**.

Key details:

- Affects any Linux distribution with XFS root filesystem and **reflink enabled** (default on RHEL, Oracle Linux, Amazon Linux, Fedora)

- Exploitation is **highly reliable** and leaves **no kernel log output**

- Attackers with a local account can escalate to full root

- Patches available in latest kernel updates

**Action:** Apply Linux kernel updates immediately. For systems where patching is delayed, consider disabling XFS reflink support (evaluating performance impact).

---
