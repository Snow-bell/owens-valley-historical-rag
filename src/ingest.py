import re
import unicodedata
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

# Text cleanup. Bump CLEAN_VERSION when the rules change; chunks record it.
# Cleanup fixes layout only: words and period spellings are never changed.
CLEAN_VERSION = 1
# A document's layout decides how its line breaks are cleaned:
#   "blocks"  PDFs; each PyMuPDF text block is a paragraph, so breaks inside are soft
#   "lines"   crawled pages; one line per HTML text fragment
WORD = re.compile(r"[A-Za-z]+")
COMPOUND = re.compile(r"\b[A-Za-z]+-[A-Za-z]+\b")
LINE_END_HYPHEN = re.compile(r"([A-Za-z]+)-[ \t]*\n[ \t]*([a-z]+)")
INVISIBLE = re.compile("[\u00ad\u200b\u200c\u200d\u2060\ufeff]")
ESCAPED_CODEPOINT = re.compile(r"\\u[0-9a-fA-F]{4}")   # OCR layers that store "\u25a0" as text
OCR_SYMBOLS = re.compile(r"(?<!\S)[■□▪▫●○◆◇•¦]+(?!\S)")
SENTENCE_END = re.compile(r"[.!?:;\"'”’)\]]$")


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
    Extract the text of each page of a clean (text-selectable) PDF using
    PyMuPDF, one text block per paragraph, separated by blank lines. Blocks
    keep the PDF's own order; sorting them would interleave newspaper columns.
    """
    doc = fitz.open(filepath)
    try:
        pages = []
        for page in doc:
            blocks = [b[4].strip("\n") for b in page.get_text("blocks") if b[6] == 0]
            pages.append("\n\n".join(b for b in blocks if b.strip()))
        return pages
    finally:
        doc.close()


def extract_text(filepath: Path) -> str:
    return "\n\n".join(extract_pages(filepath)).strip()


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


def build_vocabulary(texts: List[str]) -> Tuple[Counter, Counter]:
    """
    Counts words and hyphenated compounds across the corpus, leaving out
    words split across a line break, so join_hyphenated can tell a word
    broken by typesetting ("to-/gether") from a real compound ("well-known").
    """
    words, compounds = Counter(), Counter()
    for text in texts:
        unsplit = LINE_END_HYPHEN.sub(" ", text)
        words.update(w.lower() for w in WORD.findall(unsplit))
        compounds.update(c.lower() for c in COMPOUND.findall(unsplit))
    return words, compounds


def hyphen_join(first: str, second: str, words: Counter, compounds: Counter) -> str:
    """
    Rejoins a word hyphenated across a line break. Keeps the hyphen only when
    the corpus uses the hyphenated form more often than the joined one.
    """
    joined = first + second
    if compounds[f"{first}-{second}".lower()] > words[joined.lower()]:
        return f"{first}-{second}"
    return joined


def join_hyphenated(text: str, words: Counter, compounds: Counter) -> str:
    return LINE_END_HYPHEN.sub(lambda m: hyphen_join(m[1], m[2], words, compounds), text)


def is_heading(text: str) -> bool:
    # Short and mostly capitals, like "CHAPTER II" or "NATIVE CUSTOMS"
    letters = [c for c in text if c.isalpha()]
    return len(text) <= 80 and bool(letters) and sum(c.isupper() for c in letters) / len(letters) >= 0.8


def join_blocks(previous: str, following: str, words: Counter, compounds: Counter) -> Optional[str]:
    """
    Joins two PDF text blocks when the break between them is soft: a word
    hyphenated across it, or a block that stops mid-sentence. Returns None
    for a real paragraph break: the previous block ends a sentence or is a
    heading. Scanned books split one paragraph into many blocks, so a block
    edge alone isn't a paragraph break.
    """
    hyphen = re.search(r"([A-Za-z]+)-$", previous)
    first_word = re.match(r"([a-z]+)", following)
    if hyphen and first_word:
        joined = hyphen_join(hyphen[1], first_word[1], words, compounds)
        return previous[: hyphen.start()] + joined + following[first_word.end():]
    if SENTENCE_END.search(previous) or is_heading(previous):
        return None
    return f"{previous} {following}"


def join_lines(text: str, layout: str, words: Counter, compounds: Counter) -> str:
    """
    Turns soft line breaks into spaces. In "blocks" text every break inside
    a block is soft, and blocks are joined by join_blocks. In "lines" text a
    line joins the next only when it doesn't end a sentence and the next
    starts lowercase, so captions and headings stay on their own lines.
    """
    paragraphs = []
    for paragraph in re.split(r"\n\s*\n", text):
        lines = [line.strip() for line in paragraph.split("\n") if line.strip()]
        if not lines:
            continue
        if layout == "blocks":
            block = " ".join(lines)
            joined = join_blocks(paragraphs[-1], block, words, compounds) if paragraphs else None
            if joined is None:
                paragraphs.append(block)
            else:
                paragraphs[-1] = joined
            continue
        merged = [lines[0]]
        for line in lines[1:]:
            if not SENTENCE_END.search(merged[-1]) and line[0].islower():
                merged[-1] += " " + line
            else:
                merged.append(line)
        paragraphs.append("\n".join(merged))
    return "\n\n".join(paragraphs)


def clean_text(text: str, layout: str, words: Counter, compounds: Counter) -> str:
    """
    Fixes layout so text splits into sentences: normalizes Unicode (NFC, so
    diacritics stay), drops invisible characters and isolated OCR symbols,
    rejoins hyphenated words and joins soft line breaks.
    """
    text = unicodedata.normalize("NFC", text)
    text = INVISIBLE.sub("", text)
    text = ESCAPED_CODEPOINT.sub(" ", text)
    text = OCR_SYMBOLS.sub(" ", text)
    text = re.sub(r"[ \t\u00a0]+", " ", text)
    text = join_hyphenated(text, words, compounds)
    text = join_lines(text, layout, words, compounds)
    return re.sub(r" {2,}", " ", text).strip()


def join_pages(
    pages: List[Tuple[int, str]],
    words: Optional[Counter] = None,
    compounds: Optional[Counter] = None,
) -> Tuple[str, List[List[int]]]:
    """
    Joins cleaned page texts and records where each page starts, as
    [character offset, page number] pairs, so chunks can cite pages.
    A paragraph or word that runs over a page break is joined back together.
    """
    words = words if words is not None else Counter()
    compounds = compounds if compounds is not None else Counter()
    text, offsets = "", []
    for number, page_text in pages:
        if not page_text:
            continue
        if text:
            # Same rule as between blocks; the page starts where its own text begins
            last_paragraph = text.rsplit("\n\n", 1)[-1]
            joined = join_blocks(last_paragraph, page_text, words, compounds)
            if joined is None:
                text += "\n\n"
            else:
                head = text[: len(text) - len(last_paragraph)]
                carried = len(joined) - len(page_text)
                text, page_text = head + joined[:carried], joined[carried:]
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
    """
    Loads every corpus document in two passes: extraction (page ranges and
    page furniture for PDFs), then cleanup, which needs a vocabulary built
    from the whole corpus to rejoin hyphenated words.
    """
    corpus_files = sorted(
        list(CORPUS_DIR.rglob("*.pdf")) +
        list(CORPUS_DIR.rglob("*.txt"))
    )

    if not corpus_files:
        raise FileNotFoundError(f"No files found in {CORPUS_DIR}")

    extracted = []

    for filepath in corpus_files:
        print(f"  Loading: {filepath.name}")
        try:
            metadata = get_metadata(filepath)
            # Registry page ranges choose what to index; they aren't chunk metadata
            page_ranges = metadata.pop("pages", None)

            if filepath.suffix == ".pdf":
                pages = select_pages(extract_pages(filepath), page_ranges, filepath.name)
                stripped = strip_page_furniture([page_text for _, page_text in pages])
                content = [(number, page_text) for (number, _), page_text in zip(pages, stripped)]
                extracted.append((filepath, metadata, "blocks", content))
            elif filepath.suffix == ".txt":
                extracted.append((filepath, metadata, "lines", extract_text_file(filepath)))

        except Exception as e:
            print(f"  [ERROR] Failed to load {filepath.name}: {e}")
            continue

    words, compounds = build_vocabulary([
        page_text
        for _, _, layout, content in extracted
        for page_text in ([t for _, t in content] if layout == "blocks" else [content])
    ])

    documents = []

    for filepath, metadata, layout, content in extracted:
        try:
            page_offsets = None
            if layout == "blocks":
                cleaned = [(n, clean_text(t, layout, words, compounds)) for n, t in content]
                text, page_offsets = join_pages(cleaned, words, compounds)
            else:
                text = clean_text(content, layout, words, compounds)

            # Safety cap; long books are trimmed with registry page ranges instead
            if len(text) > MAX_CHARS:
                print(f"  [WARNING] {filepath.name} cut from {len(text):,} to {MAX_CHARS:,} characters")
                text = text[:MAX_CHARS]
                if page_offsets:
                    page_offsets = [p for p in page_offsets if p[0] < MAX_CHARS]

            if not text.strip():
                print(f"  [WARNING] No text extracted from: {filepath.name}")
                continue

            metadata["clean_version"] = CLEAN_VERSION
            documents.append({
                "text": text,
                "metadata": metadata,
                "layout": layout,
                "page_offsets": page_offsets,
            })

        except Exception as e:
            print(f"  [ERROR] Failed to clean {filepath.name}: {e}")
            continue

    print(f"\n  Loaded {len(documents)} documents from corpus.")
    return documents
