'use client';

import FileUpload from './components/FileUpload';
import { useState } from 'react';

// Use environment variable for API URL
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

type Message = {
  role: 'user' | 'assistant';
  content: string;
  toolCalls?: Array<{
    name: string;
    arguments: any;
    result: any;
  }>;
};

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          conversation_history: messages.map(m => ({
            role: m.role,
            content: m.content
          }))
        })
      });

      const data = await response.json();
      
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        toolCalls: data.tool_calls
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, there was an error processing your request.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b px-6 py-4 shadow-sm">
          <h1 className="text-2xl font-bold text-gray-900">LLM Data Copilot</h1>
          <p className="text-sm text-gray-600">Ask questions about your data and documents</p>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 mt-20">
              <h2 className="text-xl font-semibold mb-4">Welcome! 👋</h2>
              <p className="mb-4">Try asking:</p>
              <div className="space-y-2 text-sm max-w-md mx-auto">
                <div className="bg-white p-3 rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                     onClick={() => setInput("What files are available?")}>
                  💾 "What files are available?"
                </div>
                <div className="bg-white p-3 rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                     onClick={() => setInput("What's the total revenue by category?")}>
                  📊 "What's the total revenue by category?"
                </div>
                <div className="bg-white p-3 rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                     onClick={() => setInput("Index the long_report.txt file")}>
                  📄 "Index the long_report.txt file"
                </div>
              </div>
            </div>
          )}

          {messages.map((message, idx) => (
            <div key={idx} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-3xl rounded-lg px-4 py-3 ${
                message.role === 'user' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-white border border-gray-200 shadow-sm'
              }`}>
                <div className="whitespace-pre-wrap">{message.content}</div>
                
                {/* Tool Calls Display */}
                {message.toolCalls && message.toolCalls.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <p className="text-xs font-semibold text-gray-600 mb-2">
                      🔧 Tools Used:
                    </p>
                    {message.toolCalls.map((tool, tidx) => (
                      <details key={tidx} className="mb-2 text-sm">
                        <summary className="text-xs text-gray-700 cursor-pointer hover:text-gray-900 font-medium">
                          <span className="font-mono bg-gray-100 px-2 py-1 rounded">{tool.name}</span>
                          {tool.result?.success ? 
                            <span className="ml-2 text-green-600">✓</span> : 
                            <span className="ml-2 text-red-600">✗</span>
                          }
                        </summary>
                        <div className="mt-2 text-xs bg-gray-50 p-3 rounded border border-gray-200">
                          <div className="mb-2">
                            <span className="font-semibold text-gray-700">Arguments:</span>
                            <pre className="mt-1 overflow-x-auto text-xs">
                              {JSON.stringify(tool.arguments, null, 2)}
                            </pre>
                          </div>
                          <div>
                            <span className="font-semibold text-gray-700">Result:</span>
                            <pre className="mt-1 overflow-x-auto text-xs max-h-40 overflow-y-auto">
                              {JSON.stringify(tool.result, null, 2)}
                            </pre>
                          </div>
                        </div>
                      </details>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-200 rounded-lg px-4 py-3 shadow-sm">
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                  <span className="text-gray-600">Thinking...</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="bg-white border-t p-4 shadow-lg">
          <div className="max-w-4xl mx-auto flex space-x-4">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question about your data..."
              className="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={2}
              disabled={loading}
            />
            <button
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
            >
              Send
            </button>
          </div>
        </div>
      </div>

      {/* Tool Panel Sidebar */}
      <div className="w-80 bg-white border-l p-4 overflow-y-auto">
        <h3 className="font-semibold mb-3 text-gray-900">Available Tools</h3>
        <FileUpload /> 
        <div className="space-y-2 text-sm">
          <ToolCard name="files_list" description="List available files" />
          <ToolCard name="files_read" description="Read file contents" />
          <ToolCard name="sqlite_query" description="Query the database" />
          <ToolCard name="doc_index" description="Index documents for search" />
          <ToolCard name="doc_search" description="Semantic document search" />
          <ToolCard name="doc_list" description="List indexed documents" />
        </div>

        <div className="mt-6 pt-6 border-t">
          <h3 className="font-semibold mb-2 text-sm text-gray-900">Tips</h3>
          <ul className="text-xs text-gray-600 space-y-1">
            <li>• Be specific in your questions</li>
            <li>• Index documents before searching</li>
            <li>• The AI will choose which tools to use</li>
            <li>• Click tool names to see details</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

function ToolCard({ name, description }: { name: string; description: string }) {
  return (
    <div className="p-3 bg-gray-50 rounded-lg border border-gray-200">
      <div className="font-mono text-xs text-blue-600 font-medium">{name}</div>
      <div className="text-gray-600 mt-1">{description}</div>
    </div>
  );
}