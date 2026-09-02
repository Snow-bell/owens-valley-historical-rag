import json
from typing import Dict
from openai import OpenAI
from src.config import (
    OPENAI_API_KEY,
    GENERATION_MODEL,
    MAX_TOKENS,
)

client = OpenAI(api_key=OPENAI_API_KEY)


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


def judge(query: str, answer: str, chunks: list) -> Dict:
    """
    Scores answer quality on three dimensions using an LLM judge.
    Returns scores and reasoning. On parse failure returns error dict
    rather than crashing the evaluation pipeline.
    """
    context = "\n\n---\n\n".join(
        f"[{c['metadata']['source']}"
        f" | bias: {c['metadata']['bias_tag']}"
        f" | level: {c['metadata']['bias_level']}]\n{c['text']}"
        for c in chunks
    )

    user_message = (
        f"Research question: {query}\n\n"
        f"Answer to evaluate:\n{answer}\n\n"
        f"Source passages used:\n{context}"
    )

    response = client.chat.completions.create(
        model=GENERATION_MODEL,
        temperature=0.0,
        max_tokens=300,
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    raw = response.choices[0].message.content.strip()

    try:
        scores = json.loads(raw)
        scores["query"] = query
        return scores
    except json.JSONDecodeError:
        return {
            "query": query,
            "contextual_alignment": None,
            "source_faithfulness": None,
            "specificity": None,
            "bias_handling": None,
            "reasoning": f"Parse error — raw response: {raw}",
        }