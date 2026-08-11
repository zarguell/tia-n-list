Malwarebytes' Threatdown team has identified a new hands-on-keyboard ransomware operation named **Prinz Eugen** with several unusual characteristics.

Key findings from the investigation:

- **Initial access**: Stolen RDP credentials, followed by manual payload deployment (`servertool.exe`)

- **RMM abuse**: RemotePC tool used for persistence via backdoor admin account

- **Encryption**: Go-based binary using **ChaCha20-Poly1305** with Argon2id/SHA-256/HKDF-SHA256 key derivation; processes files in 1 MB chunks with SHA-256 integrity verification

- **Targeting prioritization**: Most recently modified files encrypted first; when timestamps tie, alphabetical order — designed to maximize pressure on victims by hitting business-critical data in active use

- **Anti-forensics**: Encryption key overwritten with zeroes, garbage collection forced, then self-deletes from disk

At least **5 victims** identified by researchers, with only 3 currently listed on the leak site. In one incident (Standard Bank), the attacker demanded 1 BTC and was refused.

---
