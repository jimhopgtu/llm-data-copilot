from .file_tools import files_list, files_read
from .db_tools import sqlite_query
# from .search_tools import doc_index, doc_search, doc_list  # Commented out for deployment

# Tool registry (without RAG tools)
TOOLS = {
    "files_list": files_list,
    "files_read": files_read,
    "sqlite_query": sqlite_query,
}

def get_all_tools():
    """Return MCP tool definitions for Groq"""
    return [
        {
            "type": "function",
            "function": {
                "name": "files_list",
                "description": "List all available files in the data directory",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "files_read",
                "description": "Read the contents of a specific file",
                "parameters": {
                    "type": "object",
                    "properties": {"filename": {"type": "string", "description": "Name of the file to read"}},
                    "required": ["filename"]
                }
            }
        },
{
    "type": "function",
    "function": {
        "name": "sqlite_query",
        "description": "Execute a READ-ONLY SQL query on the SQLite database. Available tables: 'orders' (id, order_date, customer_id, product_name, category, quantity, price, total, channel) and 'customers' (id, name, email, signup_date, total_orders). Only SELECT queries are allowed.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "SQL SELECT query to execute. Example: SELECT category, SUM(total) as revenue FROM orders GROUP BY category"
                }
            },
            "required": ["query"]
        }
    }
}
    ]

async def execute_tool(tool_name: str, arguments: dict):
    if arguments is None:
        arguments = {}
    if tool_name not in TOOLS:
        return {"error": f"Tool {tool_name} not found"}
    tool_func = TOOLS[tool_name]
    return await tool_func(**arguments)
