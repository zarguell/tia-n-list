"""Multi-provider LLM client for Tia N. List project.

This module provides a unified interface for interacting with multiple LLM providers
including Gemini, OpenAI, and OpenRouter. It maintains backward compatibility with
the existing LLM client while adding provider selection and fallback capabilities.
"""

import os
import re
import logging
from typing import Dict, Any, List, Optional, Union
from .providers import create_provider, get_available_providers
from .llm_provider import BaseLLMProvider, LLMProviderError, LLMProviderUnavailableError
from .response_parser import parse_llm_response, extract_field_with_fallback

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

            # Log the actual models being used for debugging
            if hasattr(self.provider, 'model'):
                logger.info(f"Successfully initialized primary provider: {self.provider_name}")
                logger.info(f"Model: {getattr(self.provider, 'model', 'unknown')}")
                logger.info(f"Filtering model: {getattr(self.provider, 'filtering_model', 'unknown')}")
                logger.info(f"Analysis model: {getattr(self.provider, 'analysis_model', 'unknown')}")
                # Log the actual config for debugging
                if hasattr(self.provider, 'api_key'):
                    logger.info(f"Base URL: {getattr(self.provider, 'base_url', 'unknown')}")
            else:
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
                'model': os.getenv('OPENROUTER_MODEL', 'openai/gpt-oss-20b:free'),
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

                # Parse responses using robust parsing
                for j, response in enumerate(responses):
                    try:
                        # Use robust parsing to handle imperfect responses
                        parsed_response = parse_llm_response(response)

                        if parsed_response.success:
                            # Extract required fields with fallbacks
                            result = {
                                "article_id": batch[j]['id'],
                                "is_relevant": extract_field_with_fallback(parsed_response, 'is_relevant', False),
                                "relevance_score": extract_field_with_fallback(parsed_response, 'relevance_score', 0),
                                "reasoning": extract_field_with_fallback(parsed_response, 'reasoning', 'Processed with robust parsing'),
                                "_parsing": {
                                    "method": parsed_response.parsing_method,
                                    "confidence": parsed_response.confidence
                                }
                            }

                            # Convert string representations to proper types
                            if isinstance(result['is_relevant'], str):
                                result['is_relevant'] = result['is_relevant'].lower() in ['true', 'yes', '1']

                            try:
                                result['relevance_score'] = int(float(result['relevance_score']))
                            except (ValueError, TypeError):
                                result['relevance_score'] = 0

                            # Cap score to valid range
                            result['relevance_score'] = max(0, min(100, result['relevance_score']))

                            results.append(result)

                            # Log low confidence parses
                            if parsed_response.confidence < 0.8:
                                logger.debug(f"Low confidence parsing ({parsed_response.confidence:.2f}) for article {batch[j]['id']}")

                        else:
                            # Robust parsing failed - create fallback result
                            results.append({
                                "article_id": batch[j]['id'],
                                "is_relevant": False,
                                "relevance_score": 0,
                                "reasoning": f"Robust parsing failed: {parsed_response.warnings[0] if parsed_response.warnings else 'Unknown error'}",
                                "_parsing": {
                                    "method": "failed",
                                    "confidence": 0.0,
                                    "warnings": parsed_response.warnings
                                }
                            })

                    except Exception as e:
                        # Unexpected error - create fallback result
                        logger.error(f"Unexpected error parsing response for article {batch[j]['id']}: {e}")
                        results.append({
                            "article_id": batch[j]['id'],
                            "is_relevant": False,
                            "relevance_score": 0,
                            "reasoning": f"Processing error: {str(e)[:100]}",
                            "_parsing": {
                                "method": "error",
                                "confidence": 0.0
                            }
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

    def _clean_batch_response(self, response: str) -> str:
        """Clean JSON response for batch processing to handle OpenRouter formatting issues.

        Args:
            response: Raw response text from LLM

        Returns:
            Cleaned JSON text ready for parsing
        """
        if not response:
            return "{}"

        cleaned = response.strip()

        # Remove leading/trailing ```json and ```
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        # Remove extra tokens like <｜begin▁of▁sentence｜>
        cleaned = re.sub(r'<｜[^｜]+｜>', '', cleaned)
        cleaned = re.sub(r'<[^>]+>', '', cleaned)  # Remove any other XML-like tags

        # Remove trailing punctuation after JSON
        cleaned = re.sub(r'[^}]\s*$', '', cleaned)

        # Find JSON boundaries - look for first { and last }
        first_brace = cleaned.find('{')
        if first_brace == -1:
            return "{}"

        last_brace = cleaned.rfind('}')
        if last_brace == -1:
            return cleaned[first_brace:]

        return cleaned[first_brace:last_brace + 1]

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