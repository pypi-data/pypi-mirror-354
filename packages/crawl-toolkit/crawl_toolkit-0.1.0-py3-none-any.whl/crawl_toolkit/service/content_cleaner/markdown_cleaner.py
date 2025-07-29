from typing import List, Optional
import re
from .abstract_cleaner import AbstractContentCleaner

class MarkdownCleaner(AbstractContentCleaner):
    """Markdown content cleaner implementation."""
    
    def __init__(self):
        self.link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
        self.image_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
        
    def clean(self, content: str) -> str:
        """
        Clean Markdown content.
        
        Args:
            content: Markdown content to clean
            
        Returns:
            Cleaned Markdown
        """
        # Remove HTML tags
        content = re.sub(r"<[^>]+>", "", content)
        
        # Remove multiple newlines
        content = re.sub(r"\n{3,}", "\n\n", content)
        
        # Remove multiple spaces
        content = re.sub(r" {2,}", " ", content)
        
        # Remove empty lines at start and end
        content = content.strip()
        
        return content
        
    def extract_links(self, content: str) -> List[str]:
        """
        Extract links from Markdown.
        
        Args:
            content: Markdown content
            
        Returns:
            List of links
        """
        links = []
        for match in self.link_pattern.finditer(content):
            url = match.group(2)
            if not url.startswith(("#", "javascript:", "mailto:", "tel:")):
                links.append(url)
        return links
        
    def extract_images(self, content: str) -> List[str]:
        """
        Extract images from Markdown.
        
        Args:
            content: Markdown content
            
        Returns:
            List of image URLs
        """
        images = []
        for match in self.image_pattern.finditer(content):
            url = match.group(2)
            if not url.startswith(("data:", "javascript:")):
                images.append(url)
        return images
        
    def normalize(self, content: str) -> str:
        """
        Normalize Markdown content.
        
        Args:
            content: Markdown content to normalize
            
        Returns:
            Normalized Markdown
        """
        # Clean first
        cleaned = self.clean(content)
        
        # Normalize headers
        for i in range(6, 0, -1):
            pattern = f"^{'#' * i}\\s+"
            replacement = f"{'#' * i} "
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.MULTILINE)
            
        # Normalize lists
        cleaned = re.sub(r"^[-*+]\s+", "- ", cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r"^\d+\.\s+", "1. ", cleaned, flags=re.MULTILINE)
        
        # Normalize code blocks
        cleaned = re.sub(r"```\s*\n", "```\n", cleaned)
        cleaned = re.sub(r"\n\s*```", "\n```", cleaned)
        
        # Normalize inline code
        cleaned = re.sub(r"`\s+", "`", cleaned)
        cleaned = re.sub(r"\s+`", "`", cleaned)
        
        return cleaned.strip() 