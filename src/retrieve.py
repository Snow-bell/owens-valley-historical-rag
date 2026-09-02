from typing import List, Dict
from openai import OpenAI
from src.config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    TOP_K,
)
from src.embed import get_chroma_collection

client = OpenAI(api_key=OPENAI_API_KEY)


def diversify(chunks: List[Dict], max_per_source: int = 2) -> List[Dict]:
    """
    Limits chunks per source to prevent any single document
    from dominating retrieval results.
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


def embed_query(query: str) -> List[float]:
    """
    Embed a user query using the same model as the corpus.
    """
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    return response.data[0].embedding


def retrieve(query: str, top_k: int = TOP_K) -> List[Dict]:
    collection = get_chroma_collection()
    query_embedding = embed_query(query)

    # Fetch 3x top_k to ensure diversity after filtering
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k * 3,
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

    return diversify(chunks, max_per_source=2)[:top_k]