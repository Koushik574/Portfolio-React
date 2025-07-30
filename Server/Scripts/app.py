from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pinecone import Pinecone
from groq import Groq
from google.generativeai import configure, embed_content
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# FastAPI app setup
app = FastAPI()

# Enable CORS (adjust in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class ChatRequest(BaseModel):
    query: str

# Configure external services
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]
INDEX_NAME = "koushik-rag-chatbot-index"

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

# Configure Gemini
configure(api_key=GOOGLE_API_KEY)

# Function to embed user query using Gemini
def get_embedding_from_gemini(text: str) -> list:
    response = embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_query"
    )
    return response["embedding"]

# Initialize Groq LLM
groq = Groq(api_key=GROQ_API_KEY)

# API route
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        query = request.query

        # Step 1: Embed the query
        embedded_query = get_embedding_from_gemini(query)

        # Step 2: Search similar chunks in Pinecone
        results = index.query(vector=embedded_query, top_k=3, include_metadata=True)

        # Step 3: Build context
        context = ""
        for match in results["matches"]:
            metadata = match.get("metadata", {})
            content = metadata.get("text") or metadata.get("content") or ""
            context += content.strip() + "\n---\n"

        if not context.strip():
            return {"answer": "Sorry, no relevant context found."}

        # Step 4: Generate answer using Groq
        response = groq.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Answer using the context below. If not found, say so."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{query}"}
            ]
        )

        answer = response.choices[0].message.content.strip()
        return {"answer": answer}

    except Exception as e:
        print("🔥 ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
