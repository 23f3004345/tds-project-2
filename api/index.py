import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr
import logging
import asyncio
from typing import Optional

# Import simplified components for Vercel
from quiz_solver_vercel import QuizSolver
import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TDS Project 2 - Quiz Solver API",
    description="LLM-powered quiz solving service (Vercel deployment)",
    version="1.0.0"
)

security = HTTPBearer(auto_error=False)

class QuizRequest(BaseModel):
    email: EmailStr
    secret: str
    quiz_url: str

def verify_credentials(email: str, secret: str) -> bool:
    """Verify student credentials"""
    return (
        email == config.EMAIL and 
        secret == config.SECRET
    )

@app.get("/")
async def root():
    """Root endpoint - API status"""
    return {
        "message": "TDS Project 2 Quiz Solver API",
        "version": "1.0.0",
        "deployment": "vercel",
        "status": "active",
        "endpoints": {
            "health": "/health",
            "quiz": "/quiz (POST)"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "deployment": "vercel",
        "llm_provider": config.LLM_PROVIDER,
        "email_configured": config.EMAIL,
        "browser_type": "simple_http"
    }

@app.post("/quiz")
async def solve_quiz(request: QuizRequest):
    """
    Solve a quiz using LLM analysis
    
    Args:
        request: Quiz request containing email, secret, and quiz_url
        
    Returns:
        Quiz solution and analysis
    """
    try:
        # Verify credentials
        if not verify_credentials(request.email, request.secret):
            logger.warning(f"Invalid credentials from {request.email}")
            raise HTTPException(
                status_code=403, 
                detail="Invalid email or secret"
            )
        
        logger.info(f"Processing quiz request from {request.email}")
        logger.info(f"Quiz URL: {request.quiz_url}")
        
        # Initialize quiz solver
        solver = QuizSolver()
        
        # Solve the quiz
        result = await solver.solve_quiz(
            quiz_url=request.quiz_url,
            email=request.email,
            secret=request.secret
        )
        
        if result["success"]:
            logger.info("Quiz solved successfully")
            return {
                "success": True,
                "message": "Quiz analyzed successfully",
                "data": result,
                "deployment_info": {
                    "platform": "vercel",
                    "browser_type": "simple_http",
                    "note": "Using aiohttp + BeautifulSoup (no Playwright)"
                }
            }
        else:
            logger.error(f"Quiz solving failed: {result.get('error')}")
            raise HTTPException(
                status_code=500,
                detail=f"Quiz solving failed: {result.get('error')}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# Vercel expects the app to be named 'app'
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)