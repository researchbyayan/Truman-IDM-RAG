from typing import List

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os
from ingest import load_documents

# Load embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# ChromaDB setup
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="truman_ids")

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """Simple sliding window chunker"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return [c for c in chunks if len(c.strip()) > 50]

def embed_and_store():
    """Embed documents and store in ChromaDB"""
    documents = load_documents()
    all_chunks = []
    metadatas = []
    ids = []
    
    for doc in documents:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            metadatas.append({"source": doc["source"], "chunk_id": i})
            ids.append(f"{doc['source']}_{i}")
    
    if all_chunks:
        embeddings = embedder.encode(all_chunks)
        collection.add(
            documents=all_chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
    print(f"✅ Stored {len(all_chunks)} chunks in vector database")

def retrieve(query: str, top_k: int = 5):
    """Semantic search"""
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    retrieved = []
    for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
        retrieved.append({
            "text": doc,
            "source": meta["source"],
            "distance": dist
        })
    return retrieved

# Run embedding on first load
if __name__ == "__main__":
    if collection.count() == 0:
        embed_and_store()
    else:
        print(f"✅ Database already has {collection.count()} chunks")
