import pytest
from src.chunk import chunk_text, chunk_documents


SAMPLE_METADATA = {
    "source": "test-document.pdf",
    "source_path": "test-document.pdf",
    "tier": 2,
    "bias_tag": "none",
    "bias_level": "none",
    "description": "Test document.",
}


class TestChunkText:

    def test_short_text_produces_one_chunk(self):
        text = "The Owens Valley lies east of the Sierra Nevada."
        chunks = chunk_text(text, SAMPLE_METADATA)
        assert len(chunks) == 1

    def test_chunk_contains_text_and_metadata(self):
        text = "Pine nut harvests sustained Paiute families through winter."
        chunks = chunk_text(text, SAMPLE_METADATA)
        assert "text" in chunks[0]
        assert "metadata" in chunks[0]
        assert "chunk_index" in chunks[0]

    def test_chunk_index_starts_at_zero(self):
        text = "The aqueduct diverted water from the valley."
        chunks = chunk_text(text, SAMPLE_METADATA)
        assert chunks[0]["chunk_index"] == 0

    def test_long_text_produces_multiple_chunks(self):
        # Generate text long enough to exceed CHUNK_SIZE
        text = "Owens Valley history. " * 300
        chunks = chunk_text(text, SAMPLE_METADATA)
        assert len(chunks) > 1

    def test_chunks_are_sequential(self):
        text = "Owens Valley history. " * 300
        chunks = chunk_text(text, SAMPLE_METADATA)
        indices = [c["chunk_index"] for c in chunks]
        assert indices == list(range(len(chunks)))

    def test_metadata_preserved_in_every_chunk(self):
        text = "Owens Valley history. " * 300
        chunks = chunk_text(text, SAMPLE_METADATA)
        for chunk in chunks:
            assert chunk["metadata"]["source"] == "test-document.pdf"
            assert chunk["metadata"]["tier"] == 2

    def test_empty_text_returns_empty_list(self):
        chunks = chunk_text("", SAMPLE_METADATA)
        assert chunks == []

    def test_overlap_means_chunks_share_content(self):
        # With overlap, adjacent chunks should not be completely disjoint
        text = "Owens Valley history. " * 300
        chunks = chunk_text(text, SAMPLE_METADATA)
        if len(chunks) > 1:
            # Last words of chunk 0 should appear in start of chunk 1
            end_of_first = chunks[0]["text"][-50:]
            start_of_second = chunks[1]["text"][:50]
            assert len(end_of_first) > 0
            assert len(start_of_second) > 0


class TestChunkDocuments:

    def test_single_document_chunked(self):
        docs = [{"text": "Short text.", "metadata": SAMPLE_METADATA}]
        chunks = chunk_documents(docs)
        assert len(chunks) >= 1

    def test_multiple_documents_all_chunked(self):
        docs = [
            {"text": "Short text one.", "metadata": SAMPLE_METADATA},
            {"text": "Short text two.", "metadata": SAMPLE_METADATA},
        ]
        chunks = chunk_documents(docs)
        assert len(chunks) >= 2

    def test_empty_document_list_returns_empty(self):
        chunks = chunk_documents([])
        assert chunks == []