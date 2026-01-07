from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from pathlib import Path

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
    model="llama-3.1-8b-instant"
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

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file to the documents directory"""
    try:
        # Security: validate file type
        allowed_extensions = {'.txt', '.csv', '.md'}
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            return {
                "success": False,
                "error": f"File type {file_ext} not allowed. Use: {', '.join(allowed_extensions)}"
            }
        
        # Save file
        data_dir = Path(os.getenv("DATA_DIR", "../data/documents"))
        file_path = data_dir / file.filename
        
        content = await file.read()
        with open(file_path, 'wb') as f:
            f.write(content)
        
        return {
            "success": True,
            "filename": file.filename,
            "message": f"File {file.filename} uploaded successfully"
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}