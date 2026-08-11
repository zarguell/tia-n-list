Palo Alto Networks' Unit 42 documented a social engineering campaign in which threat actors abuse Microsoft Teams voice calls to deploy the EtherRAT malware for initial access to corporate networks. The kill chain:

1. **Phishing email** with "Employee Survey" lure and malicious PDF attachment

2. **Microsoft Teams voice call** from an external account impersonating IT support (account: `helpdesk@Progressive936.onmicrosoft[.]com`)

3. **Remote control granted** through Teams' built-in screen sharing

4. **Legitimate RMM tools installed** (HopToDesk, AnyDesc) to maintain persistent access

5. **EtherRAT malware loaded** via malicious MSI installer (`v7.msi`) from `camorreado[.]click`, deploying a Node.js-based loader

The attack exploits a gap in most security awareness training: users are trained not to install software from unknown sources but are less prepared to refuse help from someone who has already called and established rapport.

**Recommended action:** Configure Microsoft Teams external access policies to restrict cross-tenant communications. Educate staff that IT support will never request remote control via unsolicited voice calls. Block MSI downloads from untrusted domains.

---
