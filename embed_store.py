from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings # Embedding model
import json

with open("data/tagged_questions.json") as f:
    docs = json.load(f)

texts = [d["question"] for d in docs]  # Extract questions
embedding = OllamaEmbeddings(model="phi3")
db = Chroma.from_texts(texts, embedding, persist_directory="data/chroma_db")  # Vectorize and store