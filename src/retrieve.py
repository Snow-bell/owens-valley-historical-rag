from typing import List, Dict
from openai import OpenAI
from src.config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    TOP_K,
    RERANK_CANDIDATES,
)
from src.embed import get_chroma_collection
from src.rerank import rerank

client = OpenAI(api_key=OPENAI_API_KEY)


def embed_query(query: str) -> List[float]:
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    return response.data[0].embedding


def diversify(chunks: List[Dict], max_per_source: int = 2) -> List[Dict]:
    """
    Fallback diversity filter — limits chunks per source to prevent
    any single document dominating when reranking is unavailable.
    """
    seen = {}
    result = []
    for chunk in chunks:
        source = chunk["metadata"]["source"]
        count = seen.get(source, 0)
        if count < max_per_source:
            seen[source] = count + 1
            result.append(chunk)
    return result


def get_candidates(query: str, n: int = RERANK_CANDIDATES) -> List[Dict]:
    """
    Returns the n chunks closest to the query by embedding similarity,
    before reranking.
    """
    collection = get_chroma_collection()
    query_embedding = embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text": text,
            "metadata": metadata,
            "similarity": round(1 - distance, 4),
        })
    return chunks


def retrieve(query: str, top_k: int = TOP_K, strict: bool = False) -> List[Dict]:
    """
    Fetches RERANK_CANDIDATES chunks and returns the top_k after reranking.
    If reranking fails, falls back to the diversity filter, unless strict
    is set (evaluation runs), in which case the error is raised.
    """
    chunks = get_candidates(query, max(RERANK_CANDIDATES, top_k))

    try:
        return rerank(query, chunks, top_n=top_k)
    except Exception as e:
        if strict:
            raise
        print(f"  [WARNING] Rerank failed, falling back to diversity filter: {e}")
        return diversify(chunks)[:top_k]
