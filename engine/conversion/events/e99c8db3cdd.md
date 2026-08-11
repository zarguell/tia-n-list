Hackers are actively targeting WordPress websites running WP Maps Pro — a premium interactive map plugin with **15,800+ sales** on Envato Market — exploiting a critical unauthenticated privilege escalation vulnerability tracked as **CVE-2026-8732**. The flaw lies in a "temporary access" AJAX endpoint intended for vendor support access, protected only by a publicly exposed nonce in frontend JavaScript.

Attackers send a crafted request with `check_temp` set to `false`, triggering `wp_insert_user()` to create a new WordPress administrator account with a randomized username, hardcoded email (`support@flippercode.com`), and a passwordless "magic login URL" returned in the response body. Wordfence researchers blocked **3,600+ exploitation attempts in 24 hours**.

**Impact:** Full site takeover — persistent backdoors, web shells, malicious plugin installation, private data access. All versions before 6.1.1 are vulnerable. The patch was released May 20 (vendor notified May 16 after proof of concept). Administrators should update immediately and audit for rogue admin accounts.

---
