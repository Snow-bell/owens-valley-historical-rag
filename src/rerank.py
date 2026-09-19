import cohere
from typing import List, Dict
from src.config import COHERE_API_KEY, RERANK_MODEL, RERANK_TOP_N

client = cohere.Client(api_key=COHERE_API_KEY)


def rerank(query: str, chunks: List[Dict]) -> List[Dict]:
    """
    Reranks chunks by relevance to the query using Cohere's cross-encoder.
    """
    if not chunks:
        return []

    documents = [chunk["text"] for chunk in chunks]

    results = client.rerank(
        model=RERANK_MODEL,
        query=query,
        documents=documents,
        top_n=RERANK_TOP_N,
    )

    reranked = []
    for result in results.results:
        chunk = chunks[result.index].copy()
        chunk["relevance_score"] = round(result.relevance_score, 4)
        reranked.append(chunk)

    return reranked