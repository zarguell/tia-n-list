Nebula Security published exploit code for **GhostLock**, a use-after-free vulnerability in the Linux kernel present since kernel 2.6.39 (2011) across all major distributions. The flaw exists in a task-priority cleanup helper function — when a deadlock triggers a rollback, memory is freed while a dangling pointer remains in another task, enabling local privilege escalation to root. Patched in April 2026. Nebula demonstrated container escape via Google's kernelCTF program and received a $92,337 bounty.

---
