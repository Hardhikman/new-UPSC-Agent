import os
import time
import uuid
import requests
import gradio as gr
from datetime import datetime, timedelta
from dotenv import load_dotenv
from diskcache import Cache

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings  # Optional for local embeddings

# === Load environment ===
load_dotenv()

# === Setup cache ===
cache = Cache("news_cache")

# === Langchain model setup ===
llm = ChatOpenAI(
    model="mixtral-8x7b-32768",
    openai_api_key=os.getenv("GROQ_API_KEY"),
    openai_api_base="https://api.groq.com/openai/v1"
)

# === Load vector DB ===
embedding = OllamaEmbeddings(model=os.getenv("EMBEDDING_MODEL", "phi3"))  # Optional, only used for Chroma
vectorstore = Chroma(
    persist_directory=os.getenv("PERSIST_DIR", "chroma_db"),
    embedding_function=embedding,
)
retriever = vectorstore.as_retriever()

# === Build list of topics ===
topics_set = set()
for doc in vectorstore.get()["metadatas"]:
    topics_set.add(doc["topic"])
topics = sorted(list(topics_set))

# === Prompt Template ===
template = """
You are a UPSC Mains question paper designer.

Given the following example questions from the topic: "{topic}", generate {num} new high-quality, original UPSC Mains-style questions from this topic.

Examples:
{examples}

Now generate {num} new questions only.
"""
prompt = PromptTemplate.from_template(template)

# === News fetcher ===
def fetch_recent_news(topic, months=6):
    cache_key = f"{topic}_{months}"
    cached = cache.get(cache_key)
    if cached and time.time() - cached["timestamp"] < 3600:
        return cached["news"]

    api_key = os.getenv("NEWSAPI_KEY")
    url = "https://newsapi.org/v2/everything"
    
    to_date = datetime.utcnow().date()
    from_date = to_date - timedelta(days=30 * int(months))

    params = {
        "q": topic,
        "language": "en",
        "from": from_date.isoformat(),
        "to": to_date.isoformat(),
        "sortBy": "relevancy",
        "pageSize": 5,
        "apiKey": api_key
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        if "articles" in data:
            news = "\n".join([f"- {a['title']}: {a['description']}" for a in data["articles"]])
            cache.set(cache_key, {"news": news, "timestamp": time.time()})
            return news
        else:
            return "No news articles found for this topic."
    except Exception as e:
        return f"Error fetching news: {str(e)}"

# === Main generator function ===
def generate_upsc_questions(selected_topic, num, use_ca, months):
    if use_ca:
        news_context = fetch_recent_news(selected_topic, months)
        ca_prompt = f"""
You are a UPSC question paper designer.

Based on the topic: "{selected_topic}" and the recent news below, generate {num} high-quality, analytical, UPSC Mains-style questions related to current affairs.

Recent News (Last {months} months):
{news_context}

Only output the questions.
"""
        response = llm.invoke(ca_prompt)
        return f"### 📰 Current Affairs Questions (Groq - Mixtral)\n\n{response.strip()}"
    
    else:
        retriever.search_kwargs = {"k": num, "filter": {"topic": selected_topic}}
        docs = retriever.get_relevant_documents(selected_topic)

        if not docs:
            return f"❌ No questions found for topic: {selected_topic}"

        examples = [doc.page_content for doc in docs]
        example_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(examples)])

        final_prompt = prompt.format(topic=selected_topic, examples=example_text, num=num)
        response = llm.invoke(final_prompt)

        return f"### 🔄 Static Questions (from Groq - Mixtral)\n\n{response.strip()}"

# === Gradio UI ===
gradio_app = gr.Interface(
    fn=generate_upsc_questions,
    inputs=[
        gr.Dropdown(choices=topics, label="📘 Select UPSC Topic"),
        gr.Slider(1, 10, step=1, label="Number of Questions"),
        gr.Checkbox(label="📰 Current Affairs Mode?"),
        gr.Dropdown(choices=["3", "6", "12"], value="6", label="🕒 Time Period (in Months)")
    ],
    outputs=gr.Textbox(label="📄 Generated Questions", lines=10, show_copy_button=True),
    title="🎓 UPSC GS Question Generator",
    description="Generate UPSC Mains-style questions by topic. Tick Current Affairs to include news from the last 3/6/12 months."
)

# === FastAPI app ===
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return RedirectResponse(url="/gradio")

app = gr.mount_gradio_app(app, gradio_app, path="/gradio")

# === API Input Schema ===
class QuestionRequest(BaseModel):
    topic: str
    num: int
    use_ca: bool
    months: int

@app.post("/api/generate_questions")
def api_generate_questions(req: QuestionRequest):
    result = generate_upsc_questions(req.topic, req.num, req.use_ca, req.months)
    return {"result": result}
