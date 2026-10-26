import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.ingest import (
    get_metadata, load_corpus, strip_page_furniture, select_pages, join_pages,
)
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
        (tmp_path / "ethnography-of-owens-valley-paiute.pdf").write_bytes(b"%PDF placeholder")
        (tmp_path / "owensvalleyhistory").mkdir()
        (tmp_path / "owensvalleyhistory" / "bishop.txt").write_text(
            "Bishop Creek mill, 1890.", encoding="utf-8"
        )
        (tmp_path / "owensvalleyhistory" / "empty.txt").write_text("", encoding="utf-8")
        (tmp_path / "notes.md").write_text("Not a corpus file.", encoding="utf-8")
        with patch("src.ingest.CORPUS_DIR", tmp_path):
            yield tmp_path

    @staticmethod
    def fake_pdf(page_texts):
        pages = []
        for text in page_texts:
            page = MagicMock()
            page.get_text.return_value = text
            pages.append(page)
        pdf = MagicMock()
        pdf.__iter__ = MagicMock(side_effect=lambda: iter(pages))
        return pdf

    @pytest.fixture
    def mock_fitz(self):
        pdf = self.fake_pdf(["Sample extracted text."])
        with patch("src.ingest.fitz.open", return_value=pdf) as mock_open:
            yield mock_open

    def test_load_corpus_loads_pdf_and_txt(self, corpus_dir, mock_fitz):
        documents = load_corpus()
        by_path = {d["metadata"]["source_path"]: d for d in documents}

        # Empty files and non-corpus extensions are skipped
        assert set(by_path) == {
            "ethnography-of-owens-valley-paiute.pdf",
            str(Path("owensvalleyhistory") / "bishop.txt"),
        }

        steward = by_path["ethnography-of-owens-valley-paiute.pdf"]
        assert steward["text"] == "Sample extracted text."
        assert steward["metadata"]["bias_tag"] == "academic"
        assert steward["page_offsets"] == [[0, 1]]

        bishop = by_path[str(Path("owensvalleyhistory") / "bishop.txt")]
        assert bishop["text"] == "Bishop Creek mill, 1890."
        assert bishop["metadata"]["source"] == "bishop.txt"
        assert bishop["metadata"]["tier"] == 2

    def test_page_ranges_from_registry(self, tmp_path):
        (tmp_path / "story-of-inyo.pdf").write_bytes(b"%PDF placeholder")
        words = "alpha bravo charlie delta echo foxtrot golf hotel india juliet kilo lima".split()
        pages = [f"Page {n} text, {words[n - 1]}." for n in range(1, 13)]
        with patch("src.ingest.CORPUS_DIR", tmp_path), \
             patch("src.ingest.fitz.open", return_value=self.fake_pdf(pages)):
            documents = load_corpus()

        # story-of-inyo.pdf has "pages": [[9, 361]] in the registry
        inyo = documents[0]
        assert inyo["text"].startswith("Page 9 text")
        assert "Page 8 text" not in inyo["text"]
        assert [n for _, n in inyo["page_offsets"]] == [9, 10, 11, 12]
        assert "pages" not in inyo["metadata"]

    def test_txt_files_have_no_page_offsets(self, corpus_dir, mock_fitz):
        documents = load_corpus()
        bishop = [d for d in documents if d["metadata"]["source"] == "bishop.txt"][0]
        assert bishop["page_offsets"] is None

    def test_load_corpus_caps_document_length(self, corpus_dir, mock_fitz):
        with patch("src.ingest.MAX_CHARS", 6):
            documents = load_corpus()
        assert all(len(d["text"]) <= 6 for d in documents)

    @patch("src.ingest.CORPUS_DIR")
    def test_empty_corpus_raises_error(self, mock_corpus_dir):
        mock_corpus_dir.rglob.return_value = []
        with pytest.raises(FileNotFoundError):
            load_corpus()


class TestStripPageFurniture:

    def pages(self):
        return [
            f"{n}\nTHE STORY OF INYO\nIndians gathered pine nuts\non page {n}.\nTHE"
            for n in range(30, 34)
        ]

    def test_removes_page_numbers_and_running_heads(self):
        stripped = strip_page_furniture(self.pages())
        assert stripped[0].startswith("Indians gathered pine nuts")
        assert "THE STORY OF INYO" not in stripped[0]
        assert not stripped[0].startswith("30")

    def test_keeps_short_repeated_words(self):
        # "THE" ends every page but is body text in a word-per-line layout
        assert all(page.endswith("THE") for page in strip_page_furniture(self.pages()))

    def test_running_head_needs_three_pages(self):
        pages = ["MEDICINE MEN AND LEGENDS\nText one.", "MEDICINE MEN AND LEGENDS\nText two."]
        assert strip_page_furniture(pages)[0].startswith("MEDICINE MEN")

    def test_keeps_years(self):
        assert strip_page_furniture(["1906\nThe aqueduct bonds passed."])[0].startswith("1906")

    def test_strips_at_most_three_lines_per_edge(self):
        page = "1\n2\n3\n4\nBody text."
        assert strip_page_furniture([page])[0] == "4\nBody text."


class TestSelectPages:

    def test_none_keeps_all(self):
        assert select_pages(["a", "b"], None) == [(1, "a"), (2, "b")]

    def test_inclusive_ranges(self):
        pages = [str(n) for n in range(1, 11)]
        assert [n for n, _ in select_pages(pages, [[2, 3], [9, 10]])] == [2, 3, 9, 10]

    def test_out_of_range_warns(self, capsys):
        select_pages(["a", "b"], [[1, 5]], "short.pdf")
        assert "outside 1-2" in capsys.readouterr().out


class TestJoinPages:

    def test_records_page_start_offsets(self):
        text, offsets = join_pages([(9, "First page"), (10, "Second\n"), (11, "Third")])
        assert text == "First page\nSecond\nThird"
        assert offsets == [[0, 9], [11, 10], [18, 11]]
        assert text[offsets[1][0]:].startswith("Second")
