from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
import asyncio
from typing import Optional
import config
from quiz_solver import QuizSolver

app = FastAPI(title="LLM Analysis Quiz API")

class QuizRequest(BaseModel):
    email: str
    secret: str
    url: str

class QuizResponse(BaseModel):
    status: str
    message: str

@app.post("/quiz", response_model=QuizResponse)
async def handle_quiz(request: QuizRequest):
    """
    Handle incoming quiz requests.
    Verify credentials and start quiz solving process.
    """
    # Verify email and secret
    if request.email != config.EMAIL:
        raise HTTPException(status_code=403, detail="Invalid email")
    
    if request.secret != config.SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")
    
    # Start quiz solving in background
    solver = QuizSolver()
    asyncio.create_task(solver.solve_quiz_chain(request.url, request.email, request.secret))
    
    return QuizResponse(
        status="accepted",
        message=f"Quiz solving started for {request.url}"
    )

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "running", "service": "LLM Analysis Quiz Solver"}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    return {"error": str(exc), "status": "error"}

def main():
    """Start the FastAPI server"""
    print(f"Starting server on {config.HOST}:{config.PORT}")
    print(f"Configured for email: {config.EMAIL}")
    uvicorn.run(app, host=config.HOST, port=config.PORT)

if __name__ == "__main__":
    main()
