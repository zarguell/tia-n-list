Firmware security firm Binarly has disclosed six vulnerabilities in the U-Boot bootloader's FIT (Flattened Image Tree) signature verification code. Two flaws (BRLY-2026-037, BRLY-2026-038) can lead to arbitrary code execution during firmware verification, while four others cause denial of service via crashes. The vulnerable code has existed since U-Boot version 2013.07, potentially affecting 50+ stable releases and downstream vendor forks.

Because exploitation occurs before the operating system loads, attackers can disable firmware security features, install persistent firmware malware, and carry out actions undetectable by OS-level security tools. On systems like BMCs that support remote firmware updates, exploitation does not always require physical access — a compromised management interface is sufficient. Patches have been accepted into upstream U-Boot, but distribution to end devices depends on individual hardware vendors' firmware update cycles.

---
