import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse, urljoin
from src.config import CORPUS_DIR

BASE_URL = "http://www.owensvalleyhistory.com"
OUTPUT_DIR = CORPUS_DIR / "owensvalleyhistory"

SKIP_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".ico"}
PDF_EXTENSION = ".pdf"
RATE_LIMIT = 1.5  # seconds between requests


def is_internal(url: str) -> bool:
    """Only follow links within owensvalleyhistory.com."""
    parsed = urlparse(url)
    return parsed.netloc in {
        "www.owensvalleyhistory.com",
        "owensvalleyhistory.com",
        "",
    }


def get_extension(url: str) -> str:
    return Path(urlparse(url).path).suffix.lower()


PACK_TRAIN_PATHS = {
    "whitney_pack_trains",
    "whitney_packers1",
    "whitney_packers2",
    "whitney_packers5",
    "whitney_packers6",
    "bob_swandt",
    "packers",
    "packers_reunion",
    "brochures5",
    "sierra_experience1",
    "monache_meadows",
    "packing_50yr_ago",
    "mj_archives01",
    "bancroft_archives",
    "kipp_archives",
    "duane_rossi",
    "ed_brown",
    "ed_turner",
    "irene_kritz",
    "rena_moore",
    "tommy_jefferson",
    "20_mule_team01",
    "chrysler_n_cook",
    "chrysler_n_cook_days",
    "golden_trout",
    "packer_publications",
}


def is_pack_trains_url(url: str) -> bool:
    path = urlparse(url).path
    return any(segment in path for segment in PACK_TRAIN_PATHS)


def fetch(url: str) -> str | None:
    # Returns None on failure rather than raising — caller handles missing pages
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"  [ERROR] Failed to fetch {url}: {e}")
        return None


def download_pdf(url: str) -> None:
    # Flattens subfolder structure into filename to avoid nested dirs in OUTPUT_DIR
    filename = Path(urlparse(url).path).name
    
    # Flatten subfolder structure into filename
    safe_name = urlparse(url).path.strip("/").replace("/", "__") + ".pdf"
    dest = OUTPUT_DIR / safe_name

    if dest.exists():
        print(f"  [SKIP] Already downloaded: {filename}")
        return

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        dest.write_bytes(response.content)
        print(f"  [PDF] Saved: {safe_name}")
    except Exception as e:
        print(f"  [ERROR] Failed to download PDF {url}: {e}")


def extract_text(html: str, url: str) -> str:
    # url param unused but kept for future source-aware filtering
    soup = BeautifulSoup(html, "html.parser")

    # Remove non-content tags
    for tag in soup(["script", "style", "img", "a"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # Clean up whitespace
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def save_text(text: str, url: str) -> None:
    # Skips if file already exists — safe to re-run after interruption
    safe_name = urlparse(url).path.strip("/").replace("/", "__") + ".txt"
    dest = OUTPUT_DIR / safe_name

    if dest.exists():
        print(f"  [SKIP] Already saved: {safe_name}")
        return

    dest.write_text(text, encoding="utf-8")
    print(f"  [PAGE] Saved: {safe_name}")


def get_index_links(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")

    # Find the index heading. Ignore everything above it
    index_heading = None
    for tag in soup.find_all("b"):
        if "Owens Valley History Website Index" in tag.get_text():
            index_heading = tag
            break

    if not index_heading:
        print("  [ERROR] Could not find index heading on homepage.")
        return []

    # Find the next table after the heading
    index_table = None
    for sibling in index_heading.parents:
        next_table = sibling.find_next_sibling("table")
        if next_table:
            index_table = next_table
            break

    if not index_table:
        print("  [ERROR] Could not find index table after heading.")
        return []

    links = []
    for a_tag in index_table.find_all("a", href=True):
        href = a_tag["href"].strip()
        if not href:
            continue
        full_url = urljoin(BASE_URL, href)
        if is_internal(full_url) and not is_pack_trains_url(full_url):
            links.append(full_url)

    # Deduplicate while preserving order
    seen = set()
    unique_links = []
    for url in links:
        if url not in seen:
            seen.add(url)
            unique_links.append(url)

    print(f"  Found {len(unique_links)} index links across Places, People, Things.")
    return unique_links


def crawl() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    visited = set()
    queue = []

    # Mark homepage variants as visited before anything else
    visited.add(BASE_URL)
    visited.add(BASE_URL + "/")
    visited.add("http://owensvalleyhistory.com")
    visited.add("http://owensvalleyhistory.com/")

    # Step 1: fetch homepage and extract index links
    print(f"\nFetching homepage: {BASE_URL}")
    html = fetch(BASE_URL)
    if not html:
        print("[ERROR] Could not fetch homepage. Aborting.")
        return

    index_links = get_index_links(html)
    queue.extend(index_links)

    # Step 2: crawl queue
    print(f"\nStarting crawl — {len(queue)} pages in initial queue.\n")

    while queue:
        url = queue.pop(0)

        if url in visited:
            continue
        if not is_internal(url):
            continue

        ext = get_extension(url)

        if ext in SKIP_EXTENSIONS:
            continue

        visited.add(url)

        if ext == PDF_EXTENSION:
            print(f"  Downloading PDF: {url}")
            download_pdf(url)
            time.sleep(RATE_LIMIT)
            continue

        print(f"  Crawling: {url}")
        html = fetch(url)
        if not html:
            time.sleep(RATE_LIMIT)
            continue

        text = extract_text(html, url)
        if text:
            save_text(text, url)

        soup = BeautifulSoup(html, "html.parser")
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"].strip()
            full_url = urljoin(url, href)
            if (
                full_url not in visited
                and is_internal(full_url)
                and not is_pack_trains_url(full_url)
                and get_extension(full_url) not in SKIP_EXTENSIONS
            ):
                queue.append(full_url)

        time.sleep(RATE_LIMIT)

    print(f"\nCrawl complete. {len(visited)} pages visited.")
    print(f"Output saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    crawl()