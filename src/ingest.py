import pymupdf as fitz
from pathlib import Path
from typing import List, Dict
from src.config import CORPUS_DIR
from src.corpus_registry import CORPUS_REGISTRY
from src.config import CORPUS_DIR, MAX_CHARS


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
        
    elif "owensvalleyhistory" in str(filepath):
        metadata = CORPUS_REGISTRY["__owensvalleyhistory_default__"].copy()

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


def extract_text_file(filepath: Path) -> str:
    try:
        return filepath.read_text(encoding="utf-8").strip()
    except Exception as e:
        print(f"  [ERROR] Could not read {filepath.name}: {e}")
        return ""
    

def load_corpus() -> List[Dict]:
    corpus_files = sorted(
        list(CORPUS_DIR.rglob("*.pdf")) +
        list(CORPUS_DIR.rglob("*.txt"))
    )

    if not corpus_files:
        raise FileNotFoundError(f"No files found in {CORPUS_DIR}")

    documents = []

    for filepath in corpus_files:
        print(f"  Loading: {filepath.name}")
        try:
            if filepath.suffix == ".pdf":
                text = extract_text(filepath)
            elif filepath.suffix == ".txt":
                text = extract_text_file(filepath)
            else:
                continue
            
            # Cap document size to prevent runaway chunking
            MAX_CHARS = 15000
            if len(text) > MAX_CHARS:
                text = text[:MAX_CHARS]

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