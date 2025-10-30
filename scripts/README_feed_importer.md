# RSS Feed Importer

A helper script for adding RSS feeds to the Tia N. List threat intelligence system.

## Features

- **Smart URL Extraction**: Extracts RSS URLs from mixed text content
- **Dynamic Feed Names**: Automatically fetches feed names from RSS/Atom data
- **Duplicate Detection**: Prevents adding feeds that already exist
- **URL Cleaning**: Normalizes and validates URLs
- **Error Handling**: Graceful handling of network and parsing errors
- **Multiple Input Sources**: File, direct URLs, or clipboard
- **Dry Run Mode**: Test without actually adding feeds

## Installation

Install the required dependencies:

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install feedparser pyperclip
```

## Usage

### From Text File

Create a text file with RSS URLs mixed with other content:

```
# feeds.txt
Some cybersecurity feeds:
"https://example.com/feed.xml",
"https://another.com/rss",
"https://third.com/atom.xml"
```

Run the script:

```bash
# Test without adding (dry run)
python scripts/add_feeds.py --file feeds.txt --dry-run

# Actually add the feeds
python scripts/add_feeds.py --file feeds.txt
```

### Direct URLs

```bash
# Add specific URLs
python scripts/add_feeds.py --url "https://example.com/feed.xml" --url "https://another.com/rss"
```

### From Clipboard

Copy text containing RSS URLs to clipboard, then:

```bash
python scripts/add_feeds.py --clipboard
```

## What the Script Does

1. **URL Extraction**: Finds RSS/Atom URLs in mixed content using patterns like:
   - `"https://example.com/feed.xml"`
   - `'https://example.com/rss'`
   - `https://example.com/atom.xml`

2. **URL Validation**: Ensures URLs appear to be valid RSS feeds based on:
   - Proper HTTP/HTTPS scheme
   - RSS indicators in URL (feed, rss, atom, xml)
   - Valid domain structure

3. **Feed Validation**: Attempts to fetch and parse each feed to:
   - Get the actual feed title
   - Validate feed format
   - Count available entries
   - Extract metadata

4. **Duplicate Checking**: Prevents adding feeds that already exist by:
   - Checking existing source files in `data/sources/`
   - Checking the JSON storage database

5. **Feed Creation**: Creates a JSON file in `data/sources/` with:
   - Unique ID based on feed name and domain
   - Dynamic feed name from RSS data
   - Metadata about validation and import

## Output Examples

### Successful Run
```
🛡️  Tia N. List - RSS Feed Importer
==================================================
📁 Reading feeds from: feeds.txt
Found 3 RSS URLs in text:
  - https://example.com/feed.xml
  - https://another.com/rss

  📡 Fetching feed info: https://example.com/feed.xml
    ✅ Example Security Blog
    📄 15 entries
✅ Added feed: Example Security Blog -> data/sources/example-security-blog-example-com.json

📊 Summary:
==============================
✅ Added: 2
⚠️ Exists: 1
```

### Dry Run
```
🔍 DRY RUN: Would add feed: Example Security Blog

📊 Summary:
==============================
🔍 Dry Run: 2
⚠️ Exists: 1

🔍 This was a DRY RUN. No feeds were actually added.
```

## Error Handling

The script handles various error conditions gracefully:

- **Network Errors**: Timeouts, 404s, DNS failures
- **Parsing Errors**: Invalid RSS/Atom formats
- **Duplicate Feeds**: Already existing feeds
- **Invalid URLs**: Malformed or non-RSS URLs

Failed feeds are still recorded with validation status information.

## File Structure

Created feed files follow this structure:

```json
{
  "id": "example-security-blog-example-com",
  "name": "Example Security Blog",
  "url": "https://example.com/feed.xml",
  "active": true,
  "created_at": "2025-10-30T12:34:56.789Z",
  "updated_at": "2025-10-30T12:34:56.789Z",
  "metadata": {
    "language": "en",
    "description": "Latest cybersecurity news and analysis",
    "validation_status": "success",
    "total_entries": 15,
    "last_checked": "2025-10-30T12:34:56.789Z",
    "import_source": "add_feeds_script"
  }
}
```

## Tips

1. **Use Dry Run First**: Always test with `--dry-run` before adding feeds
2. **Check Network**: Some feeds may be temporarily unavailable
3. **Feed Names**: Names are extracted from RSS data; unavailable feeds get URL-based names
4. **Respect Servers**: The script includes delays between requests
5. **Manual Review**: Review added feeds in `data/sources/` after import

## Troubleshooting

### "No RSS URLs found"
- Ensure URLs contain RSS indicators (feed, rss, atom, xml)
- Check URL format and quotes
- Try using `--url` for direct input

### Network Errors
- Check internet connection
- Some feeds may be temporarily down
- Try running again later

### Import Errors
- Ensure virtual environment is activated
- Install required dependencies
- Check permissions on `data/sources/` directory

## Security Considerations

- The script uses a custom User-Agent for identification
- Requests are rate-limited to respect server resources
- All URLs are validated before processing
- No authentication data is stored or transmitted