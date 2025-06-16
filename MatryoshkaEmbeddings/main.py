from fastapi import FastAPI
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import time
import random
import string

app = FastAPI()

# Initialize Chroma with persistent storage
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="matryoshka-docs")

# Load embedding model
model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5")

@app.post("/add/")
def add_embedding(id: str, text: str):
    embedding = model.encode(text)
    collection.add(documents=[text], embeddings=[embedding.tolist()], ids=[id])
    return {"status": "added", "id": id}

@app.get("/query/")
def query_embedding(query: str, top_k: int = 3, truncate_to: int = None):
    start_time = time.time()
    embedding = model.encode(query)
    if truncate_to:
        if truncate_to > len(embedding):
            return {"error": f"truncate_to ({truncate_to}) exceeds embedding size ({len(embedding)})"}
        embedding = embedding[:truncate_to]

    results = collection.query(query_embeddings=[embedding.tolist()], n_results=top_k)
    elapsed_time = time.time() - start_time
    results["query_time_seconds"] = round(elapsed_time, 4)
    return results

@app.get("/persist/")
def persist():
    chroma_client.persist()
    return {"status": "persisted"}

@app.post("/add_bulk/")
def add_bulk(n: int = 1000):
    """Adds `n` dummy documents to the Chroma collection for benchmarking."""
    docs = []
    ids = []
    embeddings = []

    for i in range(n):
        random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
        docs.append(random_text)
        ids.append(f"doc_{i}")
        embeddings.append(model.encode(random_text).tolist())

    collection.add(documents=docs, embeddings=embeddings, ids=ids)
    return {"status": "bulk added", "count": n}

@app.get("/benchmark_query/")
def benchmark_query(query: str = "semantic search", runs: int = 5, dims_list: str = "full,256,128,64", top_k: int = 3):
    """Performs multiple queries at different embedding sizes and compares query time."""
    dims_to_test = []
    dims_list = dims_list.replace(" ", "").split(",")
    for item in dims_list:
        if item == "full":
            dims_to_test.append(None)
        else:
            dims_to_test.append(int(item))

    results = []

    for dims in dims_to_test:
        times = []
        for _ in range(runs):
            start = time.time()
            embedding = model.encode(query)
            if dims:
                embedding = embedding[:dims]
            _ = collection.query(query_embeddings=[embedding.tolist()], n_results=top_k)
            elapsed = time.time() - start
            times.append(elapsed)

        avg_time = sum(times) / runs
        results.append({
            "dimensions": "full" if dims is None else dims,
            "avg_query_time_seconds": round(avg_time, 5),
            "individual_run_times": [round(t, 5) for t in times]
        })

    return {"benchmark_results": results}
