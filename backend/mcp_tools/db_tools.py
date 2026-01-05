import sqlite3
import os
from typing import Dict, Any

DB_PATH = os.getenv("ALLOWED_DB_PATH", "../data/sample.db")

async def sqlite_query(query: str) -> Dict[str, Any]:
    """Execute a READ-ONLY SQLite query"""
    try:
        # Security: only allow SELECT queries
        query_upper = query.strip().upper()
        if not query_upper.startswith("SELECT"):
            return {
                "success": False,
                "error": "Only SELECT queries are allowed"
            }
        
        # Additional security: prevent certain dangerous keywords
        dangerous_keywords = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "CREATE"]
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return {
                    "success": False,
                    "error": f"Keyword '{keyword}' is not allowed"
                }
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Convert to list of dicts
        results = [dict(row) for row in rows]
        
        conn.close()
        
        return {
            "success": True,
            "rows": results,
            "count": len(results)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }