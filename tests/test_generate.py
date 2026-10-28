from src.generate import format_context, format_sources, format_stance, page_label, stance_note


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


STANCE = {
    "stance_paiute": "hostile",
    "stance_los_angeles": "not_mentioned",
    "stance_settlers": "favourable",
    "loaded_terms": "renegade red men; marauding",
    "framing": "frontier conflict",
    "stance_version": "gpt-4.1-mini@v1",
}


class TestStanceNote:

    def test_lists_non_neutral_stances_terms_and_framing(self):
        assert stance_note(STANCE) == (
            'Stance: hostile to Paiute, favourable to settlers'
            ' | Loaded terms: "renegade red men", "marauding" | Framing: frontier conflict'
        )

    def test_neutral_passage_keeps_only_framing(self):
        meta = {**STANCE, "stance_paiute": "neutral", "stance_settlers": "neutral", "loaded_terms": "",
                "framing": "ethnographic description"}
        assert stance_note(meta) == "Framing: ethnographic description"

    def test_unlabeled_chunk_has_no_note(self):
        assert stance_note({"source": "a.pdf"}) == ""

    def test_context_gets_stance_line_under_header(self):
        chunk = make_chunk("The war began.", title="The Story of Inyo", **STANCE)
        lines = format_context([chunk]).split("\n")
        assert lines[1].startswith("[Stance: hostile to Paiute")
        assert lines[2] == "The war began."


class TestFormatStance:

    def test_panel_entry(self):
        chunk = make_chunk("The war began.", title="The Story of Inyo", page_start=113, page_end=116, **STANCE)
        assert format_stance([chunk]) == (
            "1. The Story of Inyo, pp. 113–116   registry: settler bias (moderate)\n"
            "   Paiute: hostile · Settlers: favourable\n"
            '   Loaded terms: "renegade red men", "marauding"\n'
            "   Framing: frontier conflict"
        )

    def test_no_party_mentioned(self):
        meta = {**STANCE, "stance_paiute": "not_mentioned", "stance_settlers": "not_mentioned", "loaded_terms": ""}
        chunk = make_chunk("Bighorn sheep.", title="Fauna and Flora", bias_tag="none", bias_level="none", **meta)
        assert format_stance([chunk]).split("\n")[:2] == [
            "1. Fauna and Flora   registry: none", "   No party mentioned",
        ]

    def test_unlabeled_chunk(self):
        assert "No stance labels; reindex to add them." in format_stance([make_chunk("Text.")])
