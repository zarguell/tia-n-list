PEERSTITCH is a memory-resident ARM64 implant deployed after exploitation of CVE-2024-47575 against FortiGate devices. The intrusion targeted 500+ firewalls, with the implant persisting in memory rather than on disk. Unit 42 reported the finding on 2026-10-14, and the CVE carries a KEV flag with a score of 6.8.

Victim exposure is measured by the 500+ firewall footprint and the stealth archetype; memory residency evades standard disk forensics. The event count is low (one source, zero Reddit pickup), yet the KEV status and the specific ARM64 targeting of FortiGate make this more urgent than the broader CVE backlog. The mechanism is not a generic RCE; it is a targeted post-exploitation implant with discrete telemetry signatures.

Defenders should patch to the FortiGate release that remediates CVE-2024-47575, restrict management-plane access, and hunt for memory-only ARM64 implants with log paths tied to firewall process anomalies. Monitor for the PEERSTITCH IoC family and any new exploitation reports beyond the single Unit 42 disclosure.

Watch for second-source confirmation or an updated advisory with specific version ranges; a single-source KEV event with no telemetry pickup can shift quickly if exploitation scales.
