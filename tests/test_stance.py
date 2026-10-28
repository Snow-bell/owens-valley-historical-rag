import json
import pytest
from unittest.mock import patch, MagicMock
import src.stance as stance
from src.stance import period_terms, stance_metadata, label_chunks, cache_key


LABEL = {
    "paiute": "hostile",
    "los_angeles": "not_mentioned",
    "settlers": "favourable",
    "loaded_terms": ["renegade red men", "marauding"],
    "framing": "frontier conflict",
}


def make_chunk(text, header="The Story of Inyo · W. A. Chalfant · 1922 · local pioneer history book"):
    return {"text": text, "metadata": {"source": "story-of-inyo.pdf", "context_header": header}}


def api_response(label):
    response = MagicMock()
    response.choices[0].message.content = json.dumps(label)
    return response


@pytest.fixture(autouse=True)
def cache_file(tmp_path):
    # Tests never touch the real cache or the OpenAI API
    with patch.object(stance, "STANCE_CACHE", tmp_path / "stance_cache.json"), \
         patch.object(stance, "client") as mock_client:
        mock_client.chat.completions.create.side_effect = AssertionError("unpatched OpenAI call")
        yield tmp_path / "stance_cache.json"


class TestPeriodTerms:

    def test_finds_slurs_once_as_written(self):
        text = "The squaw and her children. Another Squaw came. The redskins fled; half-breed scouts."
        assert period_terms(text) == ["squaw", "redskins", "half-breed"]

    def test_savage_as_surname_is_not_flagged(self):
        assert period_terms("James Savage ran the Savage Trading Post.") == []
        assert period_terms("He called them savages.") == ["savages"]

    def test_ambiguous_words_are_not_flagged(self):
        assert period_terms("A buck and two does; Buck Hyers; Papoose Lake; gold diggers.") == []

    def test_digger_only_capitalized(self):
        assert period_terms('Muir mentions "Digger Indians" below Yosemite.') == ["Digger"]


class TestStanceMetadata:

    def test_flat_fields(self):
        metadata = stance_metadata(LABEL, "The renegade red men were marauding.")
        assert metadata == {
            "stance_paiute": "hostile",
            "stance_los_angeles": "not_mentioned",
            "stance_settlers": "favourable",
            "loaded_terms": "renegade red men; marauding",
            "framing": "frontier conflict",
            "stance_version": stance.STANCE_LABEL,
        }

    def test_terms_not_in_text_are_dropped(self):
        label = {**LABEL, "loaded_terms": ["wonderful growth", "renegade red men"]}
        assert stance_metadata(label, "The renegade red men gathered.")["loaded_terms"] == "renegade red men"

    def test_period_term_inside_a_model_term_is_not_repeated(self):
        label = {**LABEL, "loaded_terms": ["renegade red men"]}
        assert stance_metadata(label, "The renegade red men gathered.")["loaded_terms"] == "renegade red men"

    def test_terms_match_across_ocr_spacing_and_hyphens(self):
        label = {**LABEL, "loaded_terms": ["renegade red men", "marauding"]}
        text = "The RENEGADE RED-\nMEN were ma rauding."
        assert stance_metadata(label, text)["loaded_terms"] == "renegade red men; marauding"

    def test_period_terms_added_without_duplicates(self):
        label = {**LABEL, "loaded_terms": ["Squaw"]}
        metadata = stance_metadata(label, "The squaw sat by the redskins' camp.")
        assert metadata["loaded_terms"] == "Squaw; redskins"

    def test_model_terms_capped(self):
        label = {**LABEL, "loaded_terms": [f"term {i}" for i in range(8)]}
        text = " ".join(f"term {i}" for i in range(8))
        assert stance_metadata(label, text)["loaded_terms"].count(";") == 4


class TestLabelChunks:

    def test_labels_and_caches(self, cache_file):
        chunks = [make_chunk("The renegade red men were marauding.")]
        with patch.object(stance, "label_chunk", return_value=LABEL) as mock_label:
            label_chunks(chunks)
        mock_label.assert_called_once()
        assert chunks[0]["metadata"]["stance_paiute"] == "hostile"
        assert cache_key(chunks[0]) in json.loads(cache_file.read_text())

    def test_unchanged_chunks_come_from_cache(self):
        with patch.object(stance, "label_chunk", return_value=LABEL):
            label_chunks([make_chunk("Same text.")])
        chunks = [make_chunk("Same text."), make_chunk("New text.")]
        with patch.object(stance, "label_chunk", return_value=LABEL) as mock_label:
            label_chunks(chunks)
        assert mock_label.call_count == 1
        assert all("stance_paiute" in c["metadata"] for c in chunks)

    def test_changed_header_is_a_new_label(self):
        with patch.object(stance, "label_chunk", return_value=LABEL):
            label_chunks([make_chunk("Same text.")])
        with patch.object(stance, "label_chunk", return_value=LABEL) as mock_label:
            label_chunks([make_chunk("Same text.", header="Another title")])
        mock_label.assert_called_once()

    def test_failed_request_leaves_chunk_unlabeled(self, cache_file):
        chunks = [make_chunk("First."), make_chunk("Second.")]
        with patch.object(stance, "label_chunk", side_effect=[RuntimeError("timeout"), LABEL]):
            label_chunks(chunks)
        assert [("stance_paiute" in c["metadata"]) for c in chunks] == [False, True]
        assert len(json.loads(cache_file.read_text())) == 1


class TestLabelChunk:

    def test_sends_schema_prompt_and_source(self):
        with patch.object(stance, "client") as mock_client:
            mock_client.chat.completions.create.return_value = api_response(LABEL)
            assert stance.label_chunk(make_chunk("Passage text.")) == LABEL
        kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert kwargs["model"] == stance.STANCE_MODEL
        assert kwargs["temperature"] == 0
        assert kwargs["response_format"]["json_schema"]["strict"] is True
        assert kwargs["messages"][1]["content"].startswith("Source: The Story of Inyo")
