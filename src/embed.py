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

# Chunk metadata stored in Chroma; Chroma accepts only str, int, float and bool
STORED_METADATA = [
    "source",
    "source_path",
    "tier",
    "bias_tag",
    "bias_level",
    "description",
    "chunk_index",
    "chunk_method",
    "clean_version",
    "token_count",      # semantic chunks
    "n_sentences",      # semantic chunks
]


def get_chroma_client():
    return chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )


def get_chroma_collection(name: str = CHROMA_COLLECTION):
    """
    Initialize ChromaDB client and return the collection for the current
    CHUNK_METHOD (or the one named). Creates the collection if it doesn't exist.
    """
    return get_chroma_client().get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"},
    )


def reset_collection(name: str = CHROMA_COLLECTION) -> None:
    """
    Deletes the named collection so a reindex starts empty. Upserting into
    an existing collection would leave chunks from deleted or shortened
    documents behind. Other collections are untouched.
    """
    chroma_client = get_chroma_client()
    if name in [c.name for c in chroma_client.list_collections()]:
        chroma_client.delete_collection(name)
        print(f"  Cleared collection {name}.")


def chunk_id(chunk: Dict) -> str:
    # source_path, not the bare file name, so same-named files in different folders don't collide
    return f"{chunk['metadata']['source_path']}__chunk{chunk['chunk_index']}"


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

    ids = [chunk_id(chunk) for chunk in chunks]

    documents = [chunk["text"] for chunk in chunks]

    metadatas = [
        {key: chunk["metadata"][key] for key in STORED_METADATA if key in chunk["metadata"]}
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