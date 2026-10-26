import pytest
from unittest.mock import patch
import src.embed as embed
from src.embed import chunk_id, store_chunks, reset_collection, get_chroma_collection


def make_chunk(path, index=0, **extra):
    return {
        "text": "Pine nuts were gathered in autumn.",
        "chunk_index": index,
        "metadata": {
            "source": path.split("/")[-1],
            "source_path": path,
            "tier": 1,
            "bias_tag": "academic",
            "bias_level": "mild",
            "description": "Steward ethnography.",
            "chunk_index": index,
            "chunk_method": "fixed",
            "clean_version": 1,
            **extra,
        },
    }


class TestChunkId:

    def test_uses_source_path(self):
        assert chunk_id(make_chunk("owensvalleyhistory/keeler.txt", 3)) == "owensvalleyhistory/keeler.txt__chunk3"

    def test_same_file_name_in_two_folders_does_not_collide(self):
        a = make_chunk("chronicling-america/page1.pdf")
        b = make_chunk("owensvalleyhistory/page1.pdf")
        assert chunk_id(a) != chunk_id(b)


class TestStoreChunks:

    @patch("src.embed.get_chroma_collection")
    def test_stores_ids_and_selected_metadata(self, mock_collection):
        store_chunks([make_chunk("a/x.pdf", 2, page_offsets=[[0, 1]])], [[0.1, 0.2]])

        kwargs = mock_collection.return_value.upsert.call_args.kwargs
        assert kwargs["ids"] == ["a/x.pdf__chunk2"]
        metadata = kwargs["metadatas"][0]
        assert metadata["chunk_method"] == "fixed"
        assert metadata["clean_version"] == 1
        assert "page_offsets" not in metadata    # lists can't be Chroma metadata


class TestResetCollection:

    @pytest.fixture
    def chroma_dir(self, tmp_path):
        with patch.object(embed, "CHROMA_DIR", tmp_path):
            yield tmp_path

    def test_clears_only_the_named_collection(self, chroma_dir):
        fixed = get_chroma_collection("fixed_test")
        semantic = get_chroma_collection("semantic_test")
        for collection in (fixed, semantic):
            collection.upsert(ids=["a"], documents=["text"], embeddings=[[0.1, 0.2]])

        reset_collection("fixed_test")

        assert get_chroma_collection("fixed_test").count() == 0
        assert get_chroma_collection("semantic_test").count() == 1

    def test_missing_collection_is_fine(self, chroma_dir):
        reset_collection("never_created")
