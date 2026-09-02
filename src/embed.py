import chromadb
from chromadb.config import Settings
from typing import List, Dict
from openai import OpenAI
from src.config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    CHROMA_DIR,
    CHROMA_COLLECTION,
)

client = OpenAI(api_key=OPENAI_API_KEY)


def get_chroma_collection():
    """
    Initialize ChromaDB client and return the collection.
    Creates the collection if it doesn't exist.
    """
    chroma_client = chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )

    collection = chroma_client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )

    return collection


def embed_chunks(chunks: List[Dict]) -> List[List[float]]:
    """
    Send chunk texts to OpenAI embeddings API.
    Returns list of embedding vectors.
    """
    texts = [chunk["text"] for chunk in chunks]

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )

    return [item.embedding for item in response.data]


def store_chunks(chunks: List[Dict], embeddings: List[List[float]]) -> None:
    """
    Store chunks and their embeddings in ChromaDB.
    """
    collection = get_chroma_collection()

    ids = [
        f"{chunk['metadata']['source']}__chunk{chunk['chunk_index']}"
        for chunk in chunks
    ]

    documents = [chunk["text"] for chunk in chunks]

    metadatas = [
        {
            "source": chunk["metadata"]["source"],
            "source_path": chunk["metadata"]["source_path"],
            "tier": chunk["metadata"]["tier"],
            "bias_tag": chunk["metadata"]["bias_tag"],
            "bias_level": chunk["metadata"]["bias_level"],
            "description": chunk["metadata"]["description"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"  Stored {len(chunks)} chunks in ChromaDB.")


def embed_and_store(chunks: List[Dict]) -> None:
    """
    Full pipeline: embed chunks and store in ChromaDB.
    Batches requests to avoid hitting API limits.
    """
    BATCH_SIZE = 100

    total = len(chunks)
    print(f"\n  Embedding {total} chunks in batches of {BATCH_SIZE}...")

    for i in range(0, total, BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        print(f"  Batch {i // BATCH_SIZE + 1} / {-(-total // BATCH_SIZE)}")

        embeddings = embed_chunks(batch)
        store_chunks(batch, embeddings)

    print(f"\n  Done. {total} chunks embedded and stored.")