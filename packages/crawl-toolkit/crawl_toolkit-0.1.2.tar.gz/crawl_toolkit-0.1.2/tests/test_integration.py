import pytest
import asyncio
from crawl_toolkit import CrawlToolkit
from crawl_toolkit.enum.language import Language
from crawl_toolkit.enum.fetch_type import FetchType
import json

class TestCrawlToolkitIntegration:
    @pytest.fixture
    async def crawl_toolkit(self):
        toolkit = CrawlToolkit(
            brightdata_serp_key='9833a165-4293-472a-aa38-8fb3db907413',
            brightdata_serp_zone='serp_collab',
            brightdata_crawl_key='9833a165-4293-472a-aa38-8fb3db907413',
            brightdata_crawl_zone='web_unlocker1',
            openai_key='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',
            helpful_ai_instructions=''
        )
        return toolkit

    @pytest.mark.asyncio
    async def test_get_top_urls_returns_array_of_urls(self, crawl_toolkit):
        keyword = 'adidas Originals adidas Samba OG Cloud White B75806'
        max_results = 20

        urls = await crawl_toolkit.get_top_urls(keyword, max_results)

        assert isinstance(urls, list)
        assert len(urls) <= max_results

        for url in urls:
            assert isinstance(url, str)
            assert url.startswith('http')

    @pytest.mark.asyncio
    async def test_analyze_text_returns_analysis_result(self, crawl_toolkit):
        keyword = 'adidas Originals adidas Samba OG Cloud White B75806'
        max_results = 1

        urls = await crawl_toolkit.get_top_urls(keyword, max_results)
        result = await crawl_toolkit.fetch_and_clean_urls(urls)

        assert isinstance(result, list)
        assert len(result) > 0
        assert hasattr(result[0], 'url')
        assert hasattr(result[0], 'content')
        assert isinstance(result[0].url, str)
        assert isinstance(result[0].content, str)

    @pytest.mark.asyncio
    async def test_process_connection_to_phrase(self, crawl_toolkit):
        keyword = 'oprogramowanie biurowe'
        max_results = 18

        urls = await crawl_toolkit.get_top_urls(keyword, max_results)
        result = await crawl_toolkit.fetch_and_clean_urls(urls)

        analysis_result = []
        for item in result:
            analysis = await crawl_toolkit.process_connection_phrase_to_content(
                keyword,
                item.content
            )
            analysis_result.append({
                'url': item.url,
                'content': item.content,
                'analysis': analysis
            })

        assert isinstance(result, list)
        assert len(result) > 0
        assert hasattr(result[0], 'url')
        assert hasattr(result[0], 'content')
        assert isinstance(result[0].url, str)
        assert isinstance(result[0].content, str)
        assert len(analysis_result) > 0

    @pytest.mark.asyncio
    async def test_get_headers_from_urls(self, crawl_toolkit):
        keyword = 'adidas Originals adidas Samba OG Cloud White B75806'
        max_results = 5

        urls = await crawl_toolkit.get_top_urls(keyword, max_results)
        result = await crawl_toolkit.get_headers_from_urls(urls)

        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_make_keyword_analysis(self, crawl_toolkit):
        keywords = [
            'adidas Originals adidas Samba OG Cloud White B75806',
        ]

        output_file_results = 'keyword_analysis_results_open_ai.txt'

        for keyword in keywords:
            max_results = 20
            urls = await crawl_toolkit.get_top_urls(keyword, max_results)
            result = await crawl_toolkit.fetch_and_clean_urls(urls)
            
            analysis_result = await crawl_toolkit.make_keyword_analysis(
                keyword,
                result[0]['content'] if result else ""
            )

            # Zapisz wyniki do pliku
            with open(output_file_results, 'a', encoding='utf-8') as f:
                f.write(f"{json.dumps(analysis_result, ensure_ascii=False, indent=2)}\n")

        assert isinstance(analysis_result, dict)

    @pytest.mark.asyncio
    async def test_just_analysis(self, crawl_toolkit):
        keyword = "adidas Originals adidas Samba OG Cloud White B75806"
        max_results = 20

        analysis_result = await crawl_toolkit.make_keyword_analysis(
            keyword,
            max_urls=20,
            language=Language.ENGLISH
        )

        assert isinstance(analysis_result, dict)

    @pytest.mark.asyncio
    async def test_fetch_url(self, crawl_toolkit):
        url = 'https://nafalinauki.pl/komputer-kwantowy/'
        content = await crawl_toolkit.fetch_and_clean_urls([url], FetchType.MARKDOWN)
        
        # Zapisz zawartość do pliku
        with open('test_fetch_url_content.md', 'w', encoding='utf-8') as f:
            f.write(content[0]['content'] if content else "")

        assert isinstance(content, list)
        assert len(content) > 0
        assert isinstance(content[0]['content'], str)
        assert len(content[0]['content']) > 0 