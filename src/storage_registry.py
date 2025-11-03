"""Storage registry for Tia N. List project.

This module provides a registry for managing different storage providers,
allowing for dynamic selection and configuration of storage backends.
"""

import os
from typing import Dict, Any, Optional, Type
from pathlib import Path

from .storage_provider import StorageProvider
from .json_storage_provider import JSONStorageProvider
from .sqlite_storage_provider import SQLiteStorageProvider


class StorageRegistry:
    """Registry for managing storage providers."""

    def __init__(self):
        """Initialize the storage registry."""
        self._providers: Dict[str, Type[StorageProvider]] = {}
        self._instances: Dict[str, StorageProvider] = {}
        self._default_provider: Optional[str] = None

        # Register built-in providers
        self.register_provider("json", JSONStorageProvider)
        self.register_provider("sqlite", SQLiteStorageProvider)

        # Set default provider
        self._default_provider = "json"

    def register_provider(self, name: str, provider_class: Type[StorageProvider]) -> None:
        """Register a new storage provider.

        Args:
            name: Unique name for the provider.
            provider_class: StorageProvider subclass.
        """
        if not issubclass(provider_class, StorageProvider):
            raise ValueError(f"Provider class {provider_class} must inherit from StorageProvider")

        self._providers[name] = provider_class

    def get_provider(self, name: Optional[str] = None, **config) -> StorageProvider:
        """Get a storage provider instance.

        Args:
            name: Name of the provider to get. If None, uses default provider.
            **config: Configuration parameters for the provider.

        Returns:
            StorageProvider instance.
        """
        if name is None:
            name = self._get_default_provider_name()

        if name not in self._providers:
            raise ValueError(f"Unknown storage provider: {name}. Available: {list(self._providers.keys())}")

        # Create cache key based on name and config
        cache_key = f"{name}:{hash(tuple(sorted(config.items())))}"

        # Return cached instance if available
        if cache_key in self._instances:
            return self._instances[cache_key]

        # Create new instance
        provider_class = self._providers[name]
        provider = provider_class(**config)

        # Initialize the provider
        provider.initialize()

        # Cache the instance
        self._instances[cache_key] = provider

        return provider

    def _get_default_provider_name(self) -> str:
        """Get the default provider name from environment or configuration."""
        # Check environment variable first
        env_provider = os.getenv("STORAGE_PROVIDER")
        if env_provider and env_provider in self._providers:
            return env_provider

        # Use configured default
        return self._default_provider

    def list_providers(self) -> list[str]:
        """List all registered provider names."""
        return list(self._providers.keys())

    def set_default_provider(self, name: str) -> None:
        """Set the default provider.

        Args:
            name: Name of the provider to set as default.
        """
        if name not in self._providers:
            raise ValueError(f"Unknown storage provider: {name}. Available: {list(self._providers.keys())}")

        self._default_provider = name

    def get_provider_info(self, name: Optional[str] = None) -> Dict[str, Any]:
        """Get information about a provider.

        Args:
            name: Name of the provider. If None, returns info about default provider.

        Returns:
            Dictionary containing provider information.
        """
        if name is None:
            name = self._get_default_provider_name()

        if name not in self._providers:
            raise ValueError(f"Unknown storage provider: {name}")

        provider_class = self._providers[name]
        return {
            "name": name,
            "class": provider_class.__name__,
            "module": provider_class.__module__,
            "doc": provider_class.__doc__,
            "is_default": name == self._default_provider
        }

    def health_check_all(self) -> Dict[str, Any]:
        """Perform health checks on all registered providers.

        Returns:
            Dictionary mapping provider names to health check results.
        """
        results = {}

        for name in self._providers.keys():
            try:
                provider = self.get_provider(name)
                results[name] = provider.health_check()
            except Exception as e:
                results[name] = {
                    "status": "unhealthy",
                    "issues": [f"Failed to initialize provider: {e}"],
                    "checks": {}
                }

        return results

    def clear_cache(self) -> None:
        """Clear the provider instance cache."""
        self._instances.clear()


# Global storage registry instance
storage_registry = StorageRegistry()


def get_storage_provider(name: Optional[str] = None, **config) -> StorageProvider:
    """Convenience function to get a storage provider.

    Args:
        name: Name of the storage provider. If None, uses default from environment.
        **config: Configuration parameters for the provider.

    Returns:
        StorageProvider instance.
    """
    return storage_registry.get_provider(name, **config)


def get_default_storage_provider() -> StorageProvider:
    """Get the default storage provider.

    Returns:
        Default StorageProvider instance.
    """
    return storage_registry.get_provider()