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

    @pytest.fixture
    def corpus_dir(self, tmp_path):
        (tmp_path / "story-of-inyo.pdf").write_bytes(b"%PDF placeholder")
        (tmp_path / "owensvalleyhistory").mkdir()
        (tmp_path / "owensvalleyhistory" / "bishop.txt").write_text(
            "Bishop Creek mill, 1890.", encoding="utf-8"
        )
        (tmp_path / "owensvalleyhistory" / "empty.txt").write_text("", encoding="utf-8")
        (tmp_path / "notes.md").write_text("Not a corpus file.", encoding="utf-8")
        with patch("src.ingest.CORPUS_DIR", tmp_path):
            yield tmp_path

    @pytest.fixture
    def mock_fitz(self):
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Sample extracted text."
        mock_pdf = MagicMock()
        mock_pdf.__iter__ = MagicMock(return_value=iter([mock_page]))
        with patch("src.ingest.fitz.open", return_value=mock_pdf) as mock_open:
            yield mock_open

    def test_load_corpus_loads_pdf_and_txt(self, corpus_dir, mock_fitz):
        documents = load_corpus()
        by_path = {d["metadata"]["source_path"]: d for d in documents}

        # Empty files and non-corpus extensions are skipped
        assert set(by_path) == {
            "story-of-inyo.pdf",
            str(Path("owensvalleyhistory") / "bishop.txt"),
        }

        inyo = by_path["story-of-inyo.pdf"]
        assert inyo["text"] == "Sample extracted text."
        assert inyo["metadata"]["bias_tag"] == "settler_bias"

        bishop = by_path[str(Path("owensvalleyhistory") / "bishop.txt")]
        assert bishop["text"] == "Bishop Creek mill, 1890."
        assert bishop["metadata"]["source"] == "bishop.txt"
        assert bishop["metadata"]["tier"] == 2

    def test_load_corpus_caps_document_length(self, corpus_dir, mock_fitz):
        with patch("src.ingest.MAX_CHARS", 6):
            documents = load_corpus()
        assert all(len(d["text"]) <= 6 for d in documents)

    @patch("src.ingest.CORPUS_DIR")
    def test_empty_corpus_raises_error(self, mock_corpus_dir):
        mock_corpus_dir.rglob.return_value = []
        with pytest.raises(FileNotFoundError):
            load_corpus()