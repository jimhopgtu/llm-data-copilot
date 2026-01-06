from groq import Groq
from typing import List, Dict, Any
import json
import os

class LLMService:
    def __init__(self, api_key: str, model: str = "llama-3.1-70b-versatile"):
        self.client = Groq(api_key=api_key)
        self.model = model
    
    async def chat(
        self, 
        message: str, 
        history: List[Dict[str, str]], 
        tools: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Send chat message to Groq with tool calling support
        """
        messages = self._build_messages(message, history)
        tool_calls_log = []
        
        try:
            # Initial LLM call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None,
                max_tokens=2000
            )
            
            assistant_message = response.choices[0].message
            
            # Handle tool calls if any
            if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    # Execute the tool
                    tool_result = await self._execute_tool(tool_name, tool_args)
                    
                    # Log for transparency
                    tool_calls_log.append({
                        "name": tool_name,
                        "arguments": tool_args,
                        "result": tool_result
                    })
                    
                    # Add tool result to conversation
                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [{
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments
                            }
                        }]
                    })
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result)
                    })
                
                # Get final response after tool execution
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=2000
                )
                final_text = final_response.choices[0].message.content
            else:
                final_text = assistant_message.content
            
            return {
                "response": final_text,
                "tool_calls": tool_calls_log
            }
        
        except Exception as e:
            return {
                "response": f"Error: {str(e)}",
                "tool_calls": []
            }
    
    def _build_messages(self, message: str, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Build message array from history"""
        messages = [
            {
                "role": "system", 
                "content": """You are a helpful data analyst assistant with access to several tools:

            1. files_list, files_read - For listing and reading raw file contents
            2. sqlite_query - For querying the database
            3. doc_index, doc_search, doc_list - For semantic search on indexed documents

            IMPORTANT: When a user asks questions about document CONTENT (like "what does the report say about X?"), you should:
            - First check if the document is indexed using doc_list
            - If not indexed, use doc_index to index it first
            - Then use doc_search with the user's question to find relevant content
            - Answer based on the search results

            Use files_read only when the user explicitly asks to "read" a file or wants the raw content.
            Use doc_search when they ask questions about what's IN a document."""
            }
        ]
        messages.extend(history)
        messages.append({"role": "user", "content": message})
        return messages
    
    async def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an MCP tool by name"""
        from mcp_tools import execute_tool
        return await execute_tool(tool_name, arguments)