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
