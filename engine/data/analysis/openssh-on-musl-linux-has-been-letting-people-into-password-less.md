CVE-2026-123158, dubbed "sshole," is a password-authentication bypass in OpenSSH's sshd on musl-based Linux systems (Alpine, OpenWrt, Buildroot, Yocto) with PAM disabled. Accounts whose password field holds only "*" (password login disabled) can be accessed using any password of 257 to 1,024 characters, because OpenSSH's 2016 fix for CVE-2016-6210 forces password hashing on unusable hashes and musl's crypt() returns "*" when hashing fails. The bug has existed since 2016.

OpenSSH 10.6p2 (November 5, 2026) fixes it; Alpine published fixed packages for branches 3.16 to edge the same day. No in-the-wild exploitation was reported at release, but the bug is trivially triggered. A hackread report links the flaw to follow-on Python backdoor installation and CISA confirmation of exploits as patched packages became available.

Patch all musl-based OpenSSH servers, especially Alpine default openssh-server installs. Audit accounts with "*" password fields and review for unauthorized access. The flaw illustrates how constant-time mitigations can introduce new failure modes when layered on libraries with different error semantics.

