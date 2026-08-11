Threat actors are actively exploiting CVE-2026-4020, a medium-severity (CVSS 5.3) unauthenticated information disclosure vulnerability in the **Gravity SMTP WordPress plugin** (100,000+ active installs). The flaw stems from an exposed REST API endpoint (`/wp-json/gravitysmtp/v1/tests/mock-data`) whose `permission_callback` always returns `true`, allowing any unauthenticated visitor to extract a comprehensive JSON system report containing:

- API keys, secrets, and OAuth tokens for configured email integrations (Amazon SES, Google, Mailjet, Resend, Zoho)

- WordPress configuration details (installed plugins, themes, software versions)

- Database configuration (server version, table names)

- PHP environment information

Wordfence has blocked **over 17 million exploit attempts** against protected customers, with a spike of 4 million on June 7 alone. Successful exploitation allows attackers to impersonate the victim organization via email services and perform reconnaissance for follow-on attacks. All plugin versions 2.1.4 and older are affected; patched in version 2.1.5 (released March 17).

**Indicator:** Requests to `GET /wp-json/gravitysmtp/v1/tests/mock-data?page=gravitysmtp-settings` in web server access logs.

**Recommended action:** Update to Gravity SMTP ≥ 2.1.5 immediately. Rotate any email service API keys and OAuth tokens that may have been exposed.

---
