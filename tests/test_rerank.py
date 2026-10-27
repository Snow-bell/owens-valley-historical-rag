import pytest
from unittest.mock import patch, MagicMock
from cohere.errors import TooManyRequestsError
import src.rerank as rerank_module
from src.rerank import rerank, wait_for_rate_limit


CHUNKS = [
    {"text": "Pine nuts were gathered in autumn.", "metadata": {"source": "a.pdf"}},
    {"text": "The aqueduct opened in 1913.", "metadata": {"source": "b.pdf"}},
]


def cohere_result(index, score):
    result = MagicMock()
    result.index = index
    result.relevance_score = score
    return result


def rate_limit_error():
    return TooManyRequestsError(body={"message": "Trial key limited to 10 calls / minute"})


@pytest.fixture(autouse=True)
def no_sleep():
    with patch.object(rerank_module.time, "sleep") as mock_sleep:
        rerank_module._last_call = 0.0
        yield mock_sleep


class TestRerank:

    @patch("src.rerank.client")
    def test_orders_chunks_by_cohere_result(self, mock_client):
        mock_client.rerank.return_value.results = [cohere_result(1, 0.91234), cohere_result(0, 0.2)]

        result = rerank("When did the aqueduct open?", CHUNKS, top_n=2)

        assert [c["metadata"]["source"] for c in result] == ["b.pdf", "a.pdf"]
        assert result[0]["relevance_score"] == 0.9123

    @patch("src.rerank.client")
    def test_sends_header_with_text_and_returns_plain_chunks(self, mock_client):
        chunk = {"text": "The aqueduct opened in 1913.", "metadata": {"source": "b.pdf", "context_header": "LA Herald · 1906"}}
        mock_client.rerank.return_value.results = [cohere_result(0, 0.5)]

        result = rerank("q", [chunk], top_n=1)

        assert mock_client.rerank.call_args.kwargs["documents"] == ["LA Herald · 1906\n\nThe aqueduct opened in 1913."]
        assert result[0]["text"] == "The aqueduct opened in 1913."

    @patch("src.rerank.client")
    def test_empty_chunks_skip_cohere(self, mock_client):
        assert rerank("q", []) == []
        mock_client.rerank.assert_not_called()

    @patch("src.rerank.client")
    def test_retries_after_rate_limit(self, mock_client, no_sleep):
        ok = MagicMock()
        ok.results = [cohere_result(0, 0.5)]
        mock_client.rerank.side_effect = [rate_limit_error(), ok]

        result = rerank("q", CHUNKS, top_n=1)

        assert mock_client.rerank.call_count == 2
        assert result[0]["relevance_score"] == 0.5
        assert any(call.args[0] == rerank_module.RATE_LIMIT_WAIT for call in no_sleep.call_args_list)

    @patch("src.rerank.client")
    def test_gives_up_after_retries(self, mock_client):
        mock_client.rerank.side_effect = rate_limit_error()

        with pytest.raises(TooManyRequestsError):
            rerank("q", CHUNKS)

        assert mock_client.rerank.call_count == rerank_module.RATE_LIMIT_RETRIES + 1

    @patch("src.rerank.client")
    def test_other_errors_are_not_retried(self, mock_client):
        mock_client.rerank.side_effect = RuntimeError("bad request")

        with pytest.raises(RuntimeError):
            rerank("q", CHUNKS)

        assert mock_client.rerank.call_count == 1


class TestRateLimitPacing:

    def test_first_call_does_not_wait(self, no_sleep):
        wait_for_rate_limit()
        no_sleep.assert_not_called()

    @patch("src.rerank.COHERE_CALLS_PER_MINUTE", 10)
    def test_back_to_back_calls_are_spaced(self, no_sleep):
        # Each call reads the clock twice: to compute the wait, then to record the call
        with patch.object(rerank_module.time, "monotonic", side_effect=[100.0, 100.0, 101.0, 106.3]):
            wait_for_rate_limit()   # first call at t=100
            wait_for_rate_limit()   # second call 1 s later
        waited = no_sleep.call_args.args[0]
        assert waited == pytest.approx(60 / 10 * 1.05 - 1.0)
