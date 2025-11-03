"""Tia N. List - Threat Intelligence Aggregator.

This package provides modules for ingesting, processing, and publishing
threat intelligence content.
"""

# Lazy imports - modules will be imported when accessed as src.module_name, etc.
import importlib
import sys

def __getattr__(name):
    """Lazy import modules when accessed."""
    if name in [
        "unified_ingestion", "unified_processing", "storage_provider",
        "storage_registry", "json_storage_provider", "sqlite_storage_provider",
        "blog_engine", "blog_engine_factory", "strategies",
        "persona", "newsletter_generator", "distribution",
        "context_builder", "title_generator", "tag_generator",
        "enhanced_json_blog_generator", "two_tier_blog_generator",
        "intelligent_blog_generator", "prompt_loader", "llm_registry",
        "threat_classifier", "source_quality", "content_fetcher",
        "optimized_prompt_generator"
    ]:
        module = importlib.import_module(f".{name}", __name__)
        sys.modules[f"{__name__}.{name}"] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "unified_ingestion",
    "unified_processing",
    "storage_provider",
    "storage_registry",
    "json_storage_provider",
    "sqlite_storage_provider",
    "blog_engine",
    "blog_engine_factory",
    "strategies",
    "persona",
    "newsletter_generator",
    "distribution",
    "context_builder",
    "title_generator",
    "tag_generator",
    "enhanced_json_blog_generator",
    "two_tier_blog_generator",
    "intelligent_blog_generator",
    "prompt_loader",
    "llm_registry",
    "threat_classifier",
    "source_quality",
    "content_fetcher",
    "optimized_prompt_generator",
]