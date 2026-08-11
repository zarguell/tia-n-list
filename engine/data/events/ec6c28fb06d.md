Qualys TRU disclosed a local privilege escalation in **snap-confine** affecting Ubuntu Desktop **24.04, 25.10, and 26.04**. An unprivileged local user can gain **full root access** by exploiting two concurrent race conditions:

1. A **FUSE filesystem mount** over the temp scratch directory before namespace isolation

2. A **symlink attack** causing snap-confine to write attacker-controlled content to an arbitrary target file

The vulnerability was introduced by a security hardening change that shifted snap-confine from set-uid-root to set-capabilities — demonstrating how hardening changes can inadvertently create new attack surfaces.

**Action:** Apply Ubuntu security updates. Restrict local access to Ubuntu Desktop systems running snap packages.

---
