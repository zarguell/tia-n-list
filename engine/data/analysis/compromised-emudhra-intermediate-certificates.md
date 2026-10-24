Cisco Talos disclosed eight eMudhra intermediate CA certificates with critically weak P-384 private keys (entropy reduced to single-digit values). Generated during an April 30, 2025 ceremony, the weak keys allow trivial impersonation. Chrome, Mozilla, Apple, and Microsoft have blocked the affected certificates.

eMudhra revoked the certificates and halted G3 root issuance. Organizations relying on these CAs should audit certificate chains and expect additional vendor patches. No active exploitation has been reported.
