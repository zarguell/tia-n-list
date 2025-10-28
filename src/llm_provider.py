"""LLM Provider module for Tia N. List project.

This module provides abstract interfaces for LLM providers, supporting multiple
API styles including Gemini, OpenAI-compatible APIs, and OpenRouter.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
import logging

logger = logging.getLogger(__name__)


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the provider with configuration.

        Args:
            config: Provider-specific configuration dictionary.
        """
        self.config = config
        self.name = config.get('name', self.__class__.__name__)

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the provider (API client, authentication, etc.)."""
        pass

    @abstractmethod
    def generate_text(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate text response from a prompt.

        Args:
            prompt: Input prompt for generation.
            max_tokens: Maximum tokens in response.
            temperature: Sampling temperature (0.0-1.0).

        Returns:
            Generated text response.
        """
        pass

    @abstractmethod
    def generate_structured(self, prompt: str, schema: Dict[str, Any], max_tokens: int = 4000) -> Dict[str, Any]:
        """Generate structured data (JSON) response from a prompt.

        Args:
            prompt: Input prompt for generation.
            schema: JSON schema for expected output structure.
            max_tokens: Maximum tokens in response.

        Returns:
            Parsed structured data matching the schema.
        """
        pass

    @abstractmethod
    def batch_generate(self, prompts: List[str], max_tokens: int = 1000) -> List[str]:
        """Generate responses for multiple prompts in a single call.

        Args:
            prompts: List of input prompts.
            max_tokens: Maximum tokens per response.

        Returns:
            List of generated text responses.
        """
        pass

    def is_available(self) -> bool:
        """Check if the provider is available and properly configured.

        Returns:
            True if provider is available, False otherwise.
        """
        try:
            self.initialize()
            return True
        except Exception as e:
            logger.error(f"Provider {self.name} not available: {e}")
            return False


class LLMProviderError(Exception):
    """Base exception for LLM provider errors."""
    pass


class LLMProviderUnavailableError(LLMProviderError):
    """Raised when provider is not available or misconfigured."""
    pass


class LLMProviderAPIError(LLMProviderError):
    """Raised when provider API call fails."""
    pass


class LLMProviderSafetyError(LLMProviderError):
    """Raised when provider blocks content due to safety policies."""
    pass