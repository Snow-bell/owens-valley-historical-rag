import pytest
from unittest.mock import patch, call, MagicMock
import main


class TestIndexCorpus:

    def test_clears_collection_after_chunking_then_embeds(self):
        order = MagicMock()
        with patch.object(main, "load_corpus", order.load), \
             patch.object(main, "chunk_documents", order.chunk), \
             patch.object(main, "label_chunks", order.label), \
             patch.object(main, "reset_collection", order.reset), \
             patch.object(main, "embed_and_store", order.embed):
            main.index_corpus()
        assert [c[0] for c in order.mock_calls] == ["load", "chunk", "label", "reset", "embed"]

    def test_stance_labels_can_be_turned_off(self):
        with patch.object(main, "STANCE_LABELS", False), \
             patch.object(main, "load_corpus"), patch.object(main, "chunk_documents"), \
             patch.object(main, "label_chunks") as mock_label, \
             patch.object(main, "reset_collection"), patch.object(main, "embed_and_store"):
            main.index_corpus()
        mock_label.assert_not_called()

    def test_failed_chunking_leaves_existing_index(self):
        with patch.object(main, "load_corpus", return_value=[]), \
             patch.object(main, "chunk_documents", side_effect=NotImplementedError("semantic")), \
             patch.object(main, "reset_collection") as mock_reset:
            with pytest.raises(NotImplementedError):
                main.index_corpus()
        mock_reset.assert_not_called()


class TestQueryLoop:

    CHUNKS = [{"text": "The war began.", "metadata": {
        "source": "story-of-inyo.pdf", "title": "The Story of Inyo", "tier": 3,
        "bias_tag": "settler_bias", "bias_level": "moderate", "stance_version": "v1",
        "stance_paiute": "hostile", "stance_los_angeles": "not_mentioned", "stance_settlers": "favourable",
        "loaded_terms": "[bracketed] term", "framing": "frontier conflict",
    }}]

    def run_loop(self, verbose):
        printed = []
        with patch.object(main.console, "input", side_effect=["When did the war begin?", "exit"]), \
             patch.object(main.console, "print", side_effect=lambda *a, **k: printed.extend(a)), \
             patch.object(main, "retrieve", return_value=self.CHUNKS), \
             patch.object(main, "generate", return_value={"answer": "In 1862.", "sources": "  • The Story of Inyo"}):
            main.query_loop(verbose=verbose)
        return [p for p in printed if isinstance(p, main.Panel)]

    def test_stance_panel_only_with_verbose(self):
        assert len(self.run_loop(verbose=False)) == 3   # banner, answer, sources
        panels = self.run_loop(verbose=True)
        assert len(panels) == 4
        assert "Paiute: hostile" in panels[-1].renderable.plain
        assert "[bracketed] term" in panels[-1].renderable.plain

    def test_flag_from_command_line(self):
        with patch.object(main.sys, "argv", ["main.py", "--verbose"]), \
             patch.object(main, "check_corpus_populated", return_value=True), \
             patch.object(main, "query_loop") as mock_loop:
            main.main()
        mock_loop.assert_called_once_with(verbose=True)
