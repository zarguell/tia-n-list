"""OpenAI-compatible provider implementation.

This module implements support for OpenAI-compatible APIs including OpenRouter
and other providers using the OpenAI API format.
"""

import json
import re
import time
import logging
from typing import Dict, Any, List, Optional
from ..llm_provider import BaseLLMProvider, LLMProviderAPIError, LLMProviderSafetyError
from ..response_parser import parse_llm_response, ParsedResponse

logger = logging.getLogger(__name__)

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI package not installed. OpenAI-compatible providers will not be available.")


class OpenAIProvider(BaseLLMProvider):
    """OpenAI-compatible provider implementation.

    Supports OpenAI API, OpenRouter, and other OpenAI-compatible endpoints.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize OpenAI provider.

        Args:
            config: Configuration dictionary with:
                - api_key: API key
                - base_url: API base URL (optional, defaults to OpenAI)
                - model: Model name for general generation
                - filtering_model: Model for relevance filtering
                - analysis_model: Model for deep analysis
                - timeout: Request timeout in seconds
                - max_retries: Maximum retry attempts
                - retry_delay: Base delay for retries
        """
        super().__init__(config)

        self.api_key = config.get('api_key')
        self.base_url = config.get('base_url', 'https://api.openai.com/v1')

        # Set default models based on provider (OpenRouter vs OpenAI)
        if 'openrouter' in self.base_url:
            self.model = config.get('model', 'openai/gpt-oss-20b:free')
            self.filtering_model = config.get('filtering_model', 'meta-llama/llama-3.3-8b-instruct:free')
            self.analysis_model = config.get('analysis_model', 'openai/gpt-oss-20b:free')
        else:
            # OpenAI or other providers
            self.model = config.get('model', 'openai/gpt-oss-20b:free')
            self.filtering_model = config.get('filtering_model', self.model)
            self.analysis_model = config.get('analysis_model', self.model)
        self.timeout = config.get('timeout', 60)
        self.max_retries = config.get('max_retries', 3)
        self.retry_delay = config.get('retry_delay', 1.0)

        self.client = None

    def initialize(self) -> None:
        """Initialize OpenAI client."""
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed. Install with: pip install openai")

        if not self.api_key:
            raise ValueError("API key is required for OpenAI provider")

        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout
        )

        # Test connection
        try:
            models = self.client.models.list()
            logger.debug(f"Connected to OpenAI-compatible API at {self.base_url}")
        except Exception as e:
            raise LLMProviderAPIError(f"Failed to connect to OpenAI API: {e}")

    def generate_text(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate text response from a prompt.

        Args:
            prompt: Input prompt for generation.
            max_tokens: Maximum tokens in response.
            temperature: Sampling temperature (0.0-1.0).

        Returns:
            Generated text response.
        """
        return self._retry_with_backoff(
            lambda: self._generate_with_model(self.model, prompt, max_tokens, temperature)
        )

    def generate_structured(self, prompt: str, schema: Dict[str, Any], max_tokens: int = 4000) -> Dict[str, Any]:
        """Generate structured data (JSON) response from a prompt with robust parsing.

        Args:
            prompt: Input prompt for generation.
            schema: JSON schema for expected output structure.
            max_tokens: Maximum tokens in response.

        Returns:
            Parsed structured data matching the schema (with fallbacks for imperfect responses).
        """
        enhanced_prompt = f"""
{prompt}

Please respond with valid JSON that matches this schema:
{json.dumps(schema, indent=2)}

Only return the JSON response, no additional text.
        """

        response_text = self._retry_with_backoff(
            lambda: self._generate_with_model(self.analysis_model, enhanced_prompt, max_tokens, 0.1)
        )

        # Use robust parsing to handle imperfect responses
        parsed_response = parse_llm_response(response_text, schema)

        if parsed_response.success:
            # Log the parsing method and confidence
            if parsed_response.confidence < 1.0:
                logger.info(f"Used {parsed_response.parsing_method} parser (confidence: {parsed_response.confidence:.2f})")
                if parsed_response.warnings:
                    logger.debug(f"Parsing warnings: {parsed_response.warnings}")

            # Ensure we have the expected structure with fallbacks
            result = parsed_response.data

            # Ensure required fields exist with reasonable defaults
            if 'iocs' not in result:
                result['iocs'] = []
            if 'ttps' not in result:
                result['ttps'] = []

            # Add metadata about parsing
            result['_parsing'] = {
                'method': parsed_response.parsing_method,
                'confidence': parsed_response.confidence,
                'warnings': parsed_response.warnings
            }

            return result
        else:
            # All parsing failed - return fallback structure
            logger.warning(f"All parsing methods failed: {parsed_response.warnings}")
            logger.debug(f"Raw response: {response_text[:200]}...")

            # Try to extract any useful information from the raw text
            fallback_result = {
                "iocs": [],
                "ttps": [],
                "_parsing": {
                    "method": "fallback",
                    "confidence": 0.0,
                    "warnings": parsed_response.warnings,
                    "raw_response": response_text[:500] if response_text else ""
                }
            }

            # Basic text analysis for fallback
            if response_text:
                # Look for any security-related content
                security_keywords = ['vulnerability', 'exploit', 'malware', 'threat', 'attack']
                found_keywords = [kw for kw in security_keywords if kw.lower() in response_text.lower()]
                if found_keywords:
                    fallback_result['_parsing']['found_keywords'] = found_keywords
                    fallback_result['_parsing']['has_security_content'] = True

            return fallback_result

    def batch_generate(self, prompts: List[str], max_tokens: int = 1000) -> List[str]:
        """Generate responses for multiple prompts in a single call.

        Args:
            prompts: List of input prompts.
            max_tokens: Maximum tokens per response.

        Returns:
            List of generated text responses.
        """
        responses = []
        for prompt in prompts:
            try:
                response = self.generate_text(prompt, max_tokens=max_tokens)
                responses.append(response)
            except Exception as e:
                logger.error(f"Error generating response for prompt: {e}")
                responses.append("")  # Empty response for failed generation
        return responses

    def _generate_with_model(self, model: str, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate text using a specific model.

        Args:
            model: Model name to use.
            prompt: Input prompt.
            max_tokens: Maximum tokens in response.
            temperature: Sampling temperature.

        Returns:
            Generated text response.
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful cybersecurity analyst."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise LLMProviderAPIError(f"OpenAI API error: {e}")

    def _generate_with_fallbacks(self, model: str, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate text using model with OpenRouter fallback support.

        Args:
            model: Primary model name to use.
            prompt: Input prompt.
            max_tokens: Maximum tokens in response.
            temperature: Sampling temperature.

        Returns:
            Generated text response.
        """
        fallback_models = getattr(self, 'fallback_models', [])
        all_models = [model] + fallback_models

        last_error = None

        for attempt, current_model in enumerate(all_models):
            try:
                if self.name == 'OpenRouter' and len(all_models) > 1:
                    # Use OpenRouter's fallback mechanism
                    response = self.client.chat.completions.create(
                        model=current_model,
                        models=all_models,  # OpenRouter fallback list
                        messages=[
                            {"role": "system", "content": "You are a helpful cybersecurity analyst."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                else:
                    # Standard single model call
                    response = self.client.chat.completions.create(
                        model=current_model,
                        messages=[
                            {"role": "system", "content": "You are a helpful cybersecurity analyst."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=max_tokens,
                        temperature=temperature
                    )

                result = response.choices[0].message.content.strip()

                # Log successful fallback usage
                if attempt > 0:
                    logger.info(f"Successfully used fallback model {current_model} after {attempt} attempts")

                return result

            except Exception as e:
                last_error = e
                logger.warning(f"Model {current_model} failed (attempt {attempt + 1}/{len(all_models)}): {e}")

                # If this is the last attempt, will raise the last error below
                continue

        # All models failed
        raise LLMProviderAPIError(f"All models failed. Last error: {last_error}")

    def _retry_with_backoff(self, func, max_retries: Optional[int] = None):
        """Retry function with exponential backoff.

        Args:
            func: Function to retry.
            max_retries: Maximum retry attempts (uses instance default if None).

        Returns:
            Function result.

        Raises:
            LLMProviderAPIError: If all retries fail.
        """
        if max_retries is None:
            max_retries = self.max_retries

        for attempt in range(max_retries + 1):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries:
                    raise LLMProviderAPIError(f"Failed after {max_retries} retries: {e}")

                delay = self.retry_delay * (2 ** attempt)
                logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {e}")
                time.sleep(delay)


class OpenRouterProvider(OpenAIProvider):
    """OpenRouter-specific provider implementation.

    Extends OpenAI provider with OpenRouter-specific features and configurations.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize OpenRouter provider.

        Args:
            config: Configuration dictionary. Uses OpenRouter defaults:
                - base_url: https://openrouter.ai/api/v1
                - filtering_model: meta-llama/llama-3.3-8b-instruct:free
                - analysis_model: openai/gpt-oss-20b:free
                - fallback_models: List of fallback models for robustness
        """
        # Set OpenRouter defaults with fallback models
        # Only set defaults if not provided in config to avoid overriding
        openrouter_config = {
            'base_url': 'https://openrouter.ai/api/v1',
            'fallback_models': [
                'z-ai/glm-4.5-air:free',        # Primary fallback
                'qwen/qwen3-235b-a22b:free',     # 1st fallback
                'microsoft/mai-ds-r1:free',      # 2nd fallback
                'google/gemini-2.0-flash-exp:free' # 3rd fallback
            ],
        }

        # Set default models only if not provided in config
        if 'model' not in config:
            openrouter_config['model'] = 'openai/gpt-oss-20b:free'
        if 'filtering_model' not in config:
            openrouter_config['filtering_model'] = 'meta-llama/llama-3.3-8b-instruct:free'
        if 'analysis_model' not in config:
            openrouter_config['analysis_model'] = 'openai/gpt-oss-20b:free'

        # Merge with provided config (config takes precedence)
        openrouter_config.update(config)

        super().__init__(openrouter_config)
        self.name = 'OpenRouter'
        self._last_request_time = 0

    def initialize(self) -> None:
        """Initialize OpenRouter client with custom headers."""
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed. Install with: pip install openai")

        if not self.api_key:
            raise ValueError("OpenRouter API key is required")

        # OpenRouter requires app name in headers
        default_headers = {
            "HTTP-Referer": "https://github.com/your-repo/tia-n-list",
            "X-Title": "Tia N. List - Threat Intelligence Aggregator"
        }

        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
            default_headers=default_headers
        )

        # Test connection
        try:
            models = self.client.models.list()
            logger.debug(f"Connected to OpenRouter API")
        except Exception as e:
            raise LLMProviderAPIError(f"Failed to connect to OpenRouter: {e}")

    def _generate_with_model(self, model: str, prompt: str, max_tokens: int, temperature: float) -> str:
        """Override to use fallback models for OpenRouter with proactive rate limiting.

        Args:
            model: Primary model name to use.
            prompt: Input prompt.
            max_tokens: Maximum tokens in response.
            temperature: Sampling temperature.

        Returns:
            Generated text response.
        """
        # Proactive throttling for OpenRouter free tier (20 requests/minute = 3 seconds between requests)
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time

        if time_since_last_request < 3.0:  # 3 second minimum between requests
            sleep_time = 3.0 - time_since_last_request
            logger.debug(f"OpenRouter rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)

        self._last_request_time = time.time()
        return self._generate_with_fallbacks(model, prompt, max_tokens, temperature)

    def _retry_with_backoff(self, func, max_retries: Optional[int] = None):
        """Retry function with exponential backoff and OpenRouter rate limiting.

        Args:
            func: Function to retry.
            max_retries: Maximum retry attempts (uses instance default if None).

        Returns:
            Function result.

        Raises:
            LLMProviderAPIError: If all retries fail.
        """
        if max_retries is None:
            max_retries = self.max_retries

        for attempt in range(max_retries + 1):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries:
                    raise LLMProviderAPIError(f"Failed after {max_retries} retries: {e}")

                # Check for OpenRouter rate limiting (HTTP 429)
                error_str = str(e).lower()
                if '429' in error_str or 'rate limit' in error_str:
                    # OpenRouter free tier: 20 requests/minute
                    # Wait 65 seconds to ensure we're well within the limit
                    delay = 65
                    logger.warning(f"OpenRouter rate limit hit, waiting {delay}s for rate limit reset: {e}")
                    time.sleep(delay)
                else:
                    # Standard exponential backoff for other errors
                    delay = self.retry_delay * (2 ** attempt)
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {e}")
                    time.sleep(delay)

    def _clean_json_response(self, response_text: str) -> str:
        """Clean JSON response to handle common OpenRouter formatting issues.

        Args:
            response_text: Raw response text from LLM

        Returns:
            Cleaned JSON text ready for parsing
        """
        if not response_text:
            return "{}"

        # Remove common extra tokens from OpenRouter
        cleaned = response_text.strip()

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

    def _aggressive_json_clean(self, response_text: str) -> str:
        """More aggressive JSON cleaning for difficult cases.

        Args:
            response_text: Raw response text from LLM

        Returns:
            Cleaned JSON text ready for parsing
        """
        if not response_text:
            return "{}"

        cleaned = response_text.strip()

        # Extract JSON using regex for difficult cases
        json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if json_match:
            return json_match.group(0)

        # Try to find JSON-like structure
        brace_count = 0
        start_idx = -1

        for i, char in enumerate(cleaned):
            if char == '{':
                if brace_count == 0:
                    start_idx = i
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0 and start_idx != -1:
                    return cleaned[start_idx:i + 1]

        # Fallback - return empty JSON
        return "{}"