Security researcher Kevin Beaumont documented a **supply chain compromise of ad network Adform** that served clipboard-swapping crypto-stealer JavaScript to users across the web — activity the security industry missed for about a week.

**Technical details:**

- Malicious code in `trackpoint-async.js` (served from `s2.adform.net`) polls the clipboard **every 3 seconds** and replaces valid **Bitcoin, Ethereum, and TRX wallet addresses** with attacker-controlled ones — victims who notice and recopy the correct address get re-swapped

- Also records **victim IP, referring website, and URL path**, beaconing to attacker server `84.32.102.230:7744`

- The sample flags as **clean across all vendors on VirusTotal** at time of writing

- Malicious code appeared to be disappearing as of publication — either Adform became aware or the attacker rotated

**Hunting hypothesis:** Monitor for clipboard API access patterns in ad-script contexts and beaconing to port 7744 from browsers; ad-integrity teams should review third-party script integrity for `s2.adform.net` resources.

**Action:** Organizations serving ads through Adform should review their ad-chain script inventory; users making crypto payments should verify addresses at the point of confirmation, not the clipboard.

---
