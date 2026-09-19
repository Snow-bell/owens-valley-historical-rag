import csv
from pathlib import Path
from typing import Dict, List
from src.config import OUTPUTS_DIR

DIMENSIONS = [
    "contextual_alignment",
    "source_faithfulness",
    "specificity",
    "bias_handling",
]

REGRESSION_THRESHOLD = 0.3


def load_results(csv_path: Path) -> List[Dict]:
    if not csv_path.exists():
        print(f"  [ERROR] File not found: {csv_path}")
        return []
    with open(csv_path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def average(results: List[Dict], dimension: str) -> float:
    scores = [
        float(r[dimension])
        for r in results
        if r.get(dimension) and r[dimension] not in ("", "None")
    ]
    return round(sum(scores) / len(scores), 2) if scores else 0.0


def run_regression(baseline_path: Path, current_path: Path) -> bool:
    """
    Compares current eval results against a baseline.
    Flags any dimension that dropped more than REGRESSION_THRESHOLD.
    Returns True if all checks pass, False if regressions detected.
    """
    baseline = load_results(baseline_path)
    current = load_results(current_path)

    if not baseline or not current:
        print("Both baseline and current results are required.")
        return False

    print("\n" + "=" * 60)
    print(f"REGRESSION CHECK")
    print(f"  Baseline: {baseline_path.name}")
    print(f"  Current:  {current_path.name}")
    print(f"  Threshold: -{REGRESSION_THRESHOLD} per dimension")
    print("=" * 60)
    print(f"  {'Dimension':<30} {'Baseline':>9} {'Current':>9} {'Delta':>9} {'Status':>8}")
    print("-" * 60)

    regressions = []

    for dim in DIMENSIONS:
        base_avg = average(baseline, dim)
        curr_avg = average(current, dim)
        delta = round(curr_avg - base_avg, 2)
        delta_str = f"{'+' if delta >= 0 else ''}{delta}"

        if delta < -REGRESSION_THRESHOLD:
            status = "FAIL"
            regressions.append((dim, delta))
        else:
            status = "PASS"

        print(f"  {dim:<30} {base_avg:>9} {curr_avg:>9} {delta_str:>9} {status:>8}")

    print("=" * 60)

    if regressions:
        print(f"\n  REGRESSIONS DETECTED: {len(regressions)}")
        for dim, delta in regressions:
            print(f"    {dim}: dropped {abs(delta)} points beyond threshold")
        return False
    else:
        print("\n  All dimensions within acceptable range.")
        return True


def main() -> None:
    import sys

    args = sys.argv[1:]

    if len(args) < 2:
        print("Usage: python -m src.regression --baseline <file> --current <file>")
        print("Example: python -m src.regression --baseline eval_results_openai.csv --current eval_results_mistral.csv")
        return

    baseline_name = None
    current_name = None

    for i, arg in enumerate(args):
        if arg == "--baseline" and i + 1 < len(args):
            baseline_name = args[i + 1]
        if arg == "--current" and i + 1 < len(args):
            current_name = args[i + 1]

    if not baseline_name or not current_name:
        print("Both --baseline and --current are required.")
        return

    baseline_path = OUTPUTS_DIR / baseline_name
    current_path = OUTPUTS_DIR / current_name

    passed = run_regression(baseline_path, current_path)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()