CVE-2026-85921 is a critical elevation of privilege vulnerability in Windows Secure Kernel Mode, disclosed by Microsoft on September 14, 2026. The flaw affects the kernel's security isolation mechanisms, allowing an attacker to escape protected execution contexts.

The vulnerability carries high severity due to its location in the secure kernel, which underpins Virtualization-Based Security (VBS) and Credential Guard. Exploitation would allow an attacker running code on a system to bypass kernel-level protections and escalate to SYSTEM privileges.

Patch immediately when Microsoft releases the fix. In the interim, ensure VBS and HVCI are enabled to reduce attack surface. Monitor MSRC for updates on exploitation status.