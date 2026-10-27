from src.generate import format_context, format_sources, page_label


def make_chunk(text, source="story-of-inyo.pdf", **extra):
    return {
        "text": text,
        "metadata": {
            "source": source,
            "tier": 3,
            "bias_tag": "settler_bias",
            "bias_level": "moderate",
            "description": "Story of Inyo by W.A. Chalfant.",
            **extra,
        },
    }


class TestPageLabel:

    def test_single_page(self):
        assert page_label(["32"]) == "p. 32"

    def test_range_and_list(self):
        assert page_label(["32–33"]) == "pp. 32–33"
        assert page_label(["32–33", "140"]) == "pp. 32–33, 140"

    def test_no_pages(self):
        assert page_label([]) == ""


class TestFormatContext:

    def test_uses_title_and_pages(self):
        chunk = make_chunk("The mill burned.", title="The Story of Inyo", page_start=32, page_end=33)
        header = format_context([chunk]).split("\n")[0]
        assert header == "[Source 1: The Story of Inyo | pp. 32–33 | Tier 3 | Bias: settler_bias (moderate)]"

    def test_falls_back_to_file_name_without_pages(self):
        chunk = make_chunk("Bishop Creek mill.", source="bishop.txt", bias_level="none")
        assert format_context([chunk]).split("\n")[0] == "[Source 1: bishop.txt | Tier 3]"


class TestFormatSources:

    def test_one_line_per_source_with_all_its_pages(self):
        chunks = [
            make_chunk("a", title="The Story of Inyo", page_start=32, page_end=33),
            make_chunk("b", source="bishop.txt", title="Bishop Creek", bias_level="none"),
            make_chunk("c", title="The Story of Inyo", page_start=140, page_end=140),
        ]
        lines = [l for l in format_sources(chunks).split("\n") if l.startswith("  •")]
        assert lines == [
            "  • The Story of Inyo, pp. 32–33, 140 (Tier 3) ⚠ Settler Bias — moderate bias",
            "  • Bishop Creek (Tier 3)",
        ]
