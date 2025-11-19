from playwright.async_api import async_playwright, Browser, Page
import base64
import asyncio
from typing import Optional

class BrowserHandler:
    """Handles browser automation for fetching and rendering quiz pages"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.playwright = None
        
    async def start(self):
        """Initialize the browser"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        
    async def stop(self):
        """Close the browser"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
            
    async def fetch_quiz_page(self, url: str, wait_time: int = 3000) -> dict:
        """
        Fetch and render a quiz page, extracting the content
        
        Args:
            url: The quiz page URL
            wait_time: Time to wait for JavaScript rendering (ms)
            
        Returns:
            dict with 'html', 'text', and 'decoded_content' keys
        """
        if not self.browser:
            await self.start()
            
        page = await self.browser.new_page()
        
        try:
            # Navigate to the page
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Wait for JavaScript rendering
            await asyncio.sleep(wait_time / 1000)
            
            # Get the page content
            html = await page.content()
            text = await page.inner_text("body")
            
            # Try to find and decode base64 content if present
            decoded_content = None
            try:
                # Look for atob() calls in scripts
                result_element = await page.query_selector("#result")
                if result_element:
                    decoded_content = await result_element.inner_text()
            except Exception as e:
                print(f"Could not extract decoded content: {e}")
            
            return {
                "html": html,
                "text": text,
                "decoded_content": decoded_content or text
            }
            
        finally:
            await page.close()
            
    async def download_file(self, url: str, save_path: str) -> str:
        """
        Download a file from a URL
        
        Args:
            url: URL to download from
            save_path: Path to save the file
            
        Returns:
            Path to the downloaded file
        """
        if not self.browser:
            await self.start()
            
        page = await self.browser.new_page()
        
        try:
            # Set up download handling
            async with page.expect_download() as download_info:
                await page.goto(url)
            
            download = await download_info.value
            await download.save_as(save_path)
            return save_path
            
        except Exception as e:
            # If direct download fails, try alternative method
            print(f"Download via browser failed: {e}, trying direct request")
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.read()
                        with open(save_path, 'wb') as f:
                            f.write(content)
                        return save_path
            raise
            
        finally:
            await page.close()
