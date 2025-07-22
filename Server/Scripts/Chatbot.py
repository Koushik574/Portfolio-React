# chatbot.py

# pickle is again to load the data which dumped before
import pickle

# Using matrix operations lets us go in all possible
# directions in the vector space and find the best match for the question

import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# os for file handling
import os
from openai import OpenAI

# dotenv for securing api key
from dotenv import load_dotenv

#code flow i can understand getting the input,exception handling, prompt to exit chat..

# Load env vars
load_dotenv()

# using Open AI api style but in base url we are mentioning that we are using GROQ
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"  # ✅ Groq endpoint
)

# Load your vector store
# with open("../vectorstore.pkl", "rb") as f:

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "..", "vectorstore.pkl"), "rb") as f:
    vectorstore = pickle.load(f)

chunks = vectorstore["chunks"]
embeddings = np.array(vectorstore["embeddings"])

# Load the same model used for chunking
# sentence transformer is to understand the prompt/query
# from the user(it can understand even if the user made
# grammatical mistake in the query,spelling mistake,
# regional dialect(especially in my case indian way of speaking english)
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_top_chunk(query):
    query_vec = model.encode([query])

    # sklearn's cosine similarity to feed the llm about relavance
    #like if user says hello then our llm must say hello,how are you?
    # and not "bye,good night"
    sims = cosine_similarity(query_vec, embeddings)[0]

    top_idx = np.argmax(sims)
    return chunks[top_idx]


def ask_chatbot(query):
    context = get_top_chunk(query)

    prompt = f"""You are a helpful AI assistant that answers questions
    about a developer named Sai Koushik using the following context.

Context:
{context}

Question:
{query}

Answer:"""

    response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return response.choices[0].message.content.strip()


# CLI loop
if __name__ == "__main__":
    print("🤖 Ask me anything about Sai Koushik!")
    while True:
        try:
            user_input = input("Please ask me a qn sir/mam: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            answer = ask_chatbot(user_input)
            print("My answer to your qn is:", answer)
        except KeyboardInterrupt:
            break
