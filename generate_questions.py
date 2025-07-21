from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA  # Required for QA chain

# Load embedding model
embedding = OllamaEmbeddings(model="phi3")

# Load vector store
db = Chroma(persist_directory="data/chroma_db", embedding_function=embedding)

# Get retriever from the vector store
retriever = db.as_retriever()

# Load LLM
llm = OllamaLLM(model="phi3")

# Create QA chain
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Function to generate questions
def generate(subject, year, count):
    prompt = f"Generate {count} UPSC GS questions on '{subject}' based on patterns from year {year}. Maintain UPSC tone and directive keywords."
    return qa.run(prompt)