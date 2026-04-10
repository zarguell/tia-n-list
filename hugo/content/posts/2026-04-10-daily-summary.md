---
title: EngageSDK credential theft exposes 50M+ Android apps 📱, VENOM PhaaS targets C-suite executives 🎯, Iranian APTs pivot to critical infrastructure ⚡, supply chain attacks accelerate via automation 🤖
date: 2026-04-10
tags: ["mobile vulnerabilities","credential theft","phishing-as-a-service","critical infrastructure","apt activity","supply chain security","ai safety","iot security","ransomware","mobile apps"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: A critical EngageSDK flaw has exposed over 50 million Android app installations to credential theft, highlighting the systemic risk of third-party library vulnerabilities in mobile ecosystems. Meanwhile, sophisticated threat actors are escalating campaigns across multiple fronts: the VENOM phishing-as-a-service platform is targeting C-suite executives with AiTM techniques that defeat traditional MFA, Iranian APTs are actively exploiting exposed Rockwell PLCs across U.S. critical infrastructure, and automated supply chain attacks via Renovate and Dependabot are compressing infection timelines to under an hour. Security teams should prioritize patching mobile dependencies, enforce FIDO2 authentication for executives, audit exposed OT environments, and implement cooldown periods for automated dependency updates to counter these converging threats.
---


# Daily Threat Intel Digest - 2026-04-10

## 🔴 Critical Threats & Active Exploitation

**[NEW] EngageSDK Vulnerability Exposes 50+ Million App Installations to Credential Theft**

A critical flaw in EngageSDK, a widely deployed Android communication library, has exposed over 50 million app installations—including more than 30 million cryptocurrency wallet applications—to severe data theft. The vulnerability (CVE details pending) allows malicious apps on the same device to bypass Android's security sandbox by exploiting an improperly exported activity component. Attackers can craft malicious intents that hijack trusted app privileges, granting persistent read/write access to private directories and enabling theft of credentials and financial data. Microsoft researchers, who discovered the flaw, report that developers must update to EngageSDK version 5.2.1 or later. Android has also implemented temporary automatic protections. Organizations should verify that cryptocurrency and financial applications are running patched versions and audit merged Android manifests when updating third-party dependencies. [[CyberPress](https://cyberpress.org/engagesdk-flaw-endangers-millions/)] [[SecurityWeek](https://www.securityweek.com/microsoft-finds-vulnerability-exposing-millions-of-android-crypto-wallet-users/)]

**[NEW] Critical Marimo Flaw Exploited Within Hours of Disclosure**

Security researchers have confirmed active exploitation of a critical vulnerability in Marimo, a popular open-source reactive notebook environment for Python. The flaw was leveraged by threat actors within hours of public disclosure, demonstrating the increasingly compressed timeline between vulnerability release and weaponization. Organizations running affected Marimo versions should apply patches immediately and monitor for indicators of compromise including unusual network connections and anomalous Python execution patterns. [[SecurityWeek](https://www.securityweek.com/critical-marimo-flaw-exploited-hours-after-public-disclosure/)]

**[NEW] Juniper Networks vLWC Default Credentials Allow Full Device Takeover**

Juniper Networks has released emergency patches for a critical vulnerability (CVE-2026-33784, CVSS 9.8) in its Support Insights Virtual Lightweight Collector (vLWC) that allows remote, unauthenticated attackers to seize complete administrative control. The flaw stems from default credentials that are not enforced to be changed during initial provisioning—any attacker with network access can authenticate using publicly known login details. All vLWC versions prior to 3.0.94 are affected. Juniper states no evidence of active exploitation exists, but the trivial exploitability warrants immediate patching. Organizations unable to patch immediately can manually change default passwords via the JSI Shell. [[CyberPress](https://cyberpress.org/juniper-networks-default-password-flaw-lets-attackers-take-full-control-of-devices/)] [[GBHackers](https://gbhackers.com/juniper-networks-default-credential-vulnerability/)]

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Iranian BITTER APT Deploys ProSpy via Fake Secure Messaging Apps**

The BITTER (Gallium) APT group is conducting a hack-for-hire espionage campaign targeting journalists, activists, and political figures across the Middle East. The operation distributes a sophisticated Android spyware called ProSpy through malicious applications impersonating popular secure messaging platforms. The campaign has been active since at least 2022, primarily targeting civil society members and potentially government officials in regional countries. Users in affected regions should exercise extreme caution when downloading messaging applications, verify app authenticity through official stores, and monitor devices for suspicious permissions or unusual behavior. [[GBHackers](https://gbhackers.com/secure-messaging-apps-2/)]

**[UPDATE] Iranian MuddyWater Shifts to Russian MaaS Infrastructure**

Researchers have uncovered fresh evidence linking the Iranian state-sponsored group MuddyWater to CastleRAT, a Russian-operated malware-as-a-service platform, in a new campaign dubbed "ChainShell." This represents a significant strategic evolution for MuddyWater, which historically relied on custom PowerShell tools. The operation deploys a previously undocumented JavaScript-based malware called ChainShell that uses blockchain smart contracts to dynamically locate its command-and-control infrastructure, making takedowns substantially more difficult. The malware operates as a "thin shell" executing attacker-delivered commands rather than containing built-in functions. MuddyWater used multiple CastleRAT builds hidden within steganographic image files and primarily targets Israeli government, defense, and technology sectors. Security teams should monitor for PowerShell execution from unexpected locations, blockchain-based C2 communications, and JWT credentials associated with serialmenot.com infrastructure. [[CyberPress](https://cyberpress.org/muddywater-adopts-russian-maas/)] [[GBHackers](https://gbhackers.com/maas-in-new-chainshell-attack/)]

**[NEW] VENOM PhaaS Platform Targets C-Suite Executives**

A previously undocumented phishing-as-a-service platform called "VENOM" is conducting credential theft campaigns targeting CEOs, CFOs, and VPs across multiple industries. Active since November 2025, the closed-access operation impersonates Microsoft SharePoint notifications and employs sophisticated evasion techniques including double Base64-encoded target emails hidden in URL fragments, QR code redirects to bypass email security scanners, and sandbox environment filtering. The platform uses adversary-in-the-middle (AiTM) techniques to capture both credentials and MFA tokens in real-time, then quickly establishes persistence by registering new devices or obtaining device code tokens. The emergence of closed-access PhaaS platforms with AiTM capabilities significantly reduces the effectiveness of traditional MFA. Security teams should enforce FIDO2 authentication for executives, disable device code flows where unnecessary, and implement stricter conditional access policies. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-venom-phishing-attacks-steal-senior-executives-microsoft-logins/)]

**[NEW] LucidRook Lua-Based Malware Targets NGOs and Universities in Taiwan**

Cisco Talos researchers are tracking a new Lua-based malware called LucidRook, attributed to threat group UAT-10362, in spear-phishing campaigns targeting non-governmental organizations and universities in Taiwan. The malware uses an embedded Lua execution environment that allows operators to update functionality via externally delivered bytecode without modifying the core implant, improving operational security and limiting forensic visibility. Infection chains leverage LNK shortcut files delivering the LucidPawn dropper or fake antivirus executables impersonating Trend Micro. After establishing persistence, LucidRook performs system reconnaissance and exfiltrates data encrypted in password-protected archives via FTP. A related reconnaissance tool called LucidKnight abuses Gmail GMTP for data exfiltration. Organizations with Taiwan-facing operations should monitor for unusual FTP connections, suspicious Trend Micro executables, and LNK files from unknown sources. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-lucidrook-malware-used-in-targeted-attacks-on-ngos-universities/)]

## ⚠️ Vulnerabilities & Patches

**[NEW] AWS Research and Engineering Studio RCE and Privilege Escalation Flaws**

AWS has released emergency patches addressing three critical vulnerabilities in its Research and Engineering Studio (RES), an open-source platform for managing secure cloud-based research environments. The flaws affect versions 2025.12.01 and earlier and could allow authenticated attackers to achieve remote code execution with root privileges on virtual desktop hosts, escalate privileges by assuming Virtual Desktop Host instance profiles, and compromise the cluster-manager EC2 instance via command injection through the FileBrowser API. Successful exploitation could enable data exfiltration, unauthorized compute usage, and lateral movement across AWS services. AWS has addressed all three CVEs (CVE-2026-5707, CVE-2026-5708, CVE-2026-5709) in RES version 2026.03. Organizations using RES should upgrade immediately. [[CyberPress](https://cyberpress.org/aws-fixes-critical-rce-and-privilege-escalation-flaws-in-research-and-engineering-studio/)] [[GBHackers](https://gbhackers.com/aws-fixes-severe-rce-privilege-escalation-flaws/)]

**[NEW] AI Model "Sockpuppeting" Attack Bypasses Safety Guardrails**

Trend Micro researchers have disclosed a novel jailbreak technique called "sockpuppeting" that exploits the assistant prefill API feature to bypass safety guardrails in 11 major large language models including ChatGPT, Claude, and Gemini. By injecting a fake response prefix (e.g., "Sure, here is how to do it:") directly into the response stream, attackers can trick models into continuing prohibited outputs. The attack requires no access to model weights or complex optimization—only API-level manipulation. Attack success rates vary by provider, with Google Gemini 2.5 Flash showing the highest vulnerability (15.7%) and DeepSeek-R1 with prefill restrictions showing zero successful attacks. Leading providers including OpenAI, Anthropic, and AWS have implemented protections that reject prefilled assistant inputs. However, self-hosted deployments using Ollama or vLLM often lack built-in validation and remain exposed. Security teams should enforce API-level message validation ensuring the final message originates from the user, not the assistant. [[CyberPress](https://cyberpress.org/single-line-of-code-can-jailbreak-11-ai-models-including-chatgpt-claude-and-gemini/)] [[GBHackers](https://gbhackers.com/11-ai-models-vulnerable-to-one-line-jailbreak/)]

**[NEW] React Server Components DoS Vulnerability**

A high-severity vulnerability (CVE-2026-23869) in React Server Components could allow unauthenticated attackers to trigger denial-of-service conditions in affected web applications. The flaw requires no privileges and involves low attack complexity, enabling easy exploitation. Organizations using server-side rendering packages should prioritize patching. [[GBHackers](https://gbhackers.com/new-react-server-components-flaw/)]

**[NEW] Iranian APT Targets 5,219 Rockwell PLCs Across U.S. Critical Infrastructure**

Censys researchers have identified over 5,200 Rockwell Automation/Allen-Bradley programmable logic controllers exposed to the internet as Iranian-affiliated APT actors actively target these devices across U.S. critical infrastructure. The same operators were previously associated with the November 2023 campaign that compromised at least 75 Unitronics PLCs in water and wastewater facilities. Security teams should immediately audit operational technology environments for exposed PLCs, implement network segmentation, and verify that PLCs are not directly accessible from the internet. [[GBHackers](https://gbhackers.com/iranian-apt-alert/)]

**[NEW] HPE Aruba Private 5G Core Vulnerability Enables Credential Theft**

A newly disclosed vulnerability (CVE-2026-23818) in HPE Aruba Networking Private 5G Core On-Prem allows threat actors to silently harvest administrative login credentials through the platform's graphical user interface. Organizations deploying HPE Aruba Private 5G Core should review HPESBNW05032EN_US and apply available patches. [[GBHackers](https://gbhackers.com/hpe-aruba-private-5g-vulnerability/)]

## 🛡️ Defense & Detection

**[NEW] Chrome 147 Patches 60 Vulnerabilities, Expands Cookie Theft Protections**

Google has released Chrome 147 patching 60 vulnerabilities, including two critical flaws with combined bug bounty awards of $86,000. Separately, Google announced expanded cookie theft protections in Chrome, implementing new defenses against session hijacking techniques that have been widely adopted by threat actors including infostealers and RATs. Organizations should ensure Chrome deployments are updated to version 147 or later. [[SecurityWeek](https://www.securityweek.com/chrome-147-patches-60-vulnerabilities-including-two-critical-flaws-worth-86000/)] [[SecurityWeek](https://www.securityweek.com/google-rolls-out-cookie-theft-protections-in-chrome/)]

**[NEW] Renovate and Dependabot Emerging as Supply Chain Attack Accelerators**

A detailed GitGuardian analysis reveals that automated dependency update tools—Renovate and Dependabot—are increasingly being weaponized to accelerate supply chain attacks. During the malicious axios 1.14.1 compromise, the malicious package was live for only hours, yet automated systems across hundreds of repositories had already processed the attack. Pull requests were opened, merged, and pushed directly to main branches without human approval. In one case, the malicious update was merged within 56 minutes due to auto-merge workflows. Organizations should implement cooldown periods (3-5 days recommended) for dependency updates, prevent Renovate from updating immutable version pins within the same version tag, and apply these controls across all package managers including npm, pip, and uv. [[GitGuardian](https://blog.gitguardian.com/renovate-dependabot-the-new-malware-delivery-system/)]

**[NEW] Remcos RAT Distributed via Google Cloud Storage Phishing**

Threat actors are leveraging trusted Google Cloud Storage infrastructure to host phishing pages distributing the Remcos Remote Access Trojan, effectively bypassing reputation-based security filters. The multi-stage infection chain uses JavaScript launchers, VBS scripts, and process hollowing into legitimate Microsoft binaries (RegSvcs.exe) to evade detection. The campaign establishes persistence via Windows Startup folder and uses behavioral analysis evasion techniques. Security teams should monitor for unusual script execution patterns, unexpected network connections from native Windows binaries, and anomalous memory allocations indicative of process hollowing. [[CyberPress](https://cyberpress.org/google-storage-drops-remcos/)]

**[NEW] GlassWorm Supply Chain Attack Expands to Developer IDEs**

The GlassWorm malware campaign, initially observed spreading through npm packages in March 2025, has expanded to abuse the OpenVSX extension marketplace targeting Visual Studio Code, Cursor, and Windsurf IDEs. Organizations using these development environments should verify extension sources, audit installed extensions, and implement strict extension signing requirements where possible. [[GBHackers](https://gbhackers.com/glassworm-malware-4/)]

## 📋 Policy & Industry News

**[NEW] FCC Bans Foreign-Made Consumer Routers**

The Federal Communications Commission has updated its Covered List to implement a ban on foreign-made consumer routers based on a National Security Determination issued by the White House on March 20, 2026. The action targets foreign-produced networking equipment identified as exploited in high-profile attacks including Volt, Flax, and Salt Typhoon campaigns. The ban affects new router models from virtually all major consumer brands; manufacturers must now seek conditional approval from the Department of Justice or Department of Homeland Security to sell products in the U.S. Existing devices are not affected. The policy shift is driving increased interest in prosumer and SMB-oriented solutions from brands like Ubiquiti and EnGenius. [[Malware.news](https://malware.news/t/why-did-the-fcc-ban-foreign-made-consumer-routers/105926#post_1)]

**[NEW] Project Glasswing: Tech Giants Unite Against AI-Accelerated Vulnerability Discovery**

An unprecedented industry coalition including AWS, Anthropic, Apple, Cisco, CrowdStrike, Google, Microsoft, NVIDIA, and Palo Alto Networks has launched "Project Glasswing" in response to frontier AI models demonstrating the ability to discover and weaponize vulnerabilities at machine speed. Anthropic's Claude Mythos Preview achieved an 83.1% score on the CyberGym benchmark measuring AI vulnerability reproduction capability—a threshold researchers describe as a "no going back" moment. Testing revealed thousands of zero-day vulnerabilities including a 27-year-old flaw in OpenBSD and a 16-year-old vulnerability in FFmpeg that evaded 5 million automated scans. The project commits $100 million in Claude usage credits and $4 million in direct donations to open-source security initiatives including the Alpha-Omega project and OpenSSF. [[SocFortress Medium](https://socfortress.medium.com/project-glasswing-why-the-worlds-biggest-tech-rivals-just-teamed-up-to-save-the-internet-0360b5c0f4e6)]

## ⚡ Quick Hits

- **Payload ransomware** claimed responsibility for cyberattack against El Wastani Petroleum Company (WASCO), an Egyptian oil and gas firm, threatening data leak. [[Malware.news](https://malware.news/t/payload-ransomware-targets-el-wastani-petroleum-company/105923#post_1)]

- **IncRansom** targeted U.S. transportation company Rood Trucking in ransomware attack. [[Malware.news](https://malware.news/t/incransom-targets-rood-trucking-in-ransomware-attack/105922#post_1)]

- **Qilin ransomware** attacked Neurologic Associates of Central Brevard, a U.S. healthcare provider. [[Malware.news](https://malware.news/t/qilin-ransomware-targets-neurologic-associates-of-central-brevard/105921#post_1)]

- **Google** rolled out Gmail end-to-end encryption for enterprise users on Android and iOS, enabling native encrypted email composition without additional applications. [[BleepingComputer](https://www.bleepingcomputer.com/news/google/google-rolls-out-gmail-end-to-end-encryption-on-mobile-devices/)]

- **WhatsApp** began rolling out username functionality allowing users to communicate without sharing phone numbers, addressing doxing and targeted spam risks. [[CyberPress](https://cyberpress.org/whatsapp-rolls-out-usernames/)] [[GBHackers](https://gbhackers.com/whatsapp-adds-username-feature/)]

- **GitHub and GitLab** continue to be abused for malware hosting and credential phishing campaigns, with threat actors leveraging developer trust to evade enterprise security controls. [[GBHackers](https://gbhackers.com/github-abused-2/)]

- **TP-Link Archer AX53 v1.0** router contains five security vulnerabilities enabling full device compromise; users should apply firmware updates when available. [[GBHackers](https://gbhackers.com/tp-link-devices-at-risk-as-multiple-security-flaws/)]