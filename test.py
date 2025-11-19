"""
Test script for the quiz solver
"""
import asyncio
import sys
from quiz_solver import QuizSolver
import config

async def test_demo_quiz():
    """Test with the demo quiz endpoint"""
    
    print("Testing Quiz Solver")
    print("=" * 60)
    print(f"Email: {config.EMAIL}")
    print(f"Secret: {'*' * len(config.SECRET)}")
    print("=" * 60)
    
    if not config.EMAIL or not config.SECRET:
        print("\nERROR: Please configure EMAIL and SECRET in .env file")
        return
        
    if not config.OPENAI_API_KEY:
        print("\nERROR: Please configure OPENAI_API_KEY in .env file")
        return
    
    solver = QuizSolver()
    
    # Test with demo endpoint
    demo_url = "https://tds-llm-analysis.s-anand.net/demo"
    
    print(f"\nSolving demo quiz at: {demo_url}\n")
    
    try:
        await solver.solve_quiz_chain(
            initial_url=demo_url,
            email=config.EMAIL,
            secret=config.SECRET
        )
        print("\n✓ Test completed!")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_browser():
    """Test browser functionality"""
    from browser_handler import BrowserHandler
    
    print("\nTesting Browser Handler...")
    browser = BrowserHandler()
    
    try:
        await browser.start()
        print("✓ Browser started successfully")
        
        # Test fetching a page
        result = await browser.fetch_quiz_page("https://example.com")
        print(f"✓ Page fetched, length: {len(result['text'])} chars")
        
        await browser.stop()
        print("✓ Browser stopped successfully")
        
    except Exception as e:
        print(f"✗ Browser test failed: {e}")
        
async def test_llm():
    """Test LLM functionality"""
    from llm_handler import LLMHandler
    
    if not config.OPENAI_API_KEY:
        print("\n✗ Cannot test LLM: OPENAI_API_KEY not configured")
        return
        
    print("\nTesting LLM Handler...")
    llm = LLMHandler()
    
    try:
        response = await llm.solve_task("What is 2 + 2?")
        print(f"✓ LLM responded: {response[:100]}...")
        
        answer = await llm.extract_answer_from_response(response, "number")
        print(f"✓ Extracted answer: {answer}")
        
    except Exception as e:
        print(f"✗ LLM test failed: {e}")

def main():
    """Run tests based on command line arguments"""
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
        
        if test_type == "browser":
            asyncio.run(test_browser())
        elif test_type == "llm":
            asyncio.run(test_llm())
        elif test_type == "demo":
            asyncio.run(test_demo_quiz())
        else:
            print(f"Unknown test type: {test_type}")
            print("Available tests: browser, llm, demo")
    else:
        # Run all tests
        print("Running all tests...\n")
        asyncio.run(test_browser())
        asyncio.run(test_llm())
        print("\n" + "=" * 60)
        print("To test with demo quiz, run: python test.py demo")
        print("=" * 60)

if __name__ == "__main__":
    main()
