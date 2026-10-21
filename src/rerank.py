import time
import cohere
from cohere.errors import TooManyRequestsError
from typing import List, Dict
from src.config import (
    COHERE_API_KEY,
    RERANK_MODEL,
    RERANK_TOP_N,
    COHERE_CALLS_PER_MINUTE,
)

client = cohere.Client(api_key=COHERE_API_KEY)

RATE_LIMIT_RETRIES = 3
RATE_LIMIT_WAIT = 65  # seconds; longer than one rate-limit window

_last_call = 0.0


def wait_for_rate_limit() -> None:
    """
    Spaces calls so they stay under COHERE_CALLS_PER_MINUTE,
    with a 5% margin. The first call never waits.
    """
    global _last_call
    interval = 60 / COHERE_CALLS_PER_MINUTE * 1.05
    wait = _last_call + interval - time.monotonic()
    if wait > 0:
        time.sleep(wait)
    _last_call = time.monotonic()


def rerank(query: str, chunks: List[Dict], top_n: int = RERANK_TOP_N) -> List[Dict]:
    """
    Reranks chunks by relevance to the query using Cohere's cross-encoder.
    Waits and retries when Cohere reports its rate limit.
    """
    if not chunks:
        return []

    documents = [chunk["text"] for chunk in chunks]

    for attempt in range(RATE_LIMIT_RETRIES + 1):
        wait_for_rate_limit()
        try:
            results = client.rerank(
                model=RERANK_MODEL,
                query=query,
                documents=documents,
                top_n=top_n,
            )
            break
        except TooManyRequestsError:
            if attempt == RATE_LIMIT_RETRIES:
                raise
            print(f"  [WARNING] Cohere rate limit reached, waiting {RATE_LIMIT_WAIT} s")
            time.sleep(RATE_LIMIT_WAIT)

    reranked = []
    for result in results.results:
        chunk = chunks[result.index].copy()
        chunk["relevance_score"] = round(result.relevance_score, 4)
        reranked.append(chunk)

    return reranked
