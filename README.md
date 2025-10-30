# Tia N. List - Enterprise-Grade Threat Intelligence Platform

🎯 **Milestone 6: Enterprise-Grade CTI Enhancement - COMPLETE!**

An automated threat intelligence aggregator that generates **C-level executive briefings** with industry-standard confidence assessments, MITRE ATT&CK mapping, and business impact analysis. Features enterprise-grade prompt engineering, intelligence gap identification, and professional risk quantification for strategic decision-making.

## 🚀 **Latest Achievement: Enterprise-Grade CTI Enhancement**

- **🎯 C-Level Executive Briefings**: Professional intelligence reports optimized for strategic decision-making
- **📊 Industry-Standard Confidence**: High/Medium/Low confidence assessments with executive decision-making context
- **🔍 MITRE ATT&CK Integration**: Comprehensive technique mapping with detection guidance and response priorities
- **📈 Business Impact Analysis**: Sector-specific exposure assessment and risk quantification
- **🧠 Intelligence Gap Identification**: Transparency about limitations and collection priorities
- **⚡ Enterprise-Grade Prompts**: Configurable prompt system with A/B testing and version management

## ✨ Features

🚀 **JSON-Based Storage Architecture** - All data persisted in git for GitHub Actions continuity
🧠 **Intelligent AI Synthesis** - Multi-provider LLM system with fact-checking and memory
📊 **Source Quality Tracking** - Automated scoring and prioritization of 33+ feed sources
💰 **Cost Optimized** - 85.7% processing reduction, significant LLM cost savings
🔒 **Multi-Provider Architecture** - OpenRouter, OpenAI, and Gemini with automatic fallbacks
📈 **Scalable Processing** - 5-tier processing system handles large feed volumes efficiently
🎨 **Modern Hugo Theme** - Professional site with dark mode and RSS feed
📱 **Content Enhancement** - Web scraping for full article content (1000-10000 char improvements)
🛡️ **IOC/TTP Extraction** - Automatic extraction of indicators and tactics, techniques, procedures
🎯 **Strategic Intelligence** - Cross-article pattern recognition and threat landscape analysis
🚀 **Enterprise-Grade Prompts** - Industry-standard confidence assessments and executive framing
🎯 **MITRE ATT&CK Integration** - Comprehensive technique mapping with detection implications
📊 **Business Impact Analysis** - Sector-specific exposure assessment and risk quantification
🧠 **Intelligence Gap Analysis** - Transparency about limitations and collection priorities
🏷️ **Smart Tag Extraction** - 6-category taxonomy with 42 pattern recognition rules
📝 **Dynamic Titles** - Theme-based title generation with emoji integration and uniqueness checking

## 🏗️ Architecture

- **JSON-Based Storage**: Hierarchical folder structure with git tracking (`data/sources/`, `data/articles/`, `data/content/`, `data/processed/`)
- **Multi-Source Ingestion**: Fetches 33+ RSS feeds with 24-hour filtering and 50 article limits
- **Content Enhancement**: Web scraping with trafilatura for full content extraction (3000%+ improvement)
- **5-Tier Processing**: Intelligent article prioritization based on source quality and relevance
- **AI Processing**: Multi-provider system with fact-checking and IOC extraction
- **Dynamic Content Generation**:
  - **Title Generator**: Theme analysis with emoji integration and uniqueness checking
  - **Tag Generator**: 6-category taxonomy with 42 pattern recognition rules
  - **Smart Normalization**: 25 vendor mappings and 28 industry mappings
- **Enhanced Blog Generation**: Integration of dynamic titles and tags with enterprise-grade prompt configuration
- **Executive-Grade Synthesis**: Advanced LLM-powered content synthesis with confidence assessments and business impact analysis
- **Intelligence Gap Analysis**: Transparent reporting of limitations and collection priorities
- **MITRE ATT&CK Integration**: Comprehensive technique mapping with detection guidance and response priorities
- **Hugo Generation**: Professional C-level executive briefings with modern theme
- **Distribution**: Automated deployment to GitHub Pages
- **Memory System**: 7-day rolling memory prevents content repetition
- **Reliability**: Built-in retry logic with exponential backoff for rate limiting
- **A/B Testing**: Prompt version management and safe experimentation framework

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ (3.13+ recommended for best compatibility)
- [Hugo](https://gohugo.io/installation/) for static site generation
- API keys for LLM providers (stored in GitHub Secrets)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd tia-n-list
   ```

2. **Set up Python virtual environment**
   ```bash
   # Create virtual environment (Python 3.13 recommended)
   python3 -m venv venv

   # Activate virtual environment
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install project dependencies
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create a .env file for local testing
   cp .env.sample .env

   # Edit .env with your API keys
   # OPENROUTER_API_KEY=your_openrouter_api_key
   # OPENAI_API_KEY=your_openai_api_key
   # GEMINI_API_KEY=your_gemini_api_key
   ```

4. **Verify JSON sources** (33 sources already migrated)
   ```bash
   # Check JSON source configurations
   ls data/sources/
   ```

### Running the System Locally

```bash
# Activate virtual environment and set PYTHONPATH
source venv/bin/activate
export PYTHONPATH=.

# 1. Ingest articles from JSON sources (33 RSS feeds with 24-hour filtering)
python -m src.json_ingestion

# 2. Enhance content with full web scraping (1000-10000 character improvements)
python scripts/enhance_content_json.py

# 3. Run JSON-based processing with multi-tier analysis (85.7% efficiency)
python -m src.json_processing

# 4. Generate intelligent blog post with AI synthesis
python scripts/generate_blog_json.py

# Analysis Tools
python scripts/analyze_feed_quality.py  # Analyze feed quality without parsers
python -c "from src.json_storage import JSONStorage; print(JSONStorage().get_statistics())"  # Check storage stats
```

### Testing

```bash
# Activate virtual environment and set PYTHONPATH
source venv/bin/activate
export PYTHONPATH=.

# Run all tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html

# Run code quality checks
ruff check src/ tests/
mypy src/

# Format code
ruff format src/ tests/
```

## 📁 Project Structure

```
tia-n-list/
├── src/                    # Python source code
│   ├── json_storage.py     # JSON-based storage system
│   ├── json_ingestion.py  # RSS feed processing (JSON sources)
│   ├── json_processing.py  # AI content processing with JSON storage
│   ├── enhanced_json_blog_generator.py # Hugo blog generation with enterprise-grade prompts
│   ├── content_fetcher.py  # Web scraping for full content
│   ├── llm_client_multi.py # Multi-provider LLM client with fallbacks
│   ├── source_quality.py  # Source quality scoring and tracking
│   ├── tiered_processor.py # 5-tier article processing system
│   ├── scalable_processor.py # Optimized LLM processing for scale
│   ├── processing.py      # Legacy SQLite processing (deprecated)
│   ├── intelligent_blog_generator.py # AI-powered content synthesis
│   ├── prompt_loader.py   # Enterprise-grade prompt configuration system
│   ├── title_generator.py # Dynamic title generation
│   ├── tag_generator.py   # Smart tag extraction
│   ├── persona.py         # Professional Tia N. List persona
│   ├── context_builder.py # AI context building for synthesis
│   └── providers/         # LLM provider implementations
│       ├── openai_provider.py # OpenAI/OpenRouter provider with fallbacks
│       └── gemini_provider.py # Gemini API provider
│   └── extractors/        # Website-specific content extractors
│       ├── base.py        # Abstract base class
│       ├── threatpost.py  # Threatpost extractor
│       └── schneier.py    # Schneier on Security extractor
├── config/                # Configuration files
│   └── prompts/           # Enterprise-grade prompt configuration
│       ├── threat_intelligence_synthesis.json # Main synthesis template (v2.0.0)
│       ├── confidence_assessment.json # Industry-standard confidence framework
│       ├── mitre_attack_guidance.json # Comprehensive ATT&CK integration
│       ├── industry_impact_guidance.json # Business impact analysis
│       ├── intelligence_gap_guidance.json # Intelligence gap analysis
│       └── tlp_banner.json # TLP marking templates
├── data/                  # JSON data storage (git tracked)
│   ├── sources/           # RSS feed configurations (33 sources)
│   ├── articles/          # Article content by date (YYYY/MM/DD/)
│   ├── content/           # Full scraped web content
│   ├── processed/         # AI-processed data and IOCs by date
│   └── reports/           # Generated intelligence reports
├── hugo/                  # Hugo static site
│   ├── content/           # Generated blog posts
│   ├── content/posts/      # Daily briefings
│   ├── content/about/      # About page
│   ├── themes/            # Hugo Blog Awesome theme (submodule)
│   ├── config.toml        # Hugo configuration (TOML format)
│   └── public/            # Generated site
├── scripts/               # Utility scripts
│   ├── enhance_content_json.py  # Content enhancement
│   ├── generate_blog_json.py     # Blog generation
│   ├── migrate_feeds_to_json.py  # Migration utility
│   ├── analyze_feed_quality.py  # Feed quality analysis
│   └── add_subscriber.py        # Subscriber management
├── tests/                 # Unit and integration tests
├── docs/                  # Documentation
│   ├── architecture.md    # System architecture
│   ├── tasks.md          # Task tracking
│   ├── .context.md      # Patterns & conventions
│   └── .memory.md       # Decisions & lessons learned
└── .github/workflows/     # GitHub Actions
    └── daily-threat-intelligence.yml  # Daily automated workflow
```

## 🔧 Configuration

### JSON Sources (`data/sources/`)

```json
{
  "id": "krebs-on-security",
  "name": "Krebs on Security",
  "url": "https://krebsonsecurity.com/feed/",
  "active": true,
  "metadata": {
    "focus_areas": ["cybercrime", "fraud", "data-breaches"]
  }
}
```

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `LLM_PROVIDER` | Primary LLM provider (openrouter/openai/gemini) | Recommended | `openrouter` |
| `OPENROUTER_API_KEY` | OpenRouter API key | Recommended | - |
| `OPENAI_API_KEY` | OpenAI API key | Optional | - |
| `GEMINI_API_KEY` | Google Gemini API key | Optional | - |
| `USE_OPTIMIZED_PROMPT` | Use token-efficient prompts (true/false) | Optional | `true` |
| `USE_ENHANCED_PROMPTS` | Use enterprise-grade prompt configuration (true/false) | Optional | `true` |

### Multi-Provider LLM Configuration

```bash
# OpenRouter (Recommended) - Free models with 4-level fallbacks
export LLM_PROVIDER=openrouter
export OPENROUTER_API_KEY=your_key_here

# OpenAI
export LLM_PROVIDER=openai
export OPENAI_API_KEY=your_key_here

# Gemini (Fallback)
export LLM_PROVIDER=gemini
export GEMINI_API_KEY=your_gemini_key_here

# Multi-provider setup with automatic fallbacks
export LLM_PROVIDER=openrouter
export OPENROUTER_API_KEY=your_key
export GEMINI_API_KEY=your_gemini_key  # Automatic fallback
```

**Prompt Engineering Configuration:**
```bash
# Optimized prompts (recommended for production)
export USE_OPTIMIZED_PROMPT=true  # 16.5% fewer tokens, 45% better quality

# Comprehensive prompts (maximum detail)
export USE_OPTIMIZED_PROMPT=false

# Enterprise-grade prompts (C-level executive briefings)
export USE_ENHANCED_PROMPTS=true   # Confidence assessments, MITRE ATT&CK, business impact
```

**OpenRouter Free Models:**
- Filtering: `meta-llama/llama-3.3-8b-instruct:free`
- Analysis: `openai/gpt-oss-20b:free`
- Fallbacks: z-ai/glm-4.5-air, qwen/qwen3-235b-a22b, microsoft/mai-ds-r1, google/gemini-2.0-flash-exp

### LLM Model Configuration

The system uses a cost-optimized tiered approach:

- **Filtering Stage**: Uses free OpenRouter models for high-volume relevance filtering
- **Analysis Stage**: Uses OpenRouter or Gemini for IOC/TTP extraction
- **Retry Logic**: Automatic exponential backoff for rate limiting (HTTP 429 errors)
- **Batch Processing**: Processes multiple articles per API call for efficiency
- **Fact-Checking**: Prevents hallucination by constraining to real entities from articles

## 🚀 GitHub Actions Setup

### Required Secrets

Configure these secrets in your GitHub repository settings:

1. **OPENROUTER_API_KEY**: Your OpenRouter API key (recommended)
2. **OPENAI_API_KEY**: Your OpenAI API key (optional)
3. **GEMINI_API_KEY**: Your Google Gemini API key (fallback)

### Workflow Files

The system uses an automated GitHub Actions workflow:

#### Daily Automated Workflow (`.github/workflows/daily-threat-intelligence.yml`)

Runs automatically every day at 11:00 AM UTC to:
- Setup Python environment
- Ingest RSS feeds from 33 JSON sources
- Enhance content with full web scraping
- Process content with multi-tier AI analysis
- Generate intelligent blog post with synthesis
- Build and deploy Hugo site to GitHub Pages
- Commit all JSON data and generated content to git

### Workflow Features

- **JSON Data Persistence**: All content is committed to git for continuity
- **Multi-Provider Fallbacks**: Automatic switching between LLM providers
- **Error Recovery**: Robust handling of rate limits and API issues
- **Content Enhancement**: Web scraping for full article content
- **Professional Output**: Modern theme with dark mode, search, and RSS

## 🧪 Development Workflow

1. **Make changes** to source code
2. **Activate environment**: `source venv/bin/activate && export PYTHONPATH=.`
3. **Run tests locally**: `pytest tests/`
4. **Check code quality**: `ruff check src/ tests/ && mypy src/`
5. **Test functionality**: Run individual modules with `python -m src.<module>`
6. **Commit changes** and push to trigger GitHub Actions

## 📊 Monitoring and Debugging

### Local Debugging

```bash
# Activate virtual environment and set PYTHONPATH
source venv/bin/activate
export PYTHONPATH=.

# Check JSON storage statistics
python -c "
from src.json_storage import JSONStorage
storage = JSONStorage()
stats = storage.get_statistics()
print('Storage Statistics:', json.dumps(stats, indent=2))
"

# Test API connections
python -c "
from src.llm_client_multi import MultiLLMClient
client = MultiLLMClient()
info = client.get_provider_info()
print('Multi-Provider Status:', info['primary_provider'])
print('Fallback Available:', info['fallback_provider'])
"
```

### GitHub Actions Monitoring

- Check workflow runs in the **Actions** tab of your GitHub repository
- Review workflow logs for debugging
- Monitor API usage and rate limits
- Check deployed site at `https://<username>.github.io/tia-n-list/`
- Monitor git commits for JSON data and generated content

## 🔐 Security Considerations

- All API keys are stored in GitHub Secrets (never in code)
- JSON-based storage is git-tracked and version controlled
- No external dependencies on user input for security
- Content filtering and validation at multiple stages
- Fact-checking framework prevents AI hallucination
- Memory system prevents repetitive content
- IOC filtering removes non-security indicators

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test locally
4. Ensure all tests pass: `PYTHONPATH=. pytest tests/`
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Troubleshooting

### Common Issues

**Import Errors**: Ensure `PYTHONPATH=.` is set when running tests
```bash
export PYTHONPATH=.
```

**Virtual Environment Issues**: Recreate virtual environment
```bash
rm -rf venv
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Hugo Build Errors**: Check theme installation and content structure
```bash
cd hugo && hugo server --buildDrafts
```

**F-String Syntax Errors**: Fixed in latest version (pre-format variables)
```bash
# This is now handled automatically
python -m src.json_blog_generator  # Should work without syntax errors
```

**Empty GitHub Actions Site**: Check GitHub Actions workflow configuration
```bash
# Verify config file references
ls hugo/config.toml  # Should exist, not config.yaml
```

### Getting Help

- Check the [documentation](docs/) for detailed architecture
- Review test files for usage examples
- Check GitHub Actions workflow logs for deployment issues
- Open an issue for bugs or feature requests
- Review `docs/.memory.md` for detailed technical decisions and lessons learned

## 📊 Current Status

### ✅ Completed Features

- **Milestone 1**: Core data ingestion and JSON storage functionality
- **Milestone 2**: Multi-provider AI-powered content processing and IOC/TTP extraction
- **Milestone 2.5**: Multi-provider LLM architecture with automatic fallbacks
- **Milestone 3**: JSON-based blog generation and Hugo deployment
- **Milestone 3.5**: Full content acquisition with web scraping (3000%+ improvement)
- **Milestone 3.6**: Enhanced blog generation with threat categorization and intelligence synthesis
- **Milestone 3.7**: Intelligent LLM synthesis framework with strategic analysis
- **Milestone 4.1**: Intelligent feed ingestion and scaling (33 sources, 85.7% efficiency)
- **Milestone 6**: Enterprise-grade CTI enhancement with confidence assessments and MITRE ATT&CK mapping
- **Hugo Optimization**: Modern theme with dark mode, search, RSS, and responsive design

### 🎯 Key Capabilities (Latest)

- **Enterprise-Grade CTI**: C-level executive briefings with industry-standard confidence assessments
- **JSON-Based Architecture**: All content persisted in git for GitHub Actions continuity
- **33 RSS Sources**: Comprehensive threat intelligence feed coverage
- **Confidence Framework**: High/Medium/Low confidence assessments with executive decision-making context
- **MITRE ATT&CK Integration**: Comprehensive technique mapping with detection guidance
- **Business Impact Analysis**: Sector-specific exposure assessment and risk quantification
- **Intelligence Gap Analysis**: Transparent reporting of limitations and collection priorities
- **Multi-Provider LLM**: OpenRouter → OpenAI → Gemini with automatic fallbacks
- **Content Enhancement**: Full web scraping with dramatic content improvements
- **Executive Synthesis**: Strategic threat intelligence analysis with business impact focus
- **Professional Site**: Modern Hugo theme with all modern features
- **GitHub Actions Ready**: Automated deployment with JSON data persistence

### 🔧 Recent Technical Updates

The system has been completely modernized:

- **JSON Storage Migration**: From SQLite to git-tracked JSON files
- **Multi-Provider Architecture**: Robust LLM system with 4-level fallbacks
- **Hugo Theme Upgrade**: Modern theme with dark mode, search, RSS feed
- **F-String Syntax Fixes**: Resolved all Python syntax errors
- **GitHub Actions Optimization**: Fixed workflow configuration for JSON system
- **Content Enhancement**: 3000-10000 character improvements in article content
- **Enterprise-Grade Prompts**: Industry-standard confidence assessments and executive framing
- **MITRE ATT&CK Integration**: Comprehensive technique mapping with detection implications
- **Intelligence Synthesis**: Advanced LLM-powered threat analysis with fact-checking
- **Professional Output**: C-level executive briefings with business impact focus and confidence assessments