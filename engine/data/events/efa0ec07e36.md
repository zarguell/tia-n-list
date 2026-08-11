A critical unauthenticated RCE in Mirasvit Full Page Cache Warmer — one of the most popular Magento/Adobe Commerce cache extensions — carries a CVSS 9.8 score. The `CacheWarmer` cookie value is passed directly to PHP's `unserialize()` with no authentication gate, enabling classic PHP Object Injection. Any internet-facing storefront page is an attack vector. Sansec estimates **6,000+ vulnerable stores** (likely far higher behind CDNs). Patched in version 1.11.12. Cookie pattern `CacheWarmer:(Tz|Qz|YT)` indicates exploitation attempts.

---
