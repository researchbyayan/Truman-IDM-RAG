import pdfplumber
import os
from typing import List, Dict

def load_documents(docs_folder: str = "docs") -> List[Dict]:
    """Load all PDFs from the docs folder."""
    documents = []
    for filename in os.listdir(docs_folder):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(docs_folder, filename)
            try:
                with pdfplumber.open(path) as pdf:
                    text = "\n\n".join(
                        page.extract_text() or "" for page in pdf.pages
                    )
                    # Basic cleaning
                    text = " ".join(text.split())  # Remove extra whitespace
                    if text.strip():
                        documents.append({"source": filename, "text": text})
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return documents

# Test the loader
if __name__ == "__main__":
    docs = load_documents()
    print(f"✅ Loaded {len(docs)} documents")
    if docs:
        print(f"Sample document: {docs[0]['source']}")
        print(f"First 300 chars: {docs[0]['text'][:300]}...")
