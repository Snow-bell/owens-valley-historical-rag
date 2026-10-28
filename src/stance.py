import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional
from openai import OpenAI
from src.config import (
    OPENAI_API_KEY,
    STANCE_MODEL,
    STANCE_PROMPT_VERSION,
    STANCE_CACHE,
    STANCE_WORKERS,
)

client = OpenAI(api_key=OPENAI_API_KEY, max_retries=5)

STANCE_LABEL = f"{STANCE_MODEL}@v{STANCE_PROMPT_VERSION}"
PARTIES = ["paiute", "los_angeles", "settlers"]
STANCES = ["favourable", "hostile", "neutral", "not_mentioned"]
MAX_LOADED_TERMS = 5
CACHE_SAVE_EVERY = 200   # chunks; an interrupted run keeps what it labeled

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        **{party: {"type": "string", "enum": STANCES} for party in PARTIES},
        "loaded_terms": {"type": "array", "items": {"type": "string"}},
        "framing": {"type": "string"},
    },
    "required": [*PARTIES, "loaded_terms", "framing"],
}

STANCE_PROMPT = """You label the stance of passages from historical sources about the Owens Valley, California. The sources range from 1860s newspapers and settler histories to modern Paiute and academic accounts.

For each party, give the stance of the passage's own author or narrator toward that party:
- paiute: the Owens Valley Paiute and other Native people
- los_angeles: the City of Los Angeles, its Department of Water and Power, and aqueduct promoters
- settlers: white settlers, ranchers, miners and Owens Valley residents

Stances:
- favourable: the author praises, defends or sympathizes with them in evaluative language
- hostile: the author demeans, mocks, blames or dehumanizes them
- neutral: they appear, but the author only describes or reports, without judging
- not_mentioned: they don't appear in the passage

Rules:
- Describing a group's customs, foods, tools or history is neutral, however detailed. Judge the author's evaluative language, not the topic.
- Recording violence or injustice done to a group is neutral, or favourable if the author takes their side. It is not hostile toward the victims.
- Recording what a group did, including violence, is neutral toward them unless the author adds judgment.
- Calling a group primitive, ignorant, childlike or doomed is demeaning, so hostile, even inside a description of their skills.
- A party counts as mentioned only if the passage names or clearly refers to it. Don't infer a party from the general topic.
- Quoted speech is the speaker's stance, not the author's, unless the author endorses it.

loaded_terms: words or short phrases quoted exactly from the passage in which the author judges a group: slurs, demeaning labels ("savages", "bucks"), dehumanizing comparisons, or promotional language ("wonderful growth", "the greatest enterprise"). Plain description of events, even of violence or loss ("massacre", "displacement", "revoked"), is not a loaded term: if the phrase would fit in a neutral encyclopedia, leave it out. At most 5; empty if none.

framing: the passage's frame in 2-5 words, e.g. "civic progress", "dispossession", "frontier conflict", "ethnographic description", "natural history", "family history"."""

# Period slurs and demeaning labels, always flagged as loaded terms. Every
# model short of GPT-4o missed some of these in the pilot. Only terms that
# are demeaning wherever they appear in the corpus: "buck" (deer, a
# nickname), "papoose" (captions, place names) and "heathen" are left out;
# "savage" is lowercase only (James Savage's trading post) and "Digger"
# capitalized only (miners dig).
PERIOD_TERMS = [
    re.compile(r"\bsquaws?\b", re.IGNORECASE),
    re.compile(r"\bred[- ]?skins?\b", re.IGNORECASE),
    re.compile(r"\bsavages?\b"),
    re.compile(r"\bred m[ae]n\b", re.IGNORECASE),
    re.compile(r"\bDiggers?\b"),
    re.compile(r"\bhalf[- ]?breeds?\b", re.IGNORECASE),
    re.compile(r"\bJaps?\b"),
    re.compile(r"\bchinam[ae]n\b", re.IGNORECASE),
    re.compile(r"\bgreasers?\b", re.IGNORECASE),
]


def period_terms(text: str) -> List[str]:
    """Period slurs in the text, each once, as written."""
    found = []
    for pattern in PERIOD_TERMS:
        for match in pattern.finditer(text):
            if match.group(0).lower() not in (term.lower() for term in found):
                found.append(match.group(0))
    return found


def model_input(chunk: Dict) -> str:
    source = chunk["metadata"].get("context_header") or chunk["metadata"]["source"]
    return f"Source: {source}\n\nPassage:\n{chunk['text']}"


def cache_key(chunk: Dict) -> str:
    # The model, prompt version and exact input decide the label
    return hashlib.sha256(f"{STANCE_LABEL}\n{model_input(chunk)}".encode("utf-8")).hexdigest()


def load_cache() -> Dict[str, Dict]:
    if not STANCE_CACHE.exists():
        return {}
    return json.loads(STANCE_CACHE.read_text(encoding="utf-8"))


def save_cache(cache: Dict[str, Dict]) -> None:
    STANCE_CACHE.parent.mkdir(parents=True, exist_ok=True)
    STANCE_CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")


def label_chunk(chunk: Dict) -> Dict:
    """Asks the stance model for one chunk's labels, constrained to SCHEMA."""
    response = client.chat.completions.create(
        model=STANCE_MODEL,
        temperature=0,
        seed=42,
        response_format={"type": "json_schema", "json_schema": {"name": "stance", "strict": True, "schema": SCHEMA}},
        messages=[
            {"role": "system", "content": STANCE_PROMPT},
            {"role": "user", "content": model_input(chunk)},
        ],
    )
    return json.loads(response.choices[0].message.content)


def stance_metadata(label: Dict, text: str) -> Dict:
    """
    Flat Chroma fields from a label. Period slurs found in the text are added
    to the model's loaded terms.
    """
    terms = label["loaded_terms"][:MAX_LOADED_TERMS]
    for term in period_terms(text):
        if term.lower() not in (t.lower() for t in terms):
            terms.append(term)
    return {
        **{f"stance_{party}": label[party] for party in PARTIES},
        "loaded_terms": "; ".join(terms),
        "framing": label["framing"],
        "stance_version": STANCE_LABEL,
    }


def label_chunks(chunks: List[Dict]) -> None:
    """
    Adds stance labels to each chunk's metadata. Labels come from the cache
    when the chunk's text is unchanged; the rest are requested in parallel.
    A chunk whose request fails is indexed without labels.
    """
    cache = load_cache()
    todo = [chunk for chunk in chunks if cache_key(chunk) not in cache]
    print(f"\n  Stance labels: {len(chunks) - len(todo)} cached, {len(todo)} to label with {STANCE_MODEL}")

    def request(chunk: Dict) -> Optional[Dict]:
        try:
            return label_chunk(chunk)
        except Exception as e:
            print(f"  [WARNING] Stance label failed for {chunk['metadata']['source']}: {e}")
            return None

    failed = 0
    with ThreadPoolExecutor(max_workers=STANCE_WORKERS) as pool:
        for done, (chunk, label) in enumerate(zip(todo, pool.map(request, todo)), start=1):
            if label is None:
                failed += 1
            else:
                cache[cache_key(chunk)] = label
            if done % CACHE_SAVE_EVERY == 0:
                save_cache(cache)
                print(f"  Labeled {done} / {len(todo)}")
    if todo:
        save_cache(cache)

    for chunk in chunks:
        label = cache.get(cache_key(chunk))
        if label:
            chunk["metadata"].update(stance_metadata(label, chunk["text"]))
    if failed:
        print(f"  [WARNING] {failed} chunks indexed without stance labels")
