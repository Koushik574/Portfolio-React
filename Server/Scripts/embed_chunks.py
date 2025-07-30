from google.generativeai import configure, embed_content
from pinecone import Pinecone, ServerlessSpec
from uuid import uuid4
import os
from dotenv import load_dotenv

# === Load .env variables ===
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "koushik-rag-chatbot-index"
TXT_FILE_PATH = "../Text-Files/rag_corpus.txt"

# === Configure Gemini ===
configure(api_key=GOOGLE_API_KEY)

# === Step 1: Load corpus ===
with open(TXT_FILE_PATH, "r", encoding="utf-8") as file:
    text = file.read()

# === Step 2: Chunk the text ===
chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]

# === Step 3: Embed chunks with Gemini ===
def embed_with_gemini(text):
    response = embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document"
    )
    return response["embedding"]

embeddings = [embed_with_gemini(chunk) for chunk in chunks]

# === Step 4: Upload to Pinecone ===
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

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
