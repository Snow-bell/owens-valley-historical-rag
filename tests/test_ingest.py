import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.ingest import get_metadata, load_corpus
from src.config import CORPUS_DIR


class TestGetMetadata:

    def test_flat_file_lookup(self):
        filepath = CORPUS_DIR / "story-of-inyo.pdf"
        metadata = get_metadata(filepath)
        assert metadata["bias_tag"] == "settler_bias"
        assert metadata["bias_level"] == "moderate"
        assert metadata["tier"] == 3

    def test_chronicling_america_subfolder_lookup(self):
        filepath = CORPUS_DIR / "chronicling-america" / "la-faces-water-crisis-july-31-1905.pdf"
        metadata = get_metadata(filepath)
        assert metadata["bias_tag"] == "institutional_bias"
        assert metadata["bias_level"] == "severe"
        assert metadata["tier"] == 2

    def test_womens_club_default_applied(self):
        filepath = CORPUS_DIR / "womens-club-biographies" / "Clara-Burdette.pdf"
        metadata = get_metadata(filepath)
        assert metadata["bias_tag"] == "none"
        assert metadata["tier"] == 2

    def test_source_field_added_to_metadata(self):
        filepath = CORPUS_DIR / "fauna-flora-ov.pdf"
        metadata = get_metadata(filepath)
        assert metadata["source"] == "fauna-flora-ov.pdf"

    def test_source_path_field_added_to_metadata(self):
        filepath = CORPUS_DIR / "fauna-flora-ov.pdf"
        metadata = get_metadata(filepath)
        assert "source_path" in metadata

    def test_unknown_file_returns_warning_metadata(self):
        filepath = CORPUS_DIR / "unknown-document.pdf"
        metadata = get_metadata(filepath)
        assert metadata["tier"] == 0
        assert metadata["bias_tag"] == "unknown"

    def test_indigenous_perspective_tag(self):
        filepath = CORPUS_DIR / "payahuunadu-oviwc.pdf"
        metadata = get_metadata(filepath)
        assert metadata["bias_tag"] == "primary_indigenous"

    def test_academic_tag(self):
        filepath = CORPUS_DIR / "ethnography-of-owens-valley-paiute.pdf"
        metadata = get_metadata(filepath)
        assert metadata["bias_tag"] == "academic"


class TestLoadCorpus:

    @patch("src.ingest.fitz.open")
    @patch("src.ingest.CORPUS_DIR")
    def test_load_corpus_returns_list(self, mock_corpus_dir, mock_fitz):
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Sample extracted text."
        mock_pdf.__iter__ = MagicMock(return_value=iter([mock_page]))
        mock_pdf.close = MagicMock()
        mock_fitz.return_value = mock_pdf

        mock_path = MagicMock()
        mock_path.name = "story-of-inyo.pdf"
        mock_path.relative_to.return_value = Path("story-of-inyo.pdf")
        mock_corpus_dir.rglob.return_value = [mock_path]

        documents = load_corpus()
        assert isinstance(documents, list)

    @patch("src.ingest.CORPUS_DIR")
    def test_empty_corpus_raises_error(self, mock_corpus_dir):
        mock_corpus_dir.rglob.return_value = []
        with pytest.raises(FileNotFoundError):
            load_corpus()