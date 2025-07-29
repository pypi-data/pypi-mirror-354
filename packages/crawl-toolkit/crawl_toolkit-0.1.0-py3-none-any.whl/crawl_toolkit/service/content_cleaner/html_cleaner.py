from typing import List, Optional
import re
from bs4 import BeautifulSoup
from .abstract_cleaner import AbstractContentCleaner

class HtmlCleaner(AbstractContentCleaner):
    """HTML content cleaner implementation."""
    
    def __init__(self):
        self.removable_tags = [
            "script", "style", "meta", "link", "noscript",
            "iframe", "object", "embed", "applet"
        ]
        self.removable_attrs = [
            "onclick", "onload", "onerror", "onmouseover",
            "onmouseout", "onkeypress", "onkeydown", "onkeyup"
        ]
        
    def clean(self, content: str) -> str:
        """
        Clean HTML content.
        
        Args:
            content: HTML content to clean
            
        Returns:
            Cleaned HTML
        """
        soup = BeautifulSoup(content, "lxml")
        
        # Remove unwanted tags
        for tag in self.removable_tags:
            for element in soup.find_all(tag):
                element.decompose()
                
        # Remove unwanted attributes
        for tag in soup.find_all(True):
            for attr in self.removable_attrs:
                if attr in tag.attrs:
                    del tag[attr]
                    
        # Remove comments
        for comment in soup.find_all(text=lambda text: isinstance(text, str) and text.strip().startswith("<!--")):
            comment.extract()
            
        # Remove empty tags
        for tag in soup.find_all():
            if len(tag.get_text(strip=True)) == 0:
                tag.decompose()
                
        return str(soup)
        
    def extract_links(self, content: str) -> List[str]:
        """
        Extract links from HTML.
        
        Args:
            content: HTML content
            
        Returns:
            List of links
        """
        soup = BeautifulSoup(content, "lxml")
        links = []
        
        for a in soup.find_all("a", href=True):
            href = a.get("href")
            if href and not href.startswith(("#", "javascript:", "mailto:", "tel:")):
                links.append(href)
                
        return links
        
    def extract_images(self, content: str) -> List[str]:
        """
        Extract images from HTML.
        
        Args:
            content: HTML content
            
        Returns:
            List of image URLs
        """
        soup = BeautifulSoup(content, "lxml")
        images = []
        
        for img in soup.find_all("img", src=True):
            src = img.get("src")
            if src and not src.startswith(("data:", "javascript:")):
                images.append(src)
                
        return images
        
    def normalize(self, content: str) -> str:
        """
        Normalize HTML content.
        
        Args:
            content: HTML content to normalize
            
        Returns:
            Normalized HTML
        """
        # Clean first
        cleaned = self.clean(content)
        
        # Normalize whitespace
        cleaned = re.sub(r"\s+", " ", cleaned)
        
        # Normalize quotes
        cleaned = cleaned.replace('"', '"').replace('"', '"')
        cleaned = cleaned.replace(''', "'").replace(''', "'")
        
        # Normalize line endings
        cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")
        
        return cleaned.strip() 