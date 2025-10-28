## Tia N. List (TI Analyst) Architecture

This document outlines the architecture for the automated threat intelligence aggregator, mailing list, and static site generator.

### Functional Requirements
- **FR-01: Automated Data Ingestion**: The system will automatically fetch entries from RSS/Atom feeds defined in `config/feeds.yml` on a daily schedule.
- **FR-02: Multi-Stage Content Processing**: A tiered LLM approach will filter, de-duplicate, analyze, extract IOCs/TTPs, and enrich content.
- **FR-03: Structured Data Storage**: All processed data, including articles, IOCs, and analysis, will be stored in a local SQLite database.
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
- **Database**: SQLite
- **Static Site Generator**: Hugo
- **LLM Provider**: Google Gemini (Flash Lite for filtering, Pro for analysis)
- **Email Service**: Beehiiv
- **Joke API**: `https://official-joke-api.appspot.com/random_joke`

### Database Schema (SQLite)
- **sources**
  - `id` (INTEGER, PRIMARY KEY)
  - `name` (TEXT)
  - `url` (TEXT, UNIQUE)
  - `last_fetched` (DATETIME)
- **articles**
  - `id` (INTEGER, PRIMARY KEY)
  - `source_id` (INTEGER)
  - `guid` (TEXT, UNIQUE)
  - `title` (TEXT)
  - `url` (TEXT)
  - `raw_content` (TEXT)
  - `processed_content` (TEXT)
  - `summary` (TEXT)
  - `score` (INTEGER)
  - `status` (TEXT) -- e.g., 'fetched', 'processed', 'published'
  - `published_at` (DATETIME)
- **iocs**
  - `id` (INTEGER, PRIMARY KEY)
  - `article_id` (INTEGER)
  - `type` (TEXT) -- e.g., 'domain', 'ip_address', 'file_hash'
  - `value` (TEXT)

### Security
- All API keys and secrets for Gemini, Beehiiv, and other services will be stored as GitHub Secrets and accessed as environment variables in the GitHub Actions workflow. No secrets shall be hardcoded in the source code.
