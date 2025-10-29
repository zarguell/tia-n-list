## Tia N. List (TI Analyst) Architecture

This document outlines the architecture for the automated threat intelligence aggregator, mailing list, and static site generator.

### Functional Requirements
- **FR-01: Automated Data Ingestion**: The system will automatically fetch entries from RSS/Atom feeds defined in `data/sources/` on a daily schedule.
- **FR-02: Multi-Stage Content Processing**: A tiered LLM approach will filter, de-duplicate, analyze, extract IOCs/TTPs, and enrich content.
- **FR-03: JSON-Based Data Storage**: All processed data, including articles, IOCs, and analysis, will be stored in JSON files for git tracking and persistence.
- **FR-04: Automated Blog Generation**: A daily summary blog post will be generated in Markdown and placed in the `hugo/content/posts/` directory.
- **FR-05: Manual Content Workflow**: A separate, manually triggered workflow will allow for publishing deep-dive articles.
- **FR-06: Automated Newsletter Generation**: The system will compile top articles into an HTML newsletter using a predefined template.
- **FR-07: Newsletter Distribution**: The generated newsletter will be sent to subscribers via the Beehiiv API.
- **FR-08: Subscriber Management**: A script will provide a mechanism to add new subscribers to Beehiiv via its API.
- **FR-09: Persona Integration**: All generated content will adopt the "Tia N. List" persona and include a "joke of the day" from an external API.
- **FR-10: Analytics Tracking**: The Hugo site and newsletter will include support for an analytics service like Plausible or Google Analytics.

### Technology Stack
- **Language**: Python 3.11+
- **CI/CD**: GitHub Actions
- **Data Storage**: JSON files with git tracking
- **Static Site Generator**: Hugo
- **LLM Provider**: Multi-provider (OpenRouter, OpenAI, Google Gemini)
- **Email Service**: Beehiiv
- **Joke API**: `https://official-joke-api.appspot.com/random_joke`

### JSON-Based Data Architecture

The system uses JSON files organized in a hierarchical folder structure:

```
data/
├── sources/                    # RSS feed configurations
│   ├── krebs-on-security.json
│   ├── schneier-on-security.json
│   └── threatpost.json
├── articles/                   # Article content organized by date
│   └── YYYY/MM/DD/
│       ├── article-id.json
│       └── ...
├── content/                    # Full scraped content
│   └── YYYY/MM/DD/
│       ├── article-id.html
│       └── ...
├── processed/                  # AI-processed data
│   └── YYYY/MM/DD/
│       ├── iocs.json
│       └── analysis.json
└── reports/                    # Generated reports
    └── YYYY/MM/DD/
        └── daily-summary.md
```

### Intelligent LLM Synthesis Framework

The system includes advanced AI-powered content synthesis capabilities:

**Multi-Provider Architecture:**
- **Primary**: OpenRouter (free models: `meta-llama/llama-3.3-8b-instruct:free`, `openai/gpt-oss-20b:free`)
- **Fallback 1**: OpenAI (GPT models)
- **Fallback 2**: Google Gemini (Flash/Pro models)

**Intelligence Synthesis Features:**
- **Context Engineering**: Comprehensive article context preparation (titles, content, IOCs, sources)
- **Cross-Article Pattern Recognition**: Identifies trends and threat landscape patterns
- **Fact-Checking Framework**: Prevents hallucination by constraining to real entities from articles
- **Memory System**: 7-day rolling memory prevents content repetition
- **Professional Output**: Strategic intelligence briefings with authentic voice

**Content Generation Methods:**
1. **Template-Based Generation**: Structured, predictable output using templates
2. **Intelligent AI Synthesis**: Advanced LLM-powered analysis with strategic insights

**Response Processing:**
- Handles both structured JSON and unstructured text LLM responses
- Automatic fallback between providers for reliability
- IOC filtering to remove non-security indicators
- Complete source attribution for verification

#### JSON Schemas

**Source Configuration (`data/sources/*.json`):**
```json
{
  "id": "source-identifier",
  "name": "Source Name",
  "url": "https://example.com/feed/",
  "last_fetched": "2025-10-29T10:00:00Z",
  "fetch_interval_hours": 1,
  "quality_score": 85,
  "active": true,
  "metadata": {
    "focus_areas": ["cybercrime", "vulnerabilities"],
    "content_quality": "full"
  }
}
```

**Article Data (`data/articles/YYYY/MM/DD/article-id.json`):**
```json
{
  "id": "source-date-hash",
  "source_id": "source-identifier",
  "guid": "unique-article-id",
  "title": "Article Title",
  "url": "https://example.com/article",
  "published_at": "2025-10-29T09:30:00Z",
  "status": "processed",
  "content": {
    "raw": "RSS excerpt...",
    "full": "Scraped full content...",
    "processed": "AI-processed content..."
  },
  "analysis": {
    "score": 85,
    "threat_category": "malware",
    "summary": "Article summary...",
    "key_entities": ["threat-actor", "vulnerability"],
    "ttps": ["initial-access", "execution"]
  },
  "processing_metadata": {
    "processed_at": "2025-10-29T10:05:00Z",
    "llm_provider": "openrouter"
  }
}
```

**IOC Data (`data/processed/YYYY/MM/DD/iocs.json`):**
```json
{
  "date": "2025-10-29",
  "iocs": [
    {
      "article_id": "article-id",
      "type": "domain",
      "value": "malicious-domain.com",
      "confidence": "high",
      "context": "C2 server mentioned in report",
      "extracted_at": "2025-10-29T10:05:00Z"
    }
  ]
}
```

### Security
- All API keys and secrets for Gemini, Beehiiv, and other services will be stored as GitHub Secrets and accessed as environment variables in the GitHub Actions workflow. No secrets shall be hardcoded in the source code.
