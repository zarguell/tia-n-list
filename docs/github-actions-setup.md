# GitHub Actions Daily Automation Setup

This document describes the automated daily workflow for threat intelligence ingestion, processing, and blog generation.

## Overview

The GitHub Actions workflow `daily-threat-intelligence.yml` automates the complete pipeline:

1. **RSS Feed Ingestion** - Fetches articles from configured feeds
2. **LLM Processing** - Filters and analyzes articles for relevance
3. **Intelligent Blog Generation** - Creates strategic threat intelligence briefings
4. **Hugo Site Building** - Compiles the static site
5. **Git Commit & Push** - Commits changes back to repository
6. **Optional GitHub Pages Deployment** - Deploys site to GitHub Pages

## Schedule

- **Daily Execution**: 6:00 AM Eastern Standard Time
- **UTC Equivalent**: 11:00 AM UTC (`cron: '0 11 * * *'`)
- **Manual Trigger**: Can be run manually via GitHub Actions UI

## Required Configuration

### 1. Repository Secrets

Configure these secrets in your GitHub repository settings (`Settings` → `Secrets and variables` → `Actions`):

```bash
# Required Secrets
GEMINI_API_KEY=your_gemini_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Optional: GitHub token (automatically provided)
GITHUB_TOKEN=automatically_provided_by_github_actions
```

### 2. Repository Variables

Configure these variables in GitHub repository settings (`Settings` → `Secrets and variables` → `Actions` → `Variables`):

```bash
# LLM Provider Configuration
LLM_PROVIDER=openrouter                    # Options: gemini, openrouter, openai
OPENROUTER_FILTERING_MODEL=meta-llama/llama-3.3-8b-instruct:free
OPENROUTER_ANALYSIS_MODEL=openai/gpt-oss-20b:free
```

### 3. GitHub Pages (Optional)

To enable automatic site deployment to GitHub Pages:

1. Go to repository `Settings` → `Pages`
2. Set source to `GitHub Actions`
3. The workflow will automatically deploy the built site

## Workflow Steps

### 1. Environment Setup
- Sets up Python 3.11
- Installs dependencies from `requirements.txt`
- Sets up Hugo for static site generation
- Configures caching for faster builds

### 2. Data Processing Pipeline
```bash
# RSS Ingestion
PYTHONPATH=. python -m src.ingestion

# LLM Processing
PYTHONPATH=. python -m src.processing

# Intelligent Blog Generation
PYTHONPATH=. python -m src.intelligent_blog_generator
```

### 3. Site Building & Deployment
- Builds Hugo site with `hugo -s hugo/ --minify`
- Commits changes with descriptive commit message
- Optionally deploys to GitHub Pages

## File Structure After Execution

```
tia-n-list/
├── .github/workflows/
│   └── daily-threat-intelligence.yml    # Workflow configuration
├── hugo/content/posts/
│   └── 2025-10-28-strategic-threat-analysis.md  # Generated blog post
├── hugo/public/                         # Built site
├── tia_n_list.db                        # SQLite database
└── data/
    └── report_memory.json               # Memory system data
```

## Monitoring & Troubleshooting

### Workflow Status

- Check `Actions` tab in GitHub repository
- Each step provides detailed logs
- Summary includes statistics on articles processed

### Common Issues

1. **API Key Issues**: Verify all required secrets are configured
2. **Rate Limiting**: Free models may have usage limits
3. **Feed Errors**: Check RSS feed URLs in `config/feeds.yml`
4. **Build Failures**: Review Hugo configuration and content

### Log Analysis

The workflow provides detailed logging:

```bash
🔄 Starting RSS feed ingestion...
✅ RSS ingestion completed
🧠 Starting LLM processing...
✅ LLM processing completed
📝 Generating intelligent blog post...
✅ Blog post generation completed
🏗️  Building Hugo site...
✅ Hugo site built successfully
📝 Committing daily threat intelligence update...
🚀 Pushing changes to repository...
```

## Customization

### Changing Schedule

Edit the cron expression in `.github/workflows/daily-threat-intelligence.yml`:

```yaml
schedule:
  # Run at 8 AM EST (13:00 UTC) instead
  - cron: '0 13 * * *'
```

### Adding Additional Steps

The workflow is modular - you can add additional steps between processing and building:

```yaml
- name: Custom Processing Step
  run: |
    # Your custom command here
    echo "Running custom analysis..."
```

### Environment-Specific Behavior

The workflow supports different LLM providers based on configuration:

- **OpenRouter** (default): Uses free models for cost optimization
- **Gemini**: Falls back if OpenRouter unavailable
- **OpenAI**: Additional fallback option

## Performance & Costs

### Optimizations

- **Caching**: Pip dependencies and Hugo are cached
- **Conditional Execution**: Only commits if changes detected
- **Free Models**: Prioritizes free OpenRouter models
- **Time Limits**: Built-in timeouts prevent hanging

### Expected Resource Usage

- **Runtime**: 5-15 minutes (depends on article count)
- **Memory**: < 1GB
- **Storage**: Database grows ~1MB per day
- **API Costs**: Minimal with free models

## Security Considerations

- All API keys stored as GitHub Secrets
- Minimal permissions requested
- No sensitive data in commit messages
- Database contains only public threat intelligence

## Next Steps

1. **Configure Hugo**: Set up theme and site configuration
2. **Test Workflow**: Run manual trigger to verify setup
3. **Monitor Results**: Check generated blog posts for quality
4. **Adjust Timing**: Modify schedule if needed
5. **Add Analytics**: Configure tracking in Hugo site

## Support

For issues with the workflow:

1. Check the Actions tab for detailed error logs
2. Verify all secrets and variables are properly configured
3. Review the project documentation in `/docs/`
4. Test components manually using the Python scripts

---

*This workflow automatically maintains your threat intelligence briefing site with minimal manual intervention.*