## Loan-Product-Assistant

A  RAG (Retrieval-Augmented Generation) system that scrapes loan information from Bank of Maharashtra pages, preprocesses it into chunks, builds a FAISS index, and serves answers using a FastAPI API +  web UI.

## Project Setup

# Step 1
Run the Scraper
"""python scraper.py"""

# Step 2
Preprocess the Data by running below command
 python preprocess.py

# Step 3
Build FAISS index
python faiss_build.py

# Step 4
Start the RAG FastAPI Server
uvicorn rag_fastapi_app:app --reload

# Step 5
open ui in browser
http://127.0.0.1:8000/static/index.html


## How the RAG System Works

1. Scraper collects:
scraper.py
Extracts headings, paragraphs, lists, and tables from bank URLs.

2. Data Preprocess converts:
data_preprocessing.py
- Converts paragraphs, list items, and table rows into clean, structured chunks.
- Splits long texts into smaller pieces for better semantic search.

3. FAISS:
faiss.py
- Converts every chunk into an embedding
- Saves the index for fast vector search

4. FastAPI:
rag.py
- Encodes the user query
- Retrieves top-k relevant chunks
- Sends chunks + question to OpenAI
- Returns an answer strictly from ingested data


# Command to run fastapi

uvicorn rag:app --reload

## Architectural Decisions
# Libraries
- Selenium: Scrapes dynamic pages with JavaScript.
- BeautifulSoup: Parses headings, paragraphs, lists, and tables.
- FAISS: Fast vector search for RAG.
- SentenceTransformers: Converts text into embeddings.
- FastAPI: Serves the RAG system via an API.
- OpenAI API: Generates answers from retrieved chunks.

# Data Strategy

Chunking: Split paragraphs, list items, and table rows into small pieces as Smaller chunks improve search accuracy and context for the LLM.

# Model Selection

- Embedding Model: all-MiniLM-L6-v2 – small, fast, effective.
- LLM: GPT-4 – high-quality, context-aware answers.

# AI Tools Used

- OpenAI GPT-4: Generates answers.
- FAISS: Fast retrieval of relevant chunks.
- SentenceTransformers: Embeddings for vector search.

# Potential Improvements

- Cache embeddings to speed up preprocessing.

- Use smarter chunking (e.g., overlapping chunks).

