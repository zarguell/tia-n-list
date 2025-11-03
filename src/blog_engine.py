"""Blog Engine abstraction for Tia N. List project.

This module provides a unified interface for different blog generation approaches,
implementing the strategy pattern to consolidate multiple blog generators.
"""

from abc import ABC, abstractmethod
from datetime import date
from pathlib import Path
from typing import List, Dict, Any, Optional

from .storage_provider import StorageProvider
from .storage_registry import get_default_storage_provider


class TransformationStrategy(ABC):
    """Abstract base class for blog transformation strategies."""

    @abstractmethod
    def generate_blog_post(self, target_date: date, context: Dict[str, Any],
                         **kwargs) -> Dict[str, Any]:
        """Generate a blog post for the given date and context.

        Args:
            target_date: Date for the blog post.
            context: Article and IOC context data.
            **kwargs: Additional strategy-specific parameters.

        Returns:
            Dictionary containing blog post content and metadata.
        """
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get the name of this transformation strategy."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get a description of this transformation strategy."""
        pass

    def validate_context(self, context: Dict[str, Any]) -> bool:
        """Validate that the context contains required data.

        Args:
            context: Context data to validate.

        Returns:
            True if context is valid for this strategy.
        """
        # Basic validation - at least some articles
        return 'articles' in context and len(context['articles']) > 0


class BlogEngine:
    """Unified blog generation engine using transformation strategies."""

    def __init__(self, storage: StorageProvider = None, output_dir: str = "hugo/content/posts"):
        """Initialize the blog engine.

        Args:
            storage: Storage provider for accessing articles and data.
            output_dir: Directory where Hugo blog posts will be written.
        """
        self.storage = storage or get_default_storage_provider()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.strategies: Dict[str, TransformationStrategy] = {}

    def register_strategy(self, strategy: TransformationStrategy) -> None:
        """Register a transformation strategy.

        Args:
            strategy: Transformation strategy to register.
        """
        strategy_name = strategy.get_strategy_name()
        self.strategies[strategy_name] = strategy

    def get_available_strategies(self) -> List[str]:
        """Get list of available transformation strategies.

        Returns:
            List of strategy names.
        """
        return list(self.strategies.keys())

    def generate_daily_post(self, target_date: date = None,
                           strategy_name: str = "enhanced",
                           **kwargs) -> Dict[str, Any]:
        """Generate a daily blog post using the specified strategy.

        Args:
            target_date: Date for the blog post. If None, uses today.
            strategy_name: Name of the transformation strategy to use.
            **kwargs: Additional parameters passed to the strategy.

        Returns:
            Dictionary with generation results and statistics.
        """
        if target_date is None:
            target_date = date.today()

        if strategy_name not in self.strategies:
            raise ValueError(f"Unknown strategy: {strategy_name}. Available: {list(self.strategies.keys())}")

        # Build context for the target date
        context = self._build_context(target_date)

        # Initialize statistics
        stats = {
            'date': target_date.isoformat(),
            'strategy_used': strategy_name,
            'total_articles': len(context.get('articles', [])),
            'total_iocs': len(context.get('iocs', [])),
            'unique_sources': len(set(article.get('source_id') for article in context.get('articles', []))),
            'success': False,
            'error': None,
            'output_file': None
        }

        try:
            # Get strategy and validate context
            strategy = self.strategies[strategy_name]
            if not strategy.validate_context(context):
                stats['error'] = f"Context validation failed for strategy {strategy_name}"
                return stats

            print(f"🎯 Generating daily blog post for {target_date.isoformat()} using {strategy_name} strategy...")
            print(f"   Articles available: {stats['total_articles']}")
            print(f"   IOCs available: {stats['total_iocs']}")
            print(f"   Unique sources: {stats['unique_sources']}")

            # Generate blog post using strategy
            result = strategy.generate_blog_post(target_date, context, **kwargs)

            # Write blog post to file
            output_file = self._write_blog_post(result, target_date)
            stats['output_file'] = output_file
            stats['success'] = True

            print(f"✅ Blog post generated successfully: {output_file}")

            # Include strategy-specific statistics
            if 'statistics' in result:
                stats.update(result['statistics'])

        except Exception as e:
            stats['error'] = str(e)
            print(f"❌ Blog post generation failed: {e}")

        return stats

    def _build_context(self, target_date: date) -> Dict[str, Any]:
        """Build context data for blog generation.

        Args:
            target_date: Date to build context for.

        Returns:
            Context dictionary with articles, IOCs, and statistics.
        """
        # Get articles for the date range (today and previous 6 days)
        from datetime import timedelta
        start_date = target_date - timedelta(days=6)
        end_date = target_date

        articles = self.storage.get_articles_by_date_range(start_date, end_date, status="processed")

        # Get IOCs for the date range
        iocs = []
        for date_offset in range(7):
            check_date = start_date + timedelta(days=date_offset)
            daily_iocs = self.storage.get_iocs_by_date(check_date)
            iocs.extend(daily_iocs)

        # Build statistics
        sources = set()
        categories = {}
        for article in articles:
            sources.add(article.get('source_id'))
            category = article.get('analysis', {}).get('threat_category', 'unknown')
            categories[category] = categories.get(category, 0) + 1

        context = {
            'target_date': target_date.isoformat(),
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'articles': articles,
            'iocs': iocs,
            'statistics': {
                'articles': {
                    'total': len(articles),
                    'sources': list(sources),
                    'categories': categories
                },
                'iocs': {
                    'total': len(iocs),
                    'by_type': {}
                }
            }
        }

        # Count IOCs by type
        for ioc in iocs:
            ioc_type = ioc.get('type', 'unknown')
            context['statistics']['iocs']['by_type'][ioc_type] = context['statistics']['iocs']['by_type'].get(ioc_type, 0) + 1

        return context

    def _write_blog_post(self, result: Dict[str, Any], target_date: date) -> str:
        """Write blog post to Hugo file.

        Args:
            result: Blog generation result from strategy.
            target_date: Date for the blog post.

        Returns:
            Path to the written file.
        """
        # Generate filename
        filename = f"{target_date.isoformat()}-daily-threat-intelligence-briefing.md"
        output_path = self.output_dir / filename

        # Write content to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result['content'])

        return str(output_path)

    def get_strategy_info(self, strategy_name: str) -> Dict[str, Any]:
        """Get information about a transformation strategy.

        Args:
            strategy_name: Name of the strategy.

        Returns:
            Dictionary with strategy information.
        """
        if strategy_name not in self.strategies:
            raise ValueError(f"Unknown strategy: {strategy_name}")

        strategy = self.strategies[strategy_name]
        return {
            'name': strategy.get_strategy_name(),
            'description': strategy.get_description(),
            'class': strategy.__class__.__name__,
            'module': strategy.__class__.__module__
        }

    def list_strategies(self) -> Dict[str, Dict[str, Any]]:
        """List all available strategies with their information.

        Returns:
            Dictionary mapping strategy names to their information.
        """
        return {
            name: self.get_strategy_info(name)
            for name in self.strategies.keys()
        }

    def health_check(self) -> Dict[str, Any]:
        """Check the health of the blog engine.

        Returns:
            Dictionary with health status information.
        """
        health = {
            "status": "healthy",
            "checks": {},
            "issues": []
        }

        try:
            # Check storage health
            storage_health = self.storage.health_check()
            health["checks"]["storage"] = storage_health["status"] == "healthy"

            if storage_health["status"] != "healthy":
                health["status"] = "degraded"
                health["issues"].extend(storage_health.get("issues", []))

            # Check output directory
            health["checks"]["output_directory"] = self.output_dir.exists() and self.output_dir.is_dir()

            if not health["checks"]["output_directory"]:
                health["status"] = "unhealthy"
                health["issues"].append(f"Output directory {self.output_dir} is not accessible")

            # Check strategies
            health["checks"]["strategies"] = len(self.strategies) > 0
            health["strategy_count"] = len(self.strategies)

            if len(self.strategies) == 0:
                health["status"] = "degraded"
                health["issues"].append("No transformation strategies registered")

        except Exception as e:
            health["status"] = "unhealthy"
            health["issues"].append(f"Health check failed: {e}")

        return health

    def get_default_strategy(self) -> str:
        """Get the default transformation strategy.

        Returns:
            Name of the default strategy.
        """
        # Preference order for default strategy
        preferences = ["enhanced", "intelligent", "two_tier"]

        for preference in preferences:
            if preference in self.strategies:
                return preference

        # Return first available strategy if no preferences match
        if self.strategies:
            return list(self.strategies.keys())[0]

        raise ValueError("No strategies registered")


# Global blog engine instance
blog_engine = BlogEngine()


def get_blog_engine() -> BlogEngine:
    """Get the global blog engine instance.

    Returns:
        BlogEngine instance.
    """
    return blog_engine