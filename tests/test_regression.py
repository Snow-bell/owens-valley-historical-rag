import csv
import pytest
from src.regression import run_regression


DIMENSIONS = [
    "contextual_alignment",
    "source_faithfulness",
    "specificity",
    "bias_handling",
]


def write_results(path, score, judge_model="gpt-4o-mini"):
    row = {"query": "q1", "judge_model": judge_model}
    row.update({dim: str(score) for dim in DIMENSIONS})
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)


class TestRunRegression:

    def test_no_change_passes(self, tmp_path):
        write_results(tmp_path / "base.csv", 4)
        write_results(tmp_path / "curr.csv", 4)
        assert run_regression(tmp_path / "base.csv", tmp_path / "curr.csv") is True

    def test_drop_beyond_threshold_fails(self, tmp_path):
        write_results(tmp_path / "base.csv", 5)
        write_results(tmp_path / "curr.csv", 4)
        assert run_regression(tmp_path / "base.csv", tmp_path / "curr.csv") is False

    def test_different_judges_fail(self, tmp_path):
        write_results(tmp_path / "base.csv", 4, judge_model="gpt-4o-mini")
        write_results(tmp_path / "curr.csv", 4, judge_model="gemma3:12b")
        assert run_regression(tmp_path / "base.csv", tmp_path / "curr.csv") is False

    def test_missing_file_fails(self, tmp_path):
        write_results(tmp_path / "base.csv", 4)
        assert run_regression(tmp_path / "base.csv", tmp_path / "missing.csv") is False
