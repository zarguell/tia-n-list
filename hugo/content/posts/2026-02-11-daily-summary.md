---
title: Microsoft zero-days 🚨, TeamPCP cloud exploits ☁️, APT36 espionage 🎯, UNC1069 AI lures 🤖, 7-Zip botnet 🦠
date: 2026-02-11
tags: ["zero-day exploits","cloud security","apt activity","malware distribution","authentication bypass","cryptocurrency targeting","espionage","ransomware","linux threats","ai-generated content"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Microsoft zero-day vulnerabilities enable system control and ransomware attacks while TeamPCP weaponizes exposed cloud services at scale. APT36 expands cross-platform surveillance with Linux RATs as UNC1069 blends AI-generated deepfake lures with multi-stage malware, and fake 7-Zip installers deploy persistent botnet infrastructure.
---

# Daily Threat Intel Digest - 2026-02-11

## 🔴 Critical Threats & Active Exploitation
**[NEW] Microsoft Patch Tuesday addresses 6 actively exploited zero-days**  
Attackers are leveraging six zero-day vulnerabilities across Windows components to achieve privilege escalation, bypass security features, and cause denial-of-service. Critical flaws include CVE-2026-21510 (Windows Shell bypassing "Mark of the Web" warnings via malicious LNK files) and CVE-2026-21519 (Desktop Window Manager elevation of privilege through type confusion). Both allow unauthenticated attackers to gain system control, with exploitation confirmed in ransomware and espionage campaigns. Organizations running Windows 10/11 and Server 2012-2025 should prioritize patches KB5077179 (Win11) and KB5075912 (Win10) immediately [[Microsoft February 2026 Patch Tuesday](https://cyberpress.org/microsoft-54-vulnerabilities-including-6-zero-days/)].

**[UPDATE] Ivanti Endpoint Manager authentication bypass enables remote data theft**  
Unauthenticated attackers can exploit CVE-2026-1603 (CVSS 8.6) in Ivanti Endpoint Manager (EPM) 2024 SU4 and earlier to extract credential data without login. This follows related Ivanti zero-days reported on Feb 10. While Microsoft patches Windows flaws, this EPM vulnerability exposes enterprise networks to credential theft via crafted requests. Administrators must upgrade to EPM 2024 SU5 and monitor for anomalous logins [[Ivanti Endpoint Manager Vulnerability](https://cyberpress.org/ivanti-endpoint-manager-vulnerability/); [GBHackers Coverage](https://gbhackers.com/ivanti-endpoint-manager-flaw/)].

**[UPDATE] FortiOS LDAP authentication bypass widens attack surface**  
CVE-2026-22153 (CVSS 7.5) in FortiOS 7.6.x allows attackers to bypass LDAP authentication if "unauthenticated binds" are enabled. This extends Fortinet vulnerabilities reported on Feb 9, enabling network infiltration without credentials by manipulating the fnbamd daemon. Affected users should upgrade to 7.6.5 or disable anonymous LDAP binds via PowerShell [[FortiOS Authentication Bypass](https://cyberpress.org/fortios-authentication-bypass-vulnerability/); [GBHackers Summary](https://gbhackers.com/fortios-vulnerability-enables-ldap-authentication-bypass/)].

## 🎯 Threat Actor Activity & Campaigns
**[NEW] TeamPCP automates cloud exploitation at scale**  
A campaign by TeamPCP (aka PCPcat) is weaponizing exposed Docker APIs, Kubernetes clusters, and Redis services to deploy a worm-like propagation infrastructure. The group's proxy.sh script installs persistence via system services and hijacks cloud resources for cryptomining, proxy resale, and data theft. By Dec 2025, 185+ Docker compromises were confirmed, with 61% of victims on Azure. Defenders should restrict public API access and monitor for unexpected DaemonSets or containers [[TeamPCP Campaign](https://cyberpress.org/teampcp-automates-cloud-exploits/)].

**[NEW] APT36 expands cross-platform espionage with Linux RATs**  
Transparent Tribe (APT36) is targeting Indian defense and government networks with Windows GETA RAT and Linux ARES RAT variants. New tools include Desk RAT (delivered via malicious PowerPoint Add-Ins) for real-time telemetry theft via WebSocket C2. The campaign leverages living-off-the-land binaries (LOLBins) on Windows and systemd services on Linux for persistence, signaling a shift toward broad-platform surveillance [[APT36 Linux Campaign](https://cyberpress.org/apt36-hits-linux-services/)].

**[NEW] UNC1069 blends AI-generated lures with multi-stage malware**  
North Korean-linked UNC1069 is using AI-generated deepfake videos in fake Zoom meetings to deploy WAVESHAPER and HYPERCALL downloaders on macOS. New malware families include DEEPBREATH (Swift-based keychain stealer) and CHROMEPUSH (browser cookie harvester), enabling credential theft from cryptocurrency targets. Organizations should block suspicious conferencing links and monitor for anomalous browser extension activity [[UNC1069 Attacks](https://cyberpress.org/unc1069-targets-finance-with-ai/)].

## ⚠️ Vulnerabilities & Patches
**[NEW] GitLab patches critical RCE and token exposure flaws**  
CVE-2025-7659 (CVSS 8.0) allows unauthenticated attackers to steal access tokens from GitLab’s Web IDE, while CVE-2025-8099 and CVE-2026-0958 (CVSS 7.5) enable denial-of-service via GraphQL and JSON validation middleware. Self-managed instances must update to 18.8.4, 18.7.4, or 18.6.6 to prevent unauthorized repository access and service crashes [[GitLab Vulnerabilities](https://cyberpress.org/gitlab-patches-multiple-vulnerabilities-enabling-dos-and-cross-site-scripting-attacks/)].

**[NEW] Fake 7-Zip installers deliver persistent proxy botnet**  
Trojanized 7-Zip installers from 7zip[.]com deploy Uphero.exe and hero.exe to Windows\System32, establishing SYSTEM-level persistence and firewall rule manipulation. The malware creates residential proxy nodes via encrypted C2, monetizing compromised systems for credential stuffing and ad fraud. IOCs include `Global\3a886eb8-fe40-4d0a-b78b-9e0bcb683fb7` mutex and hero.exe in SysWOW64 [[7-Zip Botnet](https://cyberpress.org/fake-7-zip-builds-botnet/)].

## 🛡️ Defense & Detection
**[NEW] Detect AI-generated malware with phase labels and verbose logs**  
The VoidLink Linux C2 framework (SHA256: 05eac3663d47a29da0d32f67e10d161f831138e10958dcd88b9dc97038948f69) uses AI-generated code artifacts like "Phase X:" labels and verbose debug outputs. Defenders should scan binaries for these signatures and monitor C2 communication to hardcoded IP 8.149.128.10 [[VoidLink Analysis](https://cyberpress.org/voidlink-showcases-ai-malware/)].

**[NEW] Block malicious Bing ads redirecting to fake Azure support**  
Tech support scams via Bing ads redirect users to Azure Blob Storage domains with paths ending in `werrx01USAHTML/index.html`, embedding phone numbers like 1-866-520-2041. Organizations should block sponsored search clicks and monitor for blob.core.windows.net referrals [[Bing Ad Scams](https://cyberpress.org/malicious-bing-ads-scam/)].

## 📋 Policy & Industry News
**[NEW] GitGuardian raises $50M to address non-human identity crisis**  
Funding led by Insight Partners will accelerate AI agent security and enterprise NHI (non-human identity) governance. As AI adoption exposes credential sprawl, GitGuardian aims to secure secrets and machine identities across development workflows [[GitGuardian Funding](https://blog.gitguardian.com/series-c-pr/)].

**[NEW] Model Context Protocol (MCP) introduces new AI attack surface**  
MCP standardizes AI tool integrations but risks confused deputy attacks, token passthrough, and tool poisoning. Defenders should enforce least-privilege scopes, audit MCP servers, and monitor prompt injection via tools like AI/DR Bastion [[MCP Security Risks](https://socprime.com/blog/mcp-security-risks-and-mitigations/)].