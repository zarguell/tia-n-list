#!/usr/bin/env python3
"""
Simple threat intelligence digest generator.
Replaces complex enterprise blog generation with streamlined RSS→digest workflow.
"""

import json
import logging
import os
import random
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

from .simple_memory import SimpleMemory
from .storage_registry import get_default_storage_provider
from .llm_registry import get_registry


# Configuration constants
MAX_ARTICLES_FOR_PROMPT = int(os.getenv('SIMPLE_DIGEST_MAX_ARTICLES', '10'))
MAX_CONTENT_LENGTH = int(os.getenv('SIMPLE_DIGEST_MAX_CONTENT_LENGTH', '1500'))
MIN_CONTENT_LENGTH = int(os.getenv('SIMPLE_DIGEST_MIN_CONTENT_LENGTH', '200'))
MAX_REFERENCES = int(os.getenv('SIMPLE_DIGEST_MAX_REFERENCES', '15'))
MEMORY_DAYS_BACK = int(os.getenv('SIMPLE_DIGEST_MEMORY_DAYS_BACK', '7'))
MEMORY_CLEANUP_DAYS = int(os.getenv('SIMPLE_DIGEST_MEMORY_CLEANUP_DAYS', '30'))
MAX_TOKENS = int(os.getenv('SIMPLE_DIGEST_MAX_TOKENS', '3000'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleDigestGenerator:
    """Simplified digest generator for threat intelligence."""

    def __init__(self,
                 memory_file: Optional[Path] = None,
                 prompt_file: Optional[Path] = None):
        self.storage = get_default_storage_provider()
        self.llm_registry = get_registry()
        self.memory = SimpleMemory(memory_file or Path("data/simple_memory.json"))

        # Load simple prompt template
        self.prompt_file = prompt_file or Path("config/prompts/simple_digest.json")
        self.prompt_template = self._load_prompt_template()

        # Hugo content directory
        self.hugo_content_dir = Path("hugo/content/posts")
        self.hugo_content_dir.mkdir(parents=True, exist_ok=True)

    def _load_prompt_template(self) -> Dict:
        """Load the simple digest prompt template."""
        if not self.prompt_file.exists():
            raise FileNotFoundError(f"Prompt template not found: {self.prompt_file}")

        with open(self.prompt_file, 'r') as f:
            return json.load(f)

    def _normalize_article_datetime(self, article: Dict) -> Optional[datetime]:
        """Normalize article datetime with proper timezone handling."""
        published_str = article.get('published_at')
        if not published_str:
            return None

        try:
            if published_str.endswith('Z'):
                published_str = published_str.replace('Z', '+00:00')
            published = datetime.fromisoformat(published_str)

            if published.tzinfo is None:
                published = published.replace(tzinfo=datetime.timezone.utc)

            return published
        except (ValueError, AttributeError) as e:
            logging.debug(f"Failed to parse datetime for article {article.get('id', 'unknown')}: {e}")
            return None

    def _get_fresh_articles(self, target_date: date = None) -> List[Dict]:
        """Get articles from the last 24 hours."""
        if target_date is None:
            target_date = date.today()

        # Get articles from last 24 hours
        start_time = datetime.combine(target_date, datetime.min.time()).replace(tzinfo=datetime.now().astimezone().tzinfo)
        end_time = start_time + timedelta(days=1)

        articles = self.storage.get_articles_by_date_range(
            start_date=start_time.date(),
            end_date=end_time.date(),
            status='fetched'
        )

        # Filter to last 24 hours and ensure quality
        fresh_articles = []
        for article in articles:
            published = self._normalize_article_datetime(article)
            if published and start_time <= published < end_time:
                content = self._get_article_content(article)
                if len(content) >= MIN_CONTENT_LENGTH:
                    fresh_articles.append(article)

        return fresh_articles

    def _get_article_content(self, article: Dict) -> str:
        """Get article content with fallback to raw content."""
        return (article.get('content', {}).get('processed', '') or
                article.get('content', {}).get('raw', ''))

    def _filter_unused_articles(self, articles: List[Dict]) -> List[Dict]:
        """Filter out articles that were recently used in digests."""
        recently_used = self.memory.get_recently_used_articles(days_back=MEMORY_DAYS_BACK)

        unused_articles = []
        for article in articles:
            article_id = article.get('id') or article.get('guid')
            if article_id and article_id not in recently_used:
                unused_articles.append(article)

        return unused_articles

    def _format_articles_for_prompt(self, articles: List[Dict]) -> str:
        """Format articles for the LLM prompt."""
        if not articles:
            return "No fresh articles available for analysis."

        formatted = []
        for i, article in enumerate(articles[:MAX_ARTICLES_FOR_PROMPT], 1):
            title = article.get('title', 'Untitled')
            content = self._get_article_content(article)
            url = article.get('url', '')
            source = article.get('source_id', 'unknown')
            score = article.get('analysis', {}).get('score', 0)

            # Truncate content to avoid token limits
            if len(content) > MAX_CONTENT_LENGTH:
                content = content[:MAX_CONTENT_LENGTH] + "..."

            formatted.append(f"Article {i}:\n")
            formatted.append(f"Title: {title}\n")
            formatted.append(f"Source: {source} (Score: {score})\n")
            formatted.append(f"Content: {content}\n")
            formatted.append(f"URL: {url}\n")

        return "\n".join(formatted)

    def _build_prompt(self, articles_summary: str, target_date: date) -> str:
        """Build the complete prompt for LLM synthesis."""
        template = self.prompt_template.get('template', '')

        # Substitute variables
        prompt = template.replace('{{current_date}}', target_date.strftime('%B %d, %Y'))
        prompt = prompt.replace('{{articles_summary}}', articles_summary)

        return prompt

    def _extract_themes(self, articles: List[Dict]) -> List[str]:
        """Extract key themes from articles."""
        theme_patterns = {
            'Ransomware': ['ransomware', 'lockbit', 'conti', 'revil', 'cl0p', 'babuk', 'qilin', 'kraken', 'extortion'],
            'Vulnerability': ['vulnerability', 'cve-', 'patch', 'critical', 'flaw', 'bug'],
            'Malware': ['malware', 'trojan', 'botnet', 'spyware', 'backdoor', 'rootkit', 'rat', 'worm'],
            'Law Enforcement': ['police', 'fbi', 'europol', 'interpol', 'authorities', 'takedown', 'arrest', 'disrupt'],
            'Data Breach': ['breach', 'leak', 'data', 'exposed', 'stolen', 'compromised'],
            'Critical Infrastructure': ['healthcare', 'hospital', 'energy', 'utility', 'transportation', 'government'],
            'Tech Giants': ['microsoft', 'apple', 'google', 'amazon', 'meta', 'tesla', 'oracle', 'cisco'],
            'Financial': ['bank', 'finance', 'payment', 'fraud', 'crypto', 'bitcoin'],
            'Supply Chain': ['supply chain', 'software', 'vendor', 'third-party'],
            'Phishing': ['phishing', 'email', 'credential', 'login', 'password']
        }

        themes = []
        for article in articles[:10]:  # Look at top 10 articles for better coverage
            title = article.get('title', '').lower()
            content = self._get_article_content(article).lower() if len(self._get_article_content(article)) > 100 else ''
            combined_text = f"{title} {content}"

            for theme, keywords in theme_patterns.items():
                if any(keyword in combined_text for keyword in keywords):
                    themes.append(theme)
                    break

        # Count theme frequency and return most common
        from collections import Counter
        theme_counts = Counter(themes)
        return [theme for theme, count in theme_counts.most_common(3)]

    def _generate_tags(self, articles: List[Dict]) -> List[str]:
        """Generate tags from articles."""
        tags = ['threat-intelligence', 'daily-digest', 'cybersecurity']
        for article in articles[:10]:
            source = article.get('source_id', '').replace('-', ' ').title()
            if source and source.lower() not in tags and len(tags) < 8:
                tags.append(source.lower())
        return tags[:10]  # Limit to 10 tags

    def _generate_llm_title_with_retry(self, target_date: date, articles: List[Dict]) -> Optional[str]:
        """Generate LLM-powered title with retry logic for rate limiting."""
        max_retries = 3
        base_wait_time = 60  # Start with 60 seconds for rate limits

        # Create concise article summary for the prompt
        article_summaries = []
        for i, article in enumerate(articles[:8]):  # Use top 8 articles
            title = article.get('title', '')
            source = article.get('source_id', '').replace('-', ' ').title()
            article_summaries.append(f"{i+1}. {title} ({source})")

        # Extract key themes
        themes = self._extract_themes(articles)
        themes_str = ', '.join(themes) if themes else 'General cybersecurity intelligence'

        date_str = target_date.strftime('%B %d, %Y')

        prompt = f"""Generate a compelling, SEO-optimized title for today's cybersecurity threat intelligence briefing.

DATE: {date_str}

TOP ARTICLES:
{chr(10).join(article_summaries)}

KEY THEMES: {themes_str}

REQUIREMENTS:
- Maximum 70 characters
- Include relevant emojis (⚠️, 🔥, 🏢, 📊, 🎯, 🔍, 🚨, 🍎, 🔐)
- Must be engaging and clickable
- Include key themes from above
- Avoid generic titles
- Focus on most important development

Examples of good titles:
- "⚠️ Critical CVE-2025-24893 Exploited in Wild - November 13, 2025"
- "🔥 LockBit Ransomware Targets Healthcare Sector - November 13, 2025"
- "🍎 Apple Patches 161 Critical Vulnerabilities - November 13, 2025"

Generate only the title, nothing else:"""

        for attempt in range(max_retries):
            try:
                logger.info(f"LLM title generation attempt {attempt + 1}/{max_retries}")

                response = self.llm_registry.execute_with_fallback(
                    "generate_title",
                    prompt=prompt,
                    max_tokens=50,
                    temperature=0.8
                )

                if response and response.strip():
                    title = response.strip().strip('"\'').strip()

                    # Validate title quality
                    if len(title) <= 100 and any(c in title for c in '⚠️🔥🏢📊🎯🔍🚨🍎🔐'):
                        logger.info(f"Successfully generated LLM title: {title}")
                        return title
                    else:
                        logger.warning(f"Generated title failed validation: {title}")
                else:
                    logger.warning("LLM returned empty response")

            except Exception as e:
                error_str = str(e)
                if "429" in error_str and attempt < max_retries - 1:
                    # Exponential backoff with jitter for rate limits
                    wait_time = base_wait_time * (2 ** attempt) + random.randint(1, 30)
                    logger.warning(f"Rate limited (HTTP 429), waiting {wait_time}s before retry {attempt + 1}")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"LLM title generation failed on attempt {attempt + 1}: {e}")
                    if attempt == max_retries - 1:
                        break
                # Brief wait for other errors
                if attempt < max_retries - 1:
                    time.sleep(5 + random.randint(1, 10))

        logger.error("All LLM title generation attempts failed, falling back to template")
        return None

    def _generate_title(self, target_date: date, articles: List[Dict]) -> str:
        """Generate title with LLM first, template fallback."""
        if not articles:
            return f"Daily Threat Intelligence Digest - {target_date.strftime('%B %d, %Y')}"

        # Try LLM generation first
        logger.info("Attempting LLM title generation...")
        llm_title = self._generate_llm_title_with_retry(target_date, articles)

        if llm_title:
            return llm_title

        # Fall back to enhanced template logic
        logger.info("Falling back to template title generation")
        themes = self._extract_themes(articles)

        # Create specific titles based on themes and article count
        article_count = len(articles)
        date_str = target_date.strftime('%B %d, %Y')

        if themes:
            primary_theme = themes[0]

            # Theme-specific title templates
            if primary_theme == 'Ransomware':
                return f"🔥 {article_count} Ransomware Incidents Strike Global Targets - {date_str}"
            elif primary_theme == 'Vulnerability':
                return f"⚠️ Critical Vulnerabilities Patched in Major Software - {date_str}"
            elif primary_theme == 'Law Enforcement':
                return f"🚨 Global Cyber Crime Takedowns Disrupt Major Operations - {date_str}"
            elif primary_theme == 'Data Breach':
                return f"📊 Major Data Breaches Expose Sensitive Information - {date_str}"
            elif primary_theme == 'Critical Infrastructure':
                return f"🏥 Critical Infrastructure Faces Rising Cyber Threats - {date_str}"
            elif primary_theme == 'Tech Giants':
                return f"🏢 Tech Giants Address Security Issues Across Products - {date_str}"
            elif primary_theme == 'Malware':
                return f"🦠 New Malware Strains Detected in Active Campaigns - {date_str}"
            else:
                return f"{' & '.join(themes)} Dominate Cybersecurity Landscape - {date_str}"
        else:
            # Fallback to more specific generic titles
            if article_count >= 15:
                return f"📈 {article_count} Security Developments in Latest Threat Intelligence - {date_str}"
            elif article_count >= 10:
                return f"🔍 Multiple Cyber Threats Emerge in Security Landscape - {date_str}"
            else:
                return f"🛡️ Daily Threat Intelligence Digest - {date_str}"

    def _generate_hugo_metadata(self, target_date: date, articles: List[Dict]) -> Dict:
        """Generate Hugo frontmatter metadata."""
        return {
            'title': self._generate_title(target_date, articles),
            'date': target_date.isoformat(),
            'tags': self._generate_tags(articles),
            'categories': ['Threat Intelligence'],
            'summary': f'Daily threat intelligence digest covering {len(articles)} recent security developments.',
            'draft': False,
            'author': 'Tia N. List',
            'lastmod': datetime.now().isoformat(),
            'sources': [article.get('source_id') for article in articles[:10]]
        }

    def generate_daily_digest(self, target_date: date = None) -> Optional[str]:
        """Generate a simple daily threat intelligence digest."""
        if target_date is None:
            target_date = date.today()

        logger.info(f"Generating simple digest for {target_date}")

        try:
            # 1. Get fresh articles from last 24 hours
            fresh_articles = self._get_fresh_articles(target_date)
            logger.info(f"Found {len(fresh_articles)} fresh articles from last 24 hours")

            if not fresh_articles:
                logger.info("No fresh articles found for digest generation")
                return None

            # 2. Filter out recently used articles
            unused_articles = self._filter_unused_articles(fresh_articles)
            logger.info(f"Filtered to {len(unused_articles)} unused articles")

            if not unused_articles:
                logger.info("All recent articles have been used in recent digests")
                return None

            # 3. Sort by content length (since scores may not be available for fetched articles)
            unused_articles.sort(key=lambda x: len(x.get('content', {}).get('raw', '')), reverse=True)

            # 4. Generate articles summary for prompt
            articles_summary = self._format_articles_for_prompt(unused_articles)
            logger.info(f"Formatted {len(unused_articles)} articles for LLM analysis")

            # 5. Generate digest using LLM
            prompt = self._build_prompt(articles_summary, target_date)

            logger.info("Generating digest content with LLM...")
            response = self.llm_registry.execute_with_fallback(
                "generate_text",
                prompt=prompt,
                max_tokens=MAX_TOKENS
            )

            if not response or not response.strip():
                logger.error("LLM returned empty response")
                return None

            digest_content = response.strip()
            logger.info(f"Generated digest content: {len(digest_content)} characters")

            # 6. Mark articles as used
            used_article_ids = [
                article.get('id') or article.get('guid')
                for article in unused_articles
            ]
            self.memory.mark_articles_used(used_article_ids, target_date)
            logger.info(f"Marked {len(used_article_ids)} articles as used")

            # 7. Create Hugo post
            hugo_metadata = self._generate_hugo_metadata(target_date, unused_articles)
            hugo_filename = f"daily-threat-intelligence-{target_date.strftime('%Y-%m-%d')}.md"
            hugo_filepath = self.hugo_content_dir / hugo_filename

            # Write Hugo post
            hugo_content = self._format_hugo_post(hugo_metadata, digest_content, unused_articles)

            with open(hugo_filepath, 'w', encoding='utf-8') as f:
                f.write(hugo_content)

            logger.info(f"Created Hugo post: {hugo_filepath}")

            # 8. Cleanup old memory entries
            self.memory.cleanup_old_entries(days_to_keep=MEMORY_CLEANUP_DAYS)

            return hugo_filename

        except Exception as e:
            logger.error(f"Error generating simple digest: {e}")
            return None

    def _format_hugo_post(self, metadata: Dict, content: str, articles: List[Dict]) -> str:
        """Format content as a Hugo post with frontmatter.

        Args:
            metadata: Hugo frontmatter metadata dictionary
            content: Digest content body
            articles: List of articles for references

        Returns:
            Formatted Hugo post content with TOML frontmatter
        """
        try:
            # Convert metadata to TOML frontmatter
            frontmatter_lines = ["+++"]
            for key, value in metadata.items():
                if isinstance(value, list):
                    frontmatter_lines.append(f'{key} = {json.dumps(value, ensure_ascii=False)}')
                elif isinstance(value, bool):
                    frontmatter_lines.append(f'{key} = {str(value).lower()}')
                elif isinstance(value, (int, float)):
                    frontmatter_lines.append(f'{key} = {value}')
                else:
                    frontmatter_lines.append(f'{key} = {json.dumps(value, ensure_ascii=False)}')
            frontmatter_lines.append("+++")

            frontmatter = "\n".join(frontmatter_lines)

            # Add references section
            references = self._generate_references_section(articles)

            return f"{frontmatter}\n\n{content}\n\n{references}"
        except Exception as e:
            logger.error(f"Error formatting Hugo post: {e}")
            raise

    def _generate_references_section(self, articles: List[Dict]) -> str:
        """Generate references section for the digest.

        Args:
            articles: List of articles to reference

        Returns:
            Formatted references section in Markdown
        """
        if not articles:
            return ""

        references = ["## References"]

        for i, article in enumerate(articles[:MAX_REFERENCES], 1):
            title = article.get('title', 'Untitled')
            url = article.get('url', '')
            source = article.get('source_id', 'unknown')

            if url:
                references.append(f"{i}. {title}. {source}. [{url}]({url})")
            else:
                references.append(f"{i}. {title}. {source}.")

        return "\n".join(references)

    def get_memory_statistics(self) -> Dict:
        """Get memory system statistics.

        Returns:
            Dictionary containing memory usage statistics
        """
        return self.memory.get_statistics()