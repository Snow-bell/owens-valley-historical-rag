from src.crawl import canonical_url, output_name


class TestCanonicalUrl:

    def test_spaces_and_percent_twenty_are_one_url(self):
        spaced = "http://www.owensvalleyhistory.com/stories/Lakeview Mine.pdf"
        encoded = "http://www.owensvalleyhistory.com/stories/Lakeview%20Mine.pdf"
        assert canonical_url(spaced) == canonical_url(encoded)

    def test_plain_url_unchanged(self):
        url = "http://www.owensvalleyhistory.com/keeler/page71.html"
        assert canonical_url(url) == url


class TestOutputName:

    def test_decodes_and_flattens_path(self):
        url = "http://www.owensvalleyhistory.com/stories/Lakeview%20Mine.pdf"
        assert output_name(url, ".pdf") == "stories__Lakeview Mine.pdf.pdf"

    def test_both_spellings_save_to_the_same_file(self):
        a = output_name("http://www.owensvalleyhistory.com/stories/Shotgun Kate.pdf", ".pdf")
        b = output_name("http://www.owensvalleyhistory.com/stories/Shotgun%20Kate.pdf", ".pdf")
        assert a == b
