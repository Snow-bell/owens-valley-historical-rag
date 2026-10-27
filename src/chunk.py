import re
import numpy as np
import tiktoken
from typing import Callable, List, Dict, Optional
from src.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    CHUNK_METHOD,
    SENTENCE_MODEL,
    SEMANTIC_WINDOW,
    SEMANTIC_BREAK_PERCENTILE,
    SEMANTIC_MIN_TOKENS,
    SEMANTIC_MAX_TOKENS,
    SEMANTIC_OVERLAP_MAX_TOKENS,
)

# Chunks where letters make up less than this share of the non-space
# characters are OCR garbage or numeric tables, and aren't indexed.
# Real prose heavy with figures sits around 0.65.
MIN_LETTER_SHARE = 0.5


def letter_share(text: str) -> float:
    characters = re.sub(r"\s", "", text)
    if not characters:
        return 0.0
    return sum(c.isalpha() for c in characters) / len(characters)


def with_context_header(chunk: Dict) -> str:
    """
    Chunk text with its source header (title · author · year · type) on top,
    for embedding and reranking. Stored chunks and the generator's context
    keep the plain text. Chunks indexed before headers existed have none.
    """
    header = chunk["metadata"].get("context_header")
    return f"{header}\n\n{chunk['text']}" if header else chunk["text"]


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
        chunks = chunk_semantic(documents)
    elif method == "fixed":
        chunks = [c for doc in documents for c in chunk_text(doc["text"], doc["metadata"])]
    else:
        raise ValueError(f"Unknown chunk method {method!r}. Expected \"fixed\" or \"semantic\".")

    all_chunks = []
    dropped = 0
    for chunk in chunks:
        if letter_share(chunk["text"]) < MIN_LETTER_SHARE:
            dropped += 1
            continue
        all_chunks.append(chunk)
    if dropped:
        print(f"  Dropped {dropped} chunks that are mostly symbols or digits.")
    return all_chunks


# --- Semantic chunking -------------------------------------------------------

# Period abbreviations punkt doesn't know; without them "Jno. Smith" ends a sentence
PERIOD_ABBREVIATIONS = {
    "mr", "mrs", "co", "bros", "gen", "capt", "col", "lieut", "rev",
    "jno", "wm", "chas", "geo", "jas", "thos", "benj", "saml",
}

_sentence_tokenizer = None
_sentence_model = None


def get_sentence_tokenizer():
    global _sentence_tokenizer
    if _sentence_tokenizer is None:
        import nltk
        from nltk.tokenize.punkt import PunktTokenizer
        try:
            nltk.data.find("tokenizers/punkt_tab/english/")
        except LookupError:
            nltk.download("punkt_tab", quiet=True)
        _sentence_tokenizer = PunktTokenizer("english")
        _sentence_tokenizer._params.abbrev_types.update(PERIOD_ABBREVIATIONS)
    return _sentence_tokenizer


def split_sentences(text: str) -> List[str]:
    """
    Splits cleaned text into sentences with NLTK punkt. Line and paragraph
    breaks left by the cleanup (captions, headings) also end a sentence.
    """
    tokenizer = get_sentence_tokenizer()
    sentences = []
    for line in re.split(r"\n+", text):
        line = line.strip()
        if line:
            sentences.extend(s.strip() for s in tokenizer.tokenize(line) if s.strip())
    return sentences


def embed_sentences(texts: List[str]) -> np.ndarray:
    """
    Embeds texts with the local MiniLM model, normalized so a dot product
    is cosine similarity. Loaded once, on first use.
    """
    global _sentence_model
    if _sentence_model is None:
        from sentence_transformers import SentenceTransformer
        _sentence_model = SentenceTransformer(SENTENCE_MODEL, device="cpu")
    return _sentence_model.encode(
        texts, batch_size=128, normalize_embeddings=True, show_progress_bar=len(texts) > 1000
    )


def sentence_windows(sentences: List[str], window: int = SEMANTIC_WINDOW) -> List[str]:
    # Each sentence with its neighbours, so a short sentence is judged in context
    return [
        " ".join(sentences[max(0, i - window): i + window + 1])
        for i in range(len(sentences))
    ]


def neighbour_distances(embeddings: np.ndarray) -> np.ndarray:
    # Cosine distance between each sentence window and the next
    if len(embeddings) < 2:
        return np.zeros(0)
    return 1 - np.sum(embeddings[:-1] * embeddings[1:], axis=1)


def group_sentences(
    distances: np.ndarray,
    token_counts: List[int],
    threshold: float,
    min_tokens: int = SEMANTIC_MIN_TOKENS,
    max_tokens: int = SEMANTIC_MAX_TOKENS,
) -> List[List[int]]:
    """
    Groups sentence indices into chunks. distances[i] is the distance
    between sentence i and i + 1. Breaks where it exceeds threshold and is a
    local peak: windowed embeddings spread one topic change over neighbouring
    distances, and breaking at each would leave fragments. Then splits any
    group over max_tokens at its largest internal distance, and merges groups
    under min_tokens into a neighbour when the result fits.
    """
    n = len(token_counts)
    if n == 0:
        return []

    groups, start = [], 0
    for i in range(n - 1):
        is_peak = (i == 0 or distances[i] >= distances[i - 1]) and \
                  (i == n - 2 or distances[i] >= distances[i + 1])
        if distances[i] > threshold and is_peak:
            groups.append(list(range(start, i + 1)))
            start = i + 1
    groups.append(list(range(start, n)))

    def tokens(group):
        return sum(token_counts[i] for i in group)

    def split(group):
        if tokens(group) <= max_tokens or len(group) == 1:
            return [group]
        cut = max(range(len(group) - 1), key=lambda j: distances[group[j]])
        return split(group[: cut + 1]) + split(group[cut + 1:])

    groups = [piece for group in groups for piece in split(group)]

    merged = []
    for group in groups:
        if merged and (tokens(merged[-1]) < min_tokens or tokens(group) < min_tokens) \
                and tokens(merged[-1]) + tokens(group) <= max_tokens:
            merged[-1] = merged[-1] + group
        else:
            merged.append(group)
    return merged


def chunk_semantic(
    documents: List[Dict],
    embed: Optional[Callable[[List[str]], np.ndarray]] = None,
    percentile: float = SEMANTIC_BREAK_PERCENTILE,
    min_tokens: int = SEMANTIC_MIN_TOKENS,
    max_tokens: int = SEMANTIC_MAX_TOKENS,
    overlap_max_tokens: int = SEMANTIC_OVERLAP_MAX_TOKENS,
) -> List[Dict]:
    """
    Splits documents at topic changes. Sentences are embedded with their
    neighbours, and a chunk ends where the distance between neighbouring
    windows exceeds one threshold for the whole corpus: the given percentile
    of all neighbour distances. A per-document threshold would force breaks
    into every document, even one on a single topic. Chunks stay within
    max_tokens and repeat the previous chunk's last sentence as overlap.
    """
    embed = embed or embed_sentences
    encoder = get_encoder()

    split_docs = []
    for doc in documents:
        sentences = split_sentences(doc["text"])
        split_docs.append((doc, sentences, [len(encoder.encode(s)) for s in sentences]))

    windows = [w for _, sentences, _ in split_docs for w in sentence_windows(sentences)]
    embeddings = np.asarray(embed(windows)) if windows else np.zeros((0, 1))

    doc_distances, offset = [], 0
    for _, sentences, _ in split_docs:
        doc_distances.append(neighbour_distances(embeddings[offset: offset + len(sentences)]))
        offset += len(sentences)

    all_distances = np.concatenate(doc_distances) if doc_distances else np.zeros(0)
    threshold = float(np.percentile(all_distances, percentile)) if len(all_distances) else float("inf")

    chunks = []
    for (doc, sentences, counts), distances in zip(split_docs, doc_distances):
        groups = group_sentences(distances, counts, threshold, min_tokens, max_tokens)
        chunk_index = 0
        previous_last = None
        for group in groups:
            pieces = [" ".join(sentences[i] for i in group)]
            if len(group) == 1 and counts[group[0]] > max_tokens:
                # One sentence over the cap (a run-on OCR passage): split by tokens
                tokens = encoder.encode(pieces[0])
                pieces = [encoder.decode(tokens[i: i + max_tokens]) for i in range(0, len(tokens), max_tokens)]

            # Joined text can tokenize longer than the sum of its sentences
            pieces = [
                encoder.decode(tokens[i: i + max_tokens])
                for piece in pieces
                for tokens in [encoder.encode(piece)]
                for i in range(0, len(tokens), max_tokens)
            ]

            for piece_number, text in enumerate(pieces):
                n_sentences = len(group) if len(pieces) == 1 else 0
                if piece_number == 0 and previous_last is not None:
                    overlap = sentences[previous_last]
                    combined = f"{overlap} {text}"
                    if counts[previous_last] <= overlap_max_tokens \
                            and len(encoder.encode(combined)) <= max_tokens:
                        text, n_sentences = combined, n_sentences + 1 if n_sentences else 0
                chunks.append({
                    "text": text,
                    "chunk_index": chunk_index,
                    "metadata": {
                        **doc["metadata"],
                        "chunk_index": chunk_index,
                        "chunk_method": "semantic",
                        "token_count": len(encoder.encode(text)),
                        "n_sentences": n_sentences,
                    },
                })
                chunk_index += 1
            previous_last = group[-1]

    if chunks:
        sizes = [c["metadata"]["token_count"] for c in chunks]
        print(f"  Semantic chunks: {len(chunks)} (break threshold {threshold:.3f}, "
              f"median {int(np.median(sizes))} tokens, max {max(sizes)})")
    return chunks

