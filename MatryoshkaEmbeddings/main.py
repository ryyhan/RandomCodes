from fastapi import FastAPI
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import time
import random
import string
import numpy as np
 
app = FastAPI()
 
# Initialize Chroma with persistent storage (embed-dimension fixed at model’s full size)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="matryoshka-docs")
 
# Load embedding model
model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)
 
@app.post("/add/")
def add_embedding(id: str, text: str):
    embedding = model.encode(text)
    collection.add(documents=[text], embeddings=[embedding.tolist()], ids=[id])
    return {"status": "added", "id": id}
 
@app.get("/query/")
def query_embedding(query: str, top_k: int = 3, truncate_to: int = None, candidate_pool: int = 100):
    start_time = time.time()
    # 1) Always compute full embedding for initial query
    full_emb = model.encode(query)
    # 2) Initial search against full-vector index, request embeddings & documents
    initial = collection.query(
        query_embeddings=[full_emb.tolist()],
        n_results=candidate_pool,
        include=["embeddings", "documents"]
    )
    ids = initial["ids"][0]
    docs = initial.get("documents", [[]])[0]
    embs = initial.get("embeddings", [[]])[0]  # list of full-length lists
 
    # 3) If no truncation requested, return top_k from initial
    if not truncate_to:
        chosen = list(zip(ids[:top_k], docs[:top_k]))
        elapsed = time.time() - start_time
        return {"results": chosen, "query_time_seconds": round(elapsed,4)}
 
    # 4) Validate truncate_to
    dim = truncate_to
    if dim > len(full_emb):
        return {"error": f"truncate_to ({dim}) exceeds embedding size ({len(full_emb)})"}
 
    # 5) Slice all candidate embeddings
    slice_query = full_emb[:dim]
    arr = np.array(embs)[:, :dim]
 
    # 6) Compute cosine scores in subspace
    norms = np.linalg.norm(arr, axis=1) * np.linalg.norm(slice_query)
    sims = (arr @ slice_query) / norms
 
    # 7) Select top_k by re-ranked similarity
    idxs = np.argsort(sims)[-top_k:][::-1]
    chosen = [(ids[i], docs[i], float(sims[i])) for i in idxs]
    elapsed = time.time() - start_time
 
    return {"results": chosen, "query_time_seconds": round(elapsed,4)}
 
@app.get("/persist/")
def persist():
    chroma_client.persist()
    return {"status": "persisted"}
 
@app.post("/add_bulk/")
def add_bulk(n: int = 1000):
    docs = []
    ids = []
    embeddings = []
 
    for i in range(n):
        text = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
        emb = model.encode(text)
        docs.append(text)
        ids.append(f"doc_{i}")
        embeddings.append(emb.tolist())
 
    collection.add(documents=docs, embeddings=embeddings, ids=ids)
    return {"status": "bulk added", "count": n}
 
@app.get("/benchmark_query/")
def benchmark_query(query: str = "semantic search", runs: int = 5, dims_list: str = "full,256,128,64", top_k: int = 3, candidate_pool: int = 100):
    dims = [None if x.strip() == "full" else int(x) for x in dims_list.split(",")]
    results = []
 
    for d in dims:
        times = []
        for _ in range(runs):
            t0 = time.time()
            # full embed + initial search with embeddings
            full_emb = model.encode(query)
            init = collection.query(
                query_embeddings=[full_emb.tolist()],
                n_results=candidate_pool,
                include=["embeddings"]
            )
            embs = init.get("embeddings", [[]])[0]
 
            if not d:
                # no slicing; ignore sims
                pass
            else:
                # slice and re-rank
                slice_q = full_emb[:d]
                arr = np.array(embs)[:, :d]
                norms = np.linalg.norm(arr, axis=1) * np.linalg.norm(slice_q)
                sims = (arr @ slice_q) / norms
            elapsed = time.time() - t0
            times.append(elapsed)
 
        avg = sum(times) / runs
        results.append({
            "dimensions": "full" if d is None else d,
            "avg_query_time_seconds": round(avg,5),
            "individual_run_times": [round(x,5) for x in times]
        })
 
    return {"benchmark_results": results}