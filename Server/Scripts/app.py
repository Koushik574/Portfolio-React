from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()

# Allow CORS for all origins (for frontend React later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class ChatRequest(BaseModel):
    query: str

# Load model and services
model = SentenceTransformer("all-MiniLM-L6-v2")
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index("sai-rag-chatbot-index")
groq = Groq(api_key=os.environ["GROQ_API_KEY"])

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        query = request.query

        # Step 1: Embed query
        embedded_query = model.encode(query).tolist()

        # Step 2: Search Pinecone
        results = index.query(vector=embedded_query, top_k=3, include_metadata=True)

        # Step 3: Build context
        context = ""
        for match in results["matches"]:
            metadata = match.get("metadata", {})
            content = metadata.get("text") or metadata.get("content") or ""
            context += content.strip() + "\n---\n"

        if not context.strip():
            return {"answer": "Sorry, no relevant context found."}

        # Step 4: Ask Groq LLM
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
        raise HTTPException(status_code=500, detail=str(e))
