from typing import List, Dict
from openai import OpenAI
from src.config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    TOP_K,
)
from src.embed import get_chroma_collection

client = OpenAI(api_key=OPENAI_API_KEY)


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
    """
    Embed the query and retrieve the top_k most similar
    chunks from ChromaDB.

    Returns a list of dicts with 'text' and 'metadata'.
    """
    collection = get_chroma_collection()
    query_embedding = embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
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