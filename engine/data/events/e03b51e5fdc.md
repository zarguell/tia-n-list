*Previously covered July 5 at disclosure. New today: Public proof-of-concept exploit released.*

Technical details and working PoC exploit code for CVE-2026-46242 (CVSS 7.8), the Linux kernel's "Bad Epoll" race-condition use-after-free vulnerability, have been publicly released by discoverer Jaeyoung Chung of Seoul National University. The PoC exploits the close-vs-close race condition in epoll's file-release path to leak kernel memory and hijack an indirect call via a ROP chain to obtain root privileges.

Key technical details from the published exploit:

- Bad Epoll was introduced in a 2023 kernel commit that also introduced CVE-2026-43074 (found by Anthropic's Mythos)

- Mythos likely missed Bad Epoll because, with the sibling bug fixed, it doesn't trigger KASAN (Kernel Address Sanitizer)

- The kernel maintainers' first patch did not fully fix the issue; the correct fix landed only two months after initial reporting

- Affects Linux 6.4+; confirmed exploitable on Pixel 10 devices (kernel 6.6)

- PoC uses memory leak to bypass KASLR, then ROP chain for privilege escalation

**Recommended action:** Apply latest kernel updates. For Linux 6.4+ systems where patching is delayed, monitor for unusual epoll-related activity. Android Pixel 10 users should verify security patch levels.

---
