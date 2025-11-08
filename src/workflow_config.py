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

        # LLM Provider
        if os.getenv('LLM_PROVIDER'):
            self._config['processing_settings']['llm_provider'] = os.getenv('LLM_PROVIDER')
            logger.info(f"Override: LLM_PROVIDER={os.getenv('LLM_PROVIDER')}")

        # LLM Models
        if os.getenv('OPENROUTER_FILTERING_MODEL'):
            self._config['processing_settings']['filtering_model'] = os.getenv('OPENROUTER_FILTERING_MODEL')
            logger.info(f"Override: OPENROUTER_FILTERING_MODEL={os.getenv('OPENROUTER_FILTERING_MODEL')}")

        if os.getenv('OPENROUTER_ANALYSIS_MODEL'):
            self._config['processing_settings']['analysis_model'] = os.getenv('OPENROUTER_ANALYSIS_MODEL')
            logger.info(f"Override: OPENROUTER_ANALYSIS_MODEL={os.getenv('OPENROUTER_ANALYSIS_MODEL')}")

        # Storage Provider
        if os.getenv('STORAGE_PROVIDER'):
            self._config['processing_settings']['storage_provider'] = os.getenv('STORAGE_PROVIDER')
            logger.info(f"Override: STORAGE_PROVIDER={os.getenv('STORAGE_PROVIDER')}")

        # Digest Settings
        if os.getenv('SIMPLE_DIGEST_MAX_ARTICLES'):
            try:
                value = int(os.getenv('SIMPLE_DIGEST_MAX_ARTICLES'))
                if value <= 0:
                    logger.warning(f"Invalid SIMPLE_DIGEST_MAX_ARTICLES={value}, must be positive")
                else:
                    self._config['digest_settings']['max_articles_for_prompt'] = value
                    logger.info(f"Override: max_articles_for_prompt={value}")
            except ValueError as e:
                logger.warning(f"Invalid SIMPLE_DIGEST_MAX_ARTICLES value: {e}")

        if os.getenv('SIMPLE_DIGEST_MAX_CONTENT_LENGTH'):
            try:
                value = int(os.getenv('SIMPLE_DIGEST_MAX_CONTENT_LENGTH'))
                if value <= 0:
                    logger.warning(f"Invalid SIMPLE_DIGEST_MAX_CONTENT_LENGTH={value}, must be positive")
                else:
                    self._config['digest_settings']['max_content_length'] = value
                    logger.info(f"Override: max_content_length={value}")
            except ValueError as e:
                logger.warning(f"Invalid SIMPLE_DIGEST_MAX_CONTENT_LENGTH value: {e}")

        if os.getenv('SIMPLE_DIGEST_MAX_REFERENCES'):
            try:
                value = int(os.getenv('SIMPLE_DIGEST_MAX_REFERENCES'))
                if value <= 0:
                    logger.warning(f"Invalid SIMPLE_DIGEST_MAX_REFERENCES={value}, must be positive")
                else:
                    self._config['digest_settings']['max_references'] = value
                    logger.info(f"Override: max_references={value}")
            except ValueError as e:
                logger.warning(f"Invalid SIMPLE_DIGEST_MAX_REFERENCES value: {e}")

        if os.getenv('SIMPLE_DIGEST_MAX_TOKENS'):
            try:
                value = int(os.getenv('SIMPLE_DIGEST_MAX_TOKENS'))
                if value <= 0:
                    logger.warning(f"Invalid SIMPLE_DIGEST_MAX_TOKENS={value}, must be positive")
                else:
                    self._config['digest_settings']['max_tokens'] = value
                    logger.info(f"Override: max_tokens={value}")
            except ValueError as e:
                logger.warning(f"Invalid SIMPLE_DIGEST_MAX_TOKENS value: {e}")

        # Memory Settings
        if os.getenv('SIMPLE_DIGEST_MEMORY_DAYS_BACK'):
            try:
                value = int(os.getenv('SIMPLE_DIGEST_MEMORY_DAYS_BACK'))
                if value <= 0:
                    logger.warning(f"Invalid SIMPLE_DIGEST_MEMORY_DAYS_BACK={value}, must be positive")
                else:
                    self._config['workflow_settings']['memory_days_back'] = value
                    logger.info(f"Override: memory_days_back={value}")
            except ValueError as e:
                logger.warning(f"Invalid SIMPLE_DIGEST_MEMORY_DAYS_BACK value: {e}")

        if os.getenv('SIMPLE_DIGEST_MEMORY_CLEANUP_DAYS'):
            try:
                value = int(os.getenv('SIMPLE_DIGEST_MEMORY_CLEANUP_DAYS'))
                if value <= 0:
                    logger.warning(f"Invalid SIMPLE_DIGEST_MEMORY_CLEANUP_DAYS={value}, must be positive")
                else:
                    self._config['workflow_settings']['memory_cleanup_days'] = value
                    logger.info(f"Override: memory_cleanup_days={value}")
            except ValueError as e:
                logger.warning(f"Invalid SIMPLE_DIGEST_MEMORY_CLEANUP_DAYS value: {e}")

        # Workflow Settings
        if os.getenv('WORKFLOW_MAX_ARTICLES_PER_FEED'):
            try:
                value = int(os.getenv('WORKFLOW_MAX_ARTICLES_PER_FEED'))
                if value <= 0:
                    logger.warning(f"Invalid WORKFLOW_MAX_ARTICLES_PER_FEED={value}, must be positive")
                else:
                    self._config['workflow_settings']['max_articles_per_feed'] = value
                    logger.info(f"Override: max_articles_per_feed={value}")
            except ValueError as e:
                logger.warning(f"Invalid WORKFLOW_MAX_ARTICLES_PER_FEED value: {e}")

        if os.getenv('WORKFLOW_MIN_CONTENT_LENGTH'):
            try:
                value = int(os.getenv('WORKFLOW_MIN_CONTENT_LENGTH'))
                if value < 0:
                    logger.warning(f"Invalid WORKFLOW_MIN_CONTENT_LENGTH={value}, must be non-negative")
                else:
                    self._config['workflow_settings']['min_content_length'] = value
                    logger.info(f"Override: min_content_length={value}")
            except ValueError as e:
                logger.warning(f"Invalid WORKFLOW_MIN_CONTENT_LENGTH value: {e}")

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