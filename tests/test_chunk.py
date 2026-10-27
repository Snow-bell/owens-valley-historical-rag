import pytest
from unittest.mock import patch
from src.chunk import chunk_text, chunk_documents, with_context_header, chunk_span, add_page_ranges


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

class TestJunkFilter:

    def test_letter_share(self):
        from src.chunk import letter_share
        assert letter_share("abc 123") == 0.5
        assert letter_share("   ") == 0.0

    def test_drops_symbol_and_table_chunks_keeps_prose(self):
        from src.chunk import chunk_documents
        meta = {"source": "a.pdf", "source_path": "a.pdf", "tier": 2,
                "bias_tag": "none", "bias_level": "none", "description": "d"}
        documents = [
            {"text": "The aqueduct opened in 1913 at the Cascades.", "metadata": meta},
            {"text": "! ! ! ! ! ! 0 1952.0 2943.0 20 197.6 407.6", "metadata": {**meta, "source": "b.pdf"}},
        ]
        chunks = chunk_documents(documents)
        assert [c["metadata"]["source"] for c in chunks] == ["a.pdf"]


class TestChunkMethod:

    META = {"source": "a.pdf", "source_path": "a.pdf", "tier": 2,
            "bias_tag": "none", "bias_level": "none", "description": "d"}

    def test_fixed_chunks_record_method(self):
        from src.chunk import chunk_documents
        chunks = chunk_documents([{"text": "The aqueduct opened in 1913.", "metadata": self.META}], method="fixed")
        assert chunks[0]["metadata"]["chunk_method"] == "fixed"

    def test_semantic_dispatches_and_filters_junk(self):
        from src import chunk
        documents = [{"text": "The aqueduct opened in 1913. ! ! ! ! ! ! ! !", "metadata": self.META}]
        fake = [{"text": "! ! ! ! ! ! ! !", "chunk_index": 0, "metadata": {**self.META, "chunk_index": 0}},
                {"text": "The aqueduct opened in 1913.", "chunk_index": 1, "metadata": {**self.META, "chunk_index": 1}}]
        with patch.object(chunk, "chunk_semantic", return_value=fake) as mock_semantic:
            chunks = chunk.chunk_documents(documents, method="semantic")
        mock_semantic.assert_called_once_with(documents)
        assert [c["chunk_index"] for c in chunks] == [1]

    def test_unknown_method(self):
        from src.chunk import chunk_documents
        with pytest.raises(ValueError, match="sentences"):
            chunk_documents([], method="sentences")


import numpy as np
from src.chunk import (
    split_sentences, sentence_windows, neighbour_distances, group_sentences, chunk_semantic,
)


def topic_embedder(texts):
    """Fake sentence embedder: a window's vector says which topic words it holds."""
    topics = ["aqueduct", "pine", "railroad"]
    vectors = []
    for text in texts:
        v = np.array([text.lower().count(t) for t in topics], dtype=float) + 1e-6
        vectors.append(v / np.linalg.norm(v))
    return np.array(vectors)


SEM_META = {"source": "a.pdf", "source_path": "a.pdf", "tier": 2,
            "bias_tag": "none", "bias_level": "none", "description": "d", "clean_version": 1}


class TestSplitSentences:

    def test_period_abbreviations_do_not_end_sentences(self):
        text = "Jno. Smith and Wm. Brown met Gen. Beale at Fort Tejon. W. A. Chalfant wrote it."
        assert split_sentences(text) == [
            "Jno. Smith and Wm. Brown met Gen. Beale at Fort Tejon.",
            "W. A. Chalfant wrote it.",
        ]

    def test_line_breaks_end_sentences(self):
        text = "Cabin Bar Cafe in Cartago\n(photo courtesy Ray DeLea)\n\nThe kilns were built in 1876."
        assert split_sentences(text) == [
            "Cabin Bar Cafe in Cartago", "(photo courtesy Ray DeLea)", "The kilns were built in 1876.",
        ]


class TestWindowsAndDistances:

    def test_windows_include_neighbours(self):
        assert sentence_windows(["a", "b", "c"], window=1) == ["a b", "a b c", "b c"]

    def test_distance_is_zero_for_same_direction(self):
        e = np.array([[1.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
        assert np.allclose(neighbour_distances(e), [0.0, 1.0])

    def test_single_sentence_has_no_distances(self):
        assert len(neighbour_distances(np.array([[1.0, 0.0]]))) == 0


class TestGroupSentences:

    def test_breaks_above_threshold(self):
        groups = group_sentences(np.array([0.1, 0.9, 0.1]), [200] * 4, threshold=0.5)
        assert groups == [[0, 1], [2, 3]]

    def test_breaks_only_at_local_peaks(self):
        # One topic change spread over three distances breaks once, at the peak
        groups = group_sentences(np.array([0.0, 0.1, 0.2, 0.1, 0.0]), [200] * 6, threshold=0.05)
        assert groups == [[0, 1, 2], [3, 4, 5]]

    def test_splits_over_max_at_largest_distance(self):
        groups = group_sentences(np.array([0.1, 0.3, 0.2]), [300] * 4, threshold=1.0, max_tokens=800)
        assert groups == [[0, 1], [2, 3]]

    def test_merges_small_groups_when_they_fit(self):
        groups = group_sentences(np.array([0.9, 0.9]), [50, 400, 300], threshold=0.5, min_tokens=100)
        assert groups == [[0, 1], [2]]

    def test_does_not_merge_past_max(self):
        groups = group_sentences(np.array([0.9]), [790, 50], threshold=0.5, min_tokens=100, max_tokens=800)
        assert groups == [[0], [1]]


class TestChunkSemantic:

    def doc(self, text, path="a.pdf"):
        return {"text": text, "metadata": {**SEM_META, "source": path, "source_path": path}}

    def test_breaks_at_topic_change(self):
        aqueduct = " ".join(f"The aqueduct carried water south in year {i}." for i in range(4))
        pine = " ".join(f"Families gathered pine nuts in the hills, season {i}." for i in range(4))
        chunks = chunk_semantic([self.doc(f"{aqueduct} {pine}")], embed=topic_embedder,
                                percentile=50, min_tokens=1, overlap_max_tokens=0)
        assert len(chunks) == 2
        assert "pine" not in chunks[0]["text"]
        assert "aqueduct" not in chunks[1]["text"]

    def test_threshold_is_corpus_wide(self):
        # One document on one topic, another that changes topic: only the second breaks
        coherent = " ".join(f"The aqueduct opened at the Cascades, report {i}." for i in range(6))
        mixed = ("The aqueduct carried water. The aqueduct crossed the desert. "
                 "The railroad reached Laws. The railroad carried freight.")
        chunks = chunk_semantic([self.doc(coherent, "a.pdf"), self.doc(mixed, "b.pdf")],
                                embed=topic_embedder, percentile=90, min_tokens=1, overlap_max_tokens=0)
        by_doc = {}
        for c in chunks:
            by_doc.setdefault(c["metadata"]["source_path"], []).append(c)
        assert len(by_doc["a.pdf"]) == 1
        assert len(by_doc["b.pdf"]) == 2

    def test_overlap_repeats_previous_last_sentence(self):
        text = "The aqueduct carried water. The aqueduct crossed the desert. Families gathered pine nuts. Pine nuts were stored."
        chunks = chunk_semantic([self.doc(text)], embed=topic_embedder, percentile=50, min_tokens=1)
        assert chunks[1]["text"].startswith("The aqueduct crossed the desert.")

    def test_respects_max_tokens_and_records_metadata(self):
        text = " ".join(f"The aqueduct carried water south, sentence number {i}." for i in range(200))
        chunks = chunk_semantic([self.doc(text)], embed=topic_embedder, max_tokens=120)
        assert len(chunks) > 1
        assert all(c["metadata"]["token_count"] <= 120 for c in chunks)
        assert [c["chunk_index"] for c in chunks] == list(range(len(chunks)))
        first = chunks[0]["metadata"]
        assert first["chunk_method"] == "semantic"
        assert first["clean_version"] == 1
        assert first["n_sentences"] > 0

    def test_single_sentence_over_max_is_split_by_tokens(self):
        text = " ".join(["aqueduct water"] * 300)   # no sentence end
        chunks = chunk_semantic([self.doc(text)], embed=topic_embedder, max_tokens=100)
        assert len(chunks) >= 6
        assert all(c["metadata"]["token_count"] <= 100 for c in chunks)

    def test_empty_corpus(self):
        assert chunk_semantic([], embed=topic_embedder) == []



class TestWithContextHeader:

    def test_header_goes_above_text(self):
        chunk = {"text": "The aqueduct opened.", "metadata": {"context_header": "The Story of Inyo · W. A. Chalfant"}}
        assert with_context_header(chunk) == "The Story of Inyo · W. A. Chalfant\n\nThe aqueduct opened."

    def test_chunk_without_header_is_unchanged(self):
        assert with_context_header({"text": "The aqueduct opened.", "metadata": {}}) == "The aqueduct opened."


class TestPageRanges:

    TEXT = "Page one opens here and runs on.\n\nPage two begins with the mill.\nIt burned in 1872.\n\nPage three ends the chapter."
    OFFSETS = [[0, 9], [TEXT.index("Page two"), 10], [TEXT.index("Page three"), 11]]

    def doc(self, printed):
        return {"text": self.TEXT, "metadata": {"source_path": "book.pdf"},
                "page_offsets": self.OFFSETS, "printed_pages": printed}

    @staticmethod
    def chunk(text):
        return {"text": text, "metadata": {"source_path": "book.pdf"}}

    def test_span_matches_across_different_whitespace(self):
        span = chunk_span(self.TEXT, "Page two begins with the mill. It burned in 1872.")
        assert self.TEXT[span[0]: span[1]] == "Page two begins with the mill.\nIt burned in 1872."

    def test_span_not_found(self):
        assert chunk_span(self.TEXT, "Nothing like this appears.") is None

    def test_chunks_get_printed_pages(self):
        chunks = [self.chunk("Page one opens here and runs on. Page two begins with the mill."),
                  self.chunk("It burned in 1872. Page three ends the chapter.")]
        add_page_ranges(chunks, [self.doc({9: 1, 10: 2, 11: 3})])
        assert [(c["metadata"]["page_start"], c["metadata"]["page_end"]) for c in chunks] == [(1, 2), (2, 3)]

    def test_unnumbered_pages_are_skipped(self):
        chunks = [self.chunk("Page two begins with the mill. It burned in 1872. Page three ends the chapter.")]
        add_page_ranges(chunks, [self.doc({11: 3})])
        assert (chunks[0]["metadata"]["page_start"], chunks[0]["metadata"]["page_end"]) == (3, 3)

    def test_documents_without_printed_pages_get_none(self):
        chunks = [self.chunk("Page one opens here and runs on.")]
        add_page_ranges(chunks, [self.doc({})])
        assert "page_start" not in chunks[0]["metadata"]
