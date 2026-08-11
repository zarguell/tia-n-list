Wordfence disclosed a critical unauthenticated authentication bypass in UpdraftPlus (3M+ active installs) affecting all versions ≤ 1.26.4. The vulnerability (CVE-2026-10795, CVSS 8.1) affects sites previously connected to UpdraftCentral — when the RSA decryption of the RPC message key fails, `phpseclib` returns `false` which passes to `Rijndael::setKey()`, collapsing to a deterministic all-zero AES-128 key. An attacker can forge arbitrary RPC commands as the connected admin, including uploading and activating a malicious plugin for full PHP/OS command execution.

Patched in version 1.26.5 (released June 5). Wordfence Premium users received a firewall rule on June 3; free users get protection July 3.

---
