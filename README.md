# Tia N List - n8n Workflow Documentation

The "Tia N List" workflow is an automated cybersecurity threat intelligence digest generator that collects RSS feed entries from Miniflux, analyzes them using AI, and produces daily summaries published to GitHub and sent via email.[1]

## Workflow Overview

This workflow runs daily and processes cybersecurity threat intelligence articles through multiple stages: data collection, filtering, AI analysis, and multi-channel distribution.

## Data Collection & Preparation

### RSS Feed Retrieval
The workflow retrieves the latest 40 entries from a hosted Miniflux instance for feeds in the cybersecurity category ordered by publication date, with retry logic enabled (5-second wait between retries). The workflow uses the community n8n Miniflux node, and I have noticed high volume full text article retrievals will often time out.

### Historical Context Gathering
The workflow retrieves the last 5 days of previously published articles from the GitHub repository to provide context and avoid duplicate reporting:
- Lists files from the `hugo/content/posts/` directory
- Sorts by newest first
- Limits to the 5 most recent posts
- Downloads and parses each file's content
- Extracts frontmatter metadata (title, date, summary)
- Combines all summaries into a single context string

### Filtering Pipeline
Articles pass through two sequential filters:[1]
1. **Time Filter**: Retains only articles published within the past 24 hours (after yesterday, before tomorrow)
2. **Tag Filter**: Excludes known low fidelity articles, such as "Metasploit Weekly Wrapup"

### Content Processing
The workflow prepares filtered articles for AI analysis:
- Converts HTML content to Markdown format
- Extracts only essential fields (title, URL, content_plain)
- Aggregates all filtered articles into a single data structure
- Merges with the 5-day historical summary context

## AI-Powered Analysis

### Article Creation
The primary AI agent analyzes aggregated threat intelligence using the glm-4.6 model with a 600-second timeout. The agent receives:
- Today's filtered articles (title, URL, content)
- Previous 5 days of reporting summaries
- Detailed instructions for threat analysis, categorization, deduplication, and writing style

The agent produces a comprehensive markdown digest organized into sections like Critical Threats, Threat Actor Activity, Vulnerabilities & Patches, Defense & Detection, and Policy & Industry News.

### Metadata Extraction
A second AI agent processes the generated article to extract structured metadata:
- **Title**: Comma-separated list of 3-5 headline fragments with optional emojis
- **Tags**: Array of 5-10 lowercase keywords (threats, techniques, actors, sectors)
- **Summary**: Exactly two sentences highlighting key topics and their impact

The agent uses a Structured Output Parser configured with JSON schema validation and auto-fix enabled to ensure valid JSON output.

## Distribution Channels

### GitHub Publication
The workflow publishes the article to a static site repository:
- Creates a markdown file with YAML frontmatter containing title, date, tags, categories, author, and summary
- File path: `hugo/content/posts/YYYY-MM-DD-daily-summary.md`
- Commit message: "Add YYYY-MM-DD daily summary"

### Feed Cleanup
After processing, the workflow marks all retrieved Miniflux articles as read.

## Technical Configuration

### AI Models
All AI agents use the glm-4.6 model accessed through a LiteLLM API endpoint with 600-second timeouts. GLM will often spend a long time thinking, especially with large prompts (this system averages 30-40k token input daily, depending on article volume), so the long timeout is to avoid quitting early.
