import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class SimpleBrowserHandler:
    """Simplified browser handler using aiohttp + BeautifulSoup for Vercel deployment"""
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_page_content(self, url: str) -> Optional[str]:
        """
        Get page content using aiohttp (works for static content)
        """
        try:
            logger.info(f"Fetching content from: {url}")
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Parse with BeautifulSoup for text extraction
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    # Get text content
                    text_content = soup.get_text()
                    
                    # Clean up whitespace
                    lines = (line.strip() for line in text_content.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text_content = ' '.join(chunk for chunk in chunks if chunk)
                    
                    logger.info(f"Successfully extracted {len(text_content)} characters")
                    return text_content
                else:
                    logger.error(f"Failed to fetch {url}: HTTP {response.status}")
                    return None
                    
        except asyncio.TimeoutError:
            logger.error(f"Timeout while fetching {url}")
            return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None