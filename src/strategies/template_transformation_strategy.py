"""Template-based transformation strategy for blog generation.

This module implements a simple template-based approach for blog generation.
"""

from datetime import date, datetime, timezone
from typing import Dict, Any
import json

from ..blog_engine import TransformationStrategy


class TemplateTransformationStrategy(TransformationStrategy):
    """Template-based transformation strategy for simple blog generation."""

    def get_strategy_name(self) -> str:
        """Get the strategy name."""
        return "template"

    def get_description(self) -> str:
        """Get strategy description."""
        return "Simple template-based blog generation with basic content organization"

    def generate_blog_post(self, target_date: date, context: Dict[str, Any],
                         **kwargs) -> Dict[str, Any]:
        """Generate blog post using template-based transformation.

        Args:
            target_date: Date for the blog post.
            context: Article and IOC context data.
            **kwargs: Additional parameters.

        Returns:
            Dictionary containing blog post content and metadata.
        """
        articles = context.get('articles', [])
        iocs = context.get('iocs', [])

        # Generate title
        title = f"Daily Threat Intelligence Briefing - {target_date.strftime('%B %d, %Y')}"

        # Generate basic tags
        tags = ["threat-intelligence", "cybersecurity", "daily-briefing"]
        if articles:
            tags.append("security-alerts")

        # Build content
        content = self._build_template_content(target_date, articles, iocs)

        # Build frontmatter
        frontmatter = self._build_frontmatter(target_date, title, tags)

        # Combine
        full_content = frontmatter + "\n\n" + content

        return {
            'content': full_content,
            'title': title,
            'tags': tags,
            'statistics': {
                'strategy_used': 'template',
                'articles_processed': len(articles),
                'iocs_processed': len(iocs)
            }
        }

    def _build_template_content(self, target_date: date, articles: list, iocs: list) -> str:
        """Build content using template approach.

        Args:
            target_date: Target date.
            articles: List of articles.
            iocs: List of IOCs.

        Returns:
            Generated content string.
        """
        content_parts = []

        # Header
        content_parts.append(f"# Daily Threat Intelligence Briefing")
        content_parts.append(f"*Generated for {target_date.strftime('%B %d, %Y')}*\n")

        # Summary section
        content_parts.append("## Executive Summary")
        if articles:
            content_parts.append(f"This briefing covers {len(articles)} threat intelligence items from today's analysis.")
        else:
            content_parts.append("No significant threat intelligence activity was detected today.\n")

        # Articles section
        if articles:
            content_parts.append("## Security Updates and Threats")

            # Group by source for better organization
            by_source = {}
            for article in articles:
                source = article.get('source_id', 'unknown')
                if source not in by_source:
                    by_source[source] = []
                by_source[source].append(article)

            for source, source_articles in by_source.items():
                content_parts.append(f"\n### From {source.title()}")
                for article in source_articles[:3]:  # Limit to 3 per source
                    title = article.get('title', '')
                    summary = article.get('analysis', {}).get('summary', '')
                    relevance = article.get('analysis', {}).get('relevance_score', 0)

                    content_parts.append(f"**{title}**")
                    if relevance:
                        content_parts.append(f"*Relevance: {relevance}/10*")
                    if summary:
                        content_parts.append(f"{summary}")
                    content_parts.append("")

        # IOCs section
        if iocs:
            content_parts.append("## Key Indicators of Compromise")

            # Show top 10 IOCs
            top_iocs = iocs[:10]
            content_parts.append("\nThe following indicators were identified:")
            for ioc in top_iocs:
                ioc_type = ioc.get('type', 'unknown')
                ioc_value = ioc.get('value', '')
                content_parts.append(f"• **{ioc_type.title()}**: `{ioc_value}`")

        # Recommendations
        content_parts.append("## Security Recommendations")
        content_parts.extend([
            "1. Review all identified indicators of compromise",
            "2. Update security monitoring systems with new IOCs",
            "3. Ensure all security controls are properly configured",
            "4. Continue monitoring for emerging threats"
        ])

        return "\n".join(content_parts)

    def _build_frontmatter(self, target_date: date, title: str, tags: list) -> str:
        """Build Hugo frontmatter.

        Args:
            target_date: Target date.
            title: Blog post title.
            tags: Blog post tags.

        Returns:
            Hugo frontmatter string.
        """
        frontmatter_data = {
            "title": title,
            "date": target_date.isoformat(),
            "draft": False,
            "tags": tags,
            "categories": ["threat-intelligence"],
            "author": "Tia N. List",
            "summary": f"Daily threat intelligence briefing for {target_date.strftime('%B %d, %Y')}",
            "generation_metadata": {
                "strategy": "template",
                "generated_at": datetime.now(timezone.utc).isoformat() + "Z"
            }
        }

        # Convert to YAML format
        yaml_lines = ["---"]
        for key, value in frontmatter_data.items():
            if isinstance(value, dict):
                yaml_lines.append(f"{key}:")
                for subkey, subvalue in value.items():
                    yaml_lines.append(f"  {subkey}: {subvalue}")
            elif isinstance(value, list):
                yaml_lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
            elif isinstance(value, bool):
                yaml_lines.append(f"{key}: {str(value).lower()}")
            else:
                yaml_lines.append(f'{key}: "{value}"')
        yaml_lines.append("---")

        return "\n".join(yaml_lines)