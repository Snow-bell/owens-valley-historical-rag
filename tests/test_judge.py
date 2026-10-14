import pytest
import json
from unittest.mock import patch, MagicMock
from src.judge import judge, parse_scores, SCORE_SCHEMA, JUDGE_ATTEMPTS
from src.config import JUDGE_NUM_CTX


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
    },
    {
        "text": "The Los Angeles aqueduct project was endorsed by city officials.",
        "metadata": {
            "source": "indorse-owens-project-dec-25-1906.pdf",
            "source_path": "chronicling-america/indorse-owens-project-dec-25-1906.pdf",
            "tier": 2,
            "bias_tag": "institutional_bias",
            "bias_level": "severe",
            "description": "LA newspaper endorsing aqueduct.",
            "chunk_index": 0,
        },
        "similarity": 0.84,
    },
]

SAMPLE_QUERY = "How did Paiute families sustain themselves through winter?"
SAMPLE_ANSWER = (
    "According to the Steward ethnography, Paiute families gathered "
    "pine nuts in autumn as a primary winter food source."
)


class TestJudge:

    @patch("src.judge.client")
    def test_returns_all_four_score_fields(self, mock_client):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps({
            "contextual_alignment": 5,
            "source_faithfulness": 5,
            "specificity": 4,
            "bias_handling": 4,
            "reasoning": "Answer is grounded and flags bias appropriately.",
        })
        mock_client.chat.completions.create.return_value = mock_response

        result = judge(SAMPLE_QUERY, SAMPLE_ANSWER, SAMPLE_CHUNKS)
        assert "contextual_alignment" in result
        assert "source_faithfulness" in result
        assert "specificity" in result
        assert "bias_handling" in result

    @patch("src.judge.client")
    def test_returns_query_field(self, mock_client):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps({
            "contextual_alignment": 4,
            "source_faithfulness": 4,
            "specificity": 4,
            "bias_handling": 3,
            "reasoning": "Reasonable answer.",
        })
        mock_client.chat.completions.create.return_value = mock_response

        result = judge(SAMPLE_QUERY, SAMPLE_ANSWER, SAMPLE_CHUNKS)
        assert result["query"] == SAMPLE_QUERY

    @patch("src.judge.client")
    def test_scores_are_integers(self, mock_client):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps({
            "contextual_alignment": 5,
            "source_faithfulness": 4,
            "specificity": 3,
            "bias_handling": 4,
            "reasoning": "Good answer.",
        })
        mock_client.chat.completions.create.return_value = mock_response

        result = judge(SAMPLE_QUERY, SAMPLE_ANSWER, SAMPLE_CHUNKS)
        for field in ["contextual_alignment", "source_faithfulness",
                      "specificity", "bias_handling"]:
            assert isinstance(result[field], int)

    @patch("src.judge.client")
    def test_parse_failure_returns_none_scores(self, mock_client):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "not valid json at all"
        mock_client.chat.completions.create.return_value = mock_response

        result = judge(SAMPLE_QUERY, SAMPLE_ANSWER, SAMPLE_CHUNKS)
        assert result["contextual_alignment"] is None
        assert result["source_faithfulness"] is None
        assert result["specificity"] is None
        assert result["bias_handling"] is None

    @patch("src.judge.client")
    def test_parse_failure_preserves_raw_response(self, mock_client):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "bad response"
        mock_client.chat.completions.create.return_value = mock_response

        result = judge(SAMPLE_QUERY, SAMPLE_ANSWER, SAMPLE_CHUNKS)
        assert "bad response" in result["reasoning"]

    @patch("src.judge.client")
    def test_uses_temperature_zero(self, mock_client):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps({
            "contextual_alignment": 4,
            "source_faithfulness": 4,
            "specificity": 4,
            "bias_handling": 4,
            "reasoning": "Good.",
        })
        mock_client.chat.completions.create.return_value = mock_response

        judge(SAMPLE_QUERY, SAMPLE_ANSWER, SAMPLE_CHUNKS)

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert call_kwargs["temperature"] == 0.0

    @patch("src.judge.client")
    def test_bias_context_included_in_prompt(self, mock_client):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps({
            "contextual_alignment": 4,
            "source_faithfulness": 4,
            "specificity": 4,
            "bias_handling": 4,
            "reasoning": "Good.",
        })
        mock_client.chat.completions.create.return_value = mock_response

        judge(SAMPLE_QUERY, SAMPLE_ANSWER, SAMPLE_CHUNKS)

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        user_message = call_kwargs["messages"][1]["content"]
        assert "institutional_bias" in user_message
        assert "severe" in user_message


VALID_SCORES = {
    "contextual_alignment": 5,
    "source_faithfulness": 4,
    "specificity": 4,
    "bias_handling": 3,
    "reasoning": "Grounded answer that flags the newspaper's bias.",
}


def openai_response(content):
    response = MagicMock()
    response.choices[0].message.content = content
    return response


def ollama_response(content):
    response = MagicMock()
    response.message.content = content
    return response


class TestParseScores:

    def test_valid_scores_parse(self):
        assert parse_scores(json.dumps(VALID_SCORES)) == VALID_SCORES

    @pytest.mark.parametrize("bad_value", [0, 6, "5", 4.5, True, None])
    def test_invalid_score_value_rejected(self, bad_value):
        scores = {**VALID_SCORES, "specificity": bad_value}
        assert parse_scores(json.dumps(scores)) is None

    def test_missing_dimension_rejected(self):
        scores = {k: v for k, v in VALID_SCORES.items() if k != "bias_handling"}
        assert parse_scores(json.dumps(scores)) is None

    def test_non_object_json_rejected(self):
        assert parse_scores("[5, 4, 4, 3]") is None


class TestJudgeRetry:

    @patch("src.judge.client")
    def test_retries_once_after_invalid_response(self, mock_client):
        mock_client.chat.completions.create.side_effect = [
            openai_response("not json"),
            openai_response(json.dumps(VALID_SCORES)),
        ]

        result = judge(SAMPLE_QUERY, SAMPLE_ANSWER, SAMPLE_CHUNKS)

        assert mock_client.chat.completions.create.call_count == 2
        assert result["specificity"] == 4

    @patch("src.judge.client")
    def test_out_of_range_scores_return_none(self, mock_client):
        mock_client.chat.completions.create.return_value = openai_response(
            json.dumps({**VALID_SCORES, "bias_handling": 7})
        )

        result = judge(SAMPLE_QUERY, SAMPLE_ANSWER, SAMPLE_CHUNKS)

        assert mock_client.chat.completions.create.call_count == JUDGE_ATTEMPTS
        assert result["bias_handling"] is None
        assert '"bias_handling": 7' in result["reasoning"]


@patch("src.judge.JUDGE_PROVIDER", "ollama")
class TestOllamaJudge:

    @patch("src.judge.client")
    @patch("src.judge.ollama_client")
    def test_uses_ollama_not_openai(self, mock_ollama, mock_openai):
        mock_ollama.chat.return_value = ollama_response(json.dumps(VALID_SCORES))

        result = judge(SAMPLE_QUERY, SAMPLE_ANSWER, SAMPLE_CHUNKS)

        mock_ollama.chat.assert_called_once()
        mock_openai.chat.completions.create.assert_not_called()
        assert result["query"] == SAMPLE_QUERY
        assert result["contextual_alignment"] == 5

    @patch("src.judge.JUDGE_MODEL", "gemma3:12b")
    @patch("src.judge.ollama_client")
    def test_passes_model_context_and_deterministic_options(self, mock_ollama):
        mock_ollama.chat.return_value = ollama_response(json.dumps(VALID_SCORES))

        judge(SAMPLE_QUERY, SAMPLE_ANSWER, SAMPLE_CHUNKS)

        call_kwargs = mock_ollama.chat.call_args.kwargs
        assert call_kwargs["model"] == "gemma3:12b"
        assert call_kwargs["options"]["num_ctx"] == JUDGE_NUM_CTX
        assert call_kwargs["options"]["temperature"] == 0.0
        assert "seed" in call_kwargs["options"]

    @patch("src.judge.ollama_client")
    def test_requests_score_schema(self, mock_ollama):
        mock_ollama.chat.return_value = ollama_response(json.dumps(VALID_SCORES))

        judge(SAMPLE_QUERY, SAMPLE_ANSWER, SAMPLE_CHUNKS)

        assert mock_ollama.chat.call_args.kwargs["format"] == SCORE_SCHEMA

    @patch("src.judge.ollama_client")
    def test_bias_context_included_in_prompt(self, mock_ollama):
        mock_ollama.chat.return_value = ollama_response(json.dumps(VALID_SCORES))

        judge(SAMPLE_QUERY, SAMPLE_ANSWER, SAMPLE_CHUNKS)

        user_message = mock_ollama.chat.call_args.kwargs["messages"][1]["content"]
        assert "institutional_bias" in user_message
        assert "severe" in user_message

    @patch("src.judge.ollama_client")
    def test_parse_failure_returns_none_scores(self, mock_ollama):
        mock_ollama.chat.return_value = ollama_response("bad response")

        result = judge(SAMPLE_QUERY, SAMPLE_ANSWER, SAMPLE_CHUNKS)

        assert mock_ollama.chat.call_count == JUDGE_ATTEMPTS
        assert result["contextual_alignment"] is None
        assert "bad response" in result["reasoning"]


class TestJudgeProvider:

    @patch("src.judge.JUDGE_PROVIDER", "gemini")
    def test_unknown_provider_raises(self):
        with pytest.raises(ValueError, match="gemini"):
            judge(SAMPLE_QUERY, SAMPLE_ANSWER, SAMPLE_CHUNKS)
