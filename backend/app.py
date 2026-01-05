from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

from services.llm_service import LLMService
from mcp_tools import get_all_tools

load_dotenv()

app = FastAPI(title="LLM Data Copilot")

# CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM service
llm_service = LLMService(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

class ChatRequest(BaseModel):
    message: str
    conversation_history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    response: str
    tool_calls: List[Dict[str, Any]] = []
    
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint - sends message to LLM with MCP tools"""
    try:
        result = await llm_service.chat(
            message=request.message,
            history=request.conversation_history,
            tools=get_all_tools()
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tools")
async def list_tools():
    """List all available MCP tools"""
    return {"tools": get_all_tools()}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "groq_key_set": bool(os.getenv("GROQ_API_KEY")),
        "tools_count": len(get_all_tools())
    }