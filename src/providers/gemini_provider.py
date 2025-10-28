"""Gemini provider implementation.

This module implements support for Google Gemini API as a provider,
maintaining compatibility with existing Gemini functionality.
"""

import json
import time
import logging
from typing import Dict, Any, List, Optional
from ..llm_provider import BaseLLMProvider, LLMProviderAPIError, LLMProviderSafetyError

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("Google Generative AI package not installed. Gemini provider will not be available.")


class GeminiProvider(BaseLLMProvider):
    """Gemini provider implementation.

    Maintains existing Gemini functionality while implementing the provider interface.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize Gemini provider.

        Args:
            config: Configuration dictionary with:
                - api_key: Gemini API key
                - filtering_model: Model for relevance filtering (default: gemini-2.0-flash-lite)
                - analysis_model: Model for deep analysis (default: gemini-2.5-flash)
                - timeout: Request timeout in seconds
                - max_retries: Maximum retry attempts
                - retry_delay: Base delay for retries
        """
        super().__init__(config)

        self.api_key = config.get('api_key')
        self.filtering_model_name = config.get('filtering_model', 'gemini-2.0-flash-lite')
        self.analysis_model_name = config.get('analysis_model', 'gemini-2.5-flash')
        self.timeout = config.get('timeout', 120)
        self.max_retries = config.get('max_retries', 5)
        self.retry_delay = config.get('retry_delay', 1.0)

        # Safety settings (less restrictive for cybersecurity content)
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        self.filtering_model = None
        self.analysis_model = None

    def initialize(self) -> None:
        """Initialize Gemini models."""
        if not GEMINI_AVAILABLE:
            raise ImportError("Google Generative AI package not installed. Install with: pip install google-generativeai")

        if not self.api_key:
            raise ValueError("Gemini API key is required")

        genai.configure(api_key=self.api_key)

        # Initialize models
        self.filtering_model = genai.GenerativeModel(self.filtering_model_name)
        self.analysis_model = genai.GenerativeModel(self.analysis_model_name)

        logger.debug(f"Initialized Gemini models: {self.filtering_model_name}, {self.analysis_model_name}")

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
            lambda: self._generate_with_model(self.analysis_model, prompt, max_tokens, temperature)
        )

    def generate_structured(self, prompt: str, schema: Dict[str, Any], max_tokens: int = 4000) -> Dict[str, Any]:
        """Generate structured data (JSON) response from a prompt.

        Args:
            prompt: Input prompt for generation.
            schema: JSON schema for expected output structure.
            max_tokens: Maximum tokens in response.

        Returns:
            Parsed structured data matching the schema.
        """
        enhanced_prompt = f"""
{prompt}

Please respond with valid JSON that matches this schema:
{json.dumps(schema, indent=2)}

Only return the JSON response, no additional text.
        """

        def _extract():
            response = self.analysis_model.generate_content(
                enhanced_prompt,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.1,  # Lower temperature for structured data
                    response_mime_type="application/json",
                ),
                safety_settings=self.safety_settings
            )

            # Check for safety filtering or other issues
            if response.candidates:
                candidate = response.candidates[0]
                if candidate.finish_reason == 2:  # SAFETY
                    logger.warning(f"Content was blocked by safety policies for prompt: {enhanced_prompt[:100]}...")
                    raise LLMProviderSafetyError("Content blocked by safety policies")
                elif candidate.finish_reason != 1:  # STOP
                    logger.warning(f"Content generation ended unexpectedly: finish_reason={candidate.finish_reason}")
                    raise LLMProviderAPIError(f"Generation ended unexpectedly: {candidate.finish_reason}")

            # Parse JSON response
            try:
                return json.loads(response.text)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {response.text[:200]}...")
                return {"iocs": [], "ttps": []}

        try:
            return self._retry_with_backoff(_extract)
        except LLMProviderSafetyError:
            # Return empty structure for safety errors
            return {"iocs": [], "ttps": []}

    def batch_generate(self, prompts: List[str], max_tokens: int = 1000) -> List[str]:
        """Generate responses for multiple prompts in a single call.

        For Gemini, this processes prompts individually since batch processing
        isn't natively supported in the same way as OpenAI.

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

    def _generate_with_model(self, model, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate text using a specific Gemini model.

        Args:
            model: Gemini model instance.
            prompt: Input prompt.
            max_tokens: Maximum tokens in response.
            temperature: Sampling temperature.

        Returns:
            Generated text response.
        """
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature,
                ),
                safety_settings=self.safety_settings
            )

            # Check for safety filtering
            if response.candidates:
                candidate = response.candidates[0]
                if candidate.finish_reason == 2:  # SAFETY
                    logger.warning(f"Content was blocked by safety policies for prompt: {prompt[:100]}...")
                    raise LLMProviderSafetyError("Content blocked by safety policies")
                elif candidate.finish_reason != 1:  # STOP
                    logger.warning(f"Content generation ended unexpectedly: finish_reason={candidate.finish_reason}")
                    raise LLMProviderAPIError(f"Generation ended unexpectedly: {candidate.finish_reason}")

            return response.text.strip()
        except Exception as e:
            if isinstance(e, (LLMProviderSafetyError, LLMProviderAPIError)):
                raise
            raise LLMProviderAPIError(f"Gemini API error: {e}")

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
                # Don't retry safety errors
                if isinstance(e, LLMProviderSafetyError):
                    raise

                if attempt == max_retries:
                    raise LLMProviderAPIError(f"Failed after {max_retries} retries: {e}")

                delay = self.retry_delay * (2 ** attempt)
                logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {e}")
                time.sleep(delay)