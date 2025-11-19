import asyncio
import aiohttp
import json
import re
import os
from datetime import datetime, timedelta
from typing import Optional, Any
import config
from browser_handler import BrowserHandler
from llm_handler import LLMHandler
from data_processor import DataProcessor

class QuizSolver:
    """Main quiz solving orchestrator"""
    
    def __init__(self):
        self.browser = BrowserHandler()
        self.llm = LLMHandler()
        self.processor = DataProcessor()
        self.start_time = None
        self.max_duration = timedelta(seconds=config.TIMEOUT_SECONDS)
        
    def is_time_remaining(self) -> bool:
        """Check if there's still time remaining for the quiz"""
        if not self.start_time:
            return True
        elapsed = datetime.now() - self.start_time
        return elapsed < self.max_duration
        
    async def solve_quiz_chain(self, initial_url: str, email: str, secret: str):
        """
        Solve a chain of quiz questions, following URLs until complete
        
        Args:
            initial_url: First quiz URL
            email: Student email
            secret: Student secret
        """
        self.start_time = datetime.now()
        current_url = initial_url
        attempt = 0
        
        try:
            await self.browser.start()
            
            while current_url and self.is_time_remaining():
                attempt += 1
                print(f"\n{'='*60}")
                print(f"Attempt {attempt}: Solving quiz at {current_url}")
                print(f"Time elapsed: {datetime.now() - self.start_time}")
                print(f"{'='*60}\n")
                
                try:
                    # Solve the current quiz
                    answer = await self.solve_single_quiz(current_url)
                    
                    # Submit the answer
                    submit_url = await self.extract_submit_url(current_url)
                    
                    if not submit_url:
                        print("Could not find submit URL in quiz page")
                        break
                        
                    result = await self.submit_answer(
                        submit_url=submit_url,
                        email=email,
                        secret=secret,
                        quiz_url=current_url,
                        answer=answer
                    )
                    
                    print(f"Submission result: {result}")
                    
                    # Check if correct and get next URL
                    if result.get("correct"):
                        print("✓ Answer was CORRECT!")
                        next_url = result.get("url")
                        if next_url:
                            print(f"Moving to next quiz: {next_url}")
                            current_url = next_url
                        else:
                            print("No more quizzes. Quiz chain complete!")
                            break
                    else:
                        print(f"✗ Answer was INCORRECT: {result.get('reason', 'No reason provided')}")
                        # Check if we got a next URL anyway
                        next_url = result.get("url")
                        if next_url:
                            print(f"Skipping to next quiz: {next_url}")
                            current_url = next_url
                        else:
                            # Retry if time permits
                            if self.is_time_remaining():
                                print("Retrying current quiz...")
                                continue
                            else:
                                print("Time limit exceeded. Stopping.")
                                break
                                
                except Exception as e:
                    print(f"Error solving quiz: {e}")
                    import traceback
                    traceback.print_exc()
                    
                    if not self.is_time_remaining():
                        break
                        
        finally:
            await self.browser.stop()
            
    async def solve_single_quiz(self, url: str) -> Any:
        """
        Solve a single quiz question
        
        Args:
            url: Quiz page URL
            
        Returns:
            The answer to submit
        """
        # Fetch the quiz page
        page_data = await self.browser.fetch_quiz_page(url)
        quiz_text = page_data["decoded_content"]
        
        print(f"Quiz content:\n{quiz_text[:500]}...\n")
        
        # Extract task instructions
        task_description = self.extract_task_description(quiz_text)
        
        # Check if we need to download any files
        file_urls = self.extract_file_urls(quiz_text)
        downloaded_files = []
        
        for file_url in file_urls:
            try:
                filename = os.path.basename(file_url.split('?')[0])
                if not filename:
                    filename = f"download_{len(downloaded_files)}.dat"
                    
                file_path = os.path.join(config.DOWNLOAD_DIR, filename)
                print(f"Downloading file from {file_url}...")
                await self.browser.download_file(file_url, file_path)
                downloaded_files.append(file_path)
                print(f"Downloaded to {file_path}")
            except Exception as e:
                print(f"Error downloading {file_url}: {e}")
                
        # Build context for LLM
        context = {
            "quiz_text": quiz_text,
            "downloaded_files": downloaded_files
        }
        
        # If we have data files, analyze them
        if downloaded_files:
            for file_path in downloaded_files:
                try:
                    file_summary = self.processor.get_data_summary(file_path)
                    context[f"file_summary_{os.path.basename(file_path)}"] = file_summary
                except Exception as e:
                    print(f"Error summarizing {file_path}: {e}")
                    
        # Use LLM to solve the task
        print("Asking LLM to solve the task...")
        llm_response = await self.llm.solve_task(task_description, context)
        print(f"LLM response:\n{llm_response}\n")
        
        # Extract the final answer
        answer = await self.llm.extract_answer_from_response(llm_response)
        print(f"Extracted answer: {answer}")
        
        return answer
        
    def extract_task_description(self, quiz_text: str) -> str:
        """Extract the main task description from quiz text"""
        # The task description is typically the readable text
        # Remove HTML tags if any remain
        text = re.sub(r'<[^>]+>', '', quiz_text)
        return text.strip()
        
    def extract_file_urls(self, quiz_text: str) -> list:
        """Extract file download URLs from quiz text"""
        # Look for URLs in href attributes or plain text
        urls = []
        
        # Find href URLs
        href_pattern = r'href=["\']([^"\']+)["\']'
        urls.extend(re.findall(href_pattern, quiz_text))
        
        # Find plain URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls.extend(re.findall(url_pattern, quiz_text))
        
        # Filter for likely file URLs (not the submit endpoint)
        file_extensions = ['.pdf', '.csv', '.xlsx', '.xls', '.json', '.txt', '.zip']
        file_urls = [url for url in urls if any(ext in url.lower() for ext in file_extensions)]
        
        return list(set(file_urls))  # Remove duplicates
        
    async def extract_submit_url(self, quiz_url: str) -> Optional[str]:
        """
        Extract the submit URL from the quiz page
        
        Args:
            quiz_url: The quiz page URL
            
        Returns:
            Submit endpoint URL
        """
        page_data = await self.browser.fetch_quiz_page(quiz_url)
        quiz_text = page_data["decoded_content"]
        
        # Look for submit URL patterns
        submit_patterns = [
            r'Post your answer to (https?://[^\s<>"{}|\\^`\[\]]+)',
            r'submit[^h]+(https?://[^\s<>"{}|\\^`\[\]]+)',
            r'POST[^h]+(https?://[^\s<>"{}|\\^`\[\]]+)',
        ]
        
        for pattern in submit_patterns:
            matches = re.findall(pattern, quiz_text, re.IGNORECASE)
            if matches:
                return matches[0].strip()
                
        # If no pattern matched, look for any submit-like URL
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        all_urls = re.findall(url_pattern, quiz_text)
        
        for url in all_urls:
            if 'submit' in url.lower():
                return url
                
        print("Warning: Could not find submit URL in quiz page")
        return None
        
    async def submit_answer(self, submit_url: str, email: str, secret: str, 
                          quiz_url: str, answer: Any) -> dict:
        """
        Submit an answer to the quiz endpoint
        
        Args:
            submit_url: Endpoint to submit to
            email: Student email
            secret: Student secret
            quiz_url: Original quiz URL
            answer: The answer to submit
            
        Returns:
            Response from server
        """
        payload = {
            "email": email,
            "secret": secret,
            "url": quiz_url,
            "answer": answer
        }
        
        print(f"Submitting to {submit_url}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    submit_url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    status = response.status
                    result = await response.json()
                    
                    print(f"Response status: {status}")
                    return result
                    
        except Exception as e:
            print(f"Error submitting answer: {e}")
            return {"correct": False, "error": str(e)}
