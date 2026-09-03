import csv
import json
from pathlib import Path
from typing import List, Dict
from src.retrieve import retrieve
from src.generate import generate
from src.judge import judge
from src.config import OUTPUTS_DIR

TEST_QUERIES = [
    "What did the Owens Valley Paiute families diet consist of during the winter months?",
    "Describe the landscape of the Owens Valley floor in early spring before the aqueduct was built and the land dried up.",
    "Describe where Owens Valley Paiute families lived after they returned from their forced relocation to Fort Tejon.",
    "How did the LA aqueduct project affect water access for Owens Valley residents?",
    "What role did women's clubs play in California civic life in the early 1900s?",
    "Describe the general geology of Owens Valley.",
    "Describe the eastern Sierra Nevada mountain passes and terrain.",
    "How did Los Angeles justify the acquisition of Owens Valley water rights?",
    "What flora and fauna were native to the Owens Valley region?",
    "How did Paiute communities respond to land dispossession?",
    "What were the environmental consequences of the aqueduct diversion?",
    "How did Owens Valley Paiute families live after settlers took over Owens Valley?",
    "What were some ethical and moral dilemmas created by LA's approach to the aqueduct?",
    "Who were some notable families or people in the creation of settler communities in Owens Valley?",
    "Describe Owens Valley Paiute religion.",
]

ANSWER_PREVIEW_LENGTH = 1000
CSV_PATH = OUTPUTS_DIR / "eval_results.csv"
CSV_FIELDS = [
    "query",
    "contextual_alignment",
    "source_faithfulness",
    "specificity",
    "bias_handling",
    "reasoning",
    "sources_used",
    "answer_preview",
]


def run_evaluation() -> List[Dict]:
    """
    Runs all test queries through the full RAG pipeline and scores
    each answer using the LLM judge. Returns list of result dicts.
    """
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    for i, query in enumerate(TEST_QUERIES):
        print(f"\n[{i + 1}/{len(TEST_QUERIES)}] {query}")

        try:
            chunks = retrieve(query)
            result = generate(query, chunks)
            scores = judge(query, result["answer"], chunks)

            sources_used = ", ".join(
                set(c["metadata"]["source"] for c in chunks)
            )

            answer_preview = result["answer"][:ANSWER_PREVIEW_LENGTH].replace("\n", " ")

            row = {
                "query": query,
                "contextual_alignment": scores.get("contextual_alignment"),
                "source_faithfulness": scores.get("source_faithfulness"),
                "specificity": scores.get("specificity"),
                "bias_handling": scores.get("bias_handling"),
                "reasoning": scores.get("reasoning", ""),
                "sources_used": sources_used,
                "answer_preview": answer_preview,
            }

            results.append(row)
            print(f"  Scores — alignment: {row['contextual_alignment']} | "
                  f"faithfulness: {row['source_faithfulness']} | "
                  f"specificity: {row['specificity']} | "
                  f"bias: {row['bias_handling']}")

        except Exception as e:
            print(f"  [ERROR] Query failed: {e}")
            results.append({
                "query": query,
                "contextual_alignment": None,
                "source_faithfulness": None,
                "specificity": None,
                "bias_handling": None,
                "reasoning": f"Pipeline error: {e}",
                "sources_used": "",
                "answer_preview": "",
            })

    return results


def save_results(results: List[Dict]) -> None:
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(results)
    print(f"\n  Results saved to {CSV_PATH}")


def print_summary(results: List[Dict]) -> None:
    dimensions = [
        "contextual_alignment",
        "source_faithfulness",
        "specificity",
        "bias_handling",
    ]

    print("\n" + "=" * 50)
    print("EVALUATION SUMMARY")
    print("=" * 50)

    dimension_averages = {}
    for dim in dimensions:
        scores = [r[dim] for r in results if r[dim] is not None]
        if scores:
            avg = round(sum(scores) / len(scores), 2)
            dimension_averages[dim] = avg
            print(f"  {dim:30s} {avg} / 5")
        else:
            dimension_averages[dim] = 0
            print(f"  {dim:30s} N/A")

    valid_averages = [v for v in dimension_averages.values() if v > 0]
    if valid_averages:
        overall = round(sum(valid_averages) / len(valid_averages), 2)
        weakest = min(dimension_averages, key=dimension_averages.get)
        print(f"\n  Overall average:   {overall} / 5")
        print(f"  Weakest dimension: {weakest}")

    print(f"  Queries evaluated: {len(results)}")
    print("=" * 50)


def main() -> None:
    print("Starting evaluation pipeline...")
    print(f"Queries to evaluate: {len(TEST_QUERIES)}\n")

    results = run_evaluation()
    save_results(results)
    print_summary(results)


if __name__ == "__main__":
    main()