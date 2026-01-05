import os
from pathlib import Path
from typing import Dict, Any

DATA_DIR = os.getenv("DATA_DIR", "../data/documents")

async def files_list() -> Dict[str, Any]:
    """List all files in the data directory"""
    try:
        data_path = Path(DATA_DIR)
        
        # Create directory if it doesn't exist
        data_path.mkdir(parents=True, exist_ok=True)
        
        files = [f.name for f in data_path.iterdir() if f.is_file()]
        return {
            "success": True,
            "files": files,
            "count": len(files)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

async def files_read(filename: str) -> Dict[str, Any]:
    """Read contents of a file"""
    try:
        file_path = Path(DATA_DIR) / filename
        
        # Security: ensure file is within data directory
        data_dir_resolved = Path(DATA_DIR).resolve()
        if not file_path.resolve().is_relative_to(data_dir_resolved):
            return {"success": False, "error": "Access denied"}
        
        if not file_path.exists():
            return {"success": False, "error": f"File not found: {filename}"}
        
        # Read file (limit size for safety)
        MAX_SIZE = 1024 * 1024  # 1MB
        if file_path.stat().st_size > MAX_SIZE:
            return {"success": False, "error": "File too large (max 1MB)"}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "success": True,
            "filename": filename,
            "content": content,
            "size": len(content)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}