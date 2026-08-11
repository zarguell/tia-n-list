Ruby on Rails released emergency fixes for **CVE-2026-66066**, a critical **Active Storage** vulnerability letting an unauthenticated attacker read **arbitrary files from the application server** through crafted image uploads — potentially escalating to RCE and lateral movement.

**Root cause:** Active Storage passes uploaded attachments to **libvips** (default processor since Rails 7.0) without blocking "untrusted" operations — unsafe libvips loaders can be invoked by a malicious file to disclose data readable by the Rails worker.

**Exposure:** secret_key_base, `config/master.key`, decrypted credentials, database passwords, cloud storage keys (S3/GCS/Azure), and third-party API tokens. Obtaining secret_key_base can enable session forgery and, with gadget chains, code execution. Affects Rails 7.0–7.2.3.1, 8.0–8.0.5, 8.1–8.1.3 using libvips with untrusted uploads. **No known in-the-wild exploitation**; a third-party PoC claiming an arbitrary-file-read-to-RCE chain appeared shortly after disclosure. Rails 7.0/7.1 are EOL and get no backport.

**Action:** Upgrade to Rails 7.2.3.2 / 8.0.5.1 / 8.1.3.1 with **libvips 8.13+** (or ruby-vips 2.2.1+); interim: set `VIPS_BLOCK_UNTRUSTED`. **Rotate every secret readable by the Rails process** — updating the code does not invalidate already-disclosed credentials.
