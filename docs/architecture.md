## Tia N. List (TI Analyst) - Enterprise-Grade Architecture

This document outlines the architecture for the automated threat intelligence aggregator that generates **C-level executive briefings** with industry-standard confidence assessments, MITRE ATT&CK mapping, and business impact analysis.

### Functional Requirements
- **FR-01: Automated Data Ingestion**: The system will automatically fetch entries from RSS/Atom feeds defined in `data/sources/` on a daily schedule.
- **FR-02: Multi-Stage Content Processing**: A tiered LLM approach will filter, de-duplicate, analyze, extract IOCs/TTPs, and enrich content with confidence assessments.
- **FR-03: JSON-Based Data Storage**: All processed data, including articles, IOCs, and analysis, will be stored in JSON files for git tracking and persistence.
- **FR-04: Enterprise-Grade Blog Generation**: Daily C-level executive briefings will be generated with industry-standard confidence assessments, MITRE ATT&CK mapping, and business impact analysis.
- **FR-04.1: Dynamic Title Generation**: Blog posts will feature dynamic, engaging titles based on content themes with emoji integration.
- **FR-04.2: Smart Tag Generation**: Blog posts will include intelligent tags extracted from articles using 6-category taxonomy.
- **FR-05: Manual Content Workflow**: A separate, manually triggered workflow will allow for publishing deep-dive articles.
- **FR-06: Automated Newsletter Generation**: The system will compile top articles into an HTML newsletter using a predefined template.
- **FR-07: Newsletter Distribution**: The generated newsletter will be sent to subscribers via the Beehiiv API.
- **FR-08: Subscriber Management**: A script will provide a mechanism to add new subscribers to Beehiiv via its API.
- **FR-09: Professional Persona Integration**: All generated content will adopt the professional "Tia N. List" persona optimized for C-level executive audience.
- **FR-10: Analytics Tracking**: The Hugo site and newsletter will include support for an analytics service like Plausible or Google Analytics.
- **FR-11: Enterprise-Grade Prompts**: Configurable prompt system with industry-standard confidence assessments and MITRE ATT&CK integration.
- **FR-12: Intelligence Gap Analysis**: System will explicitly identify information limitations and collection priorities for transparency.
- **FR-13: Business Impact Assessment**: All threat intelligence will include sector-specific exposure analysis and risk quantification.

### Technology Stack
- **Language**: Python 3.11+ (3.13+ recommended)
- **CI/CD**: GitHub Actions with dual workflow architecture
- **Data Storage**: JSON files with git tracking
- **Static Site Generator**: Hugo with modern theme
- **LLM Provider**: Multi-provider (OpenRouter, OpenAI, Google Gemini) with automatic fallbacks
- **Email Service**: Beehiiv
- **Prompt Configuration**: Enterprise-grade configurable prompt system with A/B testing
- **Content Enhancement**: Web scraping with trafilatura and beautifulsoup
- **Professional Standards**: MITRE ATT&CK framework, industry-standard confidence assessments

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

**Dynamic Content Generation System:**
- **Title Generator**:
  - Theme analysis extracting vulnerabilities, threat actors, vendors, industries
  - Template-based generation with emoji integration
  - Uniqueness checking with 7-day memory cache
  - LLM-powered generation with fallback strategies
- **Tag Generator**:
  - 6-category taxonomy: Technical, malware families, threat actors, vendors, industries, severity
  - 42 pattern recognition rules for entity extraction
  - Smart normalization: 25 vendor mappings, 28 industry mappings
  - Confidence scoring and importance prioritization

**Content Generation Methods:**
1. **Template-Based Generation**: Structured, predictable output using templates
2. **Intelligent AI Synthesis**: Advanced LLM-powered analysis with strategic insights
3. **Dynamic Enhancement**: Integrated title and tag generation for engaging content

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

### Enterprise-Grade Prompt Configuration System

The system includes a comprehensive prompt configuration architecture for enterprise-grade CTI enhancement:

**Configuration Directory Structure (`config/prompts/`):**
```
config/prompts/
├── threat_intelligence_synthesis.json     # Main synthesis template (v2.0.0)
├── confidence_assessment.json             # Industry-standard confidence framework
├── mitre_attack_guidance.json             # Comprehensive ATT&CK integration
├── industry_impact_guidance.json          # Business impact analysis
├── intelligence_gap_guidance.json         # Intelligence gap analysis
└── tlp_banner.json                        # TLP marking templates
```

**Main Synthesis Template (`config/prompts/threat_intelligence_synthesis.json`):**
```json
{
  "version": "2.0.0",
  "description": "Enhanced prompt template for executive-grade threat intelligence synthesis",
  "persona": {
    "name": "Tia N. List",
    "role": "Senior Threat Intelligence Analyst",
    "tone": "C-level executive briefing - concise, actionable, business-focused",
    "expertise": "Enterprise cybersecurity risk assessment and strategic threat analysis"
  },
  "sections": {
    "executive_format_requirements": {
      "template": "EXECUTIVE BRIEFING FORMAT:\n\n**Executive Summary** (3-4 bullet points with confidence levels)\n\n**Threat Landscape Analysis** (business impact focus)\n\n**Risk Quantification** (sector-specific exposure)\n\n**Intelligence Gaps** (transparency about limitations)\n\n**Strategic Recommendations** (actionable guidance)"
    }
  }
}
```

**Confidence Assessment Framework (`config/prompts/confidence_assessment.json`):**
```json
{
  "confidence_levels": {
    "high": {
      "description": "High confidence (80-100%) based on multiple reliable sources",
      "executive_framing": "Actionable intelligence with high reliability for strategic decision-making"
    },
    "medium": {
      "description": "Medium confidence (50-80%) with adequately corroborated information",
      "executive_framing": "Probabilistic assessment suitable for operational planning"
    },
    "low": {
      "description": "Low confidence (20-50%) due to information gaps or limited sources",
      "executive_framing": "Early warning intelligence requiring additional verification"
    }
  }
}
```

**MITRE ATT&CK Integration (`config/prompts/mitre_attack_guidance.json`):**
```json
{
  "tactics": {
    "TA0001": "Initial Access",
    "TA0002": "Execution",
    "TA0040": "Impact"
  },
  "common_techniques": {
    "T1190": "Exploit Public-Facing Application",
    "T1566": "Phishing",
    "T1486": "Data Encrypted for Impact"
  },
  "detection_guidance": {
    "include_detection_indicators": "For each technique referenced, include relevant detection methods",
    "log_sources": {
      "T1190": "Web application logs, WAF alerts, IDS/IPS signatures"
    }
  }
}
```

**Industry Impact Analysis (`config/prompts/industry_impact_guidance.json`):**
```json
{
  "industry_mappings": {
    "technology": {
      "impact_factors": ["Service availability", "Customer data exposure", "Revenue impact"],
      "risk_indicators": ["API endpoints", "Authentication systems", "Data centers"]
    },
    "healthcare": {
      "impact_factors": ["Patient safety", "HIPAA compliance", "Care delivery"],
      "risk_indicators": ["Electronic health records", "Medical devices", "Telemedicine platforms"]
    }
  },
  "business_impact_framework": {
    "financial_impact": ["Remediation expenses", "Regulatory fines", "Revenue loss"],
    "operational_impact": ["Service disruption", "Productivity loss", "Supply chain effects"]
  }
}
```

**Intelligence Gap Analysis (`config/prompts/intelligence_gap_guidance.json`):**
```json
{
  "gap_categories": {
    "attribution_gaps": "Missing information about threat actor attribution and motivation",
    "technical_gaps": "Incomplete technical details about vulnerabilities or attack methods",
    "impact_gaps": "Unclear or incomplete assessment of business/operational impact",
    "temporal_gaps": "Unclear timeline of events or ongoing activity",
    "mitigation_gaps": "Missing guidance on detection, response, or prevention"
  },
  "executive_reporting": {
    "format": "Intelligence Gaps section should concisely identify: 1) What we don't know, 2) Why it matters, 3) Priority for filling the gap"
  }
}
```

### Security
- All API keys and secrets for Gemini, Beehiiv, and other services will be stored as GitHub Secrets and accessed as environment variables in the GitHub Actions workflow. No secrets shall be hardcoded in the source code.
