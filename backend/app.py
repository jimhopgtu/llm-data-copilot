from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LLM Data Copilot")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    conversation_history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    response: str
    tool_calls: List[Dict[str, Any]] = []

@app.get("/health")
async def health():
    return {"status": "healthy", "groq_key_set": bool(os.getenv("GROQ_API_KEY"))}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    # For now, just echo back
    return ChatResponse(
        response=f"You said: {request.message}",
        tool_calls=[]
    )

@app.get("/api/tools")
async def list_tools():
    return {"tools": [], "message": "Tools coming next!"}