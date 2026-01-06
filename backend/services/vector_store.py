from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Any
import hashlib

class VectorStore:
    def __init__(self, persist_directory: str = "./chroma_data"):
        """Initialize vector store with Hugging Face embeddings"""
        # Initialize embedding model (local, free!)
        print("Loading embedding model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Embedding model loaded")
        
        # Create persist directory if it doesn't exist
        import os
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"description": "Document chunks with embeddings"}
        )
        
        print(f"✅ Vector store initialized at {persist_directory}")
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < text_len:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size * 0.5:  # At least 50% through
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return chunks
    
    def index_document(self, filename: str, content: str) -> Dict[str, Any]:
        """Index a document by chunking and embedding it"""
        try:
            # Chunk the document
            chunks = self._chunk_text(content)
            
            if not chunks:
                return {"success": False, "error": "No content to index"}
            
            # Generate embeddings
            embeddings = self.model.encode(chunks).tolist()
            
            # Create unique IDs for each chunk
            doc_id = hashlib.md5(filename.encode()).hexdigest()[:8]
            ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
            
            # Create metadata
            metadatas = [
                {
                    "filename": filename,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
                for i in range(len(chunks))
            ]
            
            # Add to ChromaDB
            self.collection.add(
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            
            return {
                "success": True,
                "filename": filename,
                "chunks_indexed": len(chunks),
                "message": f"Indexed {len(chunks)} chunks from {filename}"
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """Search for relevant document chunks"""
        try:
            # Generate query embedding
            query_embedding = self.model.encode([query])[0].tolist()
            
            # Search ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            # Format results
            matches = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    matches.append({
                        "text": doc,
                        "filename": results['metadatas'][0][i]['filename'],
                        "chunk_index": results['metadatas'][0][i]['chunk_index'],
                        "distance": results['distances'][0][i] if 'distances' in results else None
                    })
            
            return {
                "success": True,
                "query": query,
                "matches": matches,
                "count": len(matches)
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_indexed_documents(self) -> Dict[str, Any]:
        """List all indexed documents"""
        try:
            # Get all items from collection
            results = self.collection.get()
            
            # Extract unique filenames
            filenames = set()
            if results['metadatas']:
                for metadata in results['metadatas']:
                    filenames.add(metadata['filename'])
            
            return {
                "success": True,
                "documents": list(filenames),
                "total_chunks": len(results['ids']) if results['ids'] else 0
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}