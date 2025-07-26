import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from groq import Groq

# ✅ Load environment variables from .env
load_dotenv()

# 🔗 Load embedding model
print("🔗 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# 🌲 Connect to Pinecone
print("🌲 Connecting to Pinecone...")
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index("sai-rag-chatbot-index")

# 🤖 Initialize Groq API
groq = Groq(api_key=os.environ["GROQ_API_KEY"])

# 🧠 Query loop
while True:
    query = input("\n🧠 Ask me anything (type 'exit' to quit):\n> ")
    if query.lower() == "exit":
        break

    # 1️⃣ Embed the user query
    embedded_query = model.encode(query).tolist()

    # 2️⃣ Query Pinecone index
    results = index.query(vector=embedded_query, top_k=3, include_metadata=True)

    # 3️⃣ Extract context
    context = ""
    for match in results["matches"]:
        metadata = match.get("metadata", {})
        content = metadata.get("text") or metadata.get("content") or ""
        context += content.strip() + "\n---\n"

    print("\n📚 Retrieved Context:\n", context.strip())

    if not context.strip():
        print("\n🤖 Answer:\n Sorry, I couldn't find anything relevant in the context.\n")
        continue

    # 4️⃣ Send to LLM via Groq
    try:
        response = groq.chat.completions.create(
            model="llama3-8b-8192",  # ✅ Updated supported model
            messages=[
                {"role": "system", "content": "Answer the question using the given context below. If the answer isn't found in the context, say so."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{query}"}
            ]
        )
        answer = response.choices[0].message.content.strip()
        print("\n🤖 Answer:\n", answer, "\n")

    except Exception as e:
        print("\n❌ Groq API error:", str(e))
        print("\n🤖 Answer:\n Sorry, something went wrong while querying the LLM.\n")
