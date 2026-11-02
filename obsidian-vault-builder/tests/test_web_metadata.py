import unittest

from vault_builder.web_metadata import fetch_url_metadata, parse_html_title


class WebMetadataTests(unittest.TestCase):
    def test_parse_html_title(self):
        html = b"<html><head><title>Example Title</title></head><body></body></html>"

        self.assertEqual(parse_html_title(html), "Example Title")

    def test_fetch_url_metadata_disabled_does_not_fetch(self):
        result = fetch_url_metadata("https://example.com", allow_network=False)

        self.assertFalse(result.fetched)
        self.assertEqual(result.status_code, "")
        self.assertIn("disabled", result.error)


if __name__ == "__main__":
    unittest.main()
