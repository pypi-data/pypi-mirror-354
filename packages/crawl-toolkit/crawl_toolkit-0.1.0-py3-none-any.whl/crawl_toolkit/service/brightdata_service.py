from typing import Dict, Any, Optional, List
import aiohttp
from pydantic import BaseModel

class BrightDataService:
    """Service for handling BrightData proxy interactions."""
    
    def __init__(
        self,
        username: str,
        password: str,
        proxy_host: str = "brd.superproxy.io",
        proxy_port: int = 22225
    ):
        self.username = username
        self.password = password
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        
    def get_proxy_url(self, crawler_type: str) -> str:
        """
        Get proxy URL for specific crawler type.
        
        Args:
            crawler_type: Type of crawler to use
            
        Returns:
            Proxy URL
        """
        return f"http://{self.username}-{crawler_type}:{self.password}@{self.proxy_host}:{self.proxy_port}"
        
    async def make_request(
        self,
        url: str,
        crawler_type: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Make request through BrightData proxy.
        
        Args:
            url: Target URL
            crawler_type: Type of crawler to use
            method: HTTP method
            headers: Custom headers
            data: Request data
            timeout: Request timeout
            
        Returns:
            Response data
        """
        proxy_url = self.get_proxy_url(crawler_type)
        
        default_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        if headers:
            default_headers.update(headers)
            
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                url,
                proxy=proxy_url,
                headers=default_headers,
                json=data if data else None,
                timeout=timeout
            ) as response:
                return {
                    "status": response.status,
                    "headers": dict(response.headers),
                    "content": await response.text(),
                    "url": str(response.url)
                }
                
    async def crawl(
        self,
        url: str,
        crawler_type: str,
        max_pages: int = 1,
        follow_links: bool = False,
        custom_headers: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Crawl website using BrightData proxy.
        
        Args:
            url: Target URL
            crawler_type: Type of crawler to use
            max_pages: Maximum number of pages to crawl
            follow_links: Whether to follow links
            custom_headers: Custom headers
            
        Returns:
            List of crawl results
        """
        results = []
        visited_urls = set()
        urls_to_visit = [url]
        
        while urls_to_visit and len(results) < max_pages:
            current_url = urls_to_visit.pop(0)
            if current_url in visited_urls:
                continue
                
            result = await self.make_request(
                current_url,
                crawler_type,
                headers=custom_headers
            )
            results.append(result)
            visited_urls.add(current_url)
            
            if follow_links and len(results) < max_pages:
                # TODO: Implement link extraction and following
                pass
                
        return results 