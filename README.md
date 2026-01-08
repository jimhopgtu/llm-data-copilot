# LLM Data Copilot

> An AI-powered data analyst that uses MCP (Model Context Protocol) tools to query databases, analyze files, and provide intelligent insights through natural language.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Next.js](https://img.shields.io/badge/next.js-16.0+-black.svg)

**Built in 3 days | $0 monthly cost | Full MCP architecture**

---

## 🌟 Features

- **Natural Language Database Queries** - Ask questions about your data in plain English
- **File Management** - List, read, and analyze files through conversation
- **Multi-Tool Orchestration** - AI automatically combines multiple data sources
- **Real-Time Tool Transparency** - See exactly which tools the AI uses and their results
- **Modern Chat Interface** - Clean, responsive UI built with Next.js and Tailwind CSS
- **Semantic Document Search (Optional)** - RAG with Hugging Face embeddings

## 🎥 Demo

*Working locally with full functionality - database queries, file operations, and intelligent analysis*

Try asking:
- "What's the total revenue by category?"
- "Which customer has the most orders?"
- "Read the Q1 report and summarize it"
- "Compare database numbers to what the report says"

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 20+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation (Windows)

```bash
# 1. Clone the repository
git clone https://github.com/jimhopgtu/llm-data-copilot.git
cd llm-data-copilot

# 2. Run setup script
setup.bat

# 3. Add your Groq API key
# Create backend/.env and add:
# GROQ_API_KEY=your_key_here

# 4. Start the application
start.bat
```

### Installation (Mac/Linux)

```bash
# 1. Clone the repository
git clone https://github.com/jimhopgtu/llm-data-copilot.git
cd llm-data-copilot

# 2. Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# 3. Setup frontend
cd frontend
npm install  # or yarn install
cd ..

# 4. Initialize database
cd data
python3 init_db.py
cd ..

# 5. Add your Groq API key
echo "GROQ_API_KEY=your_key_here" > backend/.env

# 6. Start backend (Terminal 1)
cd backend
source venv/bin/activate
uvicorn app:app --reload --port 8000

# 7. Start frontend (Terminal 2)
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser!

## 🏗️ Architecture

```
llm-data-copilot/
├── backend/              # FastAPI server
│   ├── app.py           # Main API endpoints
│   ├── services/        
│   │   ├── llm_service.py      # Groq LLM integration
│   │   └── vector_store.py     # HuggingFace embeddings + ChromaDB
│   └── mcp_tools/       # MCP tool implementations
│       ├── file_tools.py       # File operations
│       ├── db_tools.py         # Database queries
│       └── search_tools.py     # Document search (optional)
├── frontend/            # Next.js UI
│   └── app/
│       ├── page.tsx            # Chat interface
│       └── components/
│           └── FileUpload.tsx  # File upload component
└── data/
    ├── documents/       # Your files
    └── sample.db        # SQLite database
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Groq API** - Fast LLM inference (Llama 3.3 70B)
- **Hugging Face Transformers** - Local embeddings (all-MiniLM-L6-v2)
- **ChromaDB** - Vector database for semantic search
- **SQLite** - Sample database with e-commerce data

### Frontend
- **Next.js 16** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling

## 📖 Usage Examples

### Database Queries
```
"What's the total revenue by category?"
"Which customer has the most orders?"
"Show me sales trends by channel"
"What's the average order value?"
```

### File Operations
```
"What files are available?"
"Read the sales_summary.csv file"
"Summarize the Q1 report"
```

### Multi-Tool Analysis
```
"Compare database revenue to what the report claims"
"Which products are mentioned in files but not in the database?"
```

## 🔧 Available MCP Tools

| Tool | Description | Example Use |
|------|-------------|-------------|
| `files_list` | List available files | Inventory of documents |
| `files_read` | Read file contents | View raw file data |
| `sqlite_query` | Execute SQL queries | Database analytics |
| `doc_index` | Index documents for search | Prepare documents for RAG |
| `doc_search` | Semantic document search | Find relevant content |
| `doc_list` | List indexed documents | See what's searchable |

## 🎯 Key Concepts

### MCP (Model Context Protocol)
A standardized way to define tools that LLMs can call. Each tool has:
- **Name** - Identifier for the tool
- **Description** - What the tool does
- **Parameters** - JSON schema of inputs
- **Implementation** - Python function that executes the tool

### Tool Transparency
Unlike black-box AI, you can see:
- Which tools were called
- What arguments were passed
- What results were returned
- How the LLM used the results

This makes the system debuggable, trustworthy, and educational.

## 📊 Sample Data

The project includes a sample e-commerce database with:
- **200 orders** across 4 sales channels (Website, Mobile App, In-Store, Phone)
- **5 customers** with purchase history
- **7 products** in 4 categories (Electronics, Furniture, Office Supplies, Appliances)
- Date range: January 2024 - December 2024
- Total revenue: ~$194,000

Sample queries work out of the box - perfect for testing and demos!

## 💰 Cost Breakdown

| Component | Cost |
|-----------|------|
| Groq API (30 req/min) | **$0/month** |
| HuggingFace models (local) | **$0/month** |
| ChromaDB (local) | **$0/month** |
| SQLite | **$0/month** |
| **Total** | **$0/month** 🎉 |

**Compare to alternatives:**
- OpenAI GPT-4 + Embeddings: ~$50-100/month
- Pinecone Vector DB: $70/month
- Claude API: $15-50/month

## 🧪 Testing

### Run Tests
```bash
# Backend tests
cd backend
pytest

# Test vector store
python test_vector_store.py

# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/tools
```

### Manual Testing
Open http://localhost:3000 and try:
1. "What files are available?" → Should list documents
2. "What's the total revenue by category?" → Should query database
3. "Read q1_report.txt" → Should show file content
4. Upload a file → Should process successfully

## 🚢 Deployment

### Option 1: Local Demo (Recommended)
Perfect for:
- Portfolio demonstrations
- Technical interviews
- Full feature access (including RAG)
- No hosting costs

### Option 2: Railway/Render
For public deployment:
- Backend: Railway/Render free tier
- Frontend: Vercel free tier
- Note: RAG features require paid tier (>4GB image)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 🛣️ Roadmap

### Completed ✅
- [x] Natural language database queries
- [x] File operations (list, read)
- [x] Multi-tool orchestration
- [x] Modern chat interface
- [x] Tool transparency panel
- [x] Semantic document search (RAG)
- [x] File upload capability

### Future Enhancements
- [ ] Add authentication (NextAuth.js)
- [ ] Add chart generation tool
- [ ] Add API integration tool (weather, stocks)
- [ ] Add conversation export
- [ ] Add dark mode
- [ ] Add streaming responses
- [ ] Support for PDF documents
- [ ] Multi-user support
- [ ] Persistent conversation history

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- [Groq](https://groq.com) - Fast LLM inference
- [Anthropic](https://anthropic.com) - MCP specification
- [Hugging Face](https://huggingface.co) - Open-source embeddings
- [ChromaDB](https://www.trychroma.com) - Vector database
- [FastAPI](https://fastapi.tiangolo.com) - Python web framework
- [Next.js](https://nextjs.org) - React framework

## 📧 Contact

**GitHub:** [jimhopgtu/llm-data-copilot](https://github.com/jimhopgtu/llm-data-copilot)

Questions? Open an issue!

---

**Built in 3 days as a learning project | Demonstrates full-stack AI development with MCP architecture**

⭐ Star this repo if you find it helpful!