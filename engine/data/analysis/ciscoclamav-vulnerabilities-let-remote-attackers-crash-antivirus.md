Cisco disclosed seven high-severity vulnerabilities in ClamAV, tracked as CVE-2026-20337, CVE-2026-20338, CVE-2026-20339, CVE-2026-20345, CVE-2026-20346, CVE-2026-20347, and CVE-2026-20348, with a maximum CVSS score of 7.5. The flaws let unauthenticated remote attackers disrupt antivirus scanning by submitting specially crafted files, in practice crashing or hanging the scanner. Cisco notes public proof-of-concept material for the issues.

ClamAV is the engine behind a lot of mail-gateway and cloud scanning pipelines, so the impact is broader than a single product. A scanner that can be killed remotely by a crafted file is a denial-of-service lever against the very controls organizations rely on for ingress filtering.

Apply the ClamAV updates wherever the engine is embedded, and inventory third-party products that bundle their own copies, since those often lag. Given public PoC availability, expect weaponization attempts against exposed scanning infrastructure.
