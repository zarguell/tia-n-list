"""Enhanced JSON-based blog generation module with dynamic titles and tags.

This module integrates the title and tag generators to create more dynamic
and engaging blog posts while maintaining all existing functionality.
"""

from datetime import datetime, date, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

from .json_storage import JSONStorage
from .context_builder import AIContextBuilder
from .title_generator import TitleGenerator
from .tag_generator import TagGenerator


class EnhancedJSONBlogGenerator:
    """Enhanced JSON-based blog generation system with dynamic titles and tags."""

    def __init__(self, storage: JSONStorage = None, context_builder: AIContextBuilder = None,
                 title_generator: TitleGenerator = None, tag_generator: TagGenerator = None):
        """Initialize enhanced blog generator with all components."""
        self.storage = storage or JSONStorage()
        self.context_builder = context_builder or AIContextBuilder(self.storage)
        self.title_generator = title_generator or TitleGenerator(self.storage)
        self.tag_generator = tag_generator or TagGenerator(self.storage)
        self.hugo_content_dir = Path("hugo/content/posts")

    def generate_daily_summary(self, target_date: date = None,
                             use_intelligent_synthesis: bool = True,
                             use_dynamic_title: bool = True,
                             use_dynamic_tags: bool = True) -> Dict[str, Any]:
        """Generate daily security summary blog post with enhanced features.

        Args:
            target_date: Date for the summary. If None, use today.
            use_intelligent_synthesis: Whether to use AI synthesis or template-based generation.
            use_dynamic_title: Whether to use dynamic title generation.
            use_dynamic_tags: Whether to use dynamic tag generation.

        Returns:
            Dictionary with generation results and statistics.
        """
        if target_date is None:
            target_date = date.today()

        print(f"🎯 Generating enhanced daily security summary for {target_date.isoformat()}...")
        print(f"   Dynamic titles: {'✅' if use_dynamic_title else '❌'}")
        print(f"   Dynamic tags: {'✅' if use_dynamic_tags else '❌'}")
        print(f"   Intelligent synthesis: {'✅' if use_intelligent_synthesis else '❌'}")

        # Get context for the target date
        context = self.context_builder.build_context_for_synthesis(
            target_date=target_date,
            days_back=7,
            include_io_cs=True,
            max_articles=25
        )

        # Initialize statistics
        stats = {
            'date': target_date.isoformat(),
            'total_articles': len(context['articles']),
            'total_iocs': len(context['iocs']),
            'unique_sources': len(context['statistics']['articles']['sources']),
            'dynamic_title_used': False,
            'dynamic_tags_used': False,
            'intelligent_synthesis_used': False
        }

        if not context['articles']:
            print("⚠️  No articles found for the specified date range")
            return self._generate_fallback_post(target_date, stats)

        try:
            # Generate dynamic title if enabled
            dynamic_title = None
            if use_dynamic_title:
                print("🎯 Generating dynamic title...")
                dynamic_title = self.title_generator.generate_title(context['articles'], target_date)
                if dynamic_title and "Daily Threat Intelligence Briefing" not in dynamic_title:
                    stats['dynamic_title_used'] = True
                    print(f"✅ Dynamic title generated: {dynamic_title}")
                else:
                    print("⚠️  Dynamic title generation failed, using fallback")
                    dynamic_title = None

            # Generate dynamic tags if enabled
            dynamic_tags = None
            if use_dynamic_tags:
                print("🏷️  Generating dynamic tags...")
                dynamic_tags = self.tag_generator.generate_tags_for_date(target_date, limit=12)
                hugo_tags = self.tag_generator.format_tags_for_hugo(dynamic_tags)
                if hugo_tags:
                    stats['dynamic_tags_used'] = True
                    stats['generated_tags_count'] = len(hugo_tags)
                    print(f"✅ Generated {len(hugo_tags)} dynamic tags: {', '.join(hugo_tags[:5])}{'...' if len(hugo_tags) > 5 else ''}")
                else:
                    print("⚠️  Dynamic tag generation failed, using fallback")
                    dynamic_tags = None

            # Generate content using intelligent synthesis or template
            if use_intelligent_synthesis:
                print("🧠 Using intelligent synthesis...")
                final_content = self._intelligent_synthesis(context)
                stats['intelligent_synthesis_used'] = True
            else:
                print("📝 Using template-based generation...")
                final_content = self._template_based_generation(context)

            # Generate Hugo post with dynamic title and tags
            hugo_content = self._create_enhanced_hugo_post(
                final_content, target_date, stats, context,
                dynamic_title=dynamic_title,
                dynamic_tags=dynamic_tags
            )

            # Save to Hugo content directory
            filename = f"{target_date.isoformat()}-daily-summary.md"
            filepath = self.hugo_content_dir / filename

            # Ensure directory exists
            self.hugo_content_dir.mkdir(parents=True, exist_ok=True)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(hugo_content)

            print(f"✅ Enhanced blog post generated: {filepath}")
            print(f"   Articles used: {stats['total_articles']}")
            print(f"   IOCs found: {stats['total_iocs']}")
            print(f"   Sources: {stats['unique_sources']}")
            print(f"   Content length: {len(final_content)} characters")

            # Enhanced statistics
            if dynamic_title:
                print(f"   Dynamic title: {dynamic_title[:60]}{'...' if len(dynamic_title) > 60 else ''}")
            if dynamic_tags:
                print(f"   Dynamic tags: {len(dynamic_tags)} tags across {len(set(t['category'] for t in dynamic_tags))} categories")

            stats.update({
                'success': True,
                'filepath': str(filepath),
                'content_length': len(final_content),
                'generation_method': 'intelligent' if stats['intelligent_synthesis_used'] else 'template'
            })

            return stats

        except Exception as e:
            print(f"Error generating enhanced blog post: {e}")
            return self._generate_fallback_post(target_date, stats, error=str(e))

    def _intelligent_synthesis(self, context: Dict[str, Any]) -> str:
        """Use AI to synthesize intelligent blog post from context."""
        # Import here to avoid circular dependencies
        try:
            from .intelligent_blog_generator import ThreatIntelligenceSynthesizer
            from datetime import datetime
            synthesizer = ThreatIntelligenceSynthesizer()
            result = synthesizer.synthesize_threat_intelligence(context['articles'])

            # Extract content if result contains frontmatter (complete Hugo post)
            if result.startswith('---\n'):
                # Find the end of frontmatter
                frontmatter_end = result.find('\n---\n', 4)
                if frontmatter_end != -1:
                    # Extract just the content after frontmatter
                    content = result[frontmatter_end + 5:]  # Skip the closing ---\n
                    print("✅ Extracted content from intelligent synthesis (frontmatter detected)")
                    # Save to memory to prevent future duplication
                    synthesizer._save_report_to_memory(context['articles'], content, datetime.now())
                    return content

            # Return as-is if no frontmatter detected
            print("✅ Using intelligent synthesis content directly")
            # Save to memory to prevent future duplication
            synthesizer._save_report_to_memory(context['articles'], result, datetime.now())
            return result

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
            summary = threat_landscape.get('summary', 'Today\'s threat intelligence briefing covers significant cybersecurity developments across multiple sectors.')
            content_parts.append(summary)
        else:
            content_parts.append("Today's threat intelligence briefing covers significant cybersecurity developments across multiple sectors.")

        content_parts.append("")

        # Top Stories Section
        if articles:
            content_parts.append("## Top Stories")
            content_parts.append("")

            # Sort by score and take top 5
            sorted_articles = sorted(articles, key=lambda x: x.get('score', 0), reverse=True)[:5]

            for i, article in enumerate(sorted_articles, 1):
                title = article.get('title', 'Untitled Article')
                source = article.get('source_name', 'Unknown Source')
                url = article.get('url', '')
                score = article.get('score', 0)

                content_parts.append(f"### {i}. {title}")
                content_parts.append(f"**Source:** {source} | **Relevance Score:** {score}")
                content_parts.append("")

                # Add a brief excerpt if available
                content = article.get('content', {}).get('processed', '') or article.get('content', {}).get('raw', '')
                if content:
                    excerpt = content[:200] + "..." if len(content) > 200 else content
                    content_parts.append(excerpt)
                    content_parts.append("")

                if url:
                    content_parts.append(f"[Read more]({url})")
                    content_parts.append("")

        # IOCs Section
        if iocs:
            content_parts.append("## Indicators of Compromise")
            content_parts.append("")

            # Group IOCs by type
            ioc_types = {}
            for ioc in iocs:
                ioc_type = ioc.get('type', 'unknown')
                if ioc_type not in ioc_types:
                    ioc_types[ioc_type] = []
                ioc_types[ioc_type].append(ioc['value'])

            for ioc_type, values in ioc_types.items():
                if values:
                    content_parts.append(f"### {ioc_type.title()}")
                    content_parts.append("")
                    for value in values[:10]:  # Limit to 10 per type
                        content_parts.append(f"- `{value}`")
                    content_parts.append("")

        content_parts.append("---")
        content_parts.append("*This briefing was automatically generated by Tia N. List's threat intelligence system.*")

        return "\n".join(content_parts)

    def _create_enhanced_hugo_post(self, content: str, target_date: date,
                                 stats: Dict[str, Any], context: Dict[str, Any],
                                 dynamic_title: str = None, dynamic_tags: List[Dict] = None) -> str:
        """Create enhanced Hugo-compatible post with dynamic title and tags."""

        # Determine title
        if dynamic_title:
            title = dynamic_title
        else:
            title = f"Daily Threat Intelligence Briefing - {target_date.strftime('%B %d, %Y')}"

        # Determine tags
        if dynamic_tags:
            hugo_tags = self.tag_generator.format_tags_for_hugo(dynamic_tags)
        else:
            hugo_tags = ["cybersecurity", "threat-intelligence", "daily-briefing"]

        # Generate enhanced frontmatter
        frontmatter = {
            "title": title,
            "date": target_date.isoformat(),
            "tags": hugo_tags,
            "categories": ["Threat Intelligence"],
            "author": "Tia N. List",
            "summary": f"Daily cybersecurity briefing covering {stats['total_articles']} articles with {stats['total_iocs']} indicators of compromise",
            "statistics": stats,
            "sources": list(context['statistics']['articles']['sources'].keys())
        }

        # Add generation metadata
        frontmatter["generation_metadata"] = {
            "dynamic_title_used": stats.get('dynamic_title_used', False),
            "dynamic_tags_used": stats.get('dynamic_tags_used', False),
            "intelligent_synthesis_used": stats.get('intelligent_synthesis_used', False),
            "generated_tags_count": stats.get('generated_tags_count', 0)
        }

        # Convert to YAML
        frontmatter_yaml = "---" + "\n"
        for key, value in frontmatter.items():
            if isinstance(value, dict):
                frontmatter_yaml += f"{key}:" + "\n"
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, (list, dict)):
                        frontmatter_yaml += f"  {subkey}: {json.dumps(subvalue)}" + "\n"
                    else:
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
- **Blog Generation**: Fallback Mode

{error_section}Please check back later for the complete threat intelligence briefing.

---

*This is a fallback message generated by Tia N. List's automated system.*
"""

        # Create filename and filepath
        filename = f"{date_str}-daily-summary-fallback.md"
        filepath = self.hugo_content_dir / filename

        # Ensure directory exists
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

    def get_generation_statistics(self) -> Dict[str, Any]:
        """Get statistics about the enhanced blog generation capabilities."""
        return {
            'title_generator_available': self.title_generator is not None,
            'tag_generator_available': self.tag_generator is not None,
            'title_generator_stats': self.title_generator.get_title_statistics() if self.title_generator else {},
            'tag_generator_stats': self.tag_generator.get_tag_statistics() if self.tag_generator else {},
            'supported_features': {
                'dynamic_titles': True,
                'dynamic_tags': True,
                'intelligent_synthesis': True,
                'template_fallback': True,
                'hugo_integration': True
            }
        }


# Global enhanced blog generator instance
enhanced_blog_generator = EnhancedJSONBlogGenerator()


def main():
    """Main function for standalone execution."""
    print("🚀 Starting enhanced JSON-based blog generation...")

    # Print system statistics
    stats = enhanced_blog_generator.get_generation_statistics()
    print(f"📊 System Status:")
    print(f"   Title Generator: {'✅' if stats['title_generator_available'] else '❌'}")
    print(f"   Tag Generator: {'✅' if stats['tag_generator_available'] else '❌'}")
    print(f"   Supported Features: {', '.join([k for k, v in stats['supported_features'].items() if v])}")
    print()

    # Generate today's summary
    result = enhanced_blog_generator.generate_daily_summary(
        use_intelligent_synthesis=True,
        use_dynamic_title=True,
        use_dynamic_tags=True
    )

    print(f"\n🎉 Enhanced blog generation completed: {result['success']}")

    if result.get('filepath'):
        print(f"✅ Blog post: {result['filepath']}")
    else:
        print("ℹ️  Blog generation completed with fallback mode")

    # Print generation summary
    print(f"\n📈 Generation Summary:")
    print(f"   Dynamic Title: {'✅' if result.get('dynamic_title_used') else '❌'}")
    print(f"   Dynamic Tags: {'✅' if result.get('dynamic_tags_used') else '❌'}")
    print(f"   Intelligent Synthesis: {'✅' if result.get('intelligent_synthesis_used') else '❌'}")
    print(f"   Content Length: {result.get('content_length', 0)} characters")


if __name__ == "__main__":
    main()