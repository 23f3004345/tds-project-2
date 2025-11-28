import gradio as gr
import asyncio
import json
import logging
from typing import Dict, Any
from quiz_solver_vercel import QuizSolver
import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_credentials(email: str, secret: str) -> bool:
    """Verify student credentials"""
    return (
        email == config.EMAIL and 
        secret == config.SECRET
    )

async def solve_quiz_async(email: str, secret: str, quiz_url: str) -> Dict[str, Any]:
    """Async quiz solving function"""
    try:
        # Verify credentials
        if not verify_credentials(email, secret):
            return {
                "success": False,
                "error": "Invalid email or secret"
            }
        
        logger.info(f"Processing quiz request from {email}")
        logger.info(f"Quiz URL: {quiz_url}")
        
        # Initialize quiz solver
        solver = QuizSolver()
        
        # Solve the quiz
        result = await solver.solve_quiz(
            quiz_url=quiz_url,
            email=email,
            secret=secret
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in solve_quiz_async: {str(e)}")
        return {
            "success": False,
            "error": f"Quiz solving failed: {str(e)}"
        }

def solve_quiz_gradio(email: str, secret: str, quiz_url: str) -> str:
    """Gradio interface function - must be synchronous"""
    try:
        # Run the async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(solve_quiz_async(email, secret, quiz_url))
        loop.close()
        
        # Format the response
        if result["success"]:
            return json.dumps({
                "status": "SUCCESS",
                "message": "Quiz analyzed successfully",
                "data": result,
                "platform": "Hugging Face Spaces",
                "browser_type": "simple_http"
            }, indent=2)
        else:
            return json.dumps({
                "status": "ERROR", 
                "error": result.get("error", "Unknown error"),
                "platform": "Hugging Face Spaces"
            }, indent=2)
            
    except Exception as e:
        return json.dumps({
            "status": "ERROR",
            "error": f"Internal error: {str(e)}",
            "platform": "Hugging Face Spaces"
        }, indent=2)

def health_check() -> str:
    """Health check function"""
    return json.dumps({
        "status": "healthy",
        "platform": "Hugging Face Spaces",
        "llm_provider": config.LLM_PROVIDER,
        "email_configured": config.EMAIL,
        "browser_type": "simple_http",
        "note": "TDS Project 2 Quiz Solver API"
    }, indent=2)

# Create Gradio interface
with gr.Blocks(
    title="TDS Project 2 - Quiz Solver",
    theme=gr.themes.Soft(),
    css=".gradio-container {max-width: 800px; margin: auto;}"
) as demo:
    
    gr.Markdown("""
    # 🧠 TDS Project 2 - Quiz Solver API
    
    **LLM-powered quiz solving service using IIT Madras AI Pipeline**
    
    This service analyzes quiz content and provides AI-generated solutions.
    """)
    
    with gr.Tab("🎯 Quiz Solver"):
        gr.Markdown("### Solve Quiz")
        
        with gr.Row():
            with gr.Column():
                email_input = gr.Textbox(
                    label="📧 Email",
                    placeholder="your-email@ds.study.iitm.ac.in",
                    value="23f3004345@ds.study.iitm.ac.in"
                )
                secret_input = gr.Textbox(
                    label="🔑 Secret", 
                    placeholder="your-secret",
                    type="password",
                    value="my-secure-secret-123"
                )
                quiz_url_input = gr.Textbox(
                    label="🌐 Quiz URL",
                    placeholder="https://example.com/quiz",
                    lines=2
                )
                
                solve_btn = gr.Button("🚀 Solve Quiz", variant="primary", size="lg")
        
        with gr.Row():
            output = gr.Textbox(
                label="📊 Result",
                lines=15,
                max_lines=20,
                show_copy_button=True
            )
        
        solve_btn.click(
            fn=solve_quiz_gradio,
            inputs=[email_input, secret_input, quiz_url_input],
            outputs=output
        )
    
    with gr.Tab("💚 Health Check"):
        gr.Markdown("### API Health Status")
        
        health_btn = gr.Button("🔍 Check Health", variant="secondary")
        health_output = gr.Textbox(
            label="🏥 Health Status",
            lines=10,
            show_copy_button=True
        )
        
        health_btn.click(
            fn=health_check,
            outputs=health_output
        )
    
    with gr.Tab("📚 API Documentation"):
        gr.Markdown("""
        ### API Endpoints
        
        **Base URL**: `https://your-space-name.hf.space`
        
        #### 1. Health Check
        ```http
        GET /health
        ```
        
        #### 2. Solve Quiz
        ```http
        POST /quiz
        Content-Type: application/json
        
        {
            "email": "23f3004345@ds.study.iitm.ac.in",
            "secret": "my-secure-secret-123", 
            "quiz_url": "https://example.com/quiz"
        }
        ```
        
        ### Features
        - ✅ **IIT Madras AI Integration**: Uses institutional LLM pipeline
        - ✅ **Simplified Browser**: aiohttp + BeautifulSoup for content extraction
        - ✅ **No Sleep Issues**: Hugging Face Spaces keeps apps running
        - ✅ **Free Deployment**: Perfect for evaluation period
        - ✅ **Gradio Interface**: Easy testing and interaction
        
        ### Deployment Info
        - **Platform**: Hugging Face Spaces
        - **SDK**: Gradio 4.44.0
        - **Browser Type**: Simple HTTP (no Playwright)
        - **LLM Provider**: IIT Madras AI Pipeline
        """)

# Launch the app
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )