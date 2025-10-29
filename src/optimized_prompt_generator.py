"""Optimized prompt generator for better token efficiency."""

from typing import List, Dict, Any
import json


class OptimizedPromptGenerator:
    """Generates token-efficient prompts for threat intelligence synthesis."""

    def create_compact_prompt(self, articles: List[Dict], constraints: Dict[str, set]) -> str:
        """Create a compact, token-efficient prompt.

        Args:
            articles: List of articles to analyze
            constraints: Factual constraints from articles

        Returns:
            Compact prompt with essential information only
        """
        # Format articles compactly
        compact_articles = self._format_articles_compactly(articles)

        # Add essential constraints (reduced size)
        essential_constraints = self._format_constraints_compactly(constraints)

        return f"""You are Tia N. List, Threat Intelligence Analyst. Today: {self._get_current_date()}.

TASK: Create 600-800 word security briefing from 24h data. Focus on NEW, actionable intelligence.

INTELLIGENCE DATA:
{compact_articles}

CONSTRAINTS:
{essential_constraints}

FORMAT:
- Opening with date/greeting
- 2-4 thematic sections (vulnerabilities, breaches, malware, advisories)
- Each section: 3-5 specific bullet points with sources
- Closing "What Matters Today" with 2-3 action items
- Markdown format, professional tone

REQUIREMENTS:
- ONLY use data provided above
- No speculation or filler content
- Include CVE/CISA IDs explicitly mentioned
- ⚡ for critical, 🔥 for actively exploited
- If no new threats, start with "No newly disclosed threats fitting today's criteria"

Deliver genuine intelligence value, not generic commentary."""

    def _format_articles_compactly(self, articles: List[Dict]) -> str:
        """Format articles in compact, token-efficient way."""
        if not articles:
            return "No articles available"

        formatted = []
        for article in articles[:20]:  # Limit to top 20 articles
            # Extract key information compactly
            title = article['title']
            source = article.get('source_name', 'Unknown')
            score = article.get('score', 0) or article.get('analysis', {}).get('score', 0)

            # Get IOCs (limit to 2 most important)
            iocs = self._get_top_iocs(article['id'], 2)
            ioc_str = f" IOCs: {', '.join(iocs)}" if iocs else ""

            # Get brief summary (use processed content if available, fallback to title)
            summary = self._get_compact_summary(article)

            formatted.append(f"- {title} ({source}) [Score:{score}]")
            if summary:
                formatted.append(f"  {summary}")
            formatted.append(ioc_str)

        return "\n".join(formatted)

    def _format_constraints_compactly(self, constraints: Dict[str, set]) -> str:
        """Format only essential constraints to save tokens."""
        essential_parts = []

        # Only include most important constraint types with 2-3 examples each
        if constraints.get('cves'):
            cves = list(constraints['cves'])[:3]
            essential_parts.append(f"CVEs: {', '.join(cves)}")

        if constraints.get('cisa_ids'):
            cisa_ids = list(constraints['cisa_ids'])[:2]
            essential_parts.append(f"CISA IDs: {', '.join(cisa_ids)}")

        if constraints.get('vendors'):
            vendors = list(constraints['vendors'])[:3]
            essential_parts.append(f"Vendors: {', '.join(vendors)}")

        return " | ".join(essential_parts) if essential_parts else "No specific constraints"

    def _get_top_iocs(self, article_id: str, limit: int = 2) -> List[str]:
        """Get top IOCs for an article."""
        try:
            from .json_storage import JSONStorage
            storage = JSONStorage()
            iocs = storage.get_article_iocs(article_id)

            # Prioritize important IOC types
            priority_types = ['domain', 'ip', 'url', 'hash', 'malware']
            filtered_iocs = []

            for ioc_type in priority_types:
                type_iocs = [ioc for ioc in iocs if ioc['type'] == ioc_type][:limit]
                for ioc in type_iocs:
                    if len(filtered_iocs) < limit:
                        filtered_iocs.append(f"{ioc['type']}:{ioc['value']}")

            return filtered_iocs
        except:
            return []

    def _get_compact_summary(self, article: Dict) -> str:
        """Get compact summary from article."""
        # Try processed content first
        if 'analysis' in article and 'summary' in article['analysis']:
            summary = article['analysis']['summary']
        elif 'summary' in article:
            summary = article['summary']
        else:
            # Fallback to processed content
            if 'content' in article and 'processed' in article['content']:
                summary = article['content']['processed']
            else:
                summary = ""

        # Truncate to 100 chars max
        if summary:
            return summary[:97] + "..." if len(summary) > 100 else summary
        return ""

    def _get_current_date(self) -> str:
        """Get current date in format."""
        from datetime import datetime
        return datetime.now().strftime('%B %d, %Y')