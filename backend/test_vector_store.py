from services.vector_store import VectorStore

# Initialize
vs = VectorStore()

# Test document
test_doc = """
Artificial Intelligence is transforming the world.
Machine learning models can now understand natural language.
Vector embeddings help find semantically similar content.
"""

# Index it
result = vs.index_document("test.txt", test_doc)
print("Index result:", result)

# Search it
search_result = vs.search("How does AI understand language?", top_k=2)
print("\nSearch result:", search_result)

# List documents
docs = vs.list_indexed_documents()
print("\nIndexed documents:", docs)