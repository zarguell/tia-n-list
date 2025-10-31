# LLM Configuration Enhancements

## Overview

This document describes the enhancements made to the LLM client configuration system to address three key issues:

1. **Configurable max_tokens with higher defaults for blog generation**
2. **max_tokens vs max_completion_tokens compatibility for different models**
3. **Custom OpenAI base URL configuration support**

## Changes Made

### 1. Enhanced Token Configuration

#### Environment Variables Added
- `LLM_MAX_TOKENS` (default: 1500) - General purpose token limit
- `LLM_MAX_TOKENS_BLOG` (default: 3000) - Blog generation token limit
- `LLM_MAX_TOKENS_FILTERING` (default: 1000) - Relevance filtering token limit
- `LLM_MAX_TOKENS_ANALYSIS` (default: 4000) - IOC/TTP analysis token limit

#### Configuration Implementation
- Updated `src/llm_client_multi.py` to include enhanced token configuration
- Added separate token limits for different use cases
- Blog generation now uses 3000 tokens by default (100% increase from 1500)

### 2. Model Compatibility Fix

#### Problem
Some models (like GPT-5-nano) require `max_completion_tokens` instead of `max_tokens` parameter, causing API errors.

#### Solution
- Updated `src/providers/openai_provider.py` with intelligent parameter detection
- Added fallback logic that tries `max_tokens` first, then `max_completion_tokens` on error
- Applied to both single model and fallback model generation methods
- Also updated `src/intelligent_blog_generator.py` for direct API calls

#### Implementation Details
```python
try:
    completion_params["max_tokens"] = max_tokens
    response = self.client.chat.completions.create(**completion_params)
except Exception as first_error:
    error_str = str(first_error).lower()
    if "max_completion_tokens" in error_str or "not supported" in error_str:
        # Model requires max_completion_tokens instead
        logger.info(f"Model {model} requires max_completion_tokens, retrying...")
        if "max_tokens" in completion_params:
            del completion_params["max_tokens"]
        completion_params["max_completion_tokens"] = max_tokens
        response = self.client.chat.completions.create(**completion_params)
    else:
        raise first_error
```

### 3. Custom OpenAI Base URL Support

#### Environment Variable Added
- `OPENAI_BASE_URL` (default: https://api.openai.com/v1) - Custom OpenAI-compatible API endpoint

#### Configuration Implementation
- Updated `src/llm_client_multi.py` to support custom base URLs
- Allows users to configure alternative OpenAI-compatible providers
- Maintains backward compatibility with existing configurations

## Usage Examples

### Basic Configuration
```bash
# Use default configuration
export LLM_PROVIDER=openai
export OPENAI_API_KEY=your_key_here
```

### Custom Token Limits
```bash
# Increase blog generation token limit
export LLM_MAX_TOKENS_BLOG=5000

# Adjust filtering and analysis limits
export LLM_MAX_TOKENS_FILTERING=1500
export LLM_MAX_TOKENS_ANALYSIS=6000
```

### Custom OpenAI Provider
```bash
# Use alternative OpenAI-compatible provider
export OPENAI_BASE_URL=https://custom-provider.com/v1
export OPENAI_API_KEY=your_custom_key_here
```

### OpenRouter Configuration
```bash
# OpenRouter with enhanced configuration
export LLM_PROVIDER=openrouter
export OPENROUTER_API_KEY=your_openrouter_key
export LLM_MAX_TOKENS_BLOG=4000
```

## Impact Analysis

### Blog Generation Quality
- **Previous**: 1500 tokens limit often caused truncated responses
- **Current**: 3000 tokens default (100% increase) with configurable up to 5000+
- **Result**: More complete, detailed threat intelligence briefings

### Model Compatibility
- **Previous**: API errors with models requiring `max_completion_tokens`
- **Current**: Automatic parameter detection and fallback
- **Result**: Broader model support without manual intervention

### Provider Flexibility
- **Previous**: Only official OpenAI API endpoints
- **Current**: Any OpenAI-compatible API endpoint
- **Result**: Support for custom providers, private deployments, and alternative services

## Files Modified

1. **src/llm_client_multi.py**
   - Added enhanced token configuration
   - Added custom base URL support
   - Updated provider configuration methods

2. **src/providers/openai_provider.py**
   - Added max_tokens/max_completion_tokens compatibility
   - Updated both single and fallback model generation
   - Added intelligent error handling and parameter switching

3. **src/intelligent_blog_generator.py**
   - Updated _openrouter_direct_synthesis method
   - Added configurable max_tokens for blog generation
   - Added parameter compatibility handling

4. **tests/test_llm_configuration.py** (new)
   - Comprehensive test suite for configuration features
   - Validates environment variable handling
   - Tests model compatibility scenarios

## Backward Compatibility

All changes maintain full backward compatibility:
- Existing configurations continue to work unchanged
- Default values provide immediate improvements
- New features are opt-in via environment variables
- No breaking changes to existing APIs

## Recommendations

### Production Deployment
1. Start with default values for initial testing
2. Monitor response completeness and adjust `LLM_MAX_TOKENS_BLOG` as needed
3. Consider higher limits for comprehensive threat intelligence briefings

### Cost Optimization
1. Use lower limits for filtering and batch processing
2. Use higher limits for critical content generation (blogs, analysis)
3. Adjust based on actual usage patterns and response quality

### Model Selection
1. Standard OpenAI models: Use default `max_tokens`
2. GPT-5-nano and similar: Automatic fallback to `max_completion_tokens`
3. Custom providers: Ensure OpenAI API compatibility

## Testing

Run the configuration test suite to validate setup:

```bash
PYTHONPATH=. python tests/test_llm_configuration.py
```

Test individual configuration components:

```bash
PYTHONPATH=. python -c "
from src.llm_client_multi import MultiLLMClient
client = MultiLLMClient()
config = client._get_provider_config('openai')
print('Blog max_tokens:', config.get('max_tokens_blog'))
print('Base URL:', config.get('base_url'))
"
```

## Troubleshooting

### Common Issues

1. **Responses still truncated**
   - Increase `LLM_MAX_TOKENS_BLOG` environment variable
   - Check if model has separate output limits

2. **API parameter errors**
   - System should automatically handle parameter switching
   - Check logs for "requires max_completion_tokens" messages

3. **Custom provider connection issues**
   - Verify `OPENAI_BASE_URL` is correct and accessible
   - Check API key compatibility with custom provider

### Debug Information

Enable debug logging to see parameter usage:

```bash
export LLM_LOG_LEVEL=DEBUG
```

The system will log:
- Which parameter is being used (max_tokens or max_completion_tokens)
- Model-specific requirements
- Configuration values being applied