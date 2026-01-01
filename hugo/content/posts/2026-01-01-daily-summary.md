---
title: Crypto governance hijack 💰, Botnet cryptominer deployment 🖥️, ClickFix automation toolkit 🎯, VS Code malware threat 💻, Healthcare enforcement ⚖️
date: 2026-01-01
tags: ["cryptocurrency theft","botnet activity","clickfix attacks","malware distribution","governance vulnerabilities","healthcare security","phishing","supply chain attacks","regulatory enforcement","macos malware"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Cryptocurrency governance attacks and botnet-driven cryptomining campaigns demonstrate evolving financial and infrastructure threats, while automated ClickFix toolkits lower the barrier for entry-level attackers. Supply chain compromises through development environments and healthcare regulatory enforcement highlight expanding attack surfaces and increasing accountability for security controls.
---

# Daily Threat Intel Digest - 2026-01-01

## 🔴 Critical Threats & Active Exploitation

**[NEW] $3.9M Crypto Theft via Multisig Governance Hijack**  
Attackers compromised Unleash Protocol's multisig governance system, executing unauthorized contract upgrades to drain $3.9M in WIP, USDC, and WETH assets [[BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-drain-39m-from-unleash-protocol-after-multisig-hijack/)]. The stolen funds were laundered through Tornado Cash, highlighting persistent weaknesses in blockchain governance controls. Unleash has paused operations amid investigations by external security firms.

**[UPDATE] RondoDox Botnet Deploys Cryptominers via React2Shell**  
Expanding beyond prior RCE exploitation [[BleepingComputer](https://www.bleepingcomputer.com/news/security/rondodox-botnet-exploits-react2shell-flaw-to-breach-nextjs-servers/); [CloudSEK](https://www.cloudsek.com/blog/rondodox-botnet-weaponizes-react2shell)], RondoDox now leverages CVE-2025-55182 to deliver coinminers (/nuts/poop) and Mirai variants (/nuts/x86) on 94,000+ exposed Next.js servers. The botnet's payloads include persistence mechanisms via /etc/crontab and aggressive competitor malware removal, with hourly IoT exploitation waves targeting consumer routers.

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] ErrTraffic v2 Industrializes ClickFix Attacks**  
The $800 ErrTraffic toolkit now automates ClickFix scams with 60% infection rates [[CyberPress](https://cyberpress.org/errtraffic-clickfix-cyberattacks/); [QuoIntelligence](https://quointelligence.eu/2025/12/threat-intelligence-snapshot-week-1-2026/)], using fake UI glitches to trick users into executing PowerShell scripts. Its dashboard excludes CIS regions and routes stolen data via Telegram bots, enabling entry-level attackers to deploy platform-specific payloads (Windows/macOS/Android) from a single HTML injection point.

**[NEW] GlassWorm Malware Targets macOS via VS Code Extensions**  
Three malicious VS Code extensions on the Open VSX marketplace delivered GlassWorm to 50,000+ macOS users [[GBHackers](https://gbhackers.com/glassworm-malware-2/)]. The self-propagating malware evolved from its initial October Unicode-based attacks, now achieving persistence through compromised development environments.

## ⚠️ Vulnerabilities & Patches

**[NEW] NYC Event Security Policy Names Specific Cyber Tools**  
The NYC mayoral inauguration explicitly banned Flipper Zero and Raspberry Pi devices [[BleepingComputer](https://www.bleepingcomputer.com/news/security/nyc-mayoral-inauguration-bans-flipper-zero-raspberry-pi-devices/)], marking a rare instance of hardware-specific restrictions at public events. The policy creates confusion as laptops/phones—capable of greater exploitation—are permitted, reflecting nascent regulatory approaches to cybersecurity hardware.

**[NEW] Trail of Bits Detects Go Integer Overflows via go-panikint**  
A modified Go compiler ($$) exposes silent arithmetic bugs by converting overflows to panics [[Trail of Bits](https://blog.trailofbits.com/2025/12/31/detect-gos-silent-arithmetic-bugs-with-go-panikint/)], revealing a live Cosmos SDK RPC pagination flaw. The tool targets a critical blind spot in Go's memory safety design, enabling fuzzing campaigns to identify reachable logic vulnerabilities.

## 🛡️ Defense & Detection

**[NEW] SIEM Integration Enables Custom Impossible Travel Detection**  
SOCFortress released an open-source architecture combining Wazuh, Graylog, and FastAPI to detect O365 impossible travel [[SOCFortress](https://socfortress.medium.com/office365-impossible-travel-detection-with-wazuh-graylog-and-a-custom-python-api-0a0a383d1603?source=rss-36613248f635------2)]. The Python API geolocates IPs, tracks user history, and calculates travel thresholds, showcasing a modular approach for stateful detections beyond built-in rule engines.

**[NEW] WordPress Phishing Harvests 3-D Secure OTPs via Telegram**  
Attackers spoofed domain renewal emails to steal credit cards and OTPs through fake 3-D Secure modals [[Malware Analysis](https://malwr-analysis.com/2025/12/31/fake-wordpress-domain-renewal-phishing-email-stealing-credit-card-and-3-d-secure-otp/)], exfiltrating data via PHP relays to Telegram bots. The campaign features artificial delays and forced OTP retries to increase credibility, exploiting weak DMARC policies (p=NONE) on compromised domains.

## 📋 Policy & Industry News

**[UPDATE] Healthcare Fines Intensify for Data Protection Failures**  
New York AG Letitia James secured $500K from OrthopedicsNY for failing to protect patient data [[DataBreaches](https://databreaches.net/2025/12/31/attorney-general-james-secures-500000-from-capital-region-health-care-provider-for-failing-to-protect-patients-information/)], continuing enforcement trends seen in prior healthcare sector penalties [[Dec 28 Summary](https://malware.news/t/rainbow-six-siege-breach-6-wired-subscriber-leak-6-edr-freeze-technique-6-mongobleed-exploitation-6/102917#post_1)]. The case underscores rising regulatory accountability for inadequate security controls.