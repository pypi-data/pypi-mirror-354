# Crawl Toolkit

Narzędzie do crawlowania i analizy treści, które integruje się z BrightData do crawlowania stron internetowych i OpenAI do analizy treści.

## Instalacja

```bash
pip install crawl-toolkit
```

## Wymagania

- Python 3.8+
- Klucz API BrightData (SERP i Crawler)
- Klucz API OpenAI

## Przykład użycia

```python
from crawl_toolkit import CrawlToolkit, Language, FetchType

# Inicjalizacja
toolkit = CrawlToolkit(
    brightdata_serp_key="your_serp_key",
    brightdata_serp_zone="your_serp_zone",
    brightdata_crawl_key="your_crawl_key",
    brightdata_crawl_zone="your_crawl_zone",
    openai_key="your_openai_key"
)

# Pobieranie najlepszych URL-i dla słowa kluczowego
urls = await toolkit.get_top_urls(
    keyword="python programming",
    max_results=20,
    language=Language.ENGLISH
)

# Pobieranie i czyszczenie treści
contents = await toolkit.fetch_and_clean_urls(
    urls=urls,
    fetch_type=FetchType.MARKDOWN
)

# Analiza słów kluczowych
analysis = await toolkit.make_keyword_analysis(
    keyword="python programming",
    max_urls=20,
    language=Language.ENGLISH
)

# Analiza z nagłówkami
analysis_with_headers = await toolkit.make_keyword_analysis_and_headers(
    keyword="python programming",
    max_urls=20,
    language=Language.ENGLISH
)
```

## Funkcjonalności

- Pobieranie najlepszych URL-i z Google dla danego słowa kluczowego
- Pobieranie i czyszczenie treści z podanych URL-i
- Analiza słów kluczowych z użyciem OpenAI
- Wyodrębnianie nagłówków z treści
- Obsługa wielu języków
- Czyszczenie treści HTML i Markdown

## Licencja

MIT 