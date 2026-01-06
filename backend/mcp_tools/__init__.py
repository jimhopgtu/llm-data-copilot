from .file_tools import files_list, files_read
from .db_tools import sqlite_query
from .search_tools import doc_index, doc_search, doc_list

# Tool registry
TOOLS = {
    "files_list": files_list,
    "files_read": files_read,
    "sqlite_query": sqlite_query,
    "doc_index": doc_index,
    "doc_search": doc_search,
    "doc_list": doc_list,
}

def get_all_tools():
    """Return MCP tool definitions for Groq"""
    return [
        {
            "type": "function",
            "function": {
                "name": "files_list",
                "description": "List all available files in the data directory",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "files_read",
                "description": "Read the contents of a specific file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Name of the file to read"
                        }
                    },
                    "required": ["filename"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "sqlite_query",
                "description": "Execute a READ-ONLY SQL query on the SQLite database. The database contains 'orders' table (id, order_date, customer_id, product_name, category, quantity, price, total, channel) and 'customers' table (id, name, email, signup_date, total_orders). Only SELECT queries are allowed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL SELECT query to execute"
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "doc_index",
                "description": "Index a document for semantic search. This chunks the document and creates embeddings so it can be searched later.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Name of the file to index"
                        }
                    },
                    "required": ["filename"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "doc_search",
                "description": "Search through the TEXT CONTENT of indexed documents using semantic similarity. Use this to answer questions like 'What does the report say about X?' or 'Find information about Y in the documents'. This searches actual document text, NOT the database.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The question or topic to search for in document content"
                        },
                        "top_k": {
                            "type": "integer",
                            "description": "Number of relevant text chunks to return (default 3)",
                            "default": 3
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "doc_list",
                "description": "List all documents that have been indexed for search",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
    ]

async def execute_tool(tool_name: str, arguments: dict):
    """Execute a tool by name"""
    if tool_name not in TOOLS:
        return {"error": f"Tool {tool_name} not found"}
    
    tool_func = TOOLS[tool_name]
    
    # Handle None arguments (tools with no parameters)
    if arguments is None:
        arguments = {}
    
    return await tool_func(**arguments)