"""Dynamic title generator for Tia N. List threat intelligence briefings.

This module generates engaging, SEO-optimized titles based on daily threat intelligence content
using multiple strategies and LLM-powered synthesis with template fallbacks.
"""

import re
import json
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date
from pathlib import Path

from .storage_provider import StorageProvider
from .storage_registry import get_default_storage_provider
from .llm_registry import get_registry


class TitleGenerator:
    """Generates dynamic, engaging titles for threat intelligence briefings."""

    def __init__(self, storage: StorageProvider = None, llm_registry=None):
        """Initialize title generator.

        Args:
            storage: Storage provider instance for accessing article data
            llm_registry: LLM registry for title generation
        """
        self.storage = storage or get_default_storage_provider()
        self.llm_registry = llm_registry or get_registry()
        self.title_cache_file = Path("data/title_cache.json")
        self.title_cache_file.parent.mkdir(exist_ok=True)
        self.title_cache = self._load_title_cache()

    def _load_title_cache(self) -> Dict[str, Any]:
        """Load title cache to prevent duplicates.

        Returns:
            Dictionary containing recent titles and themes
        """
        try:
            if self.title_cache_file.exists():
                with open(self.title_cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load title cache: {e}")

        return {
            "recent_titles": [],
            "recent_themes": [],
            "used_patterns": []
        }

    def _save_title_cache(self) -> None:
        """Save title cache to prevent duplicates."""
        try:
            with open(self.title_cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.title_cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Could not save title cache: {e}")

    def _analyze_articles_for_themes(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze articles to identify key themes and patterns.

        Args:
            articles: List of articles to analyze

        Returns:
            Dictionary containing themes, entities, and patterns
        """
        themes = {
            "critical_vulnerabilities": [],
            "threat_actors": [],
            "major_vendors": [],
            "industries": [],
            "malware_families": [],
            "attack_types": [],
            "severity_indicators": []
        }

        all_titles = " ".join([article.get('title', '') for article in articles])
        all_content = " ".join([
            article.get('content', {}).get('processed', '')
            for article in articles
        ]).lower()

        # Extract CVEs
        cve_pattern = r'(cve-\d{4}-\d{4,})'
        cves = re.findall(cve_pattern, all_content, re.IGNORECASE)
        themes["critical_vulnerabilities"] = list(set(cves))

        # Extract common threat actors
        threat_actors = [
            'apt', 'conti', 'lockbit', 'revil', 'cl0p', 'babuk', 'qilin', 'trickbot',
            'blackcat', 'alphv', 'hive', 'kinsing', 'doppelganging', 'wannacry'
        ]
        for actor in threat_actors:
            if actor in all_content:
                themes["threat_actors"].append(actor)

        # Extract major vendors
        vendor_keywords = [
            'microsoft', 'cisco', 'dell', 'vmware', 'oracle', 'adobe', 'apple',
            'google', 'amazon', 'meta', 'tesla', 'solarwinds', 'fortinet'
        ]
        for vendor in vendor_keywords:
            if vendor in all_content:
                themes["major_vendors"].append(vendor)

        # Extract industries
        industry_keywords = [
            'healthcare', 'finance', 'banking', 'government', 'education',
            'energy', 'retail', 'manufacturing', 'telecom', 'transportation'
        ]
        for industry in industry_keywords:
            if industry in all_content:
                themes["industries"].append(industry)

        # Extract malware families
        malware_keywords = [
            'ransomware', 'trojan', 'botnet', 'spyware', 'backdoor', 'rootkit',
            'worm', 'loader', 'infostealer', 'banker', 'clipper'
        ]
        for malware in malware_keywords:
            if malware in all_content:
                themes["malware_families"].append(malware)

        # Identify severity indicators
        severity_keywords = [
            'critical', 'severe', 'urgent', 'actively exploited', 'zero-day',
            'widespread', 'massive', 'emergency', 'high risk'
        ]
        for severity in severity_keywords:
            if severity in all_content:
                themes["severity_indicators"].append(severity)

        return themes

    def _check_title_uniqueness(self, title: str) -> bool:
        """Check if title is unique compared to recent titles.

        Args:
            title: Title to check

        Returns:
            True if title is unique, False if too similar to recent titles
        """
        title_lower = title.lower()

        # Check against recent titles
        for recent_title in self.title_cache.get("recent_titles", [])[-7:]:  # Last 7 days
            if self._calculate_similarity(title_lower, recent_title.lower()) > 0.8:
                return False

        return True

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text strings.

        Args:
            text1: First text string
            text2: Second text string

        Returns:
            Similarity score between 0 and 1
        """
        words1 = set(text1.split())
        words2 = set(text2.split())

        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0

        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        return intersection / union if union > 0 else 0.0

    def _generate_template_title(self, themes: Dict[str, Any], date_obj: date) -> str:
        """Generate template-based title when LLM is unavailable.

        Args:
            themes: Analyzed themes from articles
            date_obj: Date for the title

        Returns:
            Generated template-based title
        """
        date_str = date_obj.strftime('%B %d, %Y')

        # Priority-based title generation
        if themes["critical_vulnerabilities"]:
            cve = themes["critical_vulnerabilities"][0].upper()
            return f"⚠️ Critical {cve} Vulnerability Dominates Threat Landscape - {date_str}"

        if themes["threat_actors"]:
            actor = themes["threat_actors"][0].title()
            return f"🔥 {actor} Attacks Surge in Latest Cybersecurity Reports - {date_str}"

        if themes["major_vendors"]:
            vendor = themes["major_vendors"][0].title()
            return f"🏢 {vendor} Security Issues Widespread in Latest Intelligence - {date_str}"

        if themes["severity_indicators"]:
            severity = themes["severity_indicators"][0].title()
            return f"🚨 {severity.title()} Cybersecurity Threats Identified - {date_str}"

        if themes["industries"]:
            industry = themes["industries"][0].title()
            return f"📊 {industry} Sector Targeted in Latest Security Incidents - {date_str}"

        # Fallback to generic titles
        generic_titles = [
            f"🛡️ Daily Threat Intelligence Briefing - {date_str}",
            f"🔍 Security Alert: Latest Cyber Threat Analysis - {date_str}",
            f"📈 Cybersecurity Landscape Update - {date_str}",
            f"🎯 Today's Top Security Intelligence - {date_str}"
        ]

        return generic_titles[0]

    def _generate_llm_title(self, articles: List[Dict[str, Any]], themes: Dict[str, Any], date_obj: date) -> str:
        """Generate LLM-powered title.

        Args:
            articles: List of articles for context
            themes: Analyzed themes from articles
            date_obj: Date for the title

        Returns:
            LLM-generated title or None if LLM is unavailable
        """
        # Check if LLM registry is available
        if not self.llm_registry:
            return None
        # Create concise context for title generation
        article_summaries = []
        for i, article in enumerate(articles[:5]):  # Use top 5 articles
            title = article.get('title', '')
            source = article.get('source_name', 'Unknown')
            score = article.get('score', 0) or article.get('analysis', {}).get('score', 0)
            article_summaries.append(f"{i+1}. {title} ({source}, Score: {score})")

        # Create themes summary
        themes_summary = []
        if themes["critical_vulnerabilities"]:
            themes_summary.append(f"Critical CVEs: {', '.join(themes['critical_vulnerabilities'][:2])}")
        if themes["threat_actors"]:
            themes_summary.append(f"Threat Actors: {', '.join(themes['threat_actors'][:2])}")
        if themes["major_vendors"]:
            themes_summary.append(f"Major Vendors: {', '.join(themes['major_vendors'][:2])}")
        if themes["severity_indicators"]:
            themes_summary.append(f"Severity: {', '.join(themes['severity_indicators'][:2])}")

        date_str = date_obj.strftime('%B %d, %Y')

        prompt = f"""Generate a compelling, SEO-optimized title for today's cybersecurity threat intelligence briefing.

DATE: {date_str}

TOP ARTICLES:
{chr(10).join(article_summaries)}

KEY THEMES:
{chr(10).join(themes_summary) if themes_summary else "General cybersecurity intelligence"}

REQUIREMENTS:
- Maximum 60 characters
- Include relevant emojis (⚠️, 🔥, 🏢, 📊, 🎯, 🔍, 🚨)
- Must be engaging and clickable
- Include key themes from above
- Avoid generic titles
- Focus on most important development

Examples of good titles:
- "⚠️ Critical CVE-2025-24893 Exploited in Wild - October 29, 2025"
- "🔥 LockBit Ransomware Targets Healthcare Sector - October 29, 2025"
- "🏢 Microsoft Zero-Day Patch Emergency - October 29, 2025"

Generate only the title, nothing else:"""

        try:
            # Use lightweight model for title generation via LLM registry
            response = self.llm_registry.execute_with_fallback(
                "generate_text",
                prompt=prompt,
                max_tokens=50,
                temperature=0.8
            )

            if response and response.strip():
                title = response.strip()
                # Remove any surrounding quotes
                title = title.strip('"\'').strip()

                # Validate title length and quality
                if len(title) <= 80 and any(c in title for c in '⚠️🔥🏢📊🎯🔍🚨'):
                    return title

        except Exception as e:
            print(f"⚠️  LLM title generation failed: {e}")

        return None

    def generate_title(self, articles: List[Dict[str, Any]], date_obj: date = None) -> str:
        """Generate dynamic title for threat intelligence briefing.

        Args:
            articles: List of articles to base title on
            date_obj: Date for the title (defaults to today)

        Returns:
            Generated title
        """
        if date_obj is None:
            date_obj = date.today()

        if not articles:
            return f"🛡️ Daily Threat Intelligence Briefing - {date_obj.strftime('%B %d, %Y')}"

        print(f"🎯 Generating dynamic title for {len(articles)} articles...")

        # Analyze articles for themes
        themes = self._analyze_articles_for_themes(articles)

        # Try LLM generation first if available
        if self.llm_registry:
            print("🤖 Attempting LLM-powered title generation...")
            llm_title = self._generate_llm_title(articles, themes, date_obj)
        else:
            print("⚠️  LLM registry not available, using template fallback...")
            llm_title = None

        if llm_title and self._check_title_uniqueness(llm_title):
            # Update cache and return
            self.title_cache["recent_titles"].append(llm_title)
            if len(self.title_cache["recent_titles"]) > 30:
                self.title_cache["recent_titles"] = self.title_cache["recent_titles"][-30:]
            self._save_title_cache()
            print(f"✅ Generated LLM-powered title: {llm_title}")
            return llm_title

        # Fallback to template-based title
        template_title = self._generate_template_title(themes, date_obj)
        print(f"✅ Generated template-based title: {template_title}")
        return template_title

    def get_title_statistics(self) -> Dict[str, Any]:
        """Get statistics about title generation.

        Returns:
            Dictionary containing title generation statistics
        """
        return {
            "recent_titles_count": len(self.title_cache.get("recent_titles", [])),
            "cache_status": "active" if self.title_cache_file.exists() else "inactive",
            "recent_themes": self.title_cache.get("recent_themes", []),
            "used_patterns": self.title_cache.get("used_patterns", [])
        }


# Convenience function for standalone usage
def generate_daily_title(articles: List[Dict[str, Any]] = None, target_date: date = None) -> str:
    """Generate a daily title for threat intelligence briefing.

    Args:
        articles: List of articles (if None, will fetch from storage)
        target_date: Target date (if None, uses today)

    Returns:
        Generated title
    """
    generator = TitleGenerator()

    if articles is None:
        # Fetch articles from storage
        from .storage_registry import get_default_storage_provider
        storage = get_default_storage_provider()
        if target_date is None:
            target_date = date.today()

        articles = storage.get_articles_by_date_range(
            start_date=target_date,
            end_date=target_date,
            status="processed"
        )

        # Sort by score
        articles.sort(key=lambda x: x.get("analysis", {}).get("score", 0), reverse=True)

    return generator.generate_title(articles, target_date)


if __name__ == "__main__":
    # Test title generation
    print("🎯 Testing Dynamic Title Generation")
    print("=" * 50)

    title = generate_daily_title()
    print(f"Generated Title: {title}")

    # Show statistics
    generator = TitleGenerator()
    stats = generator.get_title_statistics()
    print(f"\n📊 Statistics: {stats}")