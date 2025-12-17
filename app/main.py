# backend/app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from app.agent import process_query
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Chat Assistant API",
    description="A general-purpose AI assistant powered by LangChain and OpenRouter",
    version="1.0.0"
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What is the capital of France?"
            }
        }

class QueryResponse(BaseModel):
    response: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "The capital of France is Paris..."
            }
        }

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "AI Chat Assistant API is running",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "POST /query": "Send a message to the AI assistant",
            "GET /health": "Check API health status"
        }
    }

@app.post("/query", response_model=QueryResponse)
async def query_assistant(request: QueryRequest):
    """
    Main endpoint to process user queries
    
    Accepts any question and returns an AI-generated response.
    The AI can answer questions on any topic and use tools when needed.
    """
    try:
        # Validate input
        if not request.message or not request.message.strip():
            raise HTTPException(
                status_code=400, 
                detail="Message cannot be empty. Please provide a question or statement."
            )
        
        # Log the incoming query
        logger.info(f"Received query: {request.message[:100]}...")
        
        # Process the query through the agent
        response = await process_query(request.message)
        
        # Log the response
        logger.info(f"Generated response: {response[:100]}...")
        
        return QueryResponse(response=response)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in query_assistant: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="An internal error occurred while processing your request. Please try again."
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Chat Assistant",
        "api_version": "1.0.0"
    }

@app.get("/info")
async def info():
    """Get information about the AI assistant's capabilities"""
    return {
        "name": "AI Chat Assistant",
        "description": "A versatile AI assistant that can help with various tasks",
        "capabilities": [
            "Answer questions on any topic",
            "Provide explanations and tutorials",
            "Help with problem-solving",
            "Assist with learning and education",
            "Get real-time weather information",
            "Perform calculations",
            "Engage in creative discussions",
            "Offer recommendations and suggestions"
        ],
        "example_queries": [
            "What is quantum computing?",
            "Explain how photosynthesis works",
            "What's the weather in Pune?",
            "Calculate 15 * 23 + 47",
            "Write a short poem about technology",
            "How do I learn Python programming?",
            "What are the main causes of climate change?",
            "Explain the theory of relativity in simple terms"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)