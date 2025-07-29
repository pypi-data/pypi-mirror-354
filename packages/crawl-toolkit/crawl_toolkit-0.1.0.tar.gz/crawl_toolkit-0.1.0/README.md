# Python Crawl Toolkit

Universal package for BrightData web scraping and crawling. And making keyword research easier.

## Installation

```bash
pip install crawl-toolkit
```

## Features

- Web scraping with BrightData integration
- Keyword research tools
- OpenAI integration for content analysis
- Asynchronous crawling support
- BeautifulSoup4 and lxml for HTML parsing
- Type hints and validation with Pydantic

## Requirements

- Python 3.8+
- BrightData account and credentials
- OpenAI API key

## Usage

```python
from crawl_toolkit import CrawlToolkit

# Initialize the toolkit
toolkit = CrawlToolkit(
    brightdata_username="your_username",
    brightdata_password="your_password",
    openai_api_key="your_openai_key"
)

# Crawl a website
result = await toolkit.crawl(
    url="https://example.com",
    max_pages=10
)

# Analyze content
analysis = await toolkit.analyze_content(result.content)
```

## Development

1. Clone the repository
2. Install development dependencies:
```bash
pip install -e ".[dev]"
```
3. Run tests:
```bash
pytest
```

## License

MIT License 