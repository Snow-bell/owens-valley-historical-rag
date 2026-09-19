import csv
from pathlib import Path
from src.config import OUTPUTS_DIR

DIMENSIONS = [
    "contextual_alignment",
    "source_faithfulness",
    "specificity",
    "bias_handling",
]


def load_results(csv_path: Path) -> list:
    if not csv_path.exists():
        print(f"  [ERROR] File not found: {csv_path}")
        return []
    with open(csv_path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def average(results: list, dimension: str) -> float:
    scores = [
        float(r[dimension])
        for r in results
        if r.get(dimension) and r[dimension] not in ("", "None")
    ]
    return round(sum(scores) / len(scores), 2) if scores else 0.0


def compare() -> None:
    openai_path = OUTPUTS_DIR / "eval_results_openai.csv"
    mistral_path = OUTPUTS_DIR / "eval_results_mistral.csv"

    openai_results = load_results(openai_path)
    mistral_results = load_results(mistral_path)

    if not openai_results or not mistral_results:
        print("Both eval_results_openai.csv and eval_results_mistral.csv are required.")
        return

    print("\n" + "=" * 60)
    print("MODEL COMPARISON — GPT-4o-mini vs Mistral 7B")
    print("=" * 60)
    print(f"  {'Dimension':<30} {'OpenAI':>8} {'Mistral':>8} {'Delta':>8}")
    print("-" * 60)

    overall_openai = []
    overall_mistral = []

    for dim in DIMENSIONS:
        oa = average(openai_results, dim)
        ms = average(mistral_results, dim)
        delta = round(ms - oa, 2)
        delta_str = f"{'+' if delta >= 0 else ''}{delta}"
        print(f"  {dim:<30} {oa:>8} {ms:>8} {delta_str:>8}")
        overall_openai.append(oa)
        overall_mistral.append(ms)

    print("-" * 60)
    oa_avg = round(sum(overall_openai) / len(overall_openai), 2)
    ms_avg = round(sum(overall_mistral) / len(overall_mistral), 2)
    delta_avg = round(ms_avg - oa_avg, 2)
    delta_str = f"{'+' if delta_avg >= 0 else ''}{delta_avg}"
    print(f"  {'Overall average':<30} {oa_avg:>8} {ms_avg:>8} {delta_str:>8}")
    print("=" * 60)
    print(f"\n  OpenAI queries evaluated:  {len(openai_results)}")
    print(f"  Mistral queries evaluated: {len(mistral_results)}")


if __name__ == "__main__":
    compare()