# Agentic AI Loan Assistant

An AI-powered financial product assistant built using Retrieval-Augmented Generation (RAG) and FastAPI. The system scrapes loan-related information from banking websites, preprocesses and indexes the data using FAISS embeddings, and delivers context-aware responses through an interactive web interface.

---

## Features

* AI-powered loan product assistance
* Retrieval-Augmented Generation (RAG) pipeline
* Semantic search using FAISS vector database
* Automated web scraping for financial data ingestion
* FastAPI backend for scalable API serving
* Interactive web-based UI
* Context-aware question answering using GPT-4
* Structured document chunking for improved retrieval accuracy

---

## Tech Stack

* Python
* FastAPI
* FAISS
* OpenAI GPT-4
* SentenceTransformers
* Selenium
* BeautifulSoup
* HTML/CSS/JavaScript

---

## System Architecture

### 1. Data Scraping Layer

* Scrapes loan-related information from banking websites
* Extracts headings, paragraphs, lists, and tabular data

### 2. Data Preprocessing Layer

* Cleans and structures extracted content
* Splits large text into semantic chunks
* Optimizes chunks for vector retrieval

### 3. Embedding & Vector Storage

* Converts chunks into embeddings using SentenceTransformers
* Stores embeddings in a FAISS vector index

### 4. Retrieval-Augmented Generation Pipeline

* Encodes user query into embeddings
* Retrieves top-k semantically relevant chunks
* Sends retrieved context to GPT-4
* Generates grounded, context-aware responses

### 5. API & UI Layer

* FastAPI backend for inference serving
* Lightweight web interface for user interaction

---
```
Project Structure
agentic-ai-loan-assistant/
│
├── .gitignore
├── README.md
├── chunks_grouped.json
├── data_preprocessing.py
├── faiss_build.py
├── index_to_text.json
├── loan_faiss.index
├── questions.txt
├── rag.py
├── requirements.txt
├── scraped_pages.json
├── scraper.py
└── static/
    └── index.html
```
---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd agentic-ai-loan-assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Data Scraper

```bash
python scraper.py
```

### 4. Preprocess Extracted Data

```bash
python preprocess.py
```

### 5. Build FAISS Vector Index

```bash
python faiss_build.py
```

### 6. Start FastAPI Server

```bash
uvicorn rag_fastapi_app:app --reload
```

### 7. Launch Web UI

Open browser:

```bash
http://127.0.0.1:8000/static/index.html
```

---

## AI Models Used

### Embedding Model

* all-MiniLM-L6-v2

### Large Language Model

* GPT-4

---

## Architectural Decisions

### Why FAISS?

FAISS enables efficient semantic vector retrieval for large-scale text search and improves retrieval latency.

### Why Chunking?

Smaller semantic chunks improve retrieval precision and contextual grounding for LLM responses.

### Why FastAPI?

FastAPI provides lightweight, high-performance API serving suitable for scalable AI systems.

---

## Future Improvements

* Hybrid search (BM25 + vector retrieval)
* Agentic workflow integration
* Multi-bank financial product ingestion
* GraphRAG integration
* Streaming responses
* Authentication & user session memory
* Dockerized deployment
* PostgreSQL/pgvector migration

---

## Potential Enterprise Use Cases

* AI-powered banking assistant
* Loan eligibility guidance
* Financial product recommendation
* Internal banking knowledge assistant
* Automated customer support workflows

---

## License

This project is intended for educational and research purposes.
