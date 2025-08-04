import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.docstore.document import Document
import os
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
CHUNK_FILE = "data/chunks.json"
PERSIST_DIR = os.getenv("PERSIST_DIR", "chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "")    #you need to change here inside " " - Which LLM model of GROQ you are using

# --- Check if data exists ---
if not os.path.exists(CHUNK_FILE) or os.path.getsize(CHUNK_FILE) == 0:
    print(f"⚠️ '{CHUNK_FILE}' is empty or does not exist. Run 'parse_pdfs.py' first.")
    exit()

# --- Load Data ---
with open(CHUNK_FILE, "r") as f:
    data = json.load(f)

# --- Prepare Documents ---
documents = [
    Document(page_content=q, metadata={"topic": item["topic"]})
    for item in data
    for q in item["questions"]
]

if not documents:
    print("No documents to index. Exiting.")
    exit()

# --- Initialize ChromaDB ---
embedding = OllamaEmbeddings(model=EMBEDDING_MODEL)

if os.path.exists(PERSIST_DIR):
    print(f"Appending to existing ChromaDB at '{PERSIST_DIR}'...")
    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embedding
    )
    
    # Get existing documents' content to avoid duplicates
    existing_docs = vectorstore.get(include=["metadatas", "documents"])
    existing_contents = set(doc for doc in existing_docs['documents'])
    
    new_documents = [doc for doc in documents if doc.page_content not in existing_contents]
    
    if new_documents:
        vectorstore.add_documents(new_documents)
        print(f"✅ Added {len(new_documents)} new documents to ChromaDB.")
    else:
        print("No new documents to add.")
else:
    print(f"Creating new ChromaDB at '{PERSIST_DIR}'...")
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding,
        persist_directory=PERSIST_DIR
    )
    print(f"✅ Indexed {len(documents)} documents into ChromaDB.")

vectorstore.persist()
