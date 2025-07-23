from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from Chatbot import ask_chatbot
from Scripts.Chatbot import ask_chatbot


app = FastAPI()

# CORS
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

class QueryInput(BaseModel):
    query: str

# @app.post("/chat")
# def chat_with_bot(user_input: QueryInput):
#     answer = ask_chatbot(user_input)
#     return {"answer": answer}

@app.post("/chat")
def chat_with_bot(user_input: QueryInput):
    answer = ask_chatbot(user_input.query)  # 🟢 Pass only the string!
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Scripts.app:app",
                host="0.0.0.0",
                port=8000)

