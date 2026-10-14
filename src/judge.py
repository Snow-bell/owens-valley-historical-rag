import json
import ollama as ollama_client
from typing import Dict, List, Optional
from openai import OpenAI
from src.config import (
    OPENAI_API_KEY,
    JUDGE_PROVIDER,
    JUDGE_MODEL,
    JUDGE_NUM_CTX,
)
from src.results import DIMENSIONS

client = OpenAI(api_key=OPENAI_API_KEY)

JUDGE_MAX_TOKENS = 300
JUDGE_SEED = 42
JUDGE_ATTEMPTS = 2  # one retry when the response isn't valid scores

# Bump when JUDGE_PROMPT changes. Recorded with the model in each results row,
# so scores from different prompt versions are never compared.
# v1 (endpoint-only anchors) is in commit c631743.
JUDGE_PROMPT_VERSION = "v2"
JUDGE_LABEL = f"{JUDGE_MODEL}@{JUDGE_PROMPT_VERSION}"


JUDGE_PROMPT = """You are an evaluator assessing the quality of a historical
research assistant's answer. You will be given a research question, the answer
produced, and the source passages used — each labeled with their bias context.

Score the answer on four dimensions. Respond ONLY with a valid JSON object —
no preamble, no markdown, no explanation outside the JSON.

Score each dimension against its level descriptions. A 5 means the
answer meets every part of that level's description. An answer that
is good but falls short in any one way is a 4.

Scoring dimensions (each 1-5):

1. contextual_alignment
   How well does the answer address the specific question asked?
   1 = answer is off-topic or ignores the question
   2 = touches the topic but misses what the question asks
   3 = answers part of the question; other parts are skipped or answered
       only in general terms
   4 = answers the question, but drifts into tangents or covers one part
       thinly
   5 = addresses every part of the question directly and stays on it

2. source_faithfulness
   Does the answer stay grounded in the provided sources?
   1 = central claims are unsupported by or contradict the sources
   2 = several claims cannot be traced to the sources
   3 = mostly grounded, but at least one substantive claim comes from
       outside the sources
   4 = grounded throughout, but some claims are not attributed to a named
       source or slightly overstate what a passage says
   5 = every claim is traceable to a provided passage and attributed to
       its source

3. specificity
   Are the details concrete and particular rather than vague and generic?
   1 = generic statements that could apply to any time or place
   2 = mostly generic, with one or two concrete details
   3 = a mix of concrete details and generic summary
   4 = mostly concrete, but leaves out names, dates, places or figures
       from the passages that bear on the question
   5 = uses the names, dates, places and figures from the passages that
       bear on the question

4. bias_handling
   Does the answer appropriately surface or account for source bias?
   1 = presents biased sources as neutral fact without any qualification
   3 = acknowledges bias exists but doesn't meaningfully address it
   5 = clearly flags biased sources, surfaces contradictions between
       perspectives, and does not uncritically adopt a biased framing

When the passages do not fully answer the question:
   An answer that says so plainly and does not fill the gap from outside
   knowledge is behaving correctly. Score source_faithfulness on the
   claims it does make, contextual_alignment on how well it answers what
   the passages support and how clearly it states what they leave out,
   and specificity against the details the passages actually contain.
   Do not lower a score only because the passages are thin.

Return this exact structure:
{
    "contextual_alignment": <1-5>,
    "source_faithfulness": <1-5>,
    "specificity": <1-5>,
    "bias_handling": <1-5>,
    "reasoning": "<one sentence explaining the scores>"
}"""


# Constrains Ollama output to the structure JUDGE_PROMPT asks for
SCORE_SCHEMA = {
    "type": "object",
    "properties": {
        **{dim: {"type": "integer", "minimum": 1, "maximum": 5} for dim in DIMENSIONS},
        "reasoning": {"type": "string"},
    },
    "required": [*DIMENSIONS, "reasoning"],
}


def build_user_message(query: str, answer: str, chunks: List[Dict]) -> str:
    context = "\n\n---\n\n".join(
        f"[{c['metadata']['source']}"
        f" | bias: {c['metadata']['bias_tag']}"
        f" | level: {c['metadata']['bias_level']}]\n{c['text']}"
        for c in chunks
    )

    return (
        f"Research question: {query}\n\n"
        f"Answer to evaluate:\n{answer}\n\n"
        f"Source passages used:\n{context}"
    )


def judge_openai(user_message: str) -> str:
    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        temperature=0.0,
        max_tokens=JUDGE_MAX_TOKENS,
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content.strip()


def judge_ollama(user_message: str) -> str:
    response = ollama_client.chat(
        model=JUDGE_MODEL,
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user", "content": user_message},
        ],
        format=SCORE_SCHEMA,
        options={
            "num_ctx": JUDGE_NUM_CTX,
            "num_predict": JUDGE_MAX_TOKENS,
            "temperature": 0.0,
            "seed": JUDGE_SEED,
        },
    )
    return response.message.content.strip()


JUDGE_PROVIDERS = {
    "openai": judge_openai,
    "ollama": judge_ollama,
}


def parse_scores(raw: str) -> Optional[Dict]:
    """
    Returns the parsed scores if every dimension is an integer 1-5,
    otherwise None.
    """
    try:
        scores = json.loads(raw)
    except json.JSONDecodeError:
        return None

    if not isinstance(scores, dict):
        return None

    for dim in DIMENSIONS:
        value = scores.get(dim)
        if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 5:
            return None

    return scores


def judge(query: str, answer: str, chunks: list) -> Dict:
    """
    Scores answer quality on four dimensions using an LLM judge from
    JUDGE_PROVIDER. Retries once if the response isn't valid scores, then
    returns an error dict rather than crashing the evaluation pipeline.
    """
    if JUDGE_PROVIDER not in JUDGE_PROVIDERS:
        raise ValueError(
            f"Unknown JUDGE_PROVIDER {JUDGE_PROVIDER!r}. "
            f"Expected one of: {', '.join(JUDGE_PROVIDERS)}."
        )

    call_judge = JUDGE_PROVIDERS[JUDGE_PROVIDER]
    user_message = build_user_message(query, answer, chunks)

    for _ in range(JUDGE_ATTEMPTS):
        raw = call_judge(user_message)
        scores = parse_scores(raw)
        if scores is not None:
            scores["query"] = query
            return scores

    return {
        "query": query,
        "contextual_alignment": None,
        "source_faithfulness": None,
        "specificity": None,
        "bias_handling": None,
        "reasoning": f"Parse error — raw response: {raw}",
    }
