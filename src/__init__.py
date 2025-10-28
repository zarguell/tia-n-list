"""Tia N. List - Threat Intelligence Aggregator.

This package provides modules for ingesting, processing, and publishing
threat intelligence content.
"""

# Lazy imports - modules will be imported when accessed as src.database, etc.
import importlib
import sys

def __getattr__(name):
    """Lazy import modules when accessed."""
    if name in [
        "database", "ingestion", "llm_client", "llm_client_multi", "processing",
        "persona", "blog_generator", "newsletter_generator", "distribution"
    ]:
        module = importlib.import_module(f".{name}", __name__)
        sys.modules[f"{__name__}.{name}"] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "database",
    "ingestion",
    "llm_client",
    "llm_client_multi",
    "processing",
    "persona",
    "blog_generator",
    "newsletter_generator",
    "distribution",
]