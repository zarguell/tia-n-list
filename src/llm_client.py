"""LLM Client module for Tia N. List project.

This module provides a unified interface for interacting with Google Gemini API,
supporting both Flash Lite (for high-volume filtering) and Flash (for deep analysis).
Includes retry logic, configurable models, and proper logging.
"""

import os
import time
import logging
from typing import Dict, Any, Optional, Callable
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configure logging
logger = logging.getLogger(__name__)


class ModelConfig:
    """Configuration for Gemini models."""

    DEFAULT_FILTERING_MODEL = "gemini-2.0-flash-lite"
    DEFAULT_ANALYSIS_MODEL = "gemini-2.5-flash"

    def __init__(self,
                 filtering_model: Optional[str] = None,
                 analysis_model: Optional[str] = None):
        """Initialize model configuration.

        Args:
            filtering_model: Model name for high-volume filtering
            analysis_model: Model name for deep analysis
        """
        self.filtering_model = filtering_model or os.getenv('GEMINI_FILTERING_MODEL', self.DEFAULT_FILTERING_MODEL)
        self.analysis_model = analysis_model or os.getenv('GEMINI_ANALYSIS_MODEL', self.DEFAULT_ANALYSIS_MODEL)

        logger.info(f"Model config - Filtering: {self.filtering_model}, Analysis: {self.analysis_model}")


class RetryConfig:
    """Configuration for retry logic."""

    def __init__(self,
                 max_retries: int = 3,
                 base_delay: float = 1.0,
                 max_delay: float = 60.0,
                 backoff_factor: float = 2.0):
        """Initialize retry configuration.

        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Initial delay between retries in seconds
            max_delay: Maximum delay between retries in seconds
            backoff_factor: Multiplier for exponential backoff
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor


class LLMClient:
    """Client for interacting with Google Gemini API with retry logic and configurable models."""

    def __init__(self,
                 api_key: Optional[str] = None,
                 model_config: Optional[ModelConfig] = None,
                 retry_config: Optional[RetryConfig] = None):
        """Initialize the LLM client.

        Args:
            api_key: Google Gemini API key. If None, tries to get from environment.
            model_config: Model configuration. If None, uses defaults.
            retry_config: Retry configuration. If None, uses defaults.
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not provided. Set GEMINI_API_KEY environment variable.")

        # Configure generative AI
        genai.configure(api_key=self.api_key)

        # Set up configurations
        self.model_config = model_config or ModelConfig()
        self.retry_config = retry_config or RetryConfig()

        # Initialize models
        self.filtering_model = genai.GenerativeModel(self.model_config.filtering_model)
        self.analysis_model = genai.GenerativeModel(self.model_config.analysis_model)

        # Configure safety settings
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        logger.info(f"LLM Client initialized with models: {self.model_config.filtering_model}, {self.model_config.analysis_model}")

    def _retry_with_backoff(self, operation: Callable, *args, **kwargs) -> Any:
        """Execute operation with exponential backoff retry logic.

        Args:
            operation: Function to execute
            *args: Arguments to pass to operation
            **kwargs: Keyword arguments to pass to operation

        Returns:
            Result of operation execution

        Raises:
            Exception: If all retries are exhausted
        """
        last_exception = None

        for attempt in range(self.retry_config.max_retries + 1):
            try:
                if attempt > 0:
                    delay = min(
                        self.retry_config.base_delay * (self.retry_config.backoff_factor ** (attempt - 1)),
                        self.retry_config.max_delay
                    )
                    logger.info(f"Retry attempt {attempt}/{self.retry_config.max_retries} after {delay:.2f}s delay")
                    time.sleep(delay)

                result = operation(*args, **kwargs)
                if attempt > 0:
                    logger.info(f"Operation succeeded on attempt {attempt + 1}")
                return result

            except Exception as e:
                last_exception = e
                # Check if it's a rate limiting error (HTTP 429)
                is_rate_limit = "429" in str(e) or "rate limit" in str(e).lower()

                if attempt == self.retry_config.max_retries:
                    logger.error(f"All {self.retry_config.max_retries} retry attempts failed. Last error: {e}")
                    break

                if is_rate_limit:
                    logger.warning(f"Rate limit encountered on attempt {attempt + 1}: {e}")
                else:
                    logger.warning(f"Error on attempt {attempt + 1}: {e}")

        raise Exception(f"Operation failed after {self.retry_config.max_retries} retries: {last_exception}")

    def generate_with_filtering_model(self, prompt: str, max_output_tokens: int = 1000) -> str:
        """Generate response using filtering model (Flash Lite).

        Args:
            prompt: Input prompt for generation.
            max_output_tokens: Maximum tokens in response.

        Returns:
            Generated text response.
        """
        logger.debug(f"Generating response with filtering model, tokens: {max_output_tokens}")

        def _generate():
            response = self.filtering_model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=max_output_tokens,
                    temperature=0.1,  # Lower temperature for more consistent filtering
                ),
                safety_settings=self.safety_settings
            )
            return response.text

        try:
            return self._retry_with_backoff(_generate)
        except Exception as e:
            logger.error(f"Error generating with filtering model: {e}")
            raise Exception(f"Error generating with filtering model: {e}")

    def generate_with_analysis_model(self, prompt: str, max_output_tokens: int = 4000) -> str:
        """Generate response using analysis model (Flash).

        Args:
            prompt: Input prompt for generation.
            max_output_tokens: Maximum tokens in response.

        Returns:
            Generated text response.
        """
        logger.debug(f"Generating response with analysis model, tokens: {max_output_tokens}")

        def _generate():
            response = self.analysis_model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=max_output_tokens,
                    temperature=0.3,  # Higher temperature for more creative analysis
                ),
                safety_settings=self.safety_settings
            )
            return response.text

        try:
            return self._retry_with_backoff(_generate)
        except Exception as e:
            logger.error(f"Error generating with analysis model: {e}")
            raise Exception(f"Error generating with analysis model: {e}")

    def extract_structured_data(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Extract structured data using analysis model with JSON output.

        Args:
            prompt: Input prompt for extraction.
            schema: JSON schema for expected output structure.

        Returns:
            Parsed structured data.
        """
        logger.debug("Extracting structured data with analysis model")

        # Add JSON output instruction to prompt
        enhanced_prompt = f"""
{prompt}

Please respond with valid JSON that matches this schema:
{schema}

Only return the JSON response, no additional text.
        """

        def _extract():
            response = self.analysis_model.generate_content(
                enhanced_prompt,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=4000,
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
                    return {"iocs": [], "ttps": []}
                elif candidate.finish_reason != 1:  # STOP
                    logger.warning(f"Content generation ended unexpectedly: finish_reason={candidate.finish_reason}")
                    return {"iocs": [], "ttps": []}

            # Parse JSON response
            import json
            try:
                return json.loads(response.text)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {response.text[:200]}...")
                return {"iocs": [], "ttps": []}

        try:
            return self._retry_with_backoff(_extract)
        except Exception as e:
            logger.error(f"Error extracting structured data: {e}")
            raise Exception(f"Error extracting structured data: {e}")

    # Backward compatibility methods
    def generate_with_flash(self, prompt: str, max_output_tokens: int = 1000) -> str:
        """Backward compatibility method - uses filtering model."""
        return self.generate_with_filtering_model(prompt, max_output_tokens)

    def generate_with_pro(self, prompt: str, max_output_tokens: int = 4000) -> str:
        """Backward compatibility method - uses analysis model."""
        return self.generate_with_analysis_model(prompt, max_output_tokens)

    def batch_filter_articles(self, articles: list[Dict[str, Any]], batch_size: int = 10) -> list[Dict[str, Any]]:
        """Filter multiple articles for relevance in a single API call.

        Args:
            articles: List of article dictionaries with 'id', 'title', and 'raw_content'.
            batch_size: Number of articles to process in each batch.

        Returns:
            List of analysis results for all articles.
        """
        import json

        logger.info(f"Starting batch filtering of {len(articles)} articles in batches of {batch_size}")
        all_results = []

        # Process articles in batches
        for i in range(0, len(articles), batch_size):
            batch = articles[i:i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(articles) + batch_size - 1) // batch_size

            logger.debug(f"Processing batch {batch_num}/{total_batches} with {len(batch)} articles")

            # Create batch prompt
            articles_text = ""
            for j, article in enumerate(batch):
                articles_text += f"""
Article {j+1}:
ID: {article['id']}
Title: {article['title']}
Content: {(article['raw_content'] or "")[:1500]}...
"""

            prompt = f"""
Analyze the following {len(batch)} articles for threat intelligence relevance. For each article, determine if it's relevant and provide a relevance score and reasoning.

{articles_text}

Respond with JSON containing a list of analyses:
{{
    "analyses": [
        {{
            "article_id": <article ID>,
            "is_relevant": true/false,
            "relevance_score": 0-100,
            "reasoning": "Brief explanation of decision"
        }}
    ]
}}

Criteria for relevance:
- Cybersecurity threats, vulnerabilities, attacks, or incidents
- Malware analysis or discovery
- Nation-state cyber activity
- Critical infrastructure threats
- Data breaches affecting systems security

NOT relevant:
- General tech news without security impact
- Consumer privacy issues without technical details
- Marketing content
- General business news

Please ensure the article_id in your response matches the ID provided for each article.
"""

            def _process_batch():
                response = self.filtering_model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        max_output_tokens=8000,  # Increased for batch responses
                        temperature=0.1,
                        response_mime_type="application/json",
                    ),
                    safety_settings=self.safety_settings
                )

                # Parse JSON response
                result = json.loads(response.text)
                analyses = result.get('analyses', [])

                # Validate we got results for all articles
                if len(analyses) != len(batch):
                    logger.warning(f"Expected {len(batch)} results, got {len(analyses)}")

                return analyses

            try:
                analyses = self._retry_with_backoff(_process_batch)
                all_results.extend(analyses)
                logger.info(f"Successfully processed batch {batch_num}/{total_batches}: {len(analyses)} articles")

            except Exception as e:
                logger.error(f"Error processing batch {batch_num}/{total_batches}: {e}")
                # Add fallback results for this batch
                for article in batch:
                    all_results.append({
                        'article_id': article['id'],
                        'is_relevant': False,
                        'relevance_score': 0,
                        'reasoning': f'Batch processing failed: {str(e)}'
                    })

        logger.info(f"Batch filtering completed. Total results: {len(all_results)}")
        return all_results

    def is_relevant_article(self, title: str, content: str) -> Dict[str, Any]:
        """Determine if article is relevant for threat intelligence analysis.

        Args:
            title: Article title.
            content: Article content.

        Returns:
            Dictionary with relevance analysis.
        """
        logger.debug(f"Analyzing article relevance: '{title[:50]}...'")

        prompt = f"""
Analyze this article for threat intelligence relevance:

Title: {title}

Content: {content[:2000]}...

Respond with JSON containing:
{{
    "is_relevant": true/false,
    "relevance_score": 0-100,
    "reasoning": "Brief explanation of decision"
}}

Criteria for relevance:
- Cybersecurity threats, vulnerabilities, attacks, or incidents
- Malware analysis or discovery
- Nation-state cyber activity
- Critical infrastructure threats
- Data breaches affecting systems security

NOT relevant:
- General tech news without security impact
- Consumer privacy issues without technical details
- Marketing content
- General business news
"""

        return self.extract_structured_data(
            prompt,
            {
                "type": "object",
                "properties": {
                    "is_relevant": {"type": "boolean"},
                    "relevance_score": {"type": "integer", "minimum": 0, "maximum": 100},
                    "reasoning": {"type": "string"}
                },
                "required": ["is_relevant", "relevance_score", "reasoning"]
            }
        )

    def extract_iocs_and_ttps(self, title: str, content: str) -> Dict[str, Any]:
        """Extract IOCs and TTPs from article content.

        Args:
            title: Article title.
            content: Article content.

        Returns:
            Dictionary with extracted IOCs and TTPs.
        """
        logger.debug(f"Extracting IOCs and TTPs from: '{title[:50]}...'")

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

        result = self.extract_structured_data(
            prompt,
            {
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
            }
        )

        iocs_count = len(result.get('iocs', []))
        ttps_count = len(result.get('ttps', []))
        logger.debug(f"Extracted {iocs_count} IOCs and {ttps_count} TTPs from article")

        return result