import json
import pytest
from unittest.mock import patch
import src.evaluate as evaluate


SAMPLE_CHUNKS = [
    {
        "text": "Paiute families gathered pine nuts each autumn in the foothills.",
        "metadata": {
            "source": "ethnography-of-owens-valley-paiute.pdf",
            "source_path": "ethnography-of-owens-valley-paiute.pdf",
            "tier": 1,
            "bias_tag": "academic",
            "bias_level": "mild",
            "description": "Steward ethnography.",
            "chunk_index": 0,
        },
        "similarity": 0.91,
        "relevance_score": 0.88,
    },
]

LONG_ANSWER = "Pine nuts were a winter staple. " * 100

SAMPLE_SCORES = {
    "contextual_alignment": 5,
    "source_faithfulness": 4,
    "specificity": 4,
    "bias_handling": 3,
    "reasoning": "Grounded answer.",
}

QUERIES = ["What did Paiute families eat in winter?", "Describe Owens Lake."]


@pytest.fixture
def eval_env(tmp_path):
    with patch.object(evaluate, "OUTPUTS_DIR", tmp_path), \
         patch.object(evaluate, "TEST_QUERIES", QUERIES), \
         patch.object(evaluate, "retrieve", return_value=SAMPLE_CHUNKS), \
         patch.object(evaluate, "generate", return_value={"answer": LONG_ANSWER}), \
         patch.object(evaluate, "judge", return_value=SAMPLE_SCORES) as mock_judge:
        yield tmp_path, mock_judge


class TestRunEvaluation:

    def test_rows_record_judge_model(self, eval_env):
        results = evaluate.run_evaluation("openai")
        assert all(r["judge_model"] == evaluate.JUDGE_MODEL for r in results)

    def test_saves_full_answers_and_chunks(self, eval_env):
        tmp_path, _ = eval_env
        evaluate.run_evaluation("openai")

        records = evaluate.load_answers(tmp_path / "eval_answers_openai.jsonl")
        assert len(records) == len(QUERIES)
        assert records[0]["answer"] == LONG_ANSWER
        assert len(records[0]["answer"]) > evaluate.ANSWER_PREVIEW_LENGTH
        assert records[0]["chunks"] == SAMPLE_CHUNKS

    def test_failed_query_saves_error_record(self, eval_env):
        tmp_path, _ = eval_env
        with patch.object(evaluate, "retrieve", side_effect=Exception("Chroma down")):
            results = evaluate.run_evaluation("openai")

        records = evaluate.load_answers(tmp_path / "eval_answers_openai.jsonl")
        assert records[0]["error"] == "Chroma down"
        assert "answer" not in records[0]
        assert results[0]["contextual_alignment"] is None


class TestRejudge:

    def test_rescores_saved_answers_without_generating(self, eval_env):
        tmp_path, mock_judge = eval_env
        evaluate.run_evaluation("openai")
        mock_judge.reset_mock()

        with patch.object(evaluate, "retrieve") as mock_retrieve, \
             patch.object(evaluate, "generate") as mock_generate:
            results = evaluate.rejudge(tmp_path / "eval_answers_openai.jsonl")

        mock_retrieve.assert_not_called()
        mock_generate.assert_not_called()
        assert mock_judge.call_count == len(QUERIES)
        assert mock_judge.call_args.args[1] == LONG_ANSWER
        assert mock_judge.call_args.args[2] == SAMPLE_CHUNKS
        assert results[0]["model"] == "openai"
        assert results[0]["specificity"] == 4

    def test_skips_records_without_answer(self, eval_env):
        tmp_path, mock_judge = eval_env
        answers_path = tmp_path / "eval_answers_openai.jsonl"
        answers_path.write_text(
            json.dumps({"query": "q1", "model": "openai", "error": "Chroma down"}) + "\n",
            encoding="utf-8",
        )

        results = evaluate.rejudge(answers_path)
        mock_judge.assert_not_called()
        assert results[0]["contextual_alignment"] is None
        assert "Chroma down" in results[0]["reasoning"]


class TestCsvPath:

    def test_default_path_unchanged(self, tmp_path):
        with patch.object(evaluate, "OUTPUTS_DIR", tmp_path):
            assert evaluate.get_csv_path("openai").name == "eval_results_openai.csv"

    def test_rejudged_path_includes_judge(self, tmp_path):
        with patch.object(evaluate, "OUTPUTS_DIR", tmp_path):
            path = evaluate.get_csv_path("openai", "gemma3:12b")
            assert path.name == "eval_results_openai__judge_gemma3_12b.csv"
