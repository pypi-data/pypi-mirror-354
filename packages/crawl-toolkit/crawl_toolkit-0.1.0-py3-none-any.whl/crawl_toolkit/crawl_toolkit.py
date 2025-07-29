from typing import Optional, Dict, Any, List, Union
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from enum import Enum
import json
from dataclasses import dataclass

from .enum.language import Language
from .enum.fetch_type import FetchType
from .service.openai_service import OpenAIService
from .service.brightdata_service import BrightDataService
from .service.content_cleaner import ContentCleaner
from .prompts.keyword_analysis_prompt import KEYWORD_ANALYSIS_PROMPT

@dataclass
class CrawlResult:
    """Struktura wyników crawlowania"""
    url: str
    content: str
    headers: Dict[str, str]
    status_code: int
    error: Optional[str] = None

class CrawlToolkit:
    """Główna klasa pakietu do crawlowania i analizy treści"""
    
    def __init__(
        self,
        openai_api_key: str,
        brightdata_username: str,
        brightdata_password: str,
        brightdata_zone: str,
        language: Language = Language.ENGLISH
    ):
        """
        Inicjalizacja CrawlToolkit
        
        Args:
            openai_api_key: Klucz API OpenAI
            brightdata_username: Nazwa użytkownika Brightdata
            brightdata_password: Hasło Brightdata
            brightdata_zone: Strefa Brightdata
            language: Język analizy (domyślnie angielski)
        """
        self.openai_service = OpenAIService(openai_api_key)
        self.brightdata_service = BrightDataService(
            username=brightdata_username,
            password=brightdata_password,
            zone=brightdata_zone
        )
        self.content_cleaner = ContentCleaner()
        self.language = language

    async def get_top_urls(self, keyword: str, limit: int = 5) -> List[str]:
        """
        Pobiera najlepsze URL-e dla danego słowa kluczowego
        
        Args:
            keyword: Słowo kluczowe
            limit: Maksymalna liczba URL-i
            
        Returns:
            Lista URL-i
        """
        try:
            return await self.brightdata_service.get_top_urls(keyword, limit)
        except Exception as e:
            raise RuntimeError(f"Błąd podczas pobierania URL-i: {str(e)}")

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analizuje tekst używając OpenAI
        
        Args:
            text: Tekst do analizy
            
        Returns:
            Wyniki analizy
        """
        try:
            return await self.openai_service.analyze_text(text)
        except Exception as e:
            raise RuntimeError(f"Błąd podczas analizy tekstu: {str(e)}")

    async def clean_markdown(self, content: str) -> str:
        """
        Czyści treść w formacie Markdown
        
        Args:
            content: Treść do wyczyszczenia
            
        Returns:
            Wyczyszczona treść
        """
        try:
            return self.content_cleaner.clean_markdown(content)
        except Exception as e:
            raise RuntimeError(f"Błąd podczas czyszczenia Markdown: {str(e)}")

    async def clean_html(self, content: str) -> str:
        """
        Czyści treść w formacie HTML
        
        Args:
            content: Treść do wyczyszczenia
            
        Returns:
            Wyczyszczona treść
        """
        try:
            return self.content_cleaner.clean_html(content)
        except Exception as e:
            raise RuntimeError(f"Błąd podczas czyszczenia HTML: {str(e)}")

    async def fetch_and_clean_urls(
        self,
        urls: List[str],
        fetch_type: FetchType = FetchType.HTML
    ) -> List[CrawlResult]:
        """
        Pobiera i czyści treść z podanych URL-i
        
        Args:
            urls: Lista URL-i do pobrania
            fetch_type: Typ pobieranej treści
            
        Returns:
            Lista wyników crawlowania
        """
        try:
            results = []
            for url in urls:
                try:
                    content = await self.brightdata_service.fetch_url(url)
                    headers = await self.brightdata_service.get_headers(url)
                    
                    if fetch_type == FetchType.HTML:
                        cleaned_content = await self.clean_html(content)
                    elif fetch_type == FetchType.MARKDOWN:
                        cleaned_content = await self.clean_markdown(content)
                    else:
                        cleaned_content = content
                        
                    results.append(CrawlResult(
                        url=url,
                        content=cleaned_content,
                        headers=headers,
                        status_code=200
                    ))
                except Exception as e:
                    results.append(CrawlResult(
                        url=url,
                        content="",
                        headers={},
                        status_code=500,
                        error=str(e)
                    ))
            return results
        except Exception as e:
            raise RuntimeError(f"Błąd podczas pobierania i czyszczenia URL-i: {str(e)}")

    async def process_connection_phrase_to_content(
        self,
        connection_phrase: str,
        content: str
    ) -> Dict[str, Any]:
        """
        Przetwarza frazę połączeniową na podstawie treści
        
        Args:
            connection_phrase: Fraza połączeniowa
            content: Treść do analizy
            
        Returns:
            Wyniki przetwarzania
        """
        try:
            return await self.openai_service.process_connection_phrase(
                connection_phrase,
                content
            )
        except Exception as e:
            raise RuntimeError(f"Błąd podczas przetwarzania frazy: {str(e)}")

    async def get_headers_from_urls(self, urls: List[str]) -> List[Dict[str, str]]:
        """
        Pobiera nagłówki z podanych URL-i
        
        Args:
            urls: Lista URL-i
            
        Returns:
            Lista nagłówków
        """
        try:
            return await asyncio.gather(*[
                self.brightdata_service.get_headers(url)
                for url in urls
            ])
        except Exception as e:
            raise RuntimeError(f"Błąd podczas pobierania nagłówków: {str(e)}")

    async def make_keyword_analysis(
        self,
        keyword: str,
        content: str
    ) -> Dict[str, Any]:
        """
        Wykonuje analizę słów kluczowych
        
        Args:
            keyword: Główne słowo kluczowe
            content: Treść do analizy
            
        Returns:
            Wyniki analizy słów kluczowych
        """
        try:
            prompt = KEYWORD_ANALYSIS_PROMPT.format(
                keyword=keyword,
                language=self.language.value,
                content=content
            )
            
            response = await self.openai_service.analyze_text(prompt)
            return json.loads(response)
        except Exception as e:
            raise RuntimeError(f"Błąd podczas analizy słów kluczowych: {str(e)}")

    async def get_keywords_from_urls(
        self,
        keyword: str,
        urls: List[str],
        fetch_type: FetchType = FetchType.HTML
    ) -> Dict[str, Any]:
        """
        Pobiera i analizuje słowa kluczowe z podanych URL-i
        
        Args:
            keyword: Główne słowo kluczowe
            urls: Lista URL-i do analizy
            fetch_type: Typ pobieranej treści
            
        Returns:
            Wyniki analizy słów kluczowych
        """
        try:
            results = await self.fetch_and_clean_urls(urls, fetch_type)
            content = "\n\n".join([r.content for r in results if r.content])
            return await self.make_keyword_analysis(keyword, content)
        except Exception as e:
            raise RuntimeError(f"Błąd podczas analizy słów kluczowych z URL-i: {str(e)}")

    async def get_keywords_from_content(
        self,
        keyword: str,
        content: str
    ) -> Dict[str, Any]:
        """
        Analizuje słowa kluczowe z podanej treści
        
        Args:
            keyword: Główne słowo kluczowe
            content: Treść do analizy
            
        Returns:
            Wyniki analizy słów kluczowych
        """
        try:
            return await self.make_keyword_analysis(keyword, content)
        except Exception as e:
            raise RuntimeError(f"Błąd podczas analizy słów kluczowych z treści: {str(e)}")

    @staticmethod
    def get_available_languages() -> List[Dict[str, str]]:
        """
        Get available languages.
        
        Returns:
            List of available languages
        """
        return [
            {"code": lang.value, "name": lang.name}
            for lang in Language
        ]

    async def analyze_content(
        self,
        content: str,
        analysis_type: str = "general",
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Analyze content using OpenAI API.
        
        Args:
            content: Content to analyze
            analysis_type: Type of analysis to perform
            max_tokens: Maximum tokens for OpenAI response
            
        Returns:
            Analysis results
        """
        prompt = self._get_analysis_prompt(analysis_type)
        
        response = await self.openai_service.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ],
            max_tokens=max_tokens
        )
        
        return {
            "analysis": response.choices[0].message.content,
            "usage": response.usage.dict()
        }
        
    def _get_analysis_prompt(self, analysis_type: str) -> str:
        """Get the appropriate prompt for the analysis type."""
        prompts = {
            "general": "Analyze the following content and provide key insights:",
            "seo": "Analyze the following content for SEO optimization opportunities:",
            "sentiment": "Analyze the sentiment of the following content:",
            "keywords": "Extract and analyze key keywords from the following content:"
        }
        return prompts.get(analysis_type, prompts["general"])
        
    async def extract_links(self, content: str) -> List[str]:
        """Extract all links from HTML content."""
        soup = BeautifulSoup(content, "lxml")
        return [a.get("href") for a in soup.find_all("a", href=True)]
        
    async def extract_text(self, content: str) -> str:
        """Extract clean text from HTML content."""
        soup = BeautifulSoup(content, "lxml")
        return soup.get_text(separator=" ", strip=True) 