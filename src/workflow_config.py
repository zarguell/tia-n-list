#!/usr/bin/env python3
"""
Workflow configuration management.
Provides centralized configuration for simple digest workflow.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


class WorkflowConfig:
    """Centralized workflow configuration."""

    def __init__(self, config_file: Path = None):
        """Initialize workflow configuration.

        Args:
            config_file: Path to configuration file. Defaults to config/workflow_config.json
        """
        if config_file is None:
            config_file = Path(__file__).parent.parent / "config" / "workflow_config.json"

        self.config_file = config_file
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Workflow config file not found: {self.config_file}")

        with open(self.config_file, 'r') as f:
            return json.load(f)

    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation.

        Args:
            key_path: Dot-separated path to configuration value
            default: Default value if key not found

        Returns:
            Configuration value or default

        Examples:
            config.get('workflow_settings.max_articles_per_feed')
            config.get('processing_settings.llm_provider')
        """
        keys = key_path.split('.')
        value = self._config

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def get_workflow_settings(self) -> Dict[str, Any]:
        """Get all workflow settings."""
        return self.get('workflow_settings', {})

    def get_processing_settings(self) -> Dict[str, Any]:
        """Get all processing settings."""
        return self.get('processing_settings', {})

    def get_digest_settings(self) -> Dict[str, Any]:
        """Get all digest settings."""
        return self.get('digest_settings', {})

    def get_git_settings(self) -> Dict[str, Any]:
        """Get all git settings."""
        return self.get('git_settings', {})

    def reload(self) -> None:
        """Reload configuration from file."""
        self._config = self._load_config()

    def apply_environment_overrides(self) -> None:
        """Apply environment variable overrides to configuration."""
        import logging
        logger = logging.getLogger(__name__)

        self._apply_string_overrides(logger)
        self._apply_integer_overrides(logger)

    def _apply_string_overrides(self, logger) -> None:
        """Apply string-based environment variable overrides."""
        string_mappings = [
            ('LLM_PROVIDER', 'processing_settings.llm_provider'),
            ('OPENROUTER_FILTERING_MODEL', 'processing_settings.filtering_model'),
            ('OPENROUTER_ANALYSIS_MODEL', 'processing_settings.analysis_model'),
            ('STORAGE_PROVIDER', 'processing_settings.storage_provider'),
        ]

        for env_var, config_path in string_mappings:
            value = os.getenv(env_var)
            if value:
                self._set_nested_value(config_path, value)
                logger.info(f"Override: {env_var}={value}")

    def _apply_integer_overrides(self, logger) -> None:
        """Apply integer-based environment variable overrides with validation."""
        integer_mappings = [
            ('SIMPLE_DIGEST_MAX_ARTICLES', 'digest_settings.max_articles_for_prompt', 'positive'),
            ('SIMPLE_DIGEST_MAX_CONTENT_LENGTH', 'digest_settings.max_content_length', 'positive'),
            ('SIMPLE_DIGEST_MAX_REFERENCES', 'digest_settings.max_references', 'positive'),
            ('SIMPLE_DIGEST_MAX_TOKENS', 'digest_settings.max_tokens', 'positive'),
            ('SIMPLE_DIGEST_MEMORY_DAYS_BACK', 'workflow_settings.memory_days_back', 'positive'),
            ('SIMPLE_DIGEST_MEMORY_CLEANUP_DAYS', 'workflow_settings.memory_cleanup_days', 'positive'),
            ('WORKFLOW_MAX_ARTICLES_PER_FEED', 'workflow_settings.max_articles_per_feed', 'positive'),
            ('WORKFLOW_MIN_CONTENT_LENGTH', 'workflow_settings.min_content_length', 'non-negative'),
        ]

        for env_var, config_path, validation_type in integer_mappings:
            value = os.getenv(env_var)
            if value:
                self._apply_integer_override(env_var, config_path, value, validation_type, logger)

    def _apply_integer_override(self, env_var: str, config_path: str, value: str,
                               validation_type: str, logger) -> None:
        """Apply a single integer override with validation."""
        try:
            int_value = int(value)
            if not self._validate_integer_value(int_value, validation_type):
                logger.warning(f"Invalid {env_var}={int_value}, must be {validation_type}")
                return

            self._set_nested_value(config_path, int_value)
            config_key = config_path.split('.')[-1]
            logger.info(f"Override: {config_key}={int_value}")
        except ValueError as e:
            logger.warning(f"Invalid {env_var} value: {e}")

    def _validate_integer_value(self, value: int, validation_type: str) -> bool:
        """Validate integer value based on validation type."""
        if validation_type == 'positive':
            return value > 0
        elif validation_type == 'non-negative':
            return value >= 0
        return True

    def _set_nested_value(self, key_path: str, value) -> None:
        """Set a nested configuration value using dot notation."""
        keys = key_path.split('.')
        config = self._config

        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        # Set the final value
        config[keys[-1]] = value

    def __str__(self) -> str:
        """String representation of configuration."""
        return json.dumps(self._config, indent=2)


# Global configuration instance
_workflow_config = None


def get_workflow_config(config_file: Path = None) -> WorkflowConfig:
    """Get global workflow configuration instance.

    Args:
        config_file: Path to configuration file

    Returns:
        WorkflowConfig instance
    """
    global _workflow_config
    if _workflow_config is None:
        _workflow_config = WorkflowConfig(config_file)
        _workflow_config.apply_environment_overrides()
    return _workflow_config


def reload_workflow_config() -> None:
    """Reload the global workflow configuration."""
    global _workflow_config
    if _workflow_config is not None:
        _workflow_config.reload()
        _workflow_config.apply_environment_overrides()