import csv
import pytest
from src.results import (
    load_results,
    average,
    judge_models,
    same_judge,
    UNRECORDED_JUDGE,
)


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


class TestLoadResults:

    def test_missing_file_returns_empty_list(self, tmp_path):
        assert load_results(tmp_path / "missing.csv") == []

    def test_reads_rows(self, tmp_path):
        path = tmp_path / "results.csv"
        write_csv(path, [{"query": "q1", "specificity": "4"}])
        rows = load_results(path)
        assert rows == [{"query": "q1", "specificity": "4"}]


class TestAverage:

    def test_skips_blank_and_none_scores(self):
        rows = [
            {"specificity": "4"},
            {"specificity": "5"},
            {"specificity": ""},
            {"specificity": "None"},
        ]
        assert average(rows, "specificity") == 4.5

    def test_no_scores_returns_zero(self):
        assert average([{"specificity": ""}], "specificity") == 0.0


class TestJudgeModels:

    def test_collects_judges(self):
        rows = [{"judge_model": "gpt-4o-mini"}, {"judge_model": "gemma3:12b"}]
        assert judge_models(rows) == {"gpt-4o-mini", "gemma3:12b"}

    def test_missing_column_is_unrecorded(self):
        assert judge_models([{"query": "q1"}]) == {UNRECORDED_JUDGE}


class TestSameJudge:

    def test_same_judge_passes(self):
        rows = [{"judge_model": "gpt-4o-mini"}]
        assert same_judge(rows, rows) is True

    def test_different_judges_fail(self):
        baseline = [{"judge_model": "gpt-4o-mini"}]
        current = [{"judge_model": "gemma3:12b"}]
        assert same_judge(baseline, current) is False

    def test_mixed_judges_in_one_file_fail(self):
        baseline = [{"judge_model": "gpt-4o-mini"}, {"judge_model": "gemma3:12b"}]
        assert same_judge(baseline, baseline) is False

    def test_unrecorded_judge_warns_but_passes(self, capsys):
        baseline = [{"query": "q1"}]
        current = [{"judge_model": "gemma3:12b"}]
        assert same_judge(baseline, current) is True
        assert "not recorded" in capsys.readouterr().out
