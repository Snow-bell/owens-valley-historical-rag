import pytest
import json
from unittest.mock import patch, MagicMock
from src.judge import judge


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