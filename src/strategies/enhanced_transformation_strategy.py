"""Enhanced transformation strategy for blog generation.

This module implements the enhanced JSON blog generation as a transformation
strategy for the unified blog engine.
"""

from datetime import date, datetime
from typing import Dict, Any, Optional
from pathlib import Path
import json

from ..blog_engine import TransformationStrategy
from ..storage_provider import StorageProvider
from ..storage_registry import get_default_storage_provider
from ..context_builder import AIContextBuilder
from ..title_generator import TitleGenerator
from ..tag_generator import TagGenerator
from ..prompt_loader import PromptLoader, PromptVersionManager


class EnhancedTransformationStrategy(TransformationStrategy):
    """Enhanced transformation strategy with dynamic titles, tags, and intelligent synthesis."""

    def __init__(self, storage: StorageProvider = None,
                 title_generator: TitleGenerator = None,
                 tag_generator: TagGenerator = None,
                 prompt_loader: PromptLoader = None,
                 prompt_version_manager: PromptVersionManager = None):
        """Initialize enhanced transformation strategy.

        Args:
            storage: Storage provider for accessing data.
            title_generator: Dynamic title generator.
            tag_generator: Dynamic tag generator.
            prompt_loader: Prompt configuration loader.
            prompt_version_manager: Prompt versioning system.
        """
        self.storage = storage or get_default_storage_provider()
        self.context_builder = AIContextBuilder(self.storage)
        self.title_generator = title_generator or TitleGenerator(self.storage)
        self.tag_generator = tag_generator or TagGenerator(self.storage)

        # Initialize prompt configuration system
        self.prompt_loader = prompt_loader
        self.prompt_version_manager = prompt_version_manager

        if self.prompt_loader is None:
            try:
                self.prompt_loader = PromptLoader(Path("config/prompts"))
                if self.prompt_version_manager is None:
                    self.prompt_version_manager = PromptVersionManager(Path("config/prompts"))
            except (FileNotFoundError, Exception):
                self.prompt_loader = None
                self.prompt_version_manager = None

    def get_strategy_name(self) -> str:
        """Get the strategy name."""
        return "enhanced"

    def get_description(self) -> str:
        """Get strategy description."""
        return "Enhanced blog generation with dynamic titles, tags, and intelligent synthesis"

    def generate_blog_post(self, target_date: date, context: Dict[str, Any],
                         use_intelligent_synthesis: bool = True,
                         use_dynamic_title: bool = True,
                         use_dynamic_tags: bool = True,
                         **kwargs) -> Dict[str, Any]:
        """Generate blog post using enhanced transformation.

        Args:
            target_date: Date for the blog post.
            context: Article and IOC context data.
            use_intelligent_synthesis: Whether to use AI synthesis.
            use_dynamic_title: Whether to use dynamic title generation.
            use_dynamic_tags: Whether to use dynamic tag generation.
            **kwargs: Additional parameters.

        Returns:
            Dictionary containing blog post content and metadata.
        """
        # Initialize statistics
        stats = {
            'dynamic_title_used': False,
            'dynamic_tags_used': False,
            'intelligent_synthesis_used': False,
            'ab_test_variant': None,
            'prompt_version_used': None
        }

        # Extract articles from context
        articles = context.get('articles', [])
        iocs = context.get('iocs', [])

        if not articles:
            return self._generate_fallback_post(target_date, stats)

        try:
            # Generate dynamic title if enabled
            title = None
            if use_dynamic_title:
                title = self._generate_dynamic_title(target_date, articles)
                stats['dynamic_title_used'] = True
                stats['title'] = title

            # Generate dynamic tags if enabled
            tags = []
            if use_dynamic_tags:
                tags = self._generate_dynamic_tags(target_date, articles)
                stats['dynamic_tags_used'] = True
                stats['tags'] = tags

            # Generate content
            if use_intelligent_synthesis and self.prompt_loader:
                content = self._intelligent_synthesis(
                    target_date, articles, iocs, title, tags, stats
                )
                stats['intelligent_synthesis_used'] = True
            else:
                content = self._template_based_generation(
                    target_date, articles, iocs, title, tags
                )

            # Build Hugo frontmatter
            frontmatter = self._build_frontmatter(
                target_date, title, tags, stats
            )

            # Combine frontmatter and content
            full_content = frontmatter + "\n\n" + content

            return {
                'content': full_content,
                'title': title,
                'tags': tags,
                'statistics': stats
            }

        except Exception as e:
            print(f"Error in enhanced transformation: {e}")
            return self._generate_fallback_post(target_date, stats)

    def _generate_dynamic_title(self, target_date: date, articles: list) -> str:
        """Generate dynamic title for the blog post.

        Args:
            target_date: Target date for the title.
            articles: List of articles for theme analysis.

        Returns:
            Dynamic title string.
        """
        try:
            title = self.title_generator.generate_title(articles, target_date)
            if title:
                return title
        except Exception as e:
            print(f"Dynamic title generation failed: {e}")

        # Fallback title
        return f"Daily Threat Intelligence Briefing - {target_date.strftime('%B %d, %Y')}"

    def _generate_dynamic_tags(self, target_date: date, articles: list) -> list:
        """Generate dynamic tags for the blog post.

        Args:
            target_date: Target date for tag generation.
            articles: List of articles for tag extraction.

        Returns:
            List of tag strings.
        """
        try:
            tags = self.tag_generator.generate_tags_for_date(target_date, limit=15)
            return self.tag_generator.format_tags_for_hugo(tags)
        except Exception as e:
            print(f"Dynamic tag generation failed: {e}")
            return ["threat-intelligence", "cybersecurity", "daily-briefing"]

    def _intelligent_synthesis(self, target_date: date, articles: list, iocs: list,
                             title: str, tags: list, stats: dict) -> str:
        """Generate content using intelligent LLM synthesis.

        Args:
            target_date: Target date.
            articles: List of articles.
            iocs: List of IOCs.
            title: Blog post title.
            tags: Blog post tags.
            stats: Statistics dictionary to update.

        Returns:
            Generated content string.
        """
        try:
            # Build enhanced synthesis prompt
            synthesis_prompt = self._build_synthesis_prompt(
                target_date, articles, iocs, title, tags
            )

            # Import here to avoid circular dependencies
            from ..intelligent_blog_generator import ThreatIntelligenceSynthesizer
            synthesizer = ThreatIntelligenceSynthesizer()

            # Generate synthesis
            synthesis_result = synthesizer.synthesize_threat_intelligence(
                synthesis_prompt, target_date
            )

            # Update statistics
            stats['ab_test_variant'] = synthesis_result.get('ab_test_variant')
            stats['prompt_version_used'] = synthesis_result.get('prompt_version')

            return synthesis_result.get('content', '')

        except Exception as e:
            print(f"Intelligent synthesis failed: {e}")
            # Fall back to template-based generation
            return self._template_based_generation(target_date, articles, iocs, title, tags)

    def _template_based_generation(self, target_date: date, articles: list, iocs: list,
                                 title: str, tags: list) -> str:
        """Generate content using template-based approach.

        Args:
            target_date: Target date.
            articles: List of articles.
            iocs: List of IOCs.
            title: Blog post title.
            tags: Blog post tags.

        Returns:
            Generated content string.
        """
        # Group articles by threat category
        categories = {}
        for article in articles:
            analysis = article.get('analysis', {})
            category = analysis.get('threat_category', 'general')
            if category not in categories:
                categories[category] = []
            categories[category].append(article)

        # Build content sections
        content_parts = []

        # Executive summary
        content_parts.append("## Executive Summary")

        high_priority_articles = [
            article for article in articles
            if article.get('analysis', {}).get('relevance_score', 0) >= 7
        ]

        if high_priority_articles:
            summary_points = []
            for article in high_priority_articles[:5]:  # Top 5 high-priority items
                title = article.get('title', '')
                source = article.get('source_id', '')
                summary_points.append(f"• **{title}** ({source})")

            content_parts.append("\n".join(summary_points))
        else:
            content_parts.append(f"This briefing covers {len(articles)} threat intelligence items from {len(categories)} categories.")

        # Threat landscape analysis
        content_parts.append("\n## Threat Landscape Analysis")

        for category, category_articles in categories.items():
            if len(category_articles) >= 2:  # Only show categories with multiple items
                content_parts.append(f"\n### {category.title()} Activity ({len(category_articles)} items)")

                for article in category_articles[:3]:  # Top 3 per category
                    title = article.get('title', '')
                    summary = article.get('analysis', {}).get('summary', '')
                    relevance = article.get('analysis', {}).get('relevance_score', 0)

                    content_parts.append(f"**{title}** (Relevance: {relevance}/10)")
                    if summary:
                        content_parts.append(f"{summary}")
                    content_parts.append("")

        # IOC summary
        if iocs:
            content_parts.append("\n## Key Indicators of Compromise")

            # Group IOCs by type
            ioc_types = {}
            for ioc in iocs[:20]:  # Limit to top 20 IOCs
                ioc_type = ioc.get('type', 'unknown')
                if ioc_type not in ioc_types:
                    ioc_types[ioc_type] = []
                ioc_types[ioc_type].append(ioc)

            for ioc_type, type_iocs in ioc_types.items():
                content_parts.append(f"\n### {ioc_type.title()} Indicators")
                for ioc in type_iocs[:5]:  # Top 5 per type
                    value = ioc.get('value', '')
                    context = ioc.get('context', '')
                    content_parts.append(f"• `{value}`")
                    if context:
                        content_parts.append(f"  Context: {context}")

        # Strategic recommendations
        content_parts.append("\n## Strategic Recommendations")
        content_parts.extend([
            "1. **Monitor High-Priority Threats**: Focus on items with relevance scores 8+.",
            "2. **IOC Integration**: Consider integrating identified indicators into security monitoring systems.",
            "3. **Threat Landscape Awareness**: Maintain awareness of emerging threat patterns.",
            f"4. **Continuous Monitoring**: This briefing covers activity from the past 7 days leading to {target_date.strftime('%B %d, %Y')}."
        ])

        return "\n".join(content_parts)

    def _build_frontmatter(self, target_date: date, title: str, tags: list, stats: dict) -> str:
        """Build Hugo frontmatter for the blog post.

        Args:
            target_date: Target date.
            title: Blog post title.
            tags: Blog post tags.
            stats: Generation statistics.

        Returns:
            Hugo frontmatter string.
        """
        frontmatter = {
            "title": title,
            "date": target_date.isoformat(),
            "draft": False,
            "tags": tags,
            "categories": ["threat-intelligence"],
            "author": "Tia N. List",
            "summary": f"Daily threat intelligence briefing for {target_date.strftime('%B %d, %Y')}",
            "generation_metadata": {
                "strategy": "enhanced",
                "dynamic_title": stats['dynamic_title_used'],
                "dynamic_tags": stats['dynamic_tags_used'],
                "intelligent_synthesis": stats['intelligent_synthesis_used'],
                "generated_at": datetime.utcnow().isoformat() + "Z"
            }
        }

        # Add A/B testing metadata if available
        if stats.get('ab_test_variant'):
            frontmatter["generation_metadata"]["ab_test_variant"] = stats['ab_test_variant']

        if stats.get('prompt_version_used'):
            frontmatter["generation_metadata"]["prompt_version"] = stats['prompt_version_used']

        # Convert to TOML format
        toml_lines = ["---"]
        for key, value in frontmatter.items():
            if isinstance(value, dict):
                toml_lines.append(f"{key}:")
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, bool):
                        toml_lines.append(f"  {subkey}: {str(subvalue).lower()}")
                    else:
                        toml_lines.append(f"  {subkey}: {subvalue}")
            elif isinstance(value, list):
                toml_lines.append(f"{key}: {json.dumps(value)}")
            elif isinstance(value, bool):
                toml_lines.append(f"{key}: {str(value).lower()}")
            else:
                toml_lines.append(f'{key}: "{value}"')
        toml_lines.append("---")

        return "\n".join(toml_lines)

    def _build_synthesis_prompt(self, target_date: date, articles: list, iocs: list,
                              title: str, tags: list) -> str:
        """Build enhanced synthesis prompt using prompt configuration.

        Args:
            target_date: Target date.
            articles: List of articles.
            iocs: List of IOCs.
            title: Blog post title.
            tags: Blog post tags.

        Returns:
            Synthesis prompt string.
        """
        if not self.prompt_loader:
            # Fallback simple prompt
            return self._build_simple_prompt(target_date, articles, iocs)

        try:
            # Build enhanced prompt using prompt loader
            prompt = self.prompt_loader.build_enhanced_synthesis_prompt(
                articles_data=self._format_articles_for_prompt(articles),
                factual_constraints=self._build_factual_constraints(articles),
                current_date=target_date.isoformat()
            )

            return prompt
        except Exception as e:
            print(f"Enhanced prompt building failed: {e}")
            return self._build_simple_prompt(target_date, articles, iocs)

    def _format_articles_for_prompt(self, articles: list) -> str:
        """Format articles for LLM prompt.

        Args:
            articles: List of articles.

        Returns:
            Formatted articles string.
        """
        article_strings = []
        for i, article in enumerate(articles[:25], 1):  # Limit to 25 articles
            title = article.get('title', '')
            source = article.get('source_id', '')
            summary = article.get('analysis', {}).get('summary', '')
            relevance = article.get('analysis', {}).get('relevance_score', 0)

            article_str = f"Article {i}: {title}\nSource: {source}\nRelevance: {relevance}/10\n"
            if summary:
                article_str += f"Summary: {summary}\n"

            article_strings.append(article_str)

        return "\n".join(article_strings)

    def _build_factual_constraints(self, articles: list) -> str:
        """Build factual constraints for LLM prompt.

        Args:
            articles: List of articles.

        Returns:
            Factual constraints string.
        """
        constraints = []

        # Extract real entities from articles
        real_cves = set()
        real_sources = set()

        for article in articles:
            # Extract CVEs (simple pattern matching)
            title = article.get('title', '')
            summary = article.get('analysis', {}).get('summary', '')

            import re
            cve_pattern = r'CVE-\d{4}-\d{4,7}'
            for cve in re.findall(cve_pattern, title + summary, re.IGNORECASE):
                real_cves.add(cve.upper())

            real_sources.add(article.get('source_id', ''))

        if real_cves:
            constraints.append(f"Only report on these CVEs: {', '.join(sorted(real_cves))}")

        if real_sources:
            constraints.append(f"Source attribution: {', '.join(sorted(real_sources))}")

        return "\n".join(constraints)

    def _build_simple_prompt(self, target_date: date, articles: list, iocs: list) -> str:
        """Build simple fallback prompt.

        Args:
            target_date: Target date.
            articles: List of articles.
            iocs: List of IOCs.

        Returns:
            Simple prompt string.
        """
        return f"""
Generate a professional threat intelligence briefing for {target_date.strftime('%B %d, %Y')}.

Articles: {len(articles)}
IOCs: {len(iocs)}

Create a concise, actionable briefing covering:
1. Executive summary
2. Key threats and vulnerabilities
3. Relevant indicators of compromise
4. Strategic recommendations

Focus on high-priority threats with relevance scores 7+.
"""

    def _generate_fallback_post(self, target_date: date, stats: dict) -> Dict[str, Any]:
        """Generate fallback post when no articles are available.

        Args:
            target_date: Target date.
            stats: Statistics dictionary.

        Returns:
            Fallback blog post content.
        """
        title = f"Daily Threat Intelligence Briefing - {target_date.strftime('%B %d, %Y')}"
        tags = ["threat-intelligence", "daily-briefing"]

        frontmatter = f"""---
title: "{title}"
date: "{target_date.isoformat()}"
draft: false
tags: {json.dumps(tags)}
categories: ["threat-intelligence"]
author: "Tia N. List"
summary: "Daily threat intelligence briefing"
generation_metadata: {{
    strategy: "enhanced",
    fallback: true,
    generated_at: "{datetime.utcnow().isoformat()}Z"
}}
---

# {title}

## Executive Summary

No significant threat intelligence activity was detected in the past 24 hours.

## Threat Landscape Analysis

Current threat landscape appears quiet with no high-priority indicators requiring immediate attention.

## Recommendations

1. Continue normal security monitoring procedures
2. Review existing security controls and configurations
3. Stay alert for emerging threat patterns

---

*This briefing is automatically generated daily. Check back tomorrow for the latest threat intelligence updates.*
"""

        return {
            'content': frontmatter,
            'title': title,
            'tags': tags,
            'statistics': {**stats, 'fallback_used': True}
        }