import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

CHUNKS_JSON = "chunks_grouped.json"
FAISS_INDEX_FILE = "loan_faiss.index"

print("[FAISS] Loading chunks...")
with open(CHUNKS_JSON, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [c["chunk_text"] for c in chunks if c.get("chunk_text")]

print(f"[FAISS] Total chunks to embed: {len(texts)}")

print("[FAISS] Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("[FAISS] Generating embeddings...")
embeddings = model.encode(texts, convert_to_tensor=False)
embeddings = np.array(embeddings, dtype=np.float32)
dim = embeddings.shape[1]

print("[FAISS] Building FAISS index...")
index = faiss.IndexFlatL2(dim)
index.add(embeddings)
print(f"[FAISS] Number of vectors in index: {index.ntotal}")

# Save FAISS index
faiss.write_index(index, FAISS_INDEX_FILE)
print(f"[FAISS] Index saved to {FAISS_INDEX_FILE}")

# save mapping from index to text for retrieval
with open("index_to_text.json", "w", encoding="utf-8") as f:
    json.dump(texts, f, ensure_ascii=False, indent=2)

print("[FAISS] Done!")