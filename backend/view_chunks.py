from services.vector_store import VectorStore
from pathlib import Path

# Read the original file
with open("../data/documents/long_report.txt", 'r') as f:
    content = f.read()

print("ORIGINAL DOCUMENT:")
print("=" * 80)
print(content)
print("\n" + "=" * 80)

# Initialize vector store
vs = VectorStore()

# Chunk it (without indexing)
chunks = vs._chunk_text(content, chunk_size=500, overlap=50)

print(f"\nCHUNKED INTO {len(chunks)} PIECES:")
print("=" * 80)

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i} ({len(chunk)} chars) ---")
    print(chunk)
    print()