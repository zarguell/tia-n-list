A use-after-free vulnerability in Linux's KVM hypervisor — dormant for 16 years — has been disclosed and patched. Tracked as CVE-2026-53359 and dubbed "Januscape," the flaw sits in the shadow MMU code shared across both Intel and AMD architectures, making it the first publicly known KVM exploit triggerable on both CPU families.

Discovered by researcher Hyunwoo Kim (@v4bel) and demonstrated in Google's kvmCTF bug bounty program (up to $250,000), the vulnerability allows an attacker with root on a guest VM to corrupt the host kernel's shadow page state, leading to full host compromise. In a public cloud scenario, a single malicious guest could panic the host kernel (denial of service against all other tenants) or execute arbitrary code with host root privileges to take over the physical machine and all VMs on it.

On RHEL-based distributions, the flaw can also be exploited by unprivileged local users for privilege escalation to root. Exploitation requires root on the guest (typically default on cloud VMs); if root is unavailable, it can be chained with a privilege escalation bug like Dirty Frag.

**Patched in mainline Linux on June 19 (commit 81ccda30b4e8).** Cloud providers and Linux distribution maintainers should have patched; enterprises should verify their kernel versions are at or past the fix commit.

**Recommended action:** Verify all KVM hosts are running kernel ≥6.12.x with the June 19 patch. Audit cloud VM fleets. If unpatched, restrict untrusted guest workloads and enable nested virtualization protections.

---
