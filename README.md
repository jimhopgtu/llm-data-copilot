# LLM Data Copilot

An AI-powered data analyst that uses MCP (Model Context Protocol) tools to query databases, search documents, and provide intelligent insights through natural language.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Next.js](https://img.shields.io/badge/next.js-16.0+-black.svg)

## 🌐 Live Demo

**Try it now:** https://tranquil-endurance-production.up.railway.app

Ask questions like:
- "What's the total revenue by category?"
- "Which customer has the most orders?"
- "Show me orders from the Mobile App channel"

## 🌟 Features

- **Natural Language Database Queries**: Ask questions about your data in plain English
- **Semantic Document Search (RAG)**: Upload documents and ask questions about their content
- **Multi-Tool Orchestration**: AI automatically combines multiple data sources to answer complex questions
- **File Management**: List, read, and analyze files through conversation
- **Real-Time Tool Transparency**: See exactly which tools the AI uses and their results
- **Modern Chat Interface**: Clean, responsive UI built with Next.js and Tailwind CSS

## 🏗️ Architecture

```
llm-data-copilot/
├── backend/              # FastAPI server
│   ├── app.py           # Main API endpoints
│   ├── services/        # Core services
│   │   ├── llm_service.py      # Groq LLM integration
│   │   └── vector_store.py     # HuggingFace embeddings + ChromaDB
│   └── mcp_tools/       # MCP tool implementations
│       ├── file_tools.py       # File operations
│       ├── db_tools.py         # Database queries
│       └── search_tools.py     # Document search
├── frontend/            # Next.js UI
│   └── app/
│       ├── page.tsx            # Chat interface
│       └── components/
│           └── FileUpload.tsx  # File upload component
└── data/
    ├── documents/       # Uploaded files
    └── sample.db        # SQLite database
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Groq API**: Fast LLM inference (Llama 3.1 8B)
- **Hugging Face Transformers**: Local embeddings (all-MiniLM-L6-v2)
- **ChromaDB**: Vector database for semantic search
- **SQLite**: Sample database with e-commerce data

### Frontend
- **Next.js 16**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 20+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GROQ_API_KEY=your_groq_api_key_here
DATA_DIR=../data/documents
ALLOWED_DB_PATH=../data/sample.db
EOF

# Initialize sample database
cd ../data
python init_db.py

# Start backend server
cd ../backend
uvicorn app:app --reload --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies (use yarn if on network drive)
yarn install
# or: npm install

# Start development server
yarn dev
# or: npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser!

## 📖 Usage Examples

### Database Queries
```
"What's the total revenue by category?"
"Which customer has the most orders?"
"Show me sales trends by channel"
```

### Document Search (RAG)
```
"Index the quarterly_report.txt file"
"What does the report say about mobile growth?"
"Summarize the key findings from the report"
```

### Multi-Tool Orchestration
```
"Compare what the report says about electronics to the actual database numbers"
"How do the mobile sales numbers in the database compare to the report's claims?"
```

### File Operations
```
"What files are available?"
"Read the sales_summary.csv file"
"List all indexed documents"
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
- **Name**: Identifier for the tool
- **Description**: What the tool does
- **Parameters**: JSON schema of inputs
- **Implementation**: Python function that executes the tool

### RAG (Retrieval Augmented Generation)
Instead of relying solely on the LLM's training data:
1. **Chunk** documents into smaller pieces
2. **Embed** chunks into vectors using HuggingFace
3. **Store** vectors in ChromaDB
4. **Search** for relevant chunks using semantic similarity
5. **Augment** LLM prompt with retrieved content
6. **Generate** answer based on actual document content

### Vector Embeddings
Text converted to numerical vectors (384 dimensions) where semantic similarity = vector proximity:
```
"mobile sales grew" → [0.23, -0.45, 0.12, ...]
"app revenue increased" → [0.21, -0.43, 0.14, ...]  # Similar!
"database error" → [-0.67, 0.89, -0.23, ...]  # Different!
```

## 💰 Cost Breakdown

| Component | Cost |
|-----------|------|
| Groq API (30 req/min) | **$0/month** |
| HuggingFace models (local) | **$0/month** |
| ChromaDB (local) | **$0/month** |
| SQLite | **$0/month** |
| **Total** | **$0/month** 🎉 |

Compare to alternatives:
- OpenAI GPT-4 + Embeddings: ~$50-100/month
- Pinecone Vector DB: $70/month
- Claude API: $15-50/month

## 📊 Sample Data

The project includes a sample e-commerce database with:
- **200 orders** across 4 sales channels
- **5 customers** with purchase history
- **7 products** in 4 categories
- Date range: January 2024 - December 2024

Categories: Electronics, Furniture, Office Supplies, Appliances
Channels: Website, Mobile App, In-Store, Phone

## 🧪 Testing

### Backend Tests
```bash
cd backend

# Test vector store
python test_vector_store.py

# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/tools
```

### Frontend Tests
```bash
cd frontend
yarn test  # or: npm test
```

## 🚢 Deployment

### Backend (Railway/Render)
1. Push code to GitHub
2. Connect Railway/Render to your repo
3. Set environment variables (GROQ_API_KEY)
4. Deploy!

### Frontend (Vercel)
1. Push code to GitHub
2. Import project to Vercel
3. Set API URL environment variable
4. Deploy!

## 🛣️ Roadmap

- [ ] Add authentication (NextAuth.js)
- [ ] Add chart generation tool
- [ ] Add API integration tool (weather, stocks, etc.)
- [ ] Add conversation export
- [ ] Add dark mode
- [ ] Add streaming responses
- [ ] Add more vector databases (Pinecone, Weaviate)
- [ ] Add support for PDF documents
- [ ] Add multi-user support
- [ ] Add deployment guides

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

Questions? Open an issue or reach out!

---

**Built in 3 days | $0 cost | Production-ready**

⭐ Star this repo if you find it helpful!
