"""Blog engine factory for Tia N. List project.

This module provides a factory for creating blog engines with all strategies
automatically registered.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path

from .blog_engine import BlogEngine, TransformationStrategy
from .storage_provider import StorageProvider
from .storage_registry import get_default_storage_provider


class BlogEngineFactory:
    """Factory for creating blog engines with registered strategies."""

    def __init__(self):
        """Initialize the factory."""
        self._strategy_classes: List[type] = []

    def register_strategy_class(self, strategy_class: type) -> None:
        """Register a strategy class for automatic instantiation.

        Args:
            strategy_class: TransformationStrategy subclass.
        """
        if not issubclass(strategy_class, TransformationStrategy):
            raise ValueError(f"Strategy class {strategy_class} must inherit from TransformationStrategy")

        self._strategy_classes.append(strategy_class)

    def create_blog_engine(self, storage: StorageProvider = None,
                          output_dir: str = "hugo/content/posts") -> BlogEngine:
        """Create a blog engine with all registered strategies.

        Args:
            storage: Storage provider for the engine.
            output_dir: Output directory for blog posts.

        Returns:
            Configured BlogEngine instance.
        """
        engine = BlogEngine(storage, output_dir)

        # Register all strategy classes
        for strategy_class in self._strategy_classes:
            try:
                strategy = self._create_strategy_instance(strategy_class, storage)
                engine.register_strategy(strategy)
                print(f"✅ Registered strategy: {strategy.get_strategy_name()}")
            except Exception as e:
                print(f"⚠️  Failed to register strategy {strategy_class.__name__}: {e}")

        return engine

    def _create_strategy_instance(self, strategy_class: type,
                                storage: StorageProvider) -> TransformationStrategy:
        """Create an instance of a strategy class.

        Args:
            strategy_class: Strategy class to instantiate.
            storage: Storage provider to pass to strategy.

        Returns:
            Strategy instance.
        """
        # Try to create strategy with storage parameter
        try:
            return strategy_class(storage=storage)
        except TypeError:
            # Fallback: try without parameters
            return strategy_class()

    def get_available_strategies(self) -> List[str]:
        """Get list of available strategy class names.

        Returns:
            List of strategy class names.
        """
        return [cls.__name__ for cls in self._strategy_classes]

    def list_strategies(self) -> Dict[str, str]:
        """List all registered strategies with their descriptions.

        Returns:
            Dictionary mapping strategy names to descriptions.
        """
        strategies = {}
        for strategy_class in self._strategy_classes:
            try:
                # Create temporary instance to get info
                instance = self._create_strategy_instance(None)
                strategies[instance.get_strategy_name()] = instance.get_description()
            except Exception:
                strategies[strategy_class.__name__] = "Description unavailable"

        return strategies


# Global factory instance
_blog_engine_factory = BlogEngineFactory()


def register_builtin_strategies():
    """Register all built-in transformation strategies."""
    from .strategies import (
        EnhancedTransformationStrategy,
        TemplateTransformationStrategy
    )

    _blog_engine_factory.register_strategy_class(EnhancedTransformationStrategy)
    _blog_engine_factory.register_strategy_class(TemplateTransformationStrategy)


def create_blog_engine(storage: StorageProvider = None,
                      output_dir: str = "hugo/content/posts") -> BlogEngine:
    """Create a blog engine with all built-in strategies registered.

    Args:
        storage: Storage provider for the engine.
        output_dir: Output directory for blog posts.

    Returns:
        Configured BlogEngine instance.
    """
    # Register built-in strategies if not already done
    if not _blog_engine_factory.get_available_strategies():
        register_builtin_strategies()

    return _blog_engine_factory.create_blog_engine(storage, output_dir)


def get_blog_engine_factory() -> BlogEngineFactory:
    """Get the global blog engine factory.

    Returns:
        BlogEngineFactory instance.
    """
    return _blog_engine_factory


def list_available_strategies() -> Dict[str, str]:
    """List all available transformation strategies.

    Returns:
        Dictionary mapping strategy names to descriptions.
    """
    # Register built-in strategies if not already done
    if not _blog_engine_factory.get_available_strategies():
        register_builtin_strategies()

    return _blog_engine_factory.list_strategies()