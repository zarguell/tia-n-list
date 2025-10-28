"""Provider package for LLM implementations.

This package contains various LLM provider implementations that follow the
BaseLLMProvider interface.
"""

from ..llm_provider import BaseLLMProvider, LLMProviderError
from .openai_provider import OpenAIProvider, OpenRouterProvider
from .gemini_provider import GeminiProvider

# Provider registry - maps provider names to provider classes
PROVIDER_REGISTRY = {
    'openai': OpenAIProvider,
    'openrouter': OpenRouterProvider,
    'gemini': GeminiProvider,
}

def create_provider(provider_name: str, config: dict) -> BaseLLMProvider:
    """Create a provider instance.

    Args:
        provider_name: Name of the provider (openai, openrouter, gemini).
        config: Provider configuration dictionary.

    Returns:
        Provider instance.

    Raises:
        ValueError: If provider name is not supported.
    """
    provider_name = provider_name.lower()
    if provider_name not in PROVIDER_REGISTRY:
        available = ', '.join(PROVIDER_REGISTRY.keys())
        raise ValueError(f"Unsupported provider '{provider_name}'. Available providers: {available}")

    provider_class = PROVIDER_REGISTRY[provider_name]
    return provider_class(config)

def get_available_providers() -> list[str]:
    """Get list of available provider names.

    Returns:
        List of supported provider names.
    """
    return list(PROVIDER_REGISTRY.keys())