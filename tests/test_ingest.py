import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from collections import Counter
from src.ingest import (
    get_metadata, load_corpus, strip_page_furniture, select_pages, join_pages,
    build_vocabulary, hyphen_join, join_hyphenated, join_blocks, join_lines,
    clean_text, is_heading, CLEAN_VERSION, file_name_title, source_title, context_header,
    printed_page_numbers,
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
        # Each page returns PyMuPDF text blocks, one per blank-line-separated paragraph
        pages = []
        for text in page_texts:
            page = MagicMock()
            blocks = [(0, 0, 0, 0, block, i, 0) for i, block in enumerate(text.split("\n\n"))]
            page.get_text.side_effect = lambda *args, blocks=blocks, text=text: blocks if args else text
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
        assert steward["printed_pages"] == {}   # no printed page numbers in the sample
        assert steward["layout"] == "blocks"
        assert steward["metadata"]["clean_version"] == CLEAN_VERSION

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

    def test_documents_get_context_headers(self, corpus_dir, mock_fitz):
        documents = {d["metadata"]["source"]: d["metadata"] for d in load_corpus()}
        # Registry title, author, year and type
        assert documents["ethnography-of-owens-valley-paiute.pdf"]["context_header"] == (
            "Ethnography of the Owens Valley Paiute · Julian H. Steward · 1933 · ethnography"
        )
        # Crawled page: its first line, plus the site default author and type
        assert documents["bishop.txt"]["title"] == "Bishop Creek mill, 1890."
        assert documents["bishop.txt"]["context_header"] == (
            "Bishop Creek mill, 1890. · owensvalleyhistory.com · local history site"
        )

    def test_txt_files_have_no_page_offsets(self, corpus_dir, mock_fitz):
        documents = load_corpus()
        bishop = [d for d in documents if d["metadata"]["source"] == "bishop.txt"][0]
        assert bishop["page_offsets"] is None
        assert bishop["layout"] == "lines"

    def test_cleans_and_joins_paragraph_across_pages(self, tmp_path):
        (tmp_path / "ethnography-of-owens-valley-paiute.pdf").write_bytes(b"%PDF placeholder")
        pages = [
            "The home of a dead person was burned, with his posses-",
            "sions. No evidence appears that goods and\n\nchattels were buried.",
        ]
        with patch("src.ingest.CORPUS_DIR", tmp_path), \
             patch("src.ingest.fitz.open", return_value=self.fake_pdf(pages)):
            text = load_corpus()[0]["text"]
        assert text == ("The home of a dead person was burned, with his possessions. "
                        "No evidence appears that goods and chattels were buried.")

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
        text, offsets = join_pages([(9, "First page ends."), (10, "Second page."), (11, "Third.")])
        assert text == "First page ends.\n\nSecond page.\n\nThird."
        assert [n for _, n in offsets] == [9, 10, 11]
        assert text[offsets[1][0]:].startswith("Second")

    def test_joins_sentence_running_over_a_page(self):
        text, offsets = join_pages([(1, "The aqueduct carried"), (2, "water south.")])
        assert text == "The aqueduct carried water south."
        assert text[offsets[1][0]:] == "water south."

    def test_joins_word_hyphenated_over_a_page(self):
        text, offsets = join_pages([(1, "his posses-"), (2, "sions were burned.")])
        assert text == "his possessions were burned."
        # Page 2 starts where its own text does, inside the rejoined word
        assert text[offsets[1][0]:] == "sions were burned."

    def test_skips_empty_pages(self):
        text, offsets = join_pages([(1, "One."), (2, ""), (3, "Three.")])
        assert [n for _, n in offsets] == [1, 3]


class TestHyphens:

    def test_vocabulary_leaves_out_line_split_halves(self):
        words, compounds = build_vocabulary(["to-\ngether we went", "a well-known trail"])
        assert words["gether"] == 0
        assert words["we"] == 1
        assert compounds["well-known"] == 1

    def test_joins_typesetting_break(self):
        assert hyphen_join("to", "gether", Counter({"together": 3}), Counter()) == "together"

    def test_keeps_compound_the_corpus_hyphenates(self):
        assert hyphen_join("well", "known", Counter(), Counter({"well-known": 4})) == "well-known"

    def test_unknown_words_are_joined(self):
        assert hyphen_join("Francis", "can", Counter(), Counter()) == "Franciscan"

    def test_only_breaks_before_lowercase_are_joined(self):
        text = "Lone Pine Paiute-\nShoshone and pos-\nsessions"
        assert join_hyphenated(text, Counter(), Counter()) == "Lone Pine Paiute-\nShoshone and possessions"


class TestJoinBlocks:

    def test_mid_sentence_blocks_join(self):
        assert join_blocks("goods and", "chattels were buried.", Counter(), Counter()) == \
            "goods and chattels were buried."

    def test_sentence_end_is_a_paragraph_break(self):
        assert join_blocks("in three days.", "The home of a dead person", Counter(), Counter()) is None

    def test_heading_is_a_paragraph_break(self):
        assert join_blocks("NATIVE CUSTOMS", "The Paiute lived", Counter(), Counter()) is None

    def test_hyphen_across_blocks(self):
        assert join_blocks("his posses-", "sions. No evidence", Counter(), Counter()) == \
            "his possessions. No evidence"

    def test_is_heading(self):
        assert is_heading("CHAPTER II")
        assert not is_heading("Chapter two begins here")


class TestJoinLines:

    def test_blocks_layout_turns_word_per_line_into_prose(self):
        text = "different\ntribes\nin\nCalifornia,\nwith the remark"
        assert join_lines(text, "blocks", Counter(), Counter()) == "different tribes in California, with the remark"

    def test_lines_layout_keeps_captions(self):
        text = "Cabin Bar Cafe in Cartago - 1970s\n(photo courtesy Lawrence Thomas)\nBuilding in Cartago"
        assert join_lines(text, "lines", Counter(), Counter()) == text

    def test_lines_layout_joins_broken_sentence(self):
        text = "The kilns were used\nto make charcoal.\nCartago"
        assert join_lines(text, "lines", Counter(), Counter()) == "The kilns were used to make charcoal.\nCartago"


class TestCleanText:

    def clean(self, text, layout="blocks"):
        return clean_text(text, layout, Counter(), Counter())

    def test_keeps_diacritics(self):
        # Decomposed u + diaeresis + macron composes to ǖ; the letters survive
        decomposed = "Payah" + "u\u0308\u0304" * 2 + "nad" + "u\u0308\u0304"
        assert self.clean(decomposed) == "Payahǖǖnadǖ"

    def test_drops_invisible_characters_and_ocr_symbols(self):
        assert self.clean("water\u00ad is ■ an absolute • necessity") == "water is an absolute necessity"

    def test_drops_escaped_codepoints_stored_as_text(self):
        assert self.clean("the 1 \\u25a0 future prosperity") == "the 1 future prosperity"

    def test_never_changes_words(self):
        text = "The Piute band camped near Bishop Creek in 1863."
        assert self.clean(text) == text


class TestSourceTitles:

    def test_file_name_becomes_title(self):
        assert file_name_title(Path("stories__dead_mining_camps.pdf.pdf")) == ("Dead Mining Camps", None)
        assert file_name_title(Path("Adella-Schloss.pdf")) == ("Adella Schloss", None)

    def test_drops_file_size_notes_and_keeps_capitals(self):
        assert file_name_title(Path("stories__Love Bug_REDUCED.pdf.pdf")) == ("Love Bug", None)

    def test_progress_citizen_issue_date(self):
        assert file_name_title(Path("progress_citizen__keeler_061148.pdf.pdf")) == (
            "Progress Citizen: Keeler", "11 Jun 1948"
        )
        assert file_name_title(Path("progress_citizen__independence__022048.pdf.pdf")) == (
            "Progress Citizen: Independence", "20 Feb 1948"
        )

    def test_progress_citizen_without_date(self):
        assert file_name_title(Path("progress_citizen__this_is_inyo.pdf.pdf")) == (
            "Progress Citizen: This Is Inyo", None
        )

    def test_crawled_page_uses_first_line(self):
        assert source_title(Path("bishop_mule_days__page101.html.txt"), "Bishop  Mule Days ") == (
            "Bishop Mule Days", None
        )

    def test_crawled_page_without_first_line_uses_file_name(self):
        assert source_title(Path("cartago__page118.html.txt"), "") == ("Page118", None)

    def test_header_skips_missing_fields(self):
        header = context_header({"title": "Payahüünadü", "author": "OVIWC", "source_type": "Paiute institutional history"})
        assert header == "Payahüünadü · OVIWC · Paiute institutional history"
        assert context_header({}) == ""


class TestPrintedPageNumbers:

    @staticmethod
    def pages(numbers, first_pdf_page=1):
        return [
            (first_pdf_page + i, f"Running head\nBody text on this page.\n{n}" if n else "Plate: a photograph")
            for i, n in enumerate(numbers)
        ]

    def test_reads_printed_numbers(self):
        assert printed_page_numbers(self.pages([233, 234, 235], first_pdf_page=7)) == {7: 233, 8: 234, 9: 235}

    def test_no_numbers_gives_empty_map(self):
        assert printed_page_numbers([(1, "A web page."), (2, "More of it.")]) == {}

    def test_lone_number_without_agreeing_neighbour_is_noise(self):
        assert printed_page_numbers(self.pages([None, None, 320, None, None])) == {}

    def test_fills_unnumbered_page_between_agreeing_numbers(self):
        assert printed_page_numbers(self.pages([10, None, 12])) == {1: 10, 2: 11, 3: 12}

    def test_unnumbered_plate_breaking_the_count_stays_out(self):
        # A plate between printed pages 324 and 325 shifts the count by one
        assert printed_page_numbers(self.pages([323, 324, None, 325, 326])) == {
            1: 323, 2: 324, 4: 325, 5: 326,
        }

    def test_does_not_fill_pages_outside_the_selected_ranges(self):
        pages = self.pages([18, 19], first_pdf_page=28) + self.pages([50, 51], first_pdf_page=60)
        assert printed_page_numbers(pages) == {28: 18, 29: 19, 60: 50, 61: 51}
