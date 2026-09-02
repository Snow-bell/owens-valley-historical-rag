import pytest
from unittest.mock import patch, MagicMock
from src.retrieve import retrieve, embed_query


class TestEmbedQuery:

    @patch("src.retrieve.client")
    def test_returns_list_of_floats(self, mock_client):
        mock_embedding = MagicMock()
        mock_embedding.embedding = [0.1, 0.2, 0.3]
        mock_client.embeddings.create.return_value.data = [mock_embedding]

        result = embed_query("What did Paiute families eat in winter?")
        assert isinstance(result, list)
        assert all(isinstance(v, float) for v in result)

    @patch("src.retrieve.client")
    def test_calls_correct_model(self, mock_client):
        mock_embedding = MagicMock()
        mock_embedding.embedding = [0.1, 0.2, 0.3]
        mock_client.embeddings.create.return_value.data = [mock_embedding]

        embed_query("test query")

        call_kwargs = mock_client.embeddings.create.call_args.kwargs
        assert call_kwargs["model"] == "text-embedding-3-small"


class TestRetrieve:

    @patch("src.retrieve.get_chroma_collection")
    @patch("src.retrieve.embed_query")
    def test_returns_list_of_chunks(self, mock_embed, mock_collection):
        mock_embed.return_value = [0.1, 0.2, 0.3]

        mock_col = MagicMock()
        mock_col.query.return_value = {
            "documents": [["Paiute families gathered pine nuts in autumn."]],
            "metadatas": [[{
                "source": "ethnography-of-owens-valley-paiute.pdf",
                "source_path": "ethnography-of-owens-valley-paiute.pdf",
                "tier": 1,
                "bias_tag": "academic",
                "bias_level": "mild",
                "description": "Steward ethnography.",
                "chunk_index": 0,
            }]],
            "distances": [[0.12]],
        }
        mock_collection.return_value = mock_col

        chunks = retrieve("What did Paiute families eat?")
        assert isinstance(chunks, list)
        assert len(chunks) == 1

    @patch("src.retrieve.get_chroma_collection")
    @patch("src.retrieve.embed_query")
    def test_chunk_has_required_fields(self, mock_embed, mock_collection):
        mock_embed.return_value = [0.1, 0.2, 0.3]

        mock_col = MagicMock()
        mock_col.query.return_value = {
            "documents": [["Sample text."]],
            "metadatas": [[{
                "source": "test.pdf",
                "source_path": "test.pdf",
                "tier": 2,
                "bias_tag": "none",
                "bias_level": "none",
                "description": "Test.",
                "chunk_index": 0,
            }]],
            "distances": [[0.2]],
        }
        mock_collection.return_value = mock_col

        chunks = retrieve("test query")
        assert "text" in chunks[0]
        assert "metadata" in chunks[0]
        assert "similarity" in chunks[0]

    @patch("src.retrieve.get_chroma_collection")
    @patch("src.retrieve.embed_query")
    def test_similarity_score_between_zero_and_one(
        self, mock_embed, mock_collection
    ):
        mock_embed.return_value = [0.1, 0.2, 0.3]

        mock_col = MagicMock()
        mock_col.query.return_value = {
            "documents": [["Sample text."]],
            "metadatas": [[{
                "source": "test.pdf",
                "source_path": "test.pdf",
                "tier": 2,
                "bias_tag": "none",
                "bias_level": "none",
                "description": "Test.",
                "chunk_index": 0,
            }]],
            "distances": [[0.35]],
        }
        mock_collection.return_value = mock_col

        chunks = retrieve("test query")
        assert 0.0 <= chunks[0]["similarity"] <= 1.0

    @patch("src.retrieve.get_chroma_collection")
    @patch("src.retrieve.embed_query")
    def test_respects_top_k(self, mock_embed, mock_collection):
        mock_embed.return_value = [0.1, 0.2, 0.3]

        mock_col = MagicMock()
        mock_col.query.return_value = {
            "documents": [["text one", "text two", "text three"]],
            "metadatas": [[
                {"source": "a.pdf", "source_path": "a.pdf", "tier": 1,
                 "bias_tag": "none", "bias_level": "none",
                 "description": "a", "chunk_index": 0},
                {"source": "b.pdf", "source_path": "b.pdf", "tier": 1,
                 "bias_tag": "none", "bias_level": "none",
                 "description": "b", "chunk_index": 0},
                {"source": "c.pdf", "source_path": "c.pdf", "tier": 1,
                 "bias_tag": "none", "bias_level": "none",
                 "description": "c", "chunk_index": 0},
            ]],
            "distances": [[0.1, 0.2, 0.3]],
        }
        mock_collection.return_value = mock_col

        chunks = retrieve("test query", top_k=3)
        assert len(chunks) == 3