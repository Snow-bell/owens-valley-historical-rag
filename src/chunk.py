import re
import tiktoken
from typing import List, Dict
from src.config import CHUNK_SIZE, CHUNK_OVERLAP, CHUNK_METHOD

# Chunks where letters make up less than this share of the non-space
# characters are OCR garbage or numeric tables, and aren't indexed.
# Real prose heavy with figures sits around 0.65.
MIN_LETTER_SHARE = 0.5


def letter_share(text: str) -> float:
    characters = re.sub(r"\s", "", text)
    if not characters:
        return 0.0
    return sum(c.isalpha() for c in characters) / len(characters)


def get_encoder():
    return tiktoken.get_encoding("cl100k_base")

def chunk_text(text: str, metadata: Dict) -> List[Dict]:
    """
    Split text into overlapping chunks with metadata.
    
    Args:
        text: Raw extracted text from a document
        metadata: Dict containing source info (filename, bias_tag, tier)
    
    Returns:
        List of dicts with 'text', 'metadata', and 'chunk_index'
    """
    encoder = get_encoder()
    tokens = encoder.encode(text)
    
    chunks = []
    start = 0
    chunk_index = 0
    
    while start < len(tokens):
        end = start + CHUNK_SIZE
        chunk_tokens = tokens[start:end]
        chunk_text = encoder.decode(chunk_tokens)
        
        chunks.append({
            "text": chunk_text,
            "chunk_index": chunk_index,
            "metadata": {
                **metadata,
                "chunk_index": chunk_index,
                "chunk_method": "fixed",
            }
        })
        
        start += CHUNK_SIZE - CHUNK_OVERLAP
        chunk_index += 1
    
    return chunks


def chunk_documents(documents: List[Dict], method: str = CHUNK_METHOD) -> List[Dict]:
    """
    Chunk a list of documents.
    
    Args:
        documents: List of dicts with 'text' and 'metadata'
        method: "fixed" (CHUNK_SIZE-token windows) or "semantic"
    
    Returns:
        Flat list of all chunks across all documents, without chunks below
        MIN_LETTER_SHARE. Kept chunks keep their chunk_index, so IDs are stable.
    """
    if method == "semantic":
        raise NotImplementedError("The semantic chunker isn't implemented yet; set CHUNK_METHOD = \"fixed\".")
    if method != "fixed":
        raise ValueError(f"Unknown chunk method {method!r}. Expected \"fixed\" or \"semantic\".")

    all_chunks = []
    dropped = 0
    for doc in documents:
        for chunk in chunk_text(doc["text"], doc["metadata"]):
            if letter_share(chunk["text"]) < MIN_LETTER_SHARE:
                dropped += 1
                continue
            all_chunks.append(chunk)
    if dropped:
        print(f"  Dropped {dropped} chunks that are mostly symbols or digits.")
    return all_chunks