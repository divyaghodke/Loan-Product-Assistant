# rag_fastapi_app_updated.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import faiss
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHUNKS_JSON = os.path.join(BASE_DIR, "chunks_grouped.json")
FAISS_INDEX_FILE = os.path.join(BASE_DIR, "loan_faiss.index")
TOP_K = 3

app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/")
def root():
    return FileResponse(os.path.join(BASE_DIR, "static/index.html"))

# Load preprocessed chunks
with open(CHUNKS_JSON, "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Load FAISS index
print("[FAISS] Loading FAISS index...")
index = faiss.read_index(FAISS_INDEX_FILE)
print(f"[FAISS] Index loaded. Total vectors: {index.ntotal}")

# Load embedding model
print("[Model] Loading SentenceTransformer...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("[Model] Ready.")

class QueryRequest(BaseModel):
    query: str

def retrieve(query: str, top_k: int = TOP_K):
    """Retrieve top-k relevant chunks from FAISS index."""
    q_vec = model.encode([query], convert_to_tensor=False)
    distances, indices = index.search(np.array(q_vec, dtype=np.float32), top_k)
    results = []
    for i in indices[0]:
        if i < len(chunks):
            results.append(chunks[i]["chunk_text"])
    return results

def generate_answer(query: str, retrieved_chunks: list):
    """Generate answer using OpenAI GPT model based on retrieved chunks."""
    context = "\n\n---\n".join(retrieved_chunks) if retrieved_chunks else "No relevant data found."

    prompt = f"""
You are a highly helpful and polite RAG (Retrieval-Augmented Generation) assistant for banking queries.

CONTEXT:
{context}

INSTRUCTIONS:
1. Base your answer ONLY on the given context.
2. If the context contains the answer, provide a clear, concise, and user-friendly response.
3. If the context contains partial information, clearly indicate: "Here is what the context contains:" and present only that info.
4. If the context is missing or unclear:
   - Use logical reasoning to infer a possible answer.
   - Make sure to mention that the answer is inferred and may not be exact.
   - Avoid hallucinating unrelated information.
5. Be polite, concise, and professional.
6. Summarize when multiple chunks contain relevant info.

USER QUESTION: "{query}"
"""
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3  
    )
    return response.choices[0].message.content.strip()

@app.post("/get_answer")
async def get_answer(request: QueryRequest):
    retrieved = retrieve(request.query)
    answer = generate_answer(request.query, retrieved)
    return {"query": request.query, "answer": answer}
