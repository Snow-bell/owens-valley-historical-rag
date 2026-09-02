import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict
from src.config import CORPUS_DIR
from src.corpus_registry import CORPUS_REGISTRY


def get_metadata(filepath: Path) -> Dict:
    """
    Look up bias metadata for a given file from the corpus registry.
    Handles flat files, subfolder files, and womens-club-biographies default.
    """
    # Build relative key from corpus dir (e.g. "chronicling-america/la-faces.pdf")
    relative_key = str(filepath.relative_to(CORPUS_DIR))

    if relative_key in CORPUS_REGISTRY:
        metadata = CORPUS_REGISTRY[relative_key].copy()

    # Check just the filename (flat corpus files)
    elif filepath.name in CORPUS_REGISTRY:
        metadata = CORPUS_REGISTRY[filepath.name].copy()

    # Apply womens club default for that subfolder
    elif "womens-club-biographies" in str(filepath):
        metadata = CORPUS_REGISTRY["__womens_club_default__"].copy()

    # Unknown file — flag it rather than silently ingesting
    else:
        print(f"  [WARNING] No registry entry found for: {relative_key}")
        metadata = {
            "tier": 0,
            "bias_tag": "unknown",
            "bias_level": "unknown",
            "description": "No registry entry found for this document.",
        }

    metadata["source"] = filepath.name
    metadata["source_path"] = relative_key
    return metadata


def extract_text(filepath: Path) -> str:
    """
    Extract text from a clean (text-selectable) PDF using PyMuPDF.
    """
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()


def load_corpus() -> List[Dict]:
    """
    Load all PDFs from the corpus directory recursively.
    Returns a list of dicts with 'text' and 'metadata' for each document.
    """
    corpus_files = sorted(
        list(CORPUS_DIR.rglob("*.pdf")) +
        list(CORPUS_DIR.rglob("*.txt"))
    )

    if not pdf_files:
        raise FileNotFoundError(f"No PDFs found in {CORPUS_DIR}")

    documents = []

    for filepath in pdf_files:
        print(f"  Loading: {filepath.name}")
        try:
            text = extract_text(filepath)

            if not text:
                print(f"  [WARNING] No text extracted from: {filepath.name}")
                continue

            metadata = get_metadata(filepath)

            documents.append({
                "text": text,
                "metadata": metadata,
            })

        except Exception as e:
            print(f"  [ERROR] Failed to load {filepath.name}: {e}")
            continue

    print(f"\n  Loaded {len(documents)} documents from corpus.")
    return documents