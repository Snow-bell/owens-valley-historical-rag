import csv
from pathlib import Path
from typing import Dict, List, Set

DIMENSIONS = [
    "contextual_alignment",
    "source_faithfulness",
    "specificity",
    "bias_handling",
]

# Results files written before judge_model was recorded
UNRECORDED_JUDGE = "unrecorded"


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


def judge_models(results: List[Dict]) -> Set[str]:
    return {r.get("judge_model") or UNRECORDED_JUDGE for r in results}


def same_judge(baseline: List[Dict], current: List[Dict]) -> bool:
    """
    Checks that two result sets were scored by the same judge model.
    Scores from different judges are not comparable. Files without a
    judge_model column only produce a warning, since older runs predate it.
    """
    base_judges = judge_models(baseline)
    curr_judges = judge_models(current)

    if UNRECORDED_JUDGE in base_judges | curr_judges:
        print("  [WARNING] Judge model not recorded in one or both files. "
              "Scores may not be comparable.")
        return True

    if len(base_judges) > 1 or len(curr_judges) > 1 or base_judges != curr_judges:
        print(f"  [ERROR] Results were scored by different judges: "
              f"baseline {sorted(base_judges)}, current {sorted(curr_judges)}.")
        print("  Re-score one run with `python -m src.evaluate --rejudge <answers file>` "
              "so both use the same judge.")
        return False

    return True
