ReliaQuest has analyzed two new phishing toolkits targeting Microsoft 365 accounts. **Jalisco** uses the device-code phishing method, generating fresh Microsoft OAuth device codes in real-time when a victim opens the phishing page — bypassing Microsoft's 15-minute device code validity window designed to fight this attack vector. Attackers register rogue devices under benign names like "Microsoft" or "Windows" and exfiltrate SharePoint/SaaS data within **six minutes** of compromise. OmegaLord uses a fake PDF reader login page to harvest email addresses, passwords, and phone numbers for MFA interception.

Both kits follow the pattern of device-code phishing kits (EvilTokens, Kali365, Tycoon2FA, Venom, Forg365) that continue to proliferate. ReliaQuest recommends reducing the Entra ID device-registration limit from the default of 50 to 1-2, blocking device-code authentication via Conditional Access, and restricting OAuth Device Authorization grants.

---
