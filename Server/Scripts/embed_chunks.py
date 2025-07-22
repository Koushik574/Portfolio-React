# langchain module has the ablility to  find or form a sentence or para
# from a large text file which is boring to learn
from langchain.text_splitter import RecursiveCharacterTextSplitter

# sentence_transformers is used to make the llm's response is contextfull,
# meaningfull and a flow to make understand the answer reader

from sentence_transformers import SentenceTransformer

# pcikle is nothing but,if we done chunking and embedding during coding itself,
# where chunks and embeddings is basically an array here so we store
# these array in a dictionary and with the help of pickle we are
# saving this in a pickle file so hereafter when a query is hit by the
# user no need to run the code for making chunks(splitting the large text
# into small meaning full sentence or info) or embeddings(knowing the tone,
# subject of the user and responding it with meaningful,contexfull answer) instead
# we just need to ask the pkl file to give me the chunks and embedding which it has
import pickle


# This line opens your combined data file (rag_corpus.txt) in read mode.
# encoding="utf-8" makes sure it correctly reads any special characters.
# Then, file.read() reads the entire text into the variable raw_text.
with open("../Text-Files/rag_corpus.txt", "r", encoding="utf-8") as file:
    raw_text = file.read()

# This creates a text_splitter object from RecursiveCharacterTextSplitter.
# chunk_size=500 means: each chunk will be ~500 characters long.
# chunk_overlap=50 means: the last 50 characters of a chunk will repeat at the start of the next chunk
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_text(raw_text)

# This line loads a small, efficient pre-trained model
# that understands natural language and converts each
# text chunk into a vector (semantic embedding).
# This is crucial for enabling the chatbot to later match user questions with relevant information.
model = SentenceTransformer("all-MiniLM-L6-v2")

#  Meaning-based pattern matching using vectors.
# “Does this question have a similar meaning to any of the chunked texts we stored earlier?”
embeddings = model.encode(chunks)

# We want to bundle the chunks and their matching vector
# representations into one place — so we can save it once and reuse later.
vector_store = {
    "chunks": chunks,
    "embeddings": embeddings
}

# dump the data in the vector_store variable into a pickle file with write binary access using pickle module
with open("../vectorstore.pkl", "wb") as f:
    pickle.dump(vector_store, f)

print("✅ Chunks embedded and saved to vectorstore.pkl")
