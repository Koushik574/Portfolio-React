from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
import os
from uuid import uuid4

# === CONFIGURATION ===
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "sai-rag-chatbot-index"
TXT_FILE_PATH = "Text-Files/rag_corpus.txt"

# === STEP 1: Load the corpus ===
with open(TXT_FILE_PATH, "r", encoding="utf-8") as file:
    text = file.read()

# === STEP 2: Chunk the text (simple line-based chunking for demo) ===
chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]

# === STEP 3: Generate embeddings ===
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks).tolist()  # Convert numpy arrays to lists for JSON serialization

# === STEP 4: Initialize Pinecone and connect to index ===
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

# === STEP 5: Upload to Pinecone ===
vectors = [
    {
        "id": str(uuid4()),
        "values": embeddings[i],
        "metadata": {"text": chunks[i]}
    }
    for i in range(len(chunks))
]

index.upsert(vectors=vectors)
print(f"✅ Uploaded {len(vectors)} vectors to index '{INDEX_NAME}'")
