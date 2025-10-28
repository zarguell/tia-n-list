"""Threat classification module for Tia N. List project.

This module provides threat categorization and classification functions
to organize articles by threat type and provide better intelligence analysis.
"""

import re
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ThreatCategory(Enum):
    """Threat categories for classification."""
    MALWARE = "malware"
    PHISHING = "phishing"
    VULNERABILITY = "vulnerability"
    DATA_BREACH = "data_breach"
    RANSOMWARE = "ransomware"
    SUPPLY_CHAIN = "supply_chain"
    APT = "apt"  # Advanced Persistent Threats
    SOCIAL_ENGINEERING = "social_engineering"
    NETWORK_SECURITY = "network_security"
    MOBILE_SECURITY = "mobile_security"
    CLOUD_SECURITY = "cloud_security"
    IOT_SECURITY = "iot_security"
    OTHER = "other"


class ThreatClassifier:
    """Classifier for categorizing threat intelligence articles."""

    def __init__(self):
        """Initialize the threat classifier."""
        self.category_keywords = {
            ThreatCategory.MALWARE: [
                'malware', 'virus', 'trojan', 'botnet', 'worm', 'backdoor',
                'spyware', 'adware', 'rootkit', 'keylogger', 'infected',
                'malicious code', 'payload', 'dropper', 'loader'
            ],
            ThreatCategory.PHISHING: [
                'phishing', 'credential theft', 'password theft', 'login theft',
                'spear phishing', 'whaling', 'smishing', 'vishing', 'email scam',
                'fake login', 'credential harvesting', 'mfa bypass', 'multi-factor'
            ],
            ThreatCategory.VULNERABILITY: [
                'vulnerability', 'cve', 'patch', 'exploit', 'zero-day', '0day',
                'security flaw', 'security bug', 'buffer overflow', 'injection',
                'remote code execution', 'privilege escalation', 'security update'
            ],
            ThreatCategory.DATA_BREACH: [
                'data breach', 'data leak', 'information disclosure', 'personal data',
                'customer data', 'sensitive data', 'data theft', 'data exposure',
                'pii', 'personal information', 'breach', 'leaked', 'exposed'
            ],
            ThreatCategory.RANSOMWARE: [
                'ransomware', 'ransom', 'encryption', 'decrypt', 'payment',
                'bitcoin', 'cryptocurrency', 'extortion', 'locked files',
                'wanna', 'locky', 'ryuk', 'conti', 'revil'
            ],
            ThreatCategory.SUPPLY_CHAIN: [
                'supply chain', 'software supply chain', 'third party', 'vendor',
                'npm', 'pip', 'github', 'package', 'library', 'dependency',
                'open source', 'code repository', 'developer tools'
            ],
            ThreatCategory.APT: [
                'apt', 'advanced persistent threat', 'state-sponsored', 'nation',
                'cyber espionage', 'foreign', 'government', 'military',
                'cyber warfare', 'sophisticated', 'targeted attack'
            ],
            ThreatCategory.SOCIAL_ENGINEERING: [
                'social engineering', 'pretexting', 'baiting', 'quid pro quo',
                'diversion theft', 'impersonation', 'ceo fraud', 'business email',
                'confidence trick', 'human manipulation', 'psychology'
            ],
            ThreatCategory.NETWORK_SECURITY: [
                'firewall', 'network', 'router', 'switch', 'vpn', 'dns',
                'ddos', 'denial of service', 'network intrusion', 'traffic',
                'packet', 'network protocol', 'tcp', 'udp', 'port scanning'
            ],
            ThreatCategory.MOBILE_SECURITY: [
                'mobile', 'android', 'ios', 'smartphone', 'tablet', 'app',
                'mobile malware', 'mobile security', 'jailbreak', 'root',
                'mobile device', 'cellular', 'wifi'
            ],
            ThreatCategory.CLOUD_SECURITY: [
                'cloud', 'aws', 'azure', 'gcp', 'saas', 'paas', 'iaas',
                'cloud security', 'container', 'kubernetes', 'docker',
                'microservices', 'serverless', 'cloud storage'
            ],
            ThreatCategory.IOT_SECURITY: [
                'iot', 'internet of things', 'smart device', 'embedded',
                'firmware', 'sensor', 'industrial control', 'scada',
                'operational technology', 'smart home', 'connected device'
            ]
        }

    def classify_article(self, title: str, content: str) -> Tuple[ThreatCategory, float]:
        """Classify an article into threat categories.

        Args:
            title: Article title.
            content: Article content.

        Returns:
            Tuple of (ThreatCategory, confidence_score).
        """
        # Combine title and content for analysis
        text = f"{title} {content}".lower()

        category_scores = {}

        # Score each category based on keyword matches
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                # Count occurrences of keywords
                count = len(re.findall(rf'\b{re.escape(keyword)}\b', text))
                score += count

                # Title matches are worth more
                if keyword in title.lower():
                    score += 2

            category_scores[category] = score

        # Find the category with highest score
        if not any(category_scores.values()):
            return ThreatCategory.OTHER, 0.0

        best_category = max(category_scores, key=category_scores.get)
        max_score = category_scores[best_category]

        # Calculate confidence based on score distribution
        total_matches = sum(category_scores.values())
        confidence = max_score / total_matches if total_matches > 0 else 0.0

        return best_category, confidence

    def get_category_emoji(self, category: ThreatCategory) -> str:
        """Get emoji for threat category.

        Args:
            category: Threat category.

        Returns:
            Emoji representing the category.
        """
        emoji_map = {
            ThreatCategory.MALWARE: "🦠",
            ThreatCategory.PHISHING: "🎣",
            ThreatCategory.VULNERABILITY: "🔓",
            ThreatCategory.DATA_BREACH: "💾",
            ThreatCategory.RANSOMWARE: "🔒",
            ThreatCategory.SUPPLY_CHAIN: "📦",
            ThreatCategory.APT: "🎯",
            ThreatCategory.SOCIAL_ENGINEERING: "👥",
            ThreatCategory.NETWORK_SECURITY: "🌐",
            ThreatCategory.MOBILE_SECURITY: "📱",
            ThreatCategory.CLOUD_SECURITY: "☁️",
            ThreatCategory.IOT_SECURITY: "🏠",
            ThreatCategory.OTHER: "⚠️"
        }
        return emoji_map.get(category, "⚠️")

    def get_category_description(self, category: ThreatCategory) -> str:
        """Get description for threat category.

        Args:
            category: Threat category.

        Returns:
            Human-readable description.
        """
        descriptions = {
            ThreatCategory.MALWARE: "Malicious software threats including viruses, trojans, and botnets",
            ThreatCategory.PHISHING: "Credential theft and social engineering attacks via email or messaging",
            ThreatCategory.VULNERABILITY: "Security flaws and exploits requiring patches or mitigation",
            ThreatCategory.DATA_BREACH: "Unauthorized access and exposure of sensitive information",
            ThreatCategory.RANSOMWARE: "Extortion attacks using file encryption and payment demands",
            ThreatCategory.SUPPLY_CHAIN: "Compromises affecting software dependencies and third-party services",
            ThreatCategory.APT: "Advanced persistent threats and state-sponsored cyber operations",
            ThreatCategory.SOCIAL_ENGINEERING: "Manipulation tactics targeting human psychology and behavior",
            ThreatCategory.NETWORK_SECURITY: "Threats affecting network infrastructure and communications",
            ThreatCategory.MOBILE_SECURITY: "Security issues impacting mobile devices and applications",
            ThreatCategory.CLOUD_SECURITY: "Threats to cloud infrastructure and services",
            ThreatCategory.IOT_SECURITY: "Security vulnerabilities in connected devices and embedded systems",
            ThreatCategory.OTHER: "Miscellaneous security threats and incidents"
        }
        return descriptions.get(category, "Uncategorized threat")


# Global classifier instance
_classifier = None


def get_threat_classifier() -> ThreatClassifier:
    """Get the global threat classifier instance.

    Returns:
        ThreatClassifier instance.
    """
    global _classifier
    if _classifier is None:
        _classifier = ThreatClassifier()
    return _classifier


def classify_article(title: str, content: str) -> Tuple[ThreatCategory, float]:
    """Classify an article into threat categories.

    Args:
        title: Article title.
        content: Article content.

    Returns:
        Tuple of (ThreatCategory, confidence_score).
    """
    classifier = get_threat_classifier()
    return classifier.classify_article(title, content)