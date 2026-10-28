import ollama as ollama_client
from typing import List, Dict, Optional
from openai import OpenAI
from src.config import (
    OPENAI_API_KEY,
    GENERATION_MODEL,
    TEMPERATURE,
    TOP_P,
    MAX_TOKENS,
)

openai_client = OpenAI(api_key=OPENAI_API_KEY)


SYSTEM_PROMPT = """You are a historical research assistant specializing in the 
Owens Valley region of California circa 1880-1930.

Your role is to answer research questions using ONLY the source passages provided 
to you. Do not draw on outside knowledge. If the provided passages do not contain 
enough information to answer the question, say so explicitly.

For every claim you make, cite the source it came from by its title, with the
page numbers when the passage gives them, e.g. (The Story of Inyo, p. 32).

If sources contradict each other, surface the contradiction and note the bias 
context of each source rather than resolving it arbitrarily.

Some passages are labeled with the stance their author takes toward the Paiute,
Los Angeles or the settlers, the loaded terms the author uses, and the passage's
framing. Use these labels to notice when sources take opposing stances toward the
same people, and say so. When you rely on a passage with loaded or demeaning
language, point that out instead of repeating its terms as your own description.
The passage text and its bias tag come first; the labels only help you read them.
Don't mention the labels themselves.

Be precise and historically grounded. You are helping a writer achieve period 
accuracy — vague answers are not useful."""


def source_title(meta: Dict) -> str:
    # Indexes built before titles existed have only the file name
    return meta.get("title") or meta["source"]


def page_range(meta: Dict) -> str:
    # Printed pages, only for documents that have them (see chunk.add_page_ranges)
    start, end = meta.get("page_start"), meta.get("page_end")
    if not start:
        return ""
    return str(start) if start == end else f"{start}–{end}"


def page_label(ranges: List[str]) -> str:
    if not ranges:
        return ""
    single = len(ranges) == 1 and "–" not in ranges[0]
    return ("p. " if single else "pp. ") + ", ".join(ranges)


PARTY_NAMES = {"paiute": "Paiute", "los_angeles": "Los Angeles", "settlers": "settlers"}


def stance_note(meta: Dict) -> str:
    """
    The chunk's stance labels for the generator: stances other than neutral
    or not mentioned, loaded terms and framing. Empty for chunks indexed
    without labels.
    """
    if "stance_version" not in meta:
        return ""
    stances = [
        f"{meta[f'stance_{party}']} to {name}"
        for party, name in PARTY_NAMES.items()
        if meta.get(f"stance_{party}") in ("favourable", "hostile")
    ]
    parts = []
    if stances:
        parts.append("Stance: " + ", ".join(stances))
    if meta.get("loaded_terms"):
        parts.append("Loaded terms: " + ", ".join(f'"{t}"' for t in meta["loaded_terms"].split("; ")))
    if meta.get("framing"):
        parts.append(f"Framing: {meta['framing']}")
    return " | ".join(parts)


def format_context(chunks: List[Dict]) -> str:
    context_parts = []

    for i, chunk in enumerate(chunks):
        meta = chunk["metadata"]

        bias_note = ""
        if meta["bias_level"] != "none":
            bias_note = (
                f" | Bias: {meta['bias_tag']} ({meta['bias_level']})"
            )

        pages = page_label([page_range(meta)] if page_range(meta) else [])
        header = (
            f"[Source {i + 1}: {source_title(meta)}"
            f"{f' | {pages}' if pages else ''}"
            f" | Tier {meta['tier']}"
            f"{bias_note}]"
        )
        stance = stance_note(meta)
        if stance:
            header += f"\n[{stance}]"

        context_parts.append(f"{header}\n{chunk['text']}")

    return "\n\n---\n\n".join(context_parts)


def format_sources(chunks: List[Dict]) -> str:
    # One line per source, in retrieval order, listing the pages of all its chunks
    pages = {}
    for chunk in chunks:
        meta = chunk["metadata"]
        pages_here = page_range(meta)
        source_pages = pages.setdefault(meta["source"], [])
        if pages_here and pages_here not in source_pages:
            source_pages.append(pages_here)

    seen = set()
    sources = []

    for chunk in chunks:
        meta = chunk["metadata"]
        source = meta["source"]

        if source in seen:
            continue
        seen.add(source)

        name = source_title(meta)
        if pages[source]:
            name += ", " + page_label(pages[source])

        bias_note = ""
        if meta["bias_level"] != "none":
            bias_note = (
                f" ⚠ {meta['bias_tag'].replace('_', ' ').title()}"
                f" — {meta['bias_level']} bias"
            )

        description = meta.get("description", "")

        sources.append(
            f"  • {name} (Tier {meta['tier']}){bias_note}\n"
            f"    {description}"
        )

    return "\n".join(sources)


def format_stance(chunks: List[Dict]) -> str:
    """
    The --verbose panel: each retrieved chunk with its pages, registry tag,
    stance toward each party it mentions, loaded terms and framing.
    """
    entries = []
    for i, chunk in enumerate(chunks, start=1):
        meta = chunk["metadata"]
        name = source_title(meta)
        if page_range(meta):
            name += ", " + page_label([page_range(meta)])
        registry = meta["bias_tag"].replace("_", " ")
        if meta["bias_level"] != "none":
            registry += f" ({meta['bias_level']})"
        lines = [f"{i}. {name}   registry: {registry}"]

        if "stance_version" not in meta:
            lines.append("   No stance labels; reindex to add them.")
        else:
            mentioned = [
                f"{label}: {meta[f'stance_{party}']}"
                for party, label in (("paiute", "Paiute"), ("los_angeles", "Los Angeles"), ("settlers", "Settlers"))
                if meta.get(f"stance_{party}") not in (None, "not_mentioned")
            ]
            lines.append("   " + (" · ".join(mentioned) if mentioned else "No party mentioned"))
            if meta.get("loaded_terms"):
                lines.append("   Loaded terms: " + ", ".join(f'"{t}"' for t in meta["loaded_terms"].split("; ")))
            if meta.get("framing"):
                lines.append(f"   Framing: {meta['framing']}")
        entries.append("\n".join(lines))
    return "\n\n".join(entries)


def generate_openai(query: str, chunks: List[Dict]) -> str:
    context = format_context(chunks)
    user_message = (
        f"Research question: {query}\n\n"
        f"Source passages:\n\n{context}"
    )
    response = openai_client.chat.completions.create(
        model=GENERATION_MODEL,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content.strip()


def generate_ollama(query: str, chunks: List[Dict], model: str) -> str:
    context = format_context(chunks)
    user_message = (
        f"Research question: {query}\n\n"
        f"Source passages:\n\n{context}"
    )
    response = ollama_client.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    return response.message.content.strip()


def generate(query: str, chunks: List[Dict], model: str = "openai") -> Dict:
    if model == "openai":
        answer = generate_openai(query, chunks)
    else:
        answer = generate_ollama(query, chunks, model)

    sources = format_sources(chunks)

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks,
        "model": model,
    }