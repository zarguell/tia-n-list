Abbott Laboratories is investigating two separate cybersecurity incidents. The primary incident involves unauthorized access to legacy Exact Sciences systems in its Cancer Diagnostics business, confirmed after the **ShinyHunters** extortion gang added Abbott to its data leak site with an initial July 18 deadline (subsequently extended to July 21). ShinyHunters claims to have gained access through a vishing attack targeting multiple Abbott employees in mid-June, compromising a Microsoft Entra SSO account to reach connected SaaS applications.

The group claims exfiltration of data from Microsoft Entra, ServiceNow, SharePoint, Databricks, and Coupa — allegedly including 30+ million rows of customer PII (names, emails, phone numbers, SSNs), 22 million client notes with doctor-patient conversations, and 20 million medical orders.

A second, separate incident involves threat actor **ShadowByt3$** claiming access to Abbott's LabCentral customer portal via compromised customer credentials. Abbott states this portal houses only publicly available technical documents.

ShinyHunters has been increasingly targeting medtech companies, with prior victims including Medtronic, OneMedical, iRhythm, AdaptHealth, and Stryker.

**Action:** Monitor for data publication on ShinyHunters leak site. Organizations using SaaS platforms connected to Entra SSO should verify vishing resilience and review conditional access policies for SSO accounts.

---
