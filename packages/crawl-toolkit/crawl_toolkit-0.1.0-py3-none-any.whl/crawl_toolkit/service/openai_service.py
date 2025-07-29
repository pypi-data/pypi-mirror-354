from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from pydantic import BaseModel

class OpenAIService:
    """Service for handling OpenAI API interactions."""
    
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        
    async def analyze_content(
        self,
        content: str,
        prompt: str,
        model: str = "gpt-4-turbo-preview",
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Analyze content using OpenAI API.
        
        Args:
            content: Content to analyze
            prompt: System prompt to use
            model: OpenAI model to use
            max_tokens: Maximum tokens for response
            temperature: Response temperature
            
        Returns:
            Analysis results
        """
        response = await self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return {
            "analysis": response.choices[0].message.content,
            "usage": response.usage.dict()
        }
        
    async def extract_keywords(
        self,
        content: str,
        max_keywords: int = 10,
        min_length: int = 3
    ) -> List[str]:
        """
        Extract keywords from content.
        
        Args:
            content: Content to analyze
            max_keywords: Maximum number of keywords to extract
            min_length: Minimum keyword length
            
        Returns:
            List of extracted keywords
        """
        prompt = f"""Extract up to {max_keywords} most important keywords from the following content.
        Keywords should be at least {min_length} characters long.
        Return only the keywords, one per line."""
        
        response = await self.analyze_content(content, prompt)
        keywords = [
            keyword.strip()
            for keyword in response["analysis"].split("\n")
            if keyword.strip() and len(keyword.strip()) >= min_length
        ]
        
        return keywords[:max_keywords]
        
    async def analyze_sentiment(
        self,
        content: str,
        detailed: bool = False
    ) -> Dict[str, Any]:
        """
        Analyze sentiment of content.
        
        Args:
            content: Content to analyze
            detailed: Whether to return detailed analysis
            
        Returns:
            Sentiment analysis results
        """
        prompt = "Analyze the sentiment of the following content."
        if detailed:
            prompt += " Provide detailed analysis including positive and negative aspects."
            
        return await self.analyze_content(content, prompt) 