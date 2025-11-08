#!/usr/bin/env python3
"""
Simple threat intelligence digest generator.
Replaces complex enterprise blog generation with streamlined RSS→digest workflow.
"""

import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

from .simple_memory import SimpleMemory
from .storage_registry import get_default_storage_provider
from .llm_registry import get_registry


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
            if article.get('published_at'):
                try:
                    # Handle different datetime formats
                    published_str = article['published_at']
                    if published_str.endswith('Z'):
                        published_str = published_str.replace('Z', '+00:00')
                    published = datetime.fromisoformat(published_str)

                    # Ensure both datetimes have timezone info for comparison
                    if published.tzinfo is None:
                        published = published.replace(tzinfo=datetime.timezone.utc)

                    if start_time <= published < end_time:
                        # Require minimum content length (no score requirement for fetched articles)
                        content = article.get('content', {}).get('processed', '') or article.get('content', {}).get('raw', '')
                        if len(content) > 200:
                            fresh_articles.append(article)
                except (ValueError, AttributeError) as e:
                    print(f"Warning: Skipping article with invalid date format. ID: {article.get('id', 'N/A')}, Error: {e}")
                    continue

        return fresh_articles

    def _filter_unused_articles(self, articles: List[Dict]) -> List[Dict]:
        """Filter out articles that were recently used in digests."""
        recently_used = self.memory.get_recently_used_articles(days_back=7)

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
        for i, article in enumerate(articles[:10], 1):  # Limit to top 10 articles
            title = article.get('title', 'Untitled')
            content = article.get('content', {}).get('processed', '') or article.get('content', {}).get('raw', '')
            url = article.get('url', '')
            source = article.get('source_id', 'unknown')
            score = article.get('analysis', {}).get('score', 0)

            # Truncate content to avoid token limits
            if len(content) > 1500:
                content = content[:1500] + "..."

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

    def _generate_hugo_metadata(self, target_date: date, articles: List[Dict]) -> Dict:
        """Generate Hugo frontmatter metadata."""
        # Create simple title based on key themes
        themes = []
        for article in articles[:5]:  # Look at top 5 articles
            title = article.get('title', '').lower()
            if 'vulnerability' in title or 'cve' in title.lower():
                themes.append('Vulnerability')
            if 'malware' in title or 'ransomware' in title:
                themes.append('Malware')
            if 'attack' in title or 'breach' in title:
                themes.append('Cyber Attack')
            if 'microsoft' in title or 'google' in title or 'apple' in title:
                themes.append('Tech Giants')

        # Unique themes
        themes = list(set(themes))[:3]  # Max 3 themes

        if themes:
            title = f"{' & '.join(themes)} Dominate Latest Threat Intelligence - {target_date.strftime('%B %d, %Y')}"
        else:
            title = f"Daily Threat Intelligence Digest - {target_date.strftime('%B %d, %Y')}"

        # Generate simple tags
        tags = ['threat-intelligence', 'daily-digest', 'cybersecurity']
        for article in articles[:10]:
            source = article.get('source_id', '').replace('-', ' ').title()
            if source not in tags and len(tags) < 8:
                tags.append(source.lower())

        return {
            'title': title,
            'date': target_date.isoformat(),
            'tags': tags[:10],  # Limit to 10 tags
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

        print(f"Generating simple digest for {target_date}")

        # 1. Get fresh articles from last 24 hours
        fresh_articles = self._get_fresh_articles(target_date)
        print(f"Found {len(fresh_articles)} fresh articles from last 24 hours")

        if not fresh_articles:
            print("No fresh articles found for digest generation")
            return None

        # 2. Filter out recently used articles
        unused_articles = self._filter_unused_articles(fresh_articles)
        print(f"Filtered to {len(unused_articles)} unused articles")

        if not unused_articles:
            print("All recent articles have been used in recent digests")
            return None

        # 3. Sort by content length (since scores may not be available for fetched articles)
        unused_articles.sort(key=lambda x: len(x.get('content', {}).get('raw', '')), reverse=True)

        # 4. Generate articles summary for prompt
        articles_summary = self._format_articles_for_prompt(unused_articles)
        print(f"Formatted {len(unused_articles)} articles for LLM analysis")

        # 5. Generate digest using LLM
        prompt = self._build_prompt(articles_summary, target_date)

        try:
            print("Generating digest content with LLM...")
            response = self.llm_registry.execute_with_fallback(
                "generate_text",
                prompt=prompt,
                max_tokens=3000
            )

            if not response or not response.strip():
                print("LLM returned empty response")
                return None

            digest_content = response.strip()
            print(f"Generated digest content: {len(digest_content)} characters")

        except Exception:
            logging.exception("Error generating digest content")
            return None

        # 6. Mark articles as used
        used_article_ids = [
            article.get('id') or article.get('guid')
            for article in unused_articles
        ]
        self.memory.mark_articles_used(used_article_ids, target_date)
        print(f"Marked {len(used_article_ids)} articles as used")

        # 7. Create Hugo post
        hugo_metadata = self._generate_hugo_metadata(target_date, unused_articles)
        hugo_filename = f"daily-threat-intelligence-{target_date.strftime('%Y-%m-%d')}.md"
        hugo_filepath = self.hugo_content_dir / hugo_filename

        # Write Hugo post
        hugo_content = self._format_hugo_post(hugo_metadata, digest_content, unused_articles)

        with open(hugo_filepath, 'w', encoding='utf-8') as f:
            f.write(hugo_content)

        print(f"Created Hugo post: {hugo_filepath}")

        # 8. Cleanup old memory entries
        self.memory.cleanup_old_entries(days_to_keep=30)

        return hugo_filename

    def _format_hugo_post(self, metadata: Dict, content: str, articles: List[Dict]) -> str:
        """Format content as a Hugo post with frontmatter."""
        # Convert metadata to TOML frontmatter
        frontmatter_lines = ["+++"]
        for key, value in metadata.items():
            if isinstance(value, list):
                frontmatter_lines.append(f'{key} = {json.dumps(value)}')
            elif isinstance(value, bool):
                frontmatter_lines.append(f'{key} = {str(value).lower()}')
            elif isinstance(value, (int, float)):
                frontmatter_lines.append(f'{key} = {value}')
            else:
                frontmatter_lines.append(f'{key} = "{value}"')
        frontmatter_lines.append("+++")

        frontmatter = "\n".join(frontmatter_lines)

        # Add references section
        references = self._generate_references_section(articles)

        return f"{frontmatter}\n\n{content}\n\n{references}"

    def _generate_references_section(self, articles: List[Dict]) -> str:
        """Generate references section for the digest."""
        if not articles:
            return ""

        references = ["## References"]

        for i, article in enumerate(articles[:15], 1):  # Limit to 15 references
            title = article.get('title', 'Untitled')
            url = article.get('url', '')
            source = article.get('source_id', 'unknown')

            if url:
                references.append(f"{i}. {title}. {source}. [{url}]({url})")
            else:
                references.append(f"{i}. {title}. {source}.")

        return "\n".join(references)

    def get_memory_statistics(self) -> Dict:
        """Get memory system statistics."""
        return self.memory.get_statistics()