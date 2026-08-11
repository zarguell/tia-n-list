AISLE's autonomous vulnerability detection platform identified the **oldest security issue ever reported in curl**, a bug dating back approximately 25 years. CVE-2026-8932 exists because libcurl could **reuse an existing connection even after client certificate or private key settings had changed**, potentially exposing credentials to the wrong endpoint. Fixed in curl release **8.21.0** (June 24, 2026). AISLE discovered 6 CVEs in curl total this year.

The curl project noted this is the oldest vulnerability ever found in the tool, underscoring both the value of AI-assisted code auditing for legacy codebases and the difficulty of discovering subtle logical errors in decades-old network protocol implementations.

---
