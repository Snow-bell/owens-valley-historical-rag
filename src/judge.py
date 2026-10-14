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


JUDGE_PROMPT = """You are an evaluator assessing the quality of a historical 
research assistant's answer. You will be given a research question, the answer 
produced, and the source passages used — each labeled with their bias context.

Score the answer on four dimensions. Respond ONLY with a valid JSON object — 
no preamble, no markdown, no explanation outside the JSON.

Scoring dimensions (each 1-5):

1. contextual_alignment
   How well does the answer address the specific question asked?
   1 = answer is off-topic or ignores the question
   5 = answer directly and completely addresses the question

2. source_faithfulness
   Does the answer stay grounded in the provided sources?
   1 = makes claims unsupported by or contradicting the sources
   5 = every claim is traceable to a provided source passage

3. specificity
   Are the details concrete and particular rather than vague and generic?
   1 = generic statements that could apply to any time or place
   5 = specific details grounded in the Owens Valley region and period

4. bias_handling
   Does the answer appropriately surface or account for source bias?
   1 = presents biased sources as neutral fact without any qualification
   3 = acknowledges bias exists but doesn't meaningfully address it
   5 = clearly flags biased sources, surfaces contradictions between
       perspectives, and does not uncritically adopt a biased framing

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
