import asyncio
import logging
from typing import Dict, Any
from simple_browser_handler import SimpleBrowserHandler
from llm_handler import LLMHandler

logger = logging.getLogger(__name__)

class QuizSolver:
    """Simplified quiz solver for Vercel deployment (no Playwright)"""
    
    def __init__(self):
        self.llm_handler = LLMHandler()
    
    async def solve_quiz(self, quiz_url: str, email: str, secret: str) -> Dict[str, Any]:
        """
        Solve a quiz by analyzing the webpage content and generating answers using LLM
        """
        try:
            logger.info(f"Starting quiz solve for URL: {quiz_url}")
            logger.info("Using simplified browser handler for Vercel")
            
            # Extract quiz content using simplified browser handler
            async with SimpleBrowserHandler() as browser:
                content = await browser.get_page_content(quiz_url)
                
                if not content:
                    return {
                        "success": False,
                        "error": "Failed to extract content from quiz page",
                        "browser_type": "simple_http"
                    }
                
                logger.info(f"Extracted {len(content)} characters from quiz page")
            
            # Analyze content and generate answers using LLM
            quiz_analysis = await self.llm_handler.analyze_quiz_content(content, quiz_url)
            
            return {
                "success": True,
                "quiz_url": quiz_url,
                "content_length": len(content),
                "analysis": quiz_analysis,
                "browser_type": "simple_http",
                "extraction_method": "http_request_beautifulsoup",
                "note": "Deployed on Vercel with simplified browser handling"
            }
            
        except Exception as e:
            logger.error(f"Error solving quiz: {str(e)}")
            return {
                "success": False,
                "error": f"Quiz solving failed: {str(e)}",
                "browser_type": "simple_http"
            }