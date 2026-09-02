import tiktoken
from typing import List, Dict
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

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
            }
        })
        
        start += CHUNK_SIZE - CHUNK_OVERLAP
        chunk_index += 1
    
    return chunks


def chunk_documents(documents: List[Dict]) -> List[Dict]:
    """
    Chunk a list of documents.
    
    Args:
        documents: List of dicts with 'text' and 'metadata'
    
    Returns:
        Flat list of all chunks across all documents
    """
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"], doc["metadata"])
        all_chunks.extend(chunks)
    return all_chunks