"""Multi-provider LLM client for Tia N. List project.

This module provides a unified interface for interacting with multiple LLM providers
including Gemini, OpenAI, and OpenRouter. It maintains backward compatibility with
the existing LLM client while adding provider selection and fallback capabilities.
"""

import os
import logging
from typing import Dict, Any, List, Optional, Union
from .providers import create_provider, get_available_providers
from .llm_provider import BaseLLMProvider, LLMProviderError, LLMProviderUnavailableError

logger = logging.getLogger(__name__)


class MultiLLMClient:
    """Multi-provider LLM client with fallback support.

    Supports provider selection via environment variables and automatic fallback
    if primary provider is unavailable.
    """

    def __init__(self, provider_name: Optional[str] = None, fallback_providers: Optional[List[str]] = None):
        """Initialize multi-provider LLM client.

        Args:
            provider_name: Primary provider to use. If None, uses LLM_PROVIDER env var.
            fallback_providers: List of fallback providers to try if primary fails.
                              If None, tries all available providers.
        """
        # Determine primary provider
        self.provider_name = provider_name or os.getenv('LLM_PROVIDER', 'gemini')
        self.fallback_providers = fallback_providers or [
            p for p in get_available_providers() if p != self.provider_name
        ]

        # Initialize providers
        self.provider = None
        self.fallback_provider = None

        self._initialize_providers()

    def _initialize_providers(self) -> None:
        """Initialize primary and fallback providers."""
        # Initialize primary provider
        try:
            config = self._get_provider_config(self.provider_name)
            self.provider = create_provider(self.provider_name, config)
            self.provider.initialize()
            logger.info(f"Successfully initialized primary provider: {self.provider_name}")
        except Exception as e:
            logger.error(f"Failed to initialize primary provider '{self.provider_name}': {e}")
            self._try_fallback_providers()

        # Initialize first available fallback provider
        if self.fallback_providers and not self.fallback_provider:
            for fallback_name in self.fallback_providers:
                try:
                    config = self._get_provider_config(fallback_name)
                    self.fallback_provider = create_provider(fallback_name, config)
                    self.fallback_provider.initialize()
                    logger.info(f"Successfully initialized fallback provider: {fallback_name}")
                    break
                except Exception as e:
                    logger.debug(f"Fallback provider '{fallback_name}' failed: {e}")

    def _try_fallback_providers(self) -> None:
        """Try to initialize fallback providers if primary fails."""
        logger.info("Trying fallback providers...")
        for fallback_name in self.fallback_providers:
            try:
                config = self._get_provider_config(fallback_name)
                provider = create_provider(fallback_name, config)
                provider.initialize()
                self.provider = provider
                self.provider_name = fallback_name
                logger.warning(f"Using fallback provider '{fallback_name}' as primary")
                return
            except Exception as e:
                logger.debug(f"Fallback provider '{fallback_name}' failed: {e}")

        raise LLMProviderUnavailableError("No LLM providers are available")

    def _get_provider_config(self, provider_name: str) -> Dict[str, Any]:
        """Get configuration for a specific provider.

        Args:
            provider_name: Name of the provider.

        Returns:
            Provider configuration dictionary.
        """
        provider_name = provider_name.lower()
        config = {'name': provider_name}

        if provider_name == 'gemini':
            config.update({
                'api_key': os.getenv('GEMINI_API_KEY'),
                'filtering_model': os.getenv('GEMINI_FILTERING_MODEL', 'gemini-2.0-flash-lite'),
                'analysis_model': os.getenv('GEMINI_ANALYSIS_MODEL', 'gemini-2.5-flash'),
            })
        elif provider_name == 'openrouter':
            config.update({
                'api_key': os.getenv('OPENROUTER_API_KEY'),
                'filtering_model': os.getenv('OPENROUTER_FILTERING_MODEL', 'meta-llama/llama-3.3-8b-instruct:free'),
                'analysis_model': os.getenv('OPENROUTER_ANALYSIS_MODEL', 'openai/gpt-oss-20b:free'),
            })
        elif provider_name == 'openai':
            config.update({
                'api_key': os.getenv('OPENAI_API_KEY'),
                'filtering_model': os.getenv('OPENAI_FILTERING_MODEL', 'gpt-4o-mini'),
                'analysis_model': os.getenv('OPENAI_ANALYSIS_MODEL', 'gpt-4o-mini'),
            })

        # Common configuration
        config.update({
            'timeout': int(os.getenv('LLM_TIMEOUT', '60')),
            'max_retries': int(os.getenv('LLM_MAX_RETRIES', '3')),
            'retry_delay': float(os.getenv('LLM_RETRY_DELAY', '1.0')),
        })

        return config

    def _execute_with_fallback(self, method_name: str, *args, **kwargs):
        """Execute a method with fallback support.

        Args:
            method_name: Name of the method to execute.
            *args: Method arguments.
            **kwargs: Method keyword arguments.

        Returns:
            Method result.

        Raises:
            LLMProviderError: If all providers fail.
        """
        providers_to_try = [self.provider]
        if self.fallback_provider:
            providers_to_try.append(self.fallback_provider)

        last_error = None
        for provider in providers_to_try:
            if not provider:
                continue

            try:
                method = getattr(provider, method_name)
                result = method(*args, **kwargs)
                if provider != self.provider:
                    logger.info(f"Successfully used fallback provider '{provider.name}'")
                return result
            except Exception as e:
                last_error = e
                logger.warning(f"Provider '{provider.name}' failed: {e}")
                continue

        raise LLMProviderError(f"All providers failed. Last error: {last_error}")

    # Public interface methods (backward compatibility)
    def is_relevant_article(self, title: str, content: str) -> Dict[str, Any]:
        """Check if an article is relevant using filtering model.

        Args:
            title: Article title.
            content: Article content.

        Returns:
            Dictionary with relevance analysis including:
            - is_relevant (bool): Whether article is relevant
            - relevance_score (int): Score from 0-100
            - reasoning (str): Explanation of relevance
        """
        prompt = f"""
Analyze this cybersecurity article for relevance to threat intelligence professionals:

Title: {title}

Content: {content[:1500]}...

Provide a JSON response with:
{{
    "is_relevant": true/false,
    "relevance_score": 0-100,
    "reasoning": "brief explanation of relevance assessment"
}}

Focus on:
- Actionable threat intelligence
- New vulnerabilities, attacks, or threat actors
- Security best practices or incident response
- Infrastructure or IOCs that would be valuable to track

Score based on practical value to security professionals.
        """

        try:
            result = self._execute_with_fallback('generate_structured', prompt, {
                "type": "object",
                "properties": {
                    "is_relevant": {"type": "boolean"},
                    "relevance_score": {"type": "number", "minimum": 0, "maximum": 100},
                    "reasoning": {"type": "string"}
                },
                "required": ["is_relevant", "relevance_score", "reasoning"]
            })
            return result
        except Exception as e:
            logger.error(f"Error in relevance analysis: {e}")
            return {"is_relevant": False, "relevance_score": 0, "reasoning": f"Error: {e}"}

    def extract_iocs_and_ttps(self, title: str, content: str) -> Dict[str, Any]:
        """Extract IOCs and TTPs from article content.

        Args:
            title: Article title.
            content: Article content.

        Returns:
            Dictionary with extracted IOCs and TTPs.
        """
        prompt = f"""
Analyze this cybersecurity article and extract technical indicators and methodologies:

Title: {title}

Content: {content}

Please identify and categorize:
1. Technical indicators (domains, IPs, file hashes, URLs, email addresses)
2. Security methodologies and techniques described

Respond with JSON containing:
{{
    "iocs": [
        {{
            "type": "domain|ip_address|file_hash|email|url",
            "value": "specific indicator value",
            "confidence": "high|medium|low",
            "context": "where in the text this was found"
        }}
    ],
    "ttps": [
        {{
            "technique": "MITRE ATT&CK technique name",
            "tactic": "MITRE ATT&CK tactic name",
            "description": "how the technique was used",
            "confidence": "high|medium|low"
        }}
    ]
}}

Focus on factual information explicitly mentioned in the article such as:
- Network infrastructure details
- File identifiers and hashes
- Described security procedures
- Software tools and platforms
- Incident response activities

Only extract information that is directly stated in the provided text.
        """

        try:
            result = self._execute_with_fallback('generate_structured', prompt, {
                "type": "object",
                "properties": {
                    "iocs": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string"},
                                "value": {"type": "string"},
                                "confidence": {"type": "string"},
                                "context": {"type": "string"}
                            },
                            "required": ["type", "value", "confidence"]
                        }
                    },
                    "ttps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "technique": {"type": "string"},
                                "tactic": {"type": "string"},
                                "description": {"type": "string"},
                                "confidence": {"type": "string"}
                            },
                            "required": ["technique", "tactic", "description", "confidence"]
                        }
                    }
                },
                "required": ["iocs", "ttps"]
            })
            return result
        except Exception as e:
            logger.error(f"Error extracting IOCs/TTPs: {e}")
            return {"iocs": [], "ttps": []}

    def batch_filter_articles(self, articles: List[Dict[str, Any]], batch_size: int = 10) -> List[Dict[str, Any]]:
        """Filter multiple articles for relevance.

        Args:
            articles: List of article dictionaries.
            batch_size: Number of articles to process in each batch.

        Returns:
            List of analysis results for all articles.
        """
        results = []

        # Process articles in batches
        for i in range(0, len(articles), batch_size):
            batch = articles[i:i + batch_size]
            batch_prompts = []

            for article in batch:
                prompt = f"""
Analyze this cybersecurity article for relevance to threat intelligence professionals:

Title: {article['title']}

Content: {article.get('raw_content', '')[:1500]}...

Provide a JSON response with:
{{
    "article_id": {article['id']},
    "is_relevant": true/false,
    "relevance_score": 0-100,
    "reasoning": "brief explanation of relevance assessment"
}}

Focus on actionable threat intelligence, new threats, and practical security insights.
                """
                batch_prompts.append(prompt)

            try:
                # Generate responses for the batch
                responses = self._execute_with_fallback('batch_generate', batch_prompts)

                # Parse responses
                for j, response in enumerate(responses):
                    try:
                        import json
                        result = json.loads(response)
                        results.append(result)
                    except (json.JSONDecodeError, KeyError) as e:
                        # Fallback result if parsing fails
                        results.append({
                            "article_id": batch[j]['id'],
                            "is_relevant": False,
                            "relevance_score": 0,
                            "reasoning": f"Parse error: {e}"
                        })

            except Exception as e:
                logger.error(f"Error in batch processing: {e}")
                # Add fallback results for this batch
                for article in batch:
                    results.append({
                        "article_id": article['id'],
                        "is_relevant": False,
                        "relevance_score": 0,
                        "reasoning": f"Batch processing error: {e}"
                    })

        return results

    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about current provider configuration.

        Returns:
            Dictionary with provider information.
        """
        return {
            'primary_provider': self.provider_name,
            'primary_available': self.provider is not None,
            'fallback_provider': self.fallback_provider.name if self.fallback_provider else None,
            'fallback_available': self.fallback_provider is not None,
            'available_providers': get_available_providers()
        }