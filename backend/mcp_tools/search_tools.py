from typing import Dict, Any
from services.vector_store import VectorStore
from pathlib import Path
import os

# Initialize vector store (singleton pattern)
vector_store = None

def get_vector_store():
    global vector_store
    if vector_store is None:
        vector_store = VectorStore(persist_directory="../chroma_data")
    return vector_store

DATA_DIR = os.getenv("DATA_DIR", "../data/documents")

async def doc_index(filename: str) -> Dict[str, Any]:
    """Index a document for semantic search"""
    try:
        file_path = Path(DATA_DIR) / filename
        
        # Security check
        if not file_path.resolve().is_relative_to(Path(DATA_DIR).resolve()):
            return {"success": False, "error": "Access denied"}
        
        if not file_path.exists():
            return {"success": False, "error": f"File not found: {filename}"}
        
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Index it
        vs = get_vector_store()
        result = vs.index_document(filename, content)
        
        return result
    
    except Exception as e:
        return {"success": False, "error": str(e)}

async def doc_search(query: str, top_k: int = 3) -> Dict[str, Any]:
    """Search indexed documents for relevant content"""
    try:
        vs = get_vector_store()
        result = vs.search(query, top_k=top_k)
        return result
    
    except Exception as e:
        return {"success": False, "error": str(e)}

async def doc_list() -> Dict[str, Any]:
    """List all indexed documents"""
    try:
        vs = get_vector_store()
        result = vs.list_indexed_documents()
        return result
    
    except Exception as e:
        return {"success": False, "error": str(e)}