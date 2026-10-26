import re
import pymupdf as fitz
from collections import Counter
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from src.config import CORPUS_DIR, MAX_CHARS
from src.corpus_registry import CORPUS_REGISTRY

# Page furniture: page numbers and running heads at the top and bottom of PDF pages
PAGE_NUMBER = re.compile(r"^[\[(]?\s*\d{1,3}\s*[\])]?$")
FURNITURE_MAX_LINES = 3       # most lines stripped from each edge of a page
RUNNING_HEAD_MIN_PAGES = 3    # an edge line repeated on this many pages is a running head
RUNNING_HEAD_MIN_CHARS = 10   # shorter repeats ("THE", "OF") are body text


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


def extract_pages(filepath: Path) -> List[str]:
    """
    Extract the text of each page of a clean (text-selectable) PDF using PyMuPDF.
    """
    doc = fitz.open(filepath)
    try:
        return [page.get_text() for page in doc]
    finally:
        doc.close()


def extract_text(filepath: Path) -> str:
    return "".join(extract_pages(filepath)).strip()


def running_head_key(line: str) -> str:
    # Ignore digits so "32 THE STORY OF INYO" and "33 THE STORY OF INYO" match
    return re.sub(r"\d+", "#", line.strip().upper())


def strip_page_furniture(pages: List[str]) -> List[str]:
    """
    Removes page numbers and running heads from the top and bottom of each
    page. A running head is a line of at least RUNNING_HEAD_MIN_CHARS that
    appears among the first or last two lines of RUNNING_HEAD_MIN_PAGES or
    more pages. At most FURNITURE_MAX_LINES lines go from each edge.
    """
    split = [page.split("\n") for page in pages]

    counts = Counter()
    for lines in split:
        content = [line for line in lines if line.strip()]
        edges = content[:2] + content[-2:]
        counts.update({running_head_key(line) for line in edges})
    running_heads = {
        key for key, count in counts.items()
        if count >= RUNNING_HEAD_MIN_PAGES and len(key) >= RUNNING_HEAD_MIN_CHARS
    }

    def is_furniture(line: str) -> bool:
        line = line.strip()
        return bool(PAGE_NUMBER.match(line)) or running_head_key(line) in running_heads

    stripped = []
    for lines in split:
        start, end = 0, len(lines)
        for step in (1, -1):
            removed = 0
            while start < end and removed < FURNITURE_MAX_LINES:
                line = lines[start] if step == 1 else lines[end - 1]
                if line.strip() and not is_furniture(line):
                    break
                if line.strip():
                    removed += 1
                if step == 1:
                    start += 1
                else:
                    end -= 1
        stripped.append("\n".join(lines[start:end]))
    return stripped


def select_pages(
    pages: List[str], ranges: Optional[List[List[int]]], name: str = ""
) -> List[Tuple[int, str]]:
    """
    Returns (page number, text) for the pages to keep. ranges are inclusive,
    1-based PDF page numbers, e.g. [[9, 361]]; None keeps every page.
    """
    numbered = list(enumerate(pages, start=1))
    if not ranges:
        return numbered
    for first, last in ranges:
        if first < 1 or last > len(pages) or first > last:
            print(f"  [WARNING] Page range {first}-{last} outside 1-{len(pages)} in {name}")
    return [(n, text) for n, text in numbered if any(a <= n <= b for a, b in ranges)]


def join_pages(pages: List[Tuple[int, str]]) -> Tuple[str, List[List[int]]]:
    """
    Joins page texts and records where each page starts, as
    [character offset, page number] pairs, so chunks can cite pages.
    """
    text, offsets = "", []
    for number, page_text in pages:
        if text and not text.endswith("\n"):
            text += "\n"
        offsets.append([len(text), number])
        text += page_text
    return text, offsets


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
            metadata = get_metadata(filepath)
            # Registry page ranges choose what to index; they aren't chunk metadata
            page_ranges = metadata.pop("pages", None)
            page_offsets = None

            if filepath.suffix == ".pdf":
                pages = select_pages(extract_pages(filepath), page_ranges, filepath.name)
                cleaned = strip_page_furniture([page_text for _, page_text in pages])
                text, page_offsets = join_pages(
                    [(number, page_text) for (number, _), page_text in zip(pages, cleaned)]
                )
            elif filepath.suffix == ".txt":
                text = extract_text_file(filepath)
            else:
                continue

            # Safety cap; long books are trimmed with registry page ranges instead
            if len(text) > MAX_CHARS:
                print(f"  [WARNING] {filepath.name} cut from {len(text):,} to {MAX_CHARS:,} characters")
                text = text[:MAX_CHARS]
                if page_offsets:
                    page_offsets = [p for p in page_offsets if p[0] < MAX_CHARS]

            if not text.strip():
                print(f"  [WARNING] No text extracted from: {filepath.name}")
                continue

            documents.append({
                "text": text,
                "metadata": metadata,
                "page_offsets": page_offsets,
            })

        except Exception as e:
            print(f"  [ERROR] Failed to load {filepath.name}: {e}")
            continue

    print(f"\n  Loaded {len(documents)} documents from corpus.")
    return documents