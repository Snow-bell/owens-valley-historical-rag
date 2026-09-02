from typing import List, Dict
from openai import OpenAI
from src.config import (
    OPENAI_API_KEY,
    GENERATION_MODEL,
    TEMPERATURE,
    TOP_P,
    MAX_TOKENS,
)

client = OpenAI(api_key=OPENAI_API_KEY)


SYSTEM_PROMPT = """You are a historical research assistant specializing in the 
Owens Valley region of California circa 1880-1915.

Your role is to answer research questions using ONLY the source passages provided 
to you. Do not draw on outside knowledge. If the provided passages do not contain 
enough information to answer the question, say so explicitly.

For every claim you make, cite the source document it came from.

If sources contradict each other, surface the contradiction and note the bias 
context of each source rather than resolving it arbitrarily.

Be precise and historically grounded. You are helping a writer achieve period 
accuracy — vague answers are not useful."""


def format_context(chunks: List[Dict]) -> str:
    context_parts = []

    for i, chunk in enumerate(chunks):
        meta = chunk["metadata"]

        bias_note = ""
        if meta["bias_level"] != "none":
            bias_note = (
                f" | Bias: {meta['bias_tag']} ({meta['bias_level']})"
            )

        header = (
            f"[Source {i + 1}: {meta['source']}"
            f" | Tier {meta['tier']}"
            f"{bias_note}]"
        )

        context_parts.append(f"{header}\n{chunk['text']}")

    return "\n\n---\n\n".join(context_parts)


def format_sources(chunks: List[Dict]) -> str:
    seen = set()
    sources = []

    for chunk in chunks:
        meta = chunk["metadata"]
        source = meta["source"]

        if source in seen:
            continue
        seen.add(source)

        bias_note = ""
        if meta["bias_level"] != "none":
            bias_note = (
                f" ⚠ {meta['bias_tag'].replace('_', ' ').title()}"
                f" — {meta['bias_level']} bias"
            )

        description = meta.get("description", "")

        sources.append(
            f"  • {source} (Tier {meta['tier']}){bias_note}\n"
            f"    {description}"
        )

    return "\n".join(sources)


def generate(query: str, chunks: List[Dict]) -> Dict:
    context = format_context(chunks)

    user_message = (
        f"Research question: {query}\n\n"
        f"Source passages:\n\n{context}"
    )

    response = client.chat.completions.create(
        model=GENERATION_MODEL,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    answer = response.choices[0].message.content.strip()
    sources = format_sources(chunks)

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks,
    }