Two CVSS 9.0 remote code execution vulnerabilities in the Linux kernel's in-kernel SMB server (KSMBD) were disclosed on public mailing lists before mainline fixes were available. One of them, ZDI-CAN-33774, is pre-authentication, meaning an unauthenticated attacker could potentially trigger it.

The disclosure happened on public mailing lists ahead of coordinated patches, leaving a window where the flaws were known but unpatched in mainline. This kind of accidental early disclosure compresses the time defenders have to react.

Administrators running KSMBD should track kernel updates closely and disable the in-kernel SMB server where it is not needed, since the pre-auth vector raises the risk of rapid exploitation once details circulate.