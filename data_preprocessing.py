import json
import re

DATA_JSON = "scraped_pages.json"
CHUNKS_JSON = "chunks_grouped.json"
CHUNK_SIZE = 300  

def split_text(text, size=CHUNK_SIZE):
    sentences = re.split(r'(?<=[.?!;])\s+', text)
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) <= size:
            current += " " + s if current else s
        else:
            chunks.append(current.strip())
            current = s
    if current:
        chunks.append(current.strip())
    return chunks

def preprocess():
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)  

    chunks = []

    for key, value in data.items():
        source = key
        paragraphs = value.get("paragraphs", []) if isinstance(value, dict) else []
        buffer = []

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            if re.match(r"^[\d\-\+%].*", paragraph) or re.match(r".*RLLR.*", paragraph):
                buffer.append(paragraph)
            else:
                if buffer:
                    combined = " | ".join(buffer)
                    chunks.append({"chunk_text": f"{source}: {combined}"})
                    buffer = []
                for c in split_text(paragraph):
                    chunks.append({"chunk_text": f"{source}: {c}"})

        if buffer:
            combined = " | ".join(buffer)
            chunks.append({"chunk_text": f"{source}: {combined}"})

    with open(CHUNKS_JSON, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"[Preprocess] Total chunks created: {len(chunks)}")
    return chunks

if __name__ == "__main__":
    preprocess()
