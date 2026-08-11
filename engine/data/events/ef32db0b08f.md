Huntress observed over **81 million password spray login attempts** between June 12–21 targeting Microsoft 365 environments through the Azure CLI, resulting in **78 compromised accounts across 64 organizations**. Attackers relied on the deprecated **OAuth ROPC (Resource Owner Password Credentials)** flow, which mints tokens without interactive MFA prompts — effectively bypassing MFA configurations not explicitly scoped to cover OAuth flows.

The attacks originated primarily from **AS32167 (LSHIY LLC)**, a Hong Kong/China/New York-based hosting provider. Huntress reports that credential spray volume has increased **155× across its customer base** in the past six months. Eight of the impacted organizations had **no MFA policy at all**. Huntress reported the abuse to LSHIY and received no response. The IPv6 ranges associated with LSHIY-linked ASNs have prior reports of originating from China.

**Recommended action:** Audit OAuth ROPC flow usage in your tenant — it is deprecated in OAuth 2.1. Ensure Conditional Access policies explicitly cover OAuth authentication flows, not just browser-based sign-ins. Review Sign-In logs for ROPC-based authentications from AS32167.

---
