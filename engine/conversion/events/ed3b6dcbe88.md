*ShinyHunters EY campaign covered Jul 28–30. New today: the group claims a second major victim — Brinks Home — as the July 31 EY deadline arrives.*

Residential security provider **Brinks Home** (1M+ customers, ~$830M annual revenue) disclosed a breach detected July 20, with the attacker threatening to publish allegedly stolen data. **ShinyHunters** claimed the attack, alleging:

- **4.9 million Salesforce records** containing PII

- **1.1M+ rows** of customer data from the "Contacts" Salesforce object

- **4,000+ rows** of employee PII (names, emails, job titles, phone numbers)

- **3.8 million customer support chat logs** from the Brinks Care Cresta instance

ShinyHunters told BleepingComputer the initial access (July 13) came via a **Microsoft Entra voice phishing (vishing)** attack — an employee was talked through an Entra authentication/registration flow. Brinks says alarm monitoring was unaffected, has not confirmed what data was taken, and warns customers about follow-on phishing impersonating the company. BleepingComputer has not verified the claimed data.

**EY deadline note:** ShinyHunters' July 31 deadline for EY arrived today with no confirmed public data release reported as of digest time. Organizations with EY-adjacent data exposure should remain alert for downstream phishing.

**Action:** The Entra vishing vector is now confirmed against two consecutive ShinyHunters targets (EY via supply chain, Brinks via voice phishing). Enforce phishing-resistant MFA (FIDO2/WebAuthn), and treat unsolicited calls asking employees to complete authentication flows as a top-tier training scenario.
