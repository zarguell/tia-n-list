Cisco Talos found that eight intermediate certificates issued by eMudhra were generated with weak private keys due to a flaw in a key generation ceremony on April 30, 2025. Several keys evaluated to single or double digit integers instead of 384 bits of entropy, making private key recovery trivial and allowing impersonation of any website or service.

Six TLS certificates trusted by Chrome, Mozilla, and Apple have already been blocked by those vendors, and two code-signing certificates used by Microsoft were also blocked. eMudhra revoked the compromised certificates and stopped issuing under its G3 root.

Defenders should expect additional patches across software that trusted the affected intermediates and should verify that their trust stores and code-signing validation reject the revoked certificates.
