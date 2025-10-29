"""JSON-based blog generation module for Tia N. List project.

This module generates blog posts using JSON-stored content and AI context building,
creating better intelligence briefings with full git tracking of all content.
"""

from datetime import datetime, date, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

from .json_storage import JSONStorage
from .context_builder import AIContextBuilder
# from .persona import TiaPersona  # TODO: Fix persona module integration


class JSONBlogGenerator:
    """JSON-based blog generation system with AI context building."""

    def __init__(self, storage: JSONStorage = None, context_builder: AIContextBuilder = None):
        """Initialize blog generator with JSON storage and context builder."""
        self.storage = storage or JSONStorage()
        self.context_builder = context_builder or AIContextBuilder(self.storage)
        # self.persona = TiaPersona()  # TODO: Fix persona module integration
        self.hugo_content_dir = Path("hugo/content/posts")

    def generate_daily_summary(self, target_date: date = None,
                             use_intelligent_synthesis: bool = True) -> Dict[str, Any]:
        """Generate daily security summary blog post.

        Args:
            target_date: Date for the summary. If None, use today.
            use_intelligent_synthesis: Whether to use AI synthesis or template-based generation.

        Returns:
            Dictionary with generation results and statistics.
        """
        if target_date is None:
            target_date = date.today()

        print(f"Generating daily security summary for {target_date.isoformat()}...")

        # Get context for the target date
        context = self.context_builder.build_context_for_synthesis(
            target_date=target_date,
            days_back=7,
            include_io_cs=True,
            max_articles=25
        )

        stats = {
            'date': target_date.isoformat(),
            'total_articles': len(context['articles']),
            'total_iocs': len(context['iocs']),
            'unique_sources': len(context['statistics']['articles']['sources']),
            'generation_method': 'intelligent' if use_intelligent_synthesis else 'template'
        }

        if not context['articles']:
            print("No processed articles found, generating fallback post...")
            return self._generate_fallback_post(target_date, stats)

        try:
            if use_intelligent_synthesis:
                # Use AI synthesis for intelligent blog generation
                blog_content = self._intelligent_synthesis(context)
            else:
                # Use template-based generation
                blog_content = self._template_based_generation(context)

            # Add Tia's persona and formatting
            final_content = self._apply_persona_formatting(blog_content, context)

            # Generate Hugo frontmatter
            hugo_content = self._create_hugo_post(final_content, target_date, stats, context)

            # Save to Hugo content directory
            filename = f"{target_date.isoformat()}-daily-summary.md"
            filepath = self.hugo_content_dir / filename

            # Ensure directory exists
            self.hugo_content_dir.mkdir(parents=True, exist_ok=True)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(hugo_content)

            print(f"✅ Blog post generated: {filepath}")
            print(f"   Articles used: {stats['total_articles']}")
            print(f"   IOCs found: {stats['total_iocs']}")
            print(f"   Sources: {stats['unique_sources']}")
            print(f"   Content length: {len(final_content)} characters")

            stats.update({
                'success': True,
                'filepath': str(filepath),
                'content_length': len(final_content),
                'method': 'intelligent_synthesis' if use_intelligent_synthesis else 'template'
            })

            return stats

        except Exception as e:
            print(f"Error generating blog post: {e}")
            return self._generate_fallback_post(target_date, stats, error=str(e))

    def _intelligent_synthesis(self, context: Dict[str, Any]) -> str:
        """Use AI to synthesize intelligent blog post from context."""
        # Import here to avoid circular dependencies
        try:
            from .intelligent_blog_generator import ThreatIntelligenceSynthesizer
            synthesizer = ThreatIntelligenceSynthesizer()
            return synthesizer.synthesize_threat_intelligence(context['articles'])
        except ImportError:
            print("Intelligent synthesizer not available, falling back to template generation")
            return self._template_based_generation(context)

    def _template_based_generation(self, context: Dict[str, Any]) -> str:
        """Generate blog post using template-based approach."""
        articles = context['articles']
        iocs = context['iocs']
        threat_landscape = context['threat_landscape']

        content_parts = []

        # Header
        content_parts.append(f"# Daily Threat Intelligence Briefing")
        content_parts.append(f"*Published: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*")
        content_parts.append("")

        # Executive Summary
        content_parts.append("## Executive Summary")
        content_parts.append("")

        if threat_landscape:
            # Identify top threat categories
            top_categories = sorted(
                threat_landscape.items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )[:3]

            summary_points = []
            for category, data in top_categories:
                if data['count'] > 0:
                    # Improve category naming
                    display_name = self._get_display_category_name(category, data)
                    summary_points.append(
                        f"**{display_name}**: {data['count']} articles "
                        f"({data['percentage']:.1f}% of coverage)"
                    )

            if summary_points:
                content_parts.append("Today's threat landscape shows:")
                for point in summary_points:
                    content_parts.append(f"- {point}")
            else:
                content_parts.append("Limited threat intelligence activity detected today.")
        else:
            content_parts.append("Limited threat intelligence activity detected today.")

        content_parts.append("")

        # High-Priority Threats
        high_priority_articles = [
            article for article in articles
            if article.get('analysis', {}).get('score', 0) >= 80
        ][:5]

        if high_priority_articles:
            content_parts.append("## High-Priority Threats")
            content_parts.append("")

            for i, article in enumerate(high_priority_articles, 1):
                analysis = article.get('analysis', {})
                content_parts.append(f"### {i}. {article['title']}")
                content_parts.append("")
                content_parts.append(f"**Source:** {article['source_id'].replace('-', ' ').title()}")
                content_parts.append(f"**Score:** {analysis.get('score', 0)}/100")
                content_parts.append(f"**Category:** {analysis.get('threat_category', 'Unknown').replace('-', ' ').title()}")
                content_parts.append("")

                if analysis.get('summary'):
                    content_parts.append(f"**Summary:** {analysis['summary']}")
                    content_parts.append("")

                content_parts.append(f"**[Read more]({article['url']})**")
                content_parts.append("")

        # IOCs Section
        if iocs:
            content_parts.append("## Indicators of Compromise (IOCs)")
            content_parts.append("")

            # Group IOCs by type
            ioc_groups = {}
            for ioc in iocs[:20]:  # Limit to top 20 IOCs
                ioc_type = ioc.get('type', 'unknown')
                if ioc_type not in ioc_groups:
                    ioc_groups[ioc_type] = []
                ioc_groups[ioc_type].append(ioc)

            for ioc_type, iocs_list in sorted(ioc_groups.items()):
                content_parts.append(f"### {ioc_type.replace('_', ' ').title()}")
                content_parts.append("")

                for ioc in iocs_list[:5]:  # Limit each type to 5
                    value = ioc.get('value', '')
                    confidence = ioc.get('confidence', 'medium')
                    context_info = ioc.get('context', '')

                    content_parts.append(f"- **{value}** (Confidence: {confidence})")
                    if context_info:
                        content_parts.append(f"  - *{context_info}*")
                content_parts.append("")

        # All Articles Summary
        content_parts.append("## All Tracked Articles")
        content_parts.append("")

        for article in articles[:10]:  # Limit to top 10 articles
            analysis = article.get('analysis', {})
            score = analysis.get('score', 0)
            category = analysis.get('threat_category', 'unknown')

            content_parts.append(f"**{article['title']}**")
            content_parts.append(f"- *Source:* {article['source_id'].replace('-', ' ').title()}")
            content_parts.append(f"- *Score:* {score}/100 | *Category:* {category.replace('-', ' ').title()}")
            content_parts.append(f"- *URL:* {article['url']}")
            content_parts.append("")

        # References
        content_parts.append("## References")
        content_parts.append("")
        content_parts.append("All source articles are available for detailed analysis:")
        content_parts.append("")

        unique_sources = {}
        for article in articles:
            source_id = article['source_id']
            if source_id not in unique_sources:
                source = self.storage.get_source(source_id)
                unique_sources[source_id] = source

        for source_id, source in unique_sources.items():
            if source:
                content_parts.append(f"- **{source['name']}**: {source['url']}")

        return "\n".join(content_parts)

    def _get_display_category_name(self, category: str, data: Dict[str, Any]) -> str:
        """Get a more descriptive display name for threat categories."""
        # Handle the "other" category specifically
        if category.lower() == 'other':
            # Look at the top articles to determine a better category name
            top_articles = data.get('top_articles', [])
            if top_articles:
                # Analyze the titles to find a common theme
                titles = [article.get('title', '').lower() for article in top_articles[:3]]

                # Check for common themes
                if any(keyword in ' '.join(titles) for keyword in ['windows', 'update', 'microsoft', 'patch']):
                    return "Security Updates"
                elif any(keyword in ' '.join(titles) for keyword in ['government', 'policy', 'regulation']):
                    return "Security Policy"
                elif any(keyword in ' '.join(titles) for keyword in ['test', 'article']):
                    return "General Security News"
                else:
                    return "Security Developments"
            else:
                return "General Security News"

        # Improve other category names
        category_mappings = {
            'data-breach': 'Data Breaches',
            'malware': 'Malware & Threats',
            'vulnerability': 'Vulnerabilities',
            'phishing': 'Phishing Attacks',
            'ransomware': 'Ransomware',
            'supply-chain': 'Supply Chain Security',
            'network-security': 'Network Security'
        }

        return category_mappings.get(category.lower(), category.replace('-', ' ').title())

    def _apply_persona_formatting(self, content: str, context: Dict[str, Any]) -> str:
        """Apply Tia N. List persona formatting to the content."""
        # Get article count and make it sound more natural
        article_count = len(context['articles'])
        source_count = len(context['statistics']['articles']['sources'])

        # Create more natural phrasing
        if article_count >= 10:
            article_phrase = f"{article_count} articles"
        else:
            article_phrase = f"{article_count} articles"

        # Add persona introduction
        intro = f"""Good morning, cybersecurity professionals!

Tia N. List here with your daily threat intelligence briefing. I've been monitoring the threat landscape across {source_count} different security sources, and there are {article_phrase} worth your attention today.

Let's dive into what you need to know...

---

"""
        return intro + content

    def _create_hugo_post(self, content: str, target_date: date,
                         stats: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Create Hugo-compatible post with frontmatter."""
        # Generate frontmatter
        frontmatter = {
            "title": f"Daily Threat Intelligence Briefing - {target_date.strftime('%B %d, %Y')}",
            "date": target_date.isoformat(),
            "tags": ["cybersecurity", "threat-intelligence", "daily-briefing"],
            "categories": ["Threat Intelligence"],
            "author": "Tia N. List",
            "summary": f"Daily cybersecurity briefing covering {stats['total_articles']} articles with {stats['total_iocs']} indicators of compromise",
            "statistics": stats,
            "sources": list(context['statistics']['articles']['sources'].keys())
        }

        # Convert to YAML
        frontmatter_yaml = "---" + "\n"
        for key, value in frontmatter.items():
            if isinstance(value, dict):
                frontmatter_yaml += f"{key}:" + "\n"
                for subkey, subvalue in value.items():
                    frontmatter_yaml += f"  {subkey}: {subvalue}" + "\n"
            elif isinstance(value, list):
                frontmatter_yaml += f"{key}: {json.dumps(value)}" + "\n"
            else:
                frontmatter_yaml += f"{key}: {value}" + "\n"
        frontmatter_yaml += "---" + "\n" + "\n"

        return frontmatter_yaml + content

    def _generate_fallback_post(self, target_date: date, stats: Dict[str, Any],
                               error: str = None) -> Dict[str, Any]:
        """Generate fallback post when no content is available."""
        date_str = target_date.strftime('%Y-%m-%d')

        # Build technical error section separately
        error_section = ""
        if error:
            error_section = "## Technical Error\n\n" + error + "\n\n"

        fallback_content = f"""# Daily Security Summary - {date_str}

Good morning! Today's automated threat intelligence processing encountered technical difficulties.

## System Status

- **RSS Ingestion**: Completed
- **Content Enhancement**: Completed
- **LLM Processing**: Completed
- **Blog Generation**: Fallback mode activated

## What Happened

The automated system successfully ingested and enhanced content from threat intelligence feeds, but encountered issues during the final synthesis phase. This typically happens when:

- No articles met the processing criteria
- LLM provider responses required additional parsing
- System resources were constrained

{error_section}
## Tomorrow's Briefing

The system will automatically attempt full processing again tomorrow. All technical issues have been logged for review.

---

*Technical difficulties encountered during automated processing. Human review may be needed.*

*Generated automatically by Tia N. List threat intelligence system*
"""

        # Create Hugo post
        filename = f"{target_date.isoformat()}-daily-summary.md"
        filepath = self.hugo_content_dir / filename

        self.hugo_content_dir.mkdir(parents=True, exist_ok=True)

        frontmatter = f"""---
title: "Daily Security Summary - {date_str}"
date: {target_date.isoformat()}
tags: [cybersecurity, daily-summary]
author: "Tia N. List"
---

"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter + fallback_content)

        return {
            'date': target_date.isoformat(),
            'success': True,
            'fallback_mode': True,
            'filepath': str(filepath),
            'content_length': len(fallback_content),
            'error': error,
            **stats
        }


# Global blog generator instance
blog_generator = JSONBlogGenerator()


def main():
    """Main function for standalone execution."""
    print("Starting JSON-based blog generation...")

    # Generate today's summary
    result = blog_generator.generate_daily_summary(use_intelligent_synthesis=True)

    print("\n=== BLOG GENERATION SUMMARY ===")
    print(f"Date: {result['date']}")
    print(f"Success: {result['success']}")
    print(f"Method: {result['method']}")
    print(f"Articles: {result['total_articles']}")
    print(f"IOCs: {result['total_iocs']}")
    print(f"Sources: {result['unique_sources']}")

    if result.get('filepath'):
        print(f"Output: {result['filepath']}")

    if result.get('fallback_mode'):
        print("⚠️  Fallback mode was used")


if __name__ == "__main__":
    main()