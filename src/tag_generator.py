#!/usr/bin/env python3
"""
Dynamic Tag Generation Module

Generates intelligent tags for cybersecurity threat intelligence articles.
Extracts entities, themes, and classification tags from processed articles.
"""

import re
import json
from datetime import datetime, date
from typing import List, Dict, Any, Set, Tuple
from collections import Counter, defaultdict
from pathlib import Path
import tldextract

from .storage_provider import StorageProvider
from .storage_registry import get_default_storage_provider
from .llm_registry import get_registry


class TagGenerator:
    """Generates intelligent tags for cybersecurity articles."""

    def __init__(self, storage: StorageProvider = None, llm_registry=None):
        """Initialize tag generator.

        Args:
            storage: Storage provider instance for accessing article data
            llm_registry: LLM registry for enhanced tag generation
        """
        self.storage = storage or get_default_storage_provider()
        self.llm_registry = llm_registry

        # Load tag taxonomy and normalization maps
        self.tag_taxonomy = self._load_tag_taxonomy()
        self.vendor_normalization = self._load_vendor_normalization()
        self.industry_normalization = self._load_industry_normalization()

    def _load_tag_taxonomy(self) -> Dict[str, Dict[str, Any]]:
        """Load tag taxonomy with categories and scoring weights."""
        return {
            "technical": {
                "weight": 0.3,
                "patterns": [
                    (r"CVE-\d{4}-\d{4,7}", lambda m: m.group(0).lower()),  # CVE numbers
                    (r"\b(CVSS)\b", lambda m: "cvss"),
                    (r"\b(Zero-day|0day|Zero day)\b", lambda m: "zero-day"),
                    (r"\b(RCE|Remote Code Execution)\b", lambda m: "remote-code-execution"),
                    (r"\b(LPE|Local Privilege Escalation)\b", lambda m: "privilege-escalation"),
                    (r"\b(XSS|Cross-site Scripting)\b", lambda m: "xss"),
                    (r"\b(SQLi|SQL Injection)\b", lambda m: "sql-injection"),
                    (r"\b(DoS|Denial of Service|DDoS)\b", lambda m: "ddos"),
                    (r"\b(Phishing|Spear phishing)\b", lambda m: "phishing"),
                    (r"\b(Malware|Ransomware|Spyware|Trojan|Worm|Botnet)\b", lambda m: m.group(0).lower()),
                    (r"\b(APT|Advanced Persistent Threat)\b", lambda m: "apt"),
                ]
            },
            "malware_families": {
                "weight": 0.25,
                "patterns": [
                    (r"\b(LockBit|Conti|REvil|DarkSide|BlackMatter|Hive)\b", lambda m: m.group(0).lower()),
                    (r"\b(Emotet|Trickbot|Qakbot|IcedID)\b", lambda m: m.group(0).lower()),
                    (r"\b(WannaCry|NotPetya|Petya|BadRabbit)\b", lambda m: m.group(0).lower()),
                    (r"\b(Stuxnet|Duqu|Flame|Gauss)\b", lambda m: m.group(0).lower()),
                    (r"\b(Mirai|Mozi|Hajime)\b", lambda m: m.group(0).lower()),
                ]
            },
            "threat_actors": {
                "weight": 0.25,
                "patterns": [
                    (r"\b(APT\d+|TA\d+)\b", lambda m: m.group(0).lower()),
                    (r"\b(Fancy Bear|Cozy Bear|Lazarus Group)\b", lambda m: m.group(0).lower().replace(" ", "-")),
                    (r"\b(Equation Group|Shadow Brokers)\b", lambda m: m.group(0).lower().replace(" ", "-")),
                ]
            },
            "vendors": {
                "weight": 0.2,
                "patterns": [
                    (r"\b(Microsoft|Windows|Office|365|Azure)\b", lambda m: "microsoft"),
                    (r"\b(Google|Android|Chrome|GCP)\b", lambda m: "google"),
                    (r"\b(Apple|iOS|macOS|iPhone|iPad)\b", lambda m: "apple"),
                    (r"\b(Amazon|AWS|EC2|S3)\b", lambda m: "amazon"),
                    (r"\b(Cisco|Juniper|Palo Alto)\b", lambda m: m.group(0).lower()),
                    (r"\b(Oracle|Java|MySQL)\b", lambda m: "oracle"),
                    (r"\b(Adobe|Flash|Reader|PDF)\b", lambda m: "adobe"),
                    (r"\b(Linux|Ubuntu|Red Hat|Debian)\b", lambda m: "linux"),
                    (r"\b(Apache|Nginx|IIS)\b", lambda m: m.group(0).lower()),
                    (r"\b(VMware|Citrix|SolarWinds)\b", lambda m: m.group(0).lower()),
                ]
            },
            "industries": {
                "weight": 0.15,
                "patterns": [
                    (r"\b(Healthcare|Hospital|Medical|Pharma)\b", lambda m: "healthcare"),
                    (r"\b(Finance|Banking|Financial|Investment|Insurance)\b", lambda m: "finance"),
                    (r"\b(Government|Federal|State|Military|Defense)\b", lambda m: "government"),
                    (r"\b(Technology|Tech|Software|SaaS)\b", lambda m: "technology"),
                    (r"\b(Education|University|School|College)\b", lambda m: "education"),
                    (r"\b(Retail|E-commerce|Shopping)\b", lambda m: "retail"),
                    (r"\b(Energy|Oil|Gas|Utility|Power)\b", lambda m: "energy"),
                    (r"\b(Manufacturing|Factory|Industrial)\b", lambda m: "manufacturing"),
                    (r"\b(Transportation|Airline|Shipping|Logistics)\b", lambda m: "transportation"),
                ]
            },
            "severity": {
                "weight": 0.1,
                "patterns": [
                    (r"\b(Critical|High severity|High risk)\b", lambda m: "critical"),
                    (r"\b(Important|Moderate|Medium)\b", lambda m: "high"),
                    (r"\b(Low|Minor)\b", lambda m: "medium"),
                    (r"\b(Actively exploited|In the wild|Widespread)\b", lambda m: "actively-exploited"),
                ]
            }
        }

    def _load_vendor_normalization(self) -> Dict[str, str]:
        """Load vendor name normalization mapping."""
        return {
            "microsoft": "microsoft",
            "ms": "microsoft",
            "windows": "microsoft",
            "office": "microsoft",
            "azure": "microsoft",
            "google": "google",
            "alphabet": "google",
            "android": "google",
            "chrome": "google",
            "apple": "apple",
            "ios": "apple",
            "macos": "apple",
            "iphone": "apple",
            "amazon": "amazon",
            "aws": "amazon",
            "cisco": "cisco",
            "oracle": "oracle",
            "java": "oracle",
            "adobe": "adobe",
            "linux": "linux",
            "apache": "apache",
            "nginx": "nginx",
            "vmware": "vmware",
            "citrix": "citrix",
            "solarwinds": "solarwinds",
        }

    def _load_industry_normalization(self) -> Dict[str, str]:
        """Load industry name normalization mapping."""
        return {
            "healthcare": "healthcare",
            "medical": "healthcare",
            "hospital": "healthcare",
            "pharma": "healthcare",
            "finance": "finance",
            "banking": "finance",
            "financial": "finance",
            "investment": "finance",
            "insurance": "finance",
            "government": "government",
            "federal": "government",
            "military": "government",
            "defense": "government",
            "technology": "technology",
            "tech": "technology",
            "software": "technology",
            "saas": "technology",
            "education": "education",
            "university": "education",
            "school": "education",
            "retail": "retail",
            "ecommerce": "retail",
            "energy": "energy",
            "utility": "energy",
            "manufacturing": "manufacturing",
            "industrial": "manufacturing",
            "transportation": "transportation",
            "airline": "transportation",
        }

    def extract_tags_from_articles(self, articles: List[Dict[str, Any]], limit: int = 15) -> List[Dict[str, Any]]:
        """Extract tags from a list of articles.

        Args:
            articles: List of articles to analyze
            limit: Maximum number of tags to return

        Returns:
            List of tags with confidence scores and categories
        """
        if not articles:
            return []

        print(f"🏷️  Extracting tags from {len(articles)} articles...")

        # Collect all text content
        all_text = []
        for article in articles:
            title = article.get('title', '')
            content = article.get('content', {}).get('full', '') or article.get('content', {}).get('raw', '')
            processed_content = article.get('processed_content', '')

            article_text = f"{title} {content} {processed_content}"
            all_text.append(article_text.lower())

        combined_text = " ".join(all_text)

        # Extract tags using pattern matching
        pattern_tags = self._extract_pattern_tags(combined_text)

        # Extract tags from IOCs if available
        ioc_tags = self._extract_ioc_tags(articles)

        # Combine and score tags
        all_tags = {}

        # Add pattern-based tags
        for tag_data in pattern_tags:
            tag = tag_data['tag']
            if tag not in all_tags:
                all_tags[tag] = {
                    'tag': tag,
                    'category': tag_data['category'],
                    'confidence': 0,
                    'count': 0,
                    'sources': []
                }
            all_tags[tag]['confidence'] += tag_data['confidence']
            all_tags[tag]['count'] += tag_data['count']
            all_tags[tag]['sources'].extend(tag_data['sources'])

        # Add IOC-based tags
        for tag_data in ioc_tags:
            tag = tag_data['tag']
            if tag not in all_tags:
                all_tags[tag] = {
                    'tag': tag,
                    'category': tag_data['category'],
                    'confidence': 0,
                    'count': 0,
                    'sources': []
                }
            all_tags[tag]['confidence'] += tag_data['confidence']
            all_tags[tag]['count'] += tag_data['count']
            all_tags[tag]['sources'].extend(tag_data['sources'])

        # Apply category weights and normalize scores
        for tag, data in all_tags.items():
            category_weight = self.tag_taxonomy.get(data['category'], {}).get('weight', 0.1)
            # Normalize confidence based on category weight and frequency
            data['confidence'] = min(1.0, data['confidence'] * category_weight * (1 + data['count'] * 0.1))
            data['sources'] = list(set(data['sources']))  # Remove duplicates

        # Sort by confidence and limit results
        sorted_tags = sorted(all_tags.values(), key=lambda x: x['confidence'], reverse=True)
        final_tags = sorted_tags[:limit]

        print(f"✅ Extracted {len(final_tags)} tags")
        return final_tags

    def _extract_pattern_tags(self, text: str) -> List[Dict[str, Any]]:
        """Extract tags using regex patterns."""
        tags = []

        for category, config in self.tag_taxonomy.items():
            for pattern, processor in config['patterns']:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    tag = processor(match)
                    if tag:
                        # Calculate confidence based on pattern specificity and context
                        confidence = 0.7  # Base confidence for pattern matches

                        # Boost confidence for technical indicators
                        if category == 'technical' and tag.startswith('cve-'):
                            confidence = 0.9
                        elif category == 'malware_families':
                            confidence = 0.8
                        elif category == 'threat_actors':
                            confidence = 0.85

                        tags.append({
                            'tag': tag,
                            'category': category,
                            'confidence': confidence,
                            'count': 1,
                            'sources': ['pattern-matching']
                        })

        return tags

    def _extract_ioc_tags(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract tags from IOCs in articles."""
        tags = []

        for article in articles:
            iocs = article.get('iocs', [])
            source = article.get('title', 'Unknown Article')

            for ioc in iocs:
                ioc_value = ioc.get('value', '').lower()
                ioc_type = ioc.get('type', '').lower()

                # Extract domain tags
                if ioc_type == 'domain':
                    # Use tldextract to get the registered_domain for comparison
                    ext = tldextract.extract(ioc_value)
                    registered_domain = f"{ext.domain}.{ext.suffix}".lower() if ext.suffix else ext.domain.lower()

                    if registered_domain == "microsoft.com":
                        tags.append({
                            'tag': 'microsoft',
                            'category': 'vendors',
                            'confidence': 0.6,
                            'count': 1,
                            'sources': [source]
                        })
                    elif registered_domain == "google.com":
                        tags.append({
                            'tag': 'google',
                            'category': 'vendors',
                            'confidence': 0.6,
                            'count': 1,
                            'sources': [source]
                        })
                    elif registered_domain in ("amazon.com", "amazonaws.com"):
                        tags.append({
                            'tag': 'amazon',
                            'category': 'vendors',
                            'confidence': 0.6,
                            'count': 1,
                            'sources': [source]
                        })
                    elif registered_domain == "cisco.com":
                        tags.append({
                            'tag': 'cisco',
                            'category': 'vendors',
                            'confidence': 0.6,
                            'count': 1,
                            'sources': [source]
                        })

                # Extract IP-based tags for cloud providers
                elif ioc_type == 'ip':
                    # Could add IP range detection for cloud providers here
                    pass

        return tags

    def generate_tags_for_date(self, target_date: date, limit: int = 15) -> List[Dict[str, Any]]:
        """Generate tags for all articles on a specific date.

        Args:
            target_date: Date to generate tags for
            limit: Maximum number of tags to return

        Returns:
            List of tags with metadata
        """
        # Get processed articles for the date
        articles = self.storage.get_articles_by_date_range(
            start_date=target_date,
            end_date=target_date,
            status='processed'
        )

        if not articles:
            print(f"⚠️  No processed articles found for {target_date}")
            return self._get_default_tags()

        # Sort by score and use top articles for tag generation
        articles.sort(key=lambda x: x.get('score', 0), reverse=True)
        articles = articles[:20]  # Use top 20 articles for tag generation

        return self.extract_tags_from_articles(articles, limit)

    def _get_default_tags(self) -> List[Dict[str, Any]]:
        """Get default tags when no articles are available."""
        return [
            {
                'tag': 'cybersecurity',
                'category': 'technical',
                'confidence': 0.5,
                'count': 0,
                'sources': ['default']
            },
            {
                'tag': 'threat-intelligence',
                'category': 'technical',
                'confidence': 0.5,
                'count': 0,
                'sources': ['default']
            }
        ]

    def format_tags_for_hugo(self, tags: List[Dict[str, Any]]) -> List[str]:
        """Format tags for Hugo front matter.

        Args:
            tags: List of tag dictionaries

        Returns:
            List of tag strings for Hugo
        """
        return [tag['tag'].replace('_', '-') for tag in tags]

    def get_tag_statistics(self) -> Dict[str, Any]:
        """Get statistics about tag generation.

        Returns:
            Dictionary containing tag generation statistics
        """
        return {
            'taxonomy_categories': list(self.tag_taxonomy.keys()),
            'total_patterns': sum(len(config['patterns']) for config in self.tag_taxonomy.values()),
            'vendor_mappings': len(self.vendor_normalization),
            'industry_mappings': len(self.industry_normalization),
            'supported_categories': {
                category: {
                    'weight': config['weight'],
                    'pattern_count': len(config['patterns'])
                }
                for category, config in self.tag_taxonomy.items()
            }
        }


def main():
    """Main function for testing tag generation."""
    from datetime import date

    print("🏷️  DYNAMIC TAG GENERATION TEST")
    print("=" * 50)

    # Initialize tag generator
    tag_generator = TagGenerator()

    # Print tag generator statistics
    stats = tag_generator.get_tag_statistics()
    print(f"📊 Tag Generator Statistics:")
    print(f"   Taxonomy categories: {stats['taxonomy_categories']}")
    print(f"   Total patterns: {stats['total_patterns']}")
    print(f"   Vendor mappings: {stats['vendor_mappings']}")
    print(f"   Industry mappings: {stats['industry_mappings']}")
    print()

    # Test tag generation for today's articles
    print(f"🎯 Testing tag generation for {date.today()}...")
    tags = tag_generator.generate_tags_for_date(date.today())

    if tags:
        print(f"✅ Generated {len(tags)} tags:")
        for i, tag in enumerate(tags, 1):
            print(f"   {i:2d}. {tag['tag']} ({tag['category']}) - Confidence: {tag['confidence']:.2f}")

        print(f"\n🏷️  Hugo-formatted tags:")
        hugo_tags = tag_generator.format_tags_for_hugo(tags)
        print(f"   {', '.join(hugo_tags)}")
    else:
        print("❌ No tags generated")

    print("\n🎉 Tag generation test completed!")


if __name__ == "__main__":
    main()